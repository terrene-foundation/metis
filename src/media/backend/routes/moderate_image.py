# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Image moderation endpoints — Sprint 1 of the Playbook (CNN · See).

Returns per-class scores from the frozen-ResNet-backbone + 5-class
fine-tuned head. The 3-family leaderboard (LR head / RF head / GBM head)
is pre-trained at startup; live `/moderate/image/train` re-runs the sweep.

Endpoints
---------
- `GET  /moderate/image/leaderboard`     — pre-computed 3-family leaderboard
- `POST /moderate/image/train`           — re-train live with {families, seed}
- `POST /moderate/image/score`           — per-class scores for a post_id
- `GET  /moderate/image/threshold`       — current per-class thresholds
- `POST /moderate/image/threshold`       — set per-class threshold (CSAM hard floor enforced)
- `POST /moderate/image/promote`         — promote chosen family to shadow|production
- `GET  /moderate/image/registry`        — promotion + threshold-change history

CSAM-adjacent threshold is structurally HARD per IMDA Online Safety Code
(`CSAM_ADJACENT_HARD_FLOOR = 0.40`). The threshold POST refuses values
below the floor with a 422; this is the rule-not-cost-balanced gate
referenced in PRODUCT_BRIEF §5 decision moment 4.
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
    CSAM_ADJACENT_HARD_FLOOR,
    IMAGE_CLASSES,
    build_image_baseline,
    get_context,
    synthesise_embeddings,
)

router = APIRouter()


# --------------------------------------------------------------------------- #
# Threshold + registry persistence (workspace-local JSON, survives restart)
# --------------------------------------------------------------------------- #


def _threshold_path() -> Path:
    return load_settings().workspace_root / "image_thresholds.json"


def _registry_path() -> Path:
    return load_settings().workspace_root / "image_registry.json"


def _default_thresholds() -> dict[str, Any]:
    state = {c: 0.50 for c in IMAGE_CLASSES}
    state["csam_adjacent"] = CSAM_ADJACENT_HARD_FLOOR
    return {
        "thresholds": state,
        "justifications": {c: "default — student has not set" for c in IMAGE_CLASSES},
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
# Serialisation helper — strip sklearn estimators / scalers from leaderboard
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
# Request models
# --------------------------------------------------------------------------- #


class ThresholdRequest(BaseModel):
    klass: str = Field(description=f"one of: {', '.join(IMAGE_CLASSES)}")
    threshold: float = Field(ge=0.0, le=1.0)
    justification: str = Field(min_length=10)


class TrainRequest(BaseModel):
    families: list[str] | None = Field(
        default=None,
        description=(
            "subset of frozen_resnet_lr_head, frozen_resnet_rf_head, frozen_resnet_gbm_head "
            "(default: all 3)"
        ),
    )
    seed: int = Field(default=20260430)


class ScoreRequest(BaseModel):
    post_id: str = Field(description="post_id present in posts_labelled.csv has_image rows")


class PromoteRequest(BaseModel):
    family: str = Field(
        description=("frozen_resnet_lr_head | frozen_resnet_rf_head | frozen_resnet_gbm_head")
    )
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
        "modality": "image",
        "classes": list(IMAGE_CLASSES),
        "label_definition": (
            "5-class moderation: nsfw / violence / weapons / csam_adjacent / safe. "
            "Labels are the human-reviewer's image_class_label decision."
        ),
        "chosen_family": ctx.image_baseline.chosen_family,
        "chosen_macro_f1": ctx.image_baseline.macro_f1,
        "stage": ctx.image_baseline.stage,
        "candidates": {
            fam: _serializable_entry(entry) for fam, entry in ctx.image_baseline.candidates.items()
        },
        "note": (
            "Pre-trained leaderboard. Students CRITIQUE this in Phase 4–6. "
            "Pick on per-class F1 + cost-balanced threshold (Phase 6) — NOT on "
            "macro-F1 alone, since CSAM-adjacent has the IMDA $1M ceiling that "
            "makes recall the dominant axis on that class."
        ),
    }


@router.post("/train")
def train(req: TrainRequest) -> dict:
    """Re-run the 3-family sweep live; updates the in-memory baseline."""
    ctx = get_context()
    new_bl = build_image_baseline(
        ctx.posts, ctx.image_embeddings, ctx.image_post_ids, seed=req.seed
    )
    if req.families:
        keep = set(req.families)
        new_bl.candidates = {f: e for f, e in new_bl.candidates.items() if f in keep}
        if new_bl.candidates:
            new_bl.chosen_family = max(
                new_bl.candidates, key=lambda k: new_bl.candidates[k].macro_f1
            )
            new_bl.macro_f1 = new_bl.candidates[new_bl.chosen_family].macro_f1
    ctx.image_baseline = new_bl
    return {
        "modality": "image",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "chosen_family": new_bl.chosen_family,
        "chosen_macro_f1": new_bl.macro_f1,
        "candidates": {fam: _serializable_entry(entry) for fam, entry in new_bl.candidates.items()},
    }


@router.post("/score")
def score(req: ScoreRequest) -> dict:
    """Return per-class probabilities + thresholded decision for one post."""
    ctx = get_context()
    if req.post_id not in set(ctx.image_post_ids):
        raise HTTPException(404, f"post_id {req.post_id!r} has no image; check has_image")
    label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["image_class_label"].to_list())
    )
    # Re-synthesise the embedding to keep it deterministic and avoid touching
    # the materialised matrix (the matrix is the train-time view; synthesis
    # respects per-post seed so the score is stable across calls).
    emb = synthesise_embeddings([req.post_id], [label_lookup[req.post_id]], modality="image")
    chosen = ctx.image_baseline.candidates[ctx.image_baseline.chosen_family]
    X_std = chosen.scaler.transform(emb)
    proba = chosen.model.predict_proba(X_std)[0]
    # Right-pad in case a rare class was missing at fit time.
    if proba.shape[0] < len(IMAGE_CLASSES):
        full = np.zeros(len(IMAGE_CLASSES), dtype=np.float32)
        for src_idx, cls_int in enumerate(chosen.model.classes_):
            full[int(cls_int)] = proba[src_idx]
        proba = full

    state = _load_thresholds()
    thresholds = state["thresholds"]
    per_class: dict[str, dict[str, Any]] = {}
    for ci, cname in enumerate(IMAGE_CLASSES):
        tau = float(thresholds.get(cname, 0.50))
        p = float(proba[ci])
        per_class[cname] = {
            "probability": round(p, 4),
            "threshold": tau,
            "above_threshold": p >= tau,
        }

    # Aggregate decision: any harmful class above its threshold => auto-action.
    harmful = [c for c in IMAGE_CLASSES if c != "safe" and per_class[c]["above_threshold"]]
    if "csam_adjacent" in harmful:
        decision = "auto_block_pending_review_imda"
    elif harmful:
        decision = "auto_remove"
    else:
        decision = "allow"
    return {
        "modality": "image",
        "post_id": req.post_id,
        "ground_truth_label": label_lookup[req.post_id],
        "per_class": per_class,
        "harmful_classes_above_threshold": harmful,
        "decision": decision,
        "chosen_family": ctx.image_baseline.chosen_family,
    }


@router.get("/threshold")
def get_thresholds() -> dict:
    return _load_thresholds() | {
        "csam_adjacent_hard_floor": CSAM_ADJACENT_HARD_FLOOR,
        "note": (
            "csam_adjacent threshold is structurally HARD per IMDA. The /threshold "
            "POST endpoint REFUSES values below the hard floor with a 422."
        ),
    }


@router.post("/threshold")
def set_threshold(req: ThresholdRequest) -> dict:
    if req.klass not in IMAGE_CLASSES:
        raise HTTPException(
            422, f"unknown class {req.klass!r}; expected one of {list(IMAGE_CLASSES)}"
        )
    if req.klass == "csam_adjacent" and req.threshold < CSAM_ADJACENT_HARD_FLOOR:
        raise HTTPException(
            422,
            (
                f"CSAM-adjacent threshold {req.threshold} is below the IMDA hard floor "
                f"({CSAM_ADJACENT_HARD_FLOOR}). This class is structurally hard, not "
                f"cost-balanced. See PRODUCT_BRIEF §5 decision moment 4."
            ),
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


@router.post("/promote")
def promote(req: PromoteRequest) -> dict:
    if req.stage not in {"shadow", "production"}:
        raise HTTPException(422, f"stage must be 'shadow' or 'production', got {req.stage!r}")
    ctx = get_context()
    if req.family not in ctx.image_baseline.candidates:
        raise HTTPException(
            422,
            (
                f"unknown family {req.family!r}; expected one of "
                f"{list(ctx.image_baseline.candidates)}"
            ),
        )
    state = _load_thresholds()
    csam_tau = float(state["thresholds"].get("csam_adjacent", CSAM_ADJACENT_HARD_FLOOR))
    if csam_tau < CSAM_ADJACENT_HARD_FLOOR:
        raise HTTPException(
            422,
            (
                f"refusing promotion: csam_adjacent threshold {csam_tau} is below the IMDA "
                f"hard floor ({CSAM_ADJACENT_HARD_FLOOR}). Set the CSAM threshold "
                f"first via POST /moderate/image/threshold."
            ),
        )
    ctx.image_baseline.chosen_family = req.family
    ctx.image_baseline.macro_f1 = ctx.image_baseline.candidates[req.family].macro_f1
    ctx.image_baseline.stage = req.stage
    history = _append_registry(
        {
            "event": "promote",
            "family": req.family,
            "stage": req.stage,
            "rationale": req.rationale,
            "at": datetime.now(timezone.utc).isoformat(),
            "csam_threshold_at_promote": csam_tau,
        }
    )
    return {
        "modality": "image",
        "promoted_family": req.family,
        "stage": req.stage,
        "history_length": len(history),
    }


@router.get("/registry")
def registry() -> dict:
    history = _load_registry()
    return {
        "modality": "image",
        "history_length": len(history),
        "history": history,
    }
