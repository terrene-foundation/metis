# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Drift endpoints — Sprint 4 of the Playbook (MLOps · Monitor).

Three drift signals, three cadences, three retrain rules — one per
moderator. Image drifts on per-class score distribution + per-pixel-domain
distribution (weekly). Text drifts on token frequency + embedding
distribution + per-class calibration (daily). Fusion drifts on cross-modal
alignment score variance + per-incident calibration decay (per-incident).

A universal "auto-retrain when X" rule is BLOCKED — Phase 13 of the
Playbook requires three independent rules with signal + variance-grounded
threshold + duration window + HITL disposition + seasonal exclusions.

Endpoints
---------
- `GET  /drift/status/{model_id}`    — whether reference is registered for image|text|fusion
- `POST /drift/check`                — run a drift check for a (model_id, window)
- `GET  /drift/retrain_rule`         — current retrain rules (all 3 moderators)
- `POST /drift/retrain_rule`         — set retrain rule for one model
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
from ..ml_context import get_context, synthesise_embeddings

router = APIRouter()

VALID_MODELS = ("image", "text", "fusion")
VALID_WINDOWS = ("recent_30d", "imda_csam_mandate", "election_cycle_drift", "custom")


# --------------------------------------------------------------------------- #
# Persistence — one rule per model, single JSON keyed by model id
# --------------------------------------------------------------------------- #


def _retrain_rule_path() -> Path:
    return load_settings().workspace_root / "drift_retrain_rules.json"


def _default_retrain_rules() -> dict:
    return {
        m: {
            "model_id": m,
            "signals": [],
            "thresholds": {},
            "duration_window_days": None,
            "human_in_the_loop": None,
            "seasonal_exclusions": [],
            "justification": None,
            "updated_at": None,
        }
        for m in VALID_MODELS
    }


def _load_retrain_rules() -> dict:
    p = _retrain_rule_path()
    if p.exists():
        rules = json.loads(p.read_text())
        for m in VALID_MODELS:
            rules.setdefault(
                m,
                {
                    "model_id": m,
                    "signals": [],
                    "thresholds": {},
                    "duration_window_days": None,
                    "human_in_the_loop": None,
                    "seasonal_exclusions": [],
                    "justification": None,
                    "updated_at": None,
                },
            )
        return rules
    return _default_retrain_rules()


def _save_retrain_rules(rules: dict) -> None:
    _retrain_rule_path().parent.mkdir(parents=True, exist_ok=True)
    _retrain_rule_path().write_text(json.dumps(rules, indent=2))


# --------------------------------------------------------------------------- #
# PSI helper — Population Stability Index
# --------------------------------------------------------------------------- #


def _psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """PSI between reference (expected) and current (actual) distributions."""
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf
    e_counts, _ = np.histogram(expected, bins=breakpoints)
    a_counts, _ = np.histogram(actual, bins=breakpoints)
    e_pct = e_counts / max(e_counts.sum(), 1)
    a_pct = a_counts / max(a_counts.sum(), 1)
    e_pct = np.where(e_pct == 0, 1e-6, e_pct)
    a_pct = np.where(a_pct == 0, 1e-6, a_pct)
    return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))


def _severity(psi: float) -> str:
    return "severe" if psi > 0.25 else "moderate" if psi > 0.10 else "none"


# --------------------------------------------------------------------------- #
# Window simulators — produce a current-distribution view for a named scenario
# --------------------------------------------------------------------------- #


def _simulate_recent_30d(embeddings: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Subsample the reference; near-zero drift expected."""
    n = embeddings.shape[0]
    idx = rng.choice(n, size=min(2000, n), replace=False)
    return embeddings[idx]


def _simulate_imda_csam_mandate(embeddings: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """IMDA scenario: shift the harm-class subset's distribution +0.30σ.

    Ground-truth label distribution is unchanged but the reviewer cohort
    starts flagging more aggressively post-mandate, drifting the per-class
    score distribution.
    """
    out = embeddings.copy()
    n = out.shape[0]
    mask = rng.random(n) < 0.18
    shift = rng.normal(loc=0.30, scale=0.05, size=out.shape[1]).astype(np.float32)
    out[mask] = out[mask] + shift
    return out


def _simulate_election_cycle_drift(embeddings: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Election cycle: adversarial drift — a 25% subset is shifted -0.40σ.

    Adversaries learn the seam and craft posts that score lower across
    the reference distribution; drift is severe on text features.
    """
    out = embeddings.copy()
    n = out.shape[0]
    mask = rng.random(n) < 0.25
    shift = rng.normal(loc=-0.40, scale=0.08, size=out.shape[1]).astype(np.float32)
    out[mask] = out[mask] + shift
    return out


# --------------------------------------------------------------------------- #
# Request models
# --------------------------------------------------------------------------- #


class DriftCheckRequest(BaseModel):
    model_id: str = Field(description=f"one of: {', '.join(VALID_MODELS)}")
    window: str = Field(
        default="recent_30d",
        description=f"one of: {', '.join(VALID_WINDOWS)}",
    )


class RetrainRuleRequest(BaseModel):
    model_id: str = Field(description=f"one of: {', '.join(VALID_MODELS)}")
    signals: list[str] = Field(min_length=1)
    thresholds: dict[str, float]
    duration_window_days: int = Field(ge=1)
    human_in_the_loop: bool
    seasonal_exclusions: list[str] = Field(default_factory=list)
    justification: str = Field(min_length=10)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@router.get("/status/{model_id}")
def drift_status(model_id: str) -> dict:
    if model_id not in VALID_MODELS:
        raise HTTPException(
            422, f"unknown model_id {model_id!r}; expected one of {list(VALID_MODELS)}"
        )
    ctx = get_context()
    ref = ctx.drift_baselines.get(model_id)
    if ref is None:
        return {
            "model_id": model_id,
            "reference_set": False,
            "note": "drift baseline not registered — startup may have failed",
        }
    return {
        "model_id": model_id,
        "reference_set": True,
        "modality": ref.modality,
        "cadence": ref.cadence,
        "n_reference_rows": ref.window_size,
        "n_features": len(ref.feature_means),
        "per_class_calibration_classes": list(ref.per_class_calibration.keys()),
    }


@router.post("/check")
def check_drift(req: DriftCheckRequest) -> dict:
    if req.model_id not in VALID_MODELS:
        raise HTTPException(
            422, f"unknown model_id {req.model_id!r}; expected one of {list(VALID_MODELS)}"
        )
    if req.window not in VALID_WINDOWS:
        raise HTTPException(
            422, f"unknown window {req.window!r}; expected one of {list(VALID_WINDOWS)}"
        )

    ctx = get_context()
    if req.model_id == "image":
        ref_embeddings = ctx.image_embeddings
    elif req.model_id == "text":
        ref_embeddings = ctx.text_embeddings
    else:  # fusion
        ref_embeddings = ctx.image_embeddings  # fusion uses joint image+text view
    rng = np.random.default_rng(7)

    if req.window == "recent_30d":
        current = _simulate_recent_30d(ref_embeddings, rng)
    elif req.window == "imda_csam_mandate":
        current = _simulate_imda_csam_mandate(ref_embeddings, rng)
    elif req.window == "election_cycle_drift":
        current = _simulate_election_cycle_drift(ref_embeddings, rng)
    else:
        # custom: re-synthesise with the per-post seed so signal is stable
        post_ids = (
            ctx.image_post_ids
            if req.model_id == "image"
            else (
                ctx.text_post_ids
                if req.model_id == "text"
                else ctx.fusion_post_ids[: len(ctx.image_post_ids)]
            )
        )
        labels_col = "image_class_label" if req.model_id != "text" else "text_class_label"
        label_lookup = dict(zip(ctx.posts["post_id"].to_list(), ctx.posts[labels_col].to_list()))
        labels = [label_lookup.get(p, "safe") for p in post_ids]
        current = synthesise_embeddings(post_ids, labels, modality=req.model_id, noise_scale=1.10)

    # Per-feature PSI: bin the reference per-feature distribution against the
    # current window; report PSI per feature + overall severity.
    per_feature: dict[str, dict[str, Any]] = {}
    for fi in range(ref_embeddings.shape[1]):
        psi = _psi(ref_embeddings[:, fi], current[:, fi])
        per_feature[f"f{fi}"] = {"psi": round(psi, 4), "severity": _severity(psi)}

    max_psi = max((v["psi"] for v in per_feature.values()), default=0.0)
    n_severe = sum(1 for v in per_feature.values() if v["severity"] == "severe")
    overall = "severe" if n_severe >= 3 else "moderate" if max_psi > 0.10 else "none"

    # Per-class calibration decay: pull the current Brier from the live
    # baseline; decay = current - reference_baseline_at_registration.
    ref_calib = ctx.drift_baselines[req.model_id].per_class_calibration
    if req.model_id == "image":
        live_calib = {
            c: ctx.image_baseline.candidates[ctx.image_baseline.chosen_family].per_class[c]["brier"]
            for c in ref_calib
        }
    elif req.model_id == "text":
        live_calib = {
            c: ctx.text_baseline.candidates[ctx.text_baseline.chosen_family].per_class[c]["brier"]
            for c in ref_calib
        }
    else:
        live_calib = {
            c: (
                ctx.fusion_baseline.early_fusion.per_class[c]["brier"]
                if ctx.fusion_baseline.early_fusion is not None
                else 0.0
            )
            for c in ref_calib
        }

    calibration_decay = {c: round(live_calib[c] - ref_calib[c]["brier"], 4) for c in ref_calib}

    report = {
        "model_id": req.model_id,
        "modality": ctx.drift_baselines[req.model_id].modality,
        "cadence": ctx.drift_baselines[req.model_id].cadence,
        "window": req.window,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "n_features": ref_embeddings.shape[1],
        "n_severe_features": n_severe,
        "max_psi": round(max_psi, 4),
        "per_feature_psi": per_feature,
        "per_class_calibration_decay": calibration_decay,
        "overall_severity": overall,
        "interpretation": (
            "PSI > 0.25 is severe drift on a single feature (retrain signal). "
            ">= 3 features at severe means structural drift, not noise. "
            "Calibration decay > 0.05 on any class indicates score reliability "
            "is degrading even when the distribution is stable."
        ),
    }
    out = load_settings().workspace_root / f"drift_report_{req.model_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    return report


@router.get("/retrain_rule")
def get_retrain_rules() -> dict:
    rules = _load_retrain_rules()
    set_count = sum(1 for r in rules.values() if r.get("updated_at"))
    return {
        "rules": rules,
        "set_count": set_count,
        "expected_count": 3,
        "complete": set_count == 3,
        "note": (
            "Phase 13 of the Playbook requires THREE independent rules. "
            "Image cadence is weekly, text is daily, fusion is per-incident. "
            "A universal 'retrain when X' is BLOCKED."
        ),
    }


@router.post("/retrain_rule")
def set_retrain_rule(req: RetrainRuleRequest) -> dict:
    if req.model_id not in VALID_MODELS:
        raise HTTPException(
            422, f"unknown model_id {req.model_id!r}; expected one of {list(VALID_MODELS)}"
        )
    rules = _load_retrain_rules()
    rules[req.model_id] = {
        "model_id": req.model_id,
        "signals": req.signals,
        "thresholds": req.thresholds,
        "duration_window_days": req.duration_window_days,
        "human_in_the_loop": req.human_in_the_loop,
        "seasonal_exclusions": req.seasonal_exclusions,
        "justification": req.justification,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_retrain_rules(rules)
    set_count = sum(1 for r in rules.values() if r.get("updated_at"))
    return {
        "model_id": req.model_id,
        "rule": rules[req.model_id],
        "set_count": set_count,
        "expected_count": 3,
        "complete": set_count == 3,
    }
