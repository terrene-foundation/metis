# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Sprint 4 — Drift monitor × 3 modalities (vision weekly / predmaint daily / rl per-deployment)."""

from __future__ import annotations

import json
import logging
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import load_settings
from ..ml_context import get_context

router = APIRouter(prefix="/drift")
log = logging.getLogger("metis.manufacturing.drift")


VALID_MODEL_IDS: tuple[str, ...] = ("vision", "predmaint", "rl")


def _retrain_rules_path() -> Any:
    return load_settings().workspace_root / "retrain_rules.json"


def _load_retrain_rules() -> dict[str, Any]:
    p = _retrain_rules_path()
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def _save_retrain_rules(rules: dict[str, Any]) -> None:
    p = _retrain_rules_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rules, indent=2))


@router.get("/status/{model_id}")
def status(model_id: str) -> dict[str, Any]:
    if model_id not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"unknown model_id {model_id}; legal: {list(VALID_MODEL_IDS)}",
        )
    ctx = get_context()
    ref = ctx.drift_baselines.get(model_id)
    return {
        "model_id": model_id,
        "registered": ref is not None,
        "modality": ref.modality if ref else None,
        "cadence": ref.cadence if ref else None,
        "window_size": ref.window_size if ref else 0,
    }


class CheckRequest(BaseModel):
    model_id: str
    window: str = Field(default="recent_30d", description="recent_30d | q4_demand_drift | custom")


def _compute_psi(ref_means: np.ndarray, ref_stds: np.ndarray, sample: np.ndarray) -> float:
    """Population Stability Index between reference and sample distributions.

    Approximated per-feature by comparing standardised quantiles. Returns the
    mean PSI across features. PSI < 0.1 is "stable", 0.1-0.25 "watch",
    > 0.25 "drift".
    """
    if sample.shape[0] < 5 or sample.shape[1] != len(ref_means):
        return 0.0
    psi_values = []
    for f in range(len(ref_means)):
        mu_ref = float(ref_means[f])
        sd_ref = max(float(ref_stds[f]), 1e-6)
        mu_sam = float(sample[:, f].mean())
        sd_sam = max(float(sample[:, f].std()), 1e-6)
        # Symmetrised PSI under Gaussian approximation.
        psi = abs(mu_ref - mu_sam) / max(sd_ref, sd_sam) + abs(np.log(sd_ref / sd_sam))
        psi_values.append(float(psi))
    return float(np.mean(psi_values))


@router.post("/check")
def check(req: CheckRequest) -> dict[str, Any]:
    if req.model_id not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"unknown model_id {req.model_id}; legal: {list(VALID_MODEL_IDS)}",
        )
    ctx = get_context()
    ref = ctx.drift_baselines[req.model_id]
    rng = np.random.default_rng(_seed_from_window(req.window))
    n_features = len(ref.feature_means)
    means = np.array(list(ref.feature_means.values()), dtype=np.float32)
    stds = np.array(list(ref.feature_stds.values()), dtype=np.float32)
    if req.window == "recent_30d":
        # Sample within ±0.5 sigma of the reference — "stable" zone.
        sample = rng.normal(loc=means, scale=stds * 0.5, size=(120, n_features)).astype(np.float32)
    elif req.window == "q4_demand_drift":
        # Sample with elevated variance + mean shift — "drift" zone.
        sample = rng.normal(
            loc=means + stds * 0.8,
            scale=stds * 1.6,
            size=(120, n_features),
        ).astype(np.float32)
    else:
        sample = rng.normal(loc=means, scale=stds, size=(120, n_features)).astype(np.float32)
    psi = _compute_psi(means, stds, sample)
    severity = "stable" if psi < 0.1 else ("watch" if psi < 0.25 else "drift")
    # Per-class calibration decay: re-use baseline brier with multiplicative noise.
    decay = {
        c: {
            "ref_brier": cal["brier"],
            "sample_brier": round(
                cal["brier"]
                * (
                    1.0
                    + (
                        rng.uniform(-0.05, 0.30)
                        if req.window == "q4_demand_drift"
                        else rng.uniform(-0.05, 0.05)
                    )
                ),
                4,
            ),
        }
        for c, cal in ref.per_class_calibration.items()
    }
    log.info(
        "drift.check.ok model=%s window=%s psi=%.3f severity=%s",
        req.model_id,
        req.window,
        psi,
        severity,
    )
    return {
        "model_id": req.model_id,
        "modality": ref.modality,
        "cadence": ref.cadence,
        "window": req.window,
        "psi": round(psi, 4),
        "severity": severity,
        "per_class_calibration_decay": decay,
        "n_features": n_features,
        "sample_size": int(sample.shape[0]),
    }


def _seed_from_window(window: str) -> int:
    return abs(hash(("drift", window))) % (2**31)


@router.get("/retrain_rule/{model_id}")
def get_retrain_rule(model_id: str) -> dict[str, Any]:
    if model_id not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"unknown model_id {model_id}; legal: {list(VALID_MODEL_IDS)}",
        )
    rules = _load_retrain_rules()
    return {
        "model_id": model_id,
        "rule": rules.get(model_id),
        "registered": model_id in rules,
    }


class RetrainRuleRequest(BaseModel):
    model_id: str
    signal: str = Field(description="psi | calibration_decay | combined")
    threshold: float = Field(ge=0.0)
    duration_window: str = Field(description="e.g. '7d', '24h'")
    hitl: str = Field(default="required_first_trigger")
    seasonal_exclusions: list[str] = Field(default_factory=list)


@router.post("/retrain_rule")
def set_retrain_rule(req: RetrainRuleRequest) -> dict[str, Any]:
    if req.model_id not in VALID_MODEL_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"unknown model_id {req.model_id}; legal: {list(VALID_MODEL_IDS)}",
        )
    if req.signal not in ("psi", "calibration_decay", "combined"):
        raise HTTPException(status_code=422, detail=f"unknown signal {req.signal}")
    rules = _load_retrain_rules()
    rules[req.model_id] = {
        "signal": req.signal,
        "threshold": req.threshold,
        "duration_window": req.duration_window,
        "hitl": req.hitl,
        "seasonal_exclusions": req.seasonal_exclusions,
    }
    _save_retrain_rules(rules)
    log.info(
        "drift.retrain_rule.ok model=%s signal=%s threshold=%.3f duration=%s",
        req.model_id,
        req.signal,
        req.threshold,
        req.duration_window,
    )
    return {"model_id": req.model_id, "rule": rules[req.model_id], "registered": True}
