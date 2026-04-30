# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Text moderation endpoints — Sprint 2 of the Playbook (Transformer · Read).

Returns per-class scores from a fine-tuned BERT-class moderator. The
3-family leaderboard (fine-tuned BERT / fine-tuned RoBERTa / zero-shot
prompted LLM) is pre-trained at startup; live `/moderate/text/train`
re-runs the sweep. No IMDA hard floor on text classes (the regulator's
hard-constraint surface is the image CSAM-adjacent class).

Endpoints
---------
- `GET  /moderate/text/leaderboard`     — pre-computed 3-family leaderboard
- `POST /moderate/text/train`           — re-train live with {families, seed}
- `POST /moderate/text/score`           — per-class scores for a post_id
- `GET  /moderate/text/threshold`       — current per-class thresholds
- `POST /moderate/text/threshold`       — set per-class threshold (no hard floor)
- `GET  /moderate/text/calibration`     — Brier + reliability bins per family
- `POST /moderate/text/promote`         — promote chosen family to shadow|production
- `GET  /moderate/text/registry`        — promotion + threshold-change history
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import load_settings
from ..ml_context import (
    TEXT_CLASSES,
    build_text_baseline,
    get_context,
    synthesise_embeddings,
)

router = APIRouter()


# --------------------------------------------------------------------------- #
# Threshold + registry persistence (workspace-local JSON, survives restart)
# --------------------------------------------------------------------------- #


def _threshold_path() -> Path:
    return load_settings().workspace_root / "text_thresholds.json"


def _registry_path() -> Path:
    return load_settings().workspace_root / "text_registry.json"


def _default_thresholds() -> dict[str, Any]:
    return {
        "thresholds": {c: 0.50 for c in TEXT_CLASSES},
        "justifications": {c: "default — student has not set" for c in TEXT_CLASSES},
        "updated_at": None,
    }


def _load_thresholds() -> dict[str, Any]:
    p = _threshold_path()
    if p.exists():
        return json.loads(p.read_text())
    return _default_thresholds()


def _save_thresholds(state: dict) -> None:
    _threshold_path().parent.mkdir(parents=True, exist_ok=True)
    _threshold_path().write_text(json.dumps(state, indent=2))


def _load_registry() -> list[dict]:
    p = _registry_path()
    if p.exists():
        return json.loads(p.read_text())
    return []


def _append_registry(entry: dict) -> list[dict]:
    history = _load_registry()
    history.append(entry)
    _registry_path().parent.mkdir(parents=True, exist_ok=True)
    _registry_path().write_text(json.dumps(history, indent=2))
    return history


# --------------------------------------------------------------------------- #
# Serialisation
# --------------------------------------------------------------------------- #


def _serializable_entry(entry: Any) -> dict:
    return {
        "family": entry.family,
        "family_why": entry.family_why,
        "macro_f1": entry.macro_f1,
        "per_class": entry.per_class,
        "threshold": entry.threshold,
    }


# --------------------------------------------------------------------------- #
# Calibration helper — reliability bins on the chosen family's predictions
# --------------------------------------------------------------------------- #


def _reliability_bins(
    y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10
) -> list[dict[str, float]]:
    """Bin predictions and report empirical accuracy per bin (the reliability diagram)."""
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    out: list[dict[str, float]] = []
    for i in range(n_bins):
        lo, hi = float(edges[i]), float(edges[i + 1])
        if i == n_bins - 1:
            mask = (y_prob >= lo) & (y_prob <= hi)
        else:
            mask = (y_prob >= lo) & (y_prob < hi)
        n = int(mask.sum())
        if n == 0:
            out.append(
                {
                    "bin_lo": round(lo, 3),
                    "bin_hi": round(hi, 3),
                    "count": 0,
                    "mean_predicted": 0.0,
                    "empirical_rate": 0.0,
                    "calibration_gap": 0.0,
                }
            )
            continue
        mp = float(y_prob[mask].mean())
        er = float(y_true[mask].mean())
        out.append(
            {
                "bin_lo": round(lo, 3),
                "bin_hi": round(hi, 3),
                "count": n,
                "mean_predicted": round(mp, 4),
                "empirical_rate": round(er, 4),
                "calibration_gap": round(mp - er, 4),
            }
        )
    return out


# --------------------------------------------------------------------------- #
# Request models
# --------------------------------------------------------------------------- #


class ThresholdRequest(BaseModel):
    klass: str = Field(description=f"one of: {', '.join(TEXT_CLASSES)}")
    threshold: float = Field(ge=0.0, le=1.0)
    justification: str = Field(min_length=10)


class TrainRequest(BaseModel):
    families: list[str] | None = Field(
        default=None,
        description=(
            "subset of fine_tuned_bert, fine_tuned_roberta, zero_shot_llm " "(default: all 3)"
        ),
    )
    seed: int = Field(default=20260430)


class ScoreRequest(BaseModel):
    post_id: str = Field(description="post_id present in posts_labelled.csv has_text rows")


class PromoteRequest(BaseModel):
    family: str = Field(description="fine_tuned_bert | fine_tuned_roberta | zero_shot_llm")
    stage: str = Field(description="shadow | production")
    rationale: str = Field(min_length=10)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@router.get("/leaderboard")
def leaderboard() -> dict:
    """Per-class precision/recall/F1/Brier × 3 families, frozen at startup."""
    ctx = get_context()
    return {
        "modality": "text",
        "classes": list(TEXT_CLASSES),
        "label_definition": (
            "5-class moderation: hate_speech / harassment / threats / "
            "self_harm / safe. Labels are the human-reviewer's "
            "text_class_label decision."
        ),
        "chosen_family": ctx.text_baseline.chosen_family,
        "chosen_macro_f1": ctx.text_baseline.macro_f1,
        "stage": ctx.text_baseline.stage,
        "candidates": {
            fam: _serializable_entry(entry) for fam, entry in ctx.text_baseline.candidates.items()
        },
        "note": (
            "Pre-trained leaderboard. Students CRITIQUE this in Phase 5 SML. "
            "Text moves faster than images (slang, dogwhistles), so the "
            "retrain cadence in Phase 13 will be DAILY for text, not weekly."
        ),
    }


@router.post("/train")
def train(req: TrainRequest) -> dict:
    """Re-run the 3-family sweep live; updates the in-memory baseline."""
    ctx = get_context()
    new_bl = build_text_baseline(ctx.posts, ctx.text_embeddings, ctx.text_post_ids, seed=req.seed)
    if req.families:
        keep = set(req.families)
        new_bl.candidates = {f: e for f, e in new_bl.candidates.items() if f in keep}
        if new_bl.candidates:
            new_bl.chosen_family = max(
                new_bl.candidates, key=lambda k: new_bl.candidates[k].macro_f1
            )
            new_bl.macro_f1 = new_bl.candidates[new_bl.chosen_family].macro_f1
    ctx.text_baseline = new_bl
    return {
        "modality": "text",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "chosen_family": new_bl.chosen_family,
        "chosen_macro_f1": new_bl.macro_f1,
        "candidates": {fam: _serializable_entry(entry) for fam, entry in new_bl.candidates.items()},
    }


@router.post("/score")
def score(req: ScoreRequest) -> dict:
    """Return per-class probabilities + thresholded decision for one post."""
    ctx = get_context()
    if req.post_id not in set(ctx.text_post_ids):
        raise HTTPException(404, f"post_id {req.post_id!r} has no text; check has_text")
    label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["text_class_label"].to_list())
    )
    emb = synthesise_embeddings([req.post_id], [label_lookup[req.post_id]], modality="text")
    chosen = ctx.text_baseline.candidates[ctx.text_baseline.chosen_family]
    X_std = chosen.scaler.transform(emb)
    proba = chosen.model.predict_proba(X_std)[0]
    if proba.shape[0] < len(TEXT_CLASSES):
        full = np.zeros(len(TEXT_CLASSES), dtype=np.float32)
        for src_idx, cls_int in enumerate(chosen.model.classes_):
            full[int(cls_int)] = proba[src_idx]
        proba = full

    state = _load_thresholds()
    thresholds = state["thresholds"]
    per_class: dict[str, dict[str, Any]] = {}
    for ci, cname in enumerate(TEXT_CLASSES):
        tau = float(thresholds.get(cname, 0.50))
        p = float(proba[ci])
        per_class[cname] = {
            "probability": round(p, 4),
            "threshold": tau,
            "above_threshold": p >= tau,
        }

    harmful = [c for c in TEXT_CLASSES if c != "safe" and per_class[c]["above_threshold"]]
    if "threats" in harmful or "self_harm" in harmful:
        decision = "auto_remove_priority_review"
    elif harmful:
        decision = "auto_remove"
    else:
        decision = "allow"
    return {
        "modality": "text",
        "post_id": req.post_id,
        "ground_truth_label": label_lookup[req.post_id],
        "per_class": per_class,
        "harmful_classes_above_threshold": harmful,
        "decision": decision,
        "chosen_family": ctx.text_baseline.chosen_family,
    }


@router.get("/threshold")
def get_thresholds() -> dict:
    return _load_thresholds() | {
        "note": (
            "Text classes have no IMDA-mandated hard floor (that constraint "
            "applies to image csam_adjacent only). Thresholds here are "
            "cost-balanced under the $320/$15 (FN/FP) asymmetry."
        ),
    }


@router.post("/threshold")
def set_threshold(req: ThresholdRequest) -> dict:
    if req.klass not in TEXT_CLASSES:
        raise HTTPException(
            422, f"unknown class {req.klass!r}; expected one of {list(TEXT_CLASSES)}"
        )
    state = _load_thresholds()
    state["thresholds"][req.klass] = req.threshold
    state["justifications"][req.klass] = req.justification
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_thresholds(state)
    _append_registry(
        {
            "event": "threshold_set",
            "klass": req.klass,
            "threshold": req.threshold,
            "justification": req.justification,
            "at": state["updated_at"],
        }
    )
    return state


@router.get("/calibration")
def calibration() -> dict:
    """Per-class reliability bins for the chosen family.

    Calibration confirmation is part of the Phase 5 SML success criteria —
    Brier alone hides where the model is over- or under-confident; the
    reliability diagram surfaces that pattern bin-by-bin.
    """
    ctx = get_context()
    chosen = ctx.text_baseline.candidates[ctx.text_baseline.chosen_family]
    label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["text_class_label"].to_list())
    )
    y_str = [label_lookup[p] for p in ctx.text_post_ids]
    class_to_int = {c: i for i, c in enumerate(TEXT_CLASSES)}
    y = np.array([class_to_int[lbl] for lbl in y_str], dtype=np.int64)
    X_std = chosen.scaler.transform(ctx.text_embeddings)
    y_proba = chosen.model.predict_proba(X_std)
    if y_proba.shape[1] < len(TEXT_CLASSES):
        full = np.zeros((y_proba.shape[0], len(TEXT_CLASSES)), dtype=np.float32)
        for src_idx, cls_int in enumerate(chosen.model.classes_):
            full[:, int(cls_int)] = y_proba[:, src_idx]
        y_proba = full
    out: dict[str, Any] = {}
    for ci, cname in enumerate(TEXT_CLASSES):
        y_true_c = (y == ci).astype(int)
        y_prob_c = y_proba[:, ci]
        out[cname] = {
            "brier": chosen.per_class[cname]["brier"],
            "reliability_bins": _reliability_bins(y_true_c, y_prob_c, n_bins=10),
        }
    return {
        "modality": "text",
        "chosen_family": ctx.text_baseline.chosen_family,
        "per_class": out,
        "note": (
            "calibration_gap = mean_predicted − empirical_rate per bin. A "
            "well-calibrated classifier has gap ≈ 0 across all bins."
        ),
    }


@router.post("/promote")
def promote(req: PromoteRequest) -> dict:
    if req.stage not in {"shadow", "production"}:
        raise HTTPException(422, f"stage must be 'shadow' or 'production', got {req.stage!r}")
    ctx = get_context()
    if req.family not in ctx.text_baseline.candidates:
        raise HTTPException(
            422,
            (
                f"unknown family {req.family!r}; expected one of "
                f"{list(ctx.text_baseline.candidates)}"
            ),
        )
    ctx.text_baseline.chosen_family = req.family
    ctx.text_baseline.macro_f1 = ctx.text_baseline.candidates[req.family].macro_f1
    ctx.text_baseline.stage = req.stage
    history = _append_registry(
        {
            "event": "promote",
            "family": req.family,
            "stage": req.stage,
            "rationale": req.rationale,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {
        "modality": "text",
        "promoted_family": req.family,
        "stage": req.stage,
        "history_length": len(history),
    }


@router.get("/registry")
def registry() -> dict:
    history = _load_registry()
    return {
        "modality": "text",
        "history_length": len(history),
        "history": history,
    }
