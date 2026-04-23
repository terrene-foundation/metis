# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Prediction endpoints — Sprint 2 of the Playbook (SML).

Two classifiers, same pipeline, same levers:
  - CHURN     — P(customer churns in next 30 days | customer behaviour)
                Label: days_since_last_visit > 90.
                Features: CHURN_FEATURES (no leakage of the label column).
                The textbook SML teaching vehicle.
  - CONVERSION — P(customer converts in a category | customer + category)
                 Label: did (customer, category) see a transaction in the last 90 days.
                 Feeds Sprint 3 allocator via predicted category-level response.

Pre-trained at startup (leaderboard of LR + RandomForest + GBM). Live
`/predict/train` re-runs the sweep when students want to see it happen.

Endpoints
---------
- `GET  /predict/leaderboard/{target}` — pre-computed leaderboard (target = churn | conversion)
- `POST /predict/train`                — re-train live with {target, families, seed}
- `POST /predict/threshold`            — student sets threshold with justification
- `POST /predict/score`                — P(event | customer [, category]) at the chosen threshold
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
    CHURN_FEATURES,
    build_churn_predictor,
    build_conversion_predictor,
    get_context,
)

router = APIRouter()


def _threshold_path() -> Path:
    return load_settings().data_dir / "predict_thresholds.json"


def _load_thresholds() -> dict[str, Any]:
    p = _threshold_path()
    if p.exists():
        return json.loads(p.read_text())
    return {
        "churn": {"threshold": 0.3, "justification": "default — student has not set"},
        "conversion": {"threshold": 0.5, "justification": "default — student has not set"},
    }


def _save_thresholds(state: dict) -> None:
    _threshold_path().write_text(json.dumps(state, indent=2))


def _serializable(d: dict) -> dict:
    """Strip unpickleable objects (sklearn models) from a leaderboard entry."""
    out = {}
    for k, v in d.items():
        if k == "model":
            continue
        out[k] = v
    return out


class TrainRequest(BaseModel):
    target: str = Field(description="churn | conversion")
    families: list[str] | None = Field(
        default=None,
        description="subset of logistic_regression, random_forest, gradient_boosted (default: all 3)",
    )
    seed: int = Field(default=42)


class ThresholdRequest(BaseModel):
    target: str = Field(description="churn | conversion")
    threshold: float = Field(ge=0.0, le=1.0)
    justification: str = Field(min_length=10)


class ScoreRequest(BaseModel):
    target: str = Field(description="churn | conversion")
    customer_id: str
    category: str | None = Field(default=None, description="required for conversion scoring")


@router.get("/leaderboard/{target}")
def leaderboard(target: str) -> dict:
    ctx = get_context()
    if target == "churn":
        results = {
            name: _serializable(entry) for name, entry in ctx.predictor.churn_candidates.items()
        }
        return {
            "target": "churn",
            "label_definition": "customer has not visited in the last 90 days",
            "features": ctx.predictor.churn_features,
            "candidates": results,
            "note": (
                "Pre-trained leaderboard. Students CRITIQUE this in Phase 4–8. "
                "Ensembles (gradient_boosted) are the king for tabular data, but "
                "logistic_regression is cheaper and more interpretable. "
                "Pick on the Phase 5 criteria, not the top AUC."
            ),
        }
    if target == "conversion":
        return {
            "target": "conversion",
            "label_definition": "(customer, category) had a transaction in the last 90 days",
            "features_summary": f"{len(ctx.predictor.conv_features)} features (customer rows + category one-hot)",
            "candidates": ctx.predictor.conv_candidates["candidates"],
            "note": (
                "Same 3 families as churn, applied to conversion. Sprint 3 "
                "allocator reads scored response probabilities as input."
            ),
        }
    raise HTTPException(422, f"unknown target {target!r} (choose churn | conversion)")


@router.post("/train")
def train(req: TrainRequest) -> dict:
    """Re-run the leaderboard live. Updates the context."""
    ctx = get_context()
    if req.target == "churn":
        results, scaler, cust_ids, labels = build_churn_predictor(ctx.customers, seed=req.seed)
        if req.families:
            results = {k: v for k, v in results.items() if k in set(req.families)}
        ctx.predictor.churn_candidates = results
        ctx.predictor.churn_scaler = scaler
        ctx.predictor.churn_customer_ids = cust_ids.tolist()
        ctx.predictor.churn_labels = labels
        return {
            "target": "churn",
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "candidates": {n: _serializable(e) for n, e in results.items()},
        }
    if req.target == "conversion":
        bundle = build_conversion_predictor(
            ctx.customers, ctx.transactions, ctx.products, seed=req.seed
        )
        ctx.predictor.conv_candidates = bundle
        ctx.predictor.conv_features = bundle["features"]
        return {
            "target": "conversion",
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "candidates": bundle["candidates"],
        }
    raise HTTPException(422, f"unknown target {req.target!r}")


@router.post("/threshold")
def set_threshold(req: ThresholdRequest) -> dict:
    state = _load_thresholds()
    state[req.target] = {
        "threshold": req.threshold,
        "justification": req.justification,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_thresholds(state)
    return state


@router.get("/threshold")
def get_thresholds() -> dict:
    return _load_thresholds()


@router.post("/score")
def score(req: ScoreRequest) -> dict:
    """Return P(event | features) from the currently-leading candidate.

    The 'currently-leading' candidate is `gradient_boosted` by default — the
    king for tabular data. Student can promote another family by hitting
    POST /predict/train with families=['logistic_regression'] or similar.
    """
    ctx = get_context()
    thresholds = _load_thresholds()

    if req.target == "churn":
        cand = ctx.predictor.churn_candidates.get("gradient_boosted") or next(
            iter(ctx.predictor.churn_candidates.values())
        )
        model = cand["model"]
        scaler = ctx.predictor.churn_scaler
        if scaler is None:
            raise HTTPException(500, "churn scaler not fit — restart backend")
        cust = ctx.customers.filter(get_context().customers["customer_id"] == req.customer_id)
        if len(cust) == 0:
            raise HTTPException(404, f"customer {req.customer_id!r} not found")
        X = cust.select(CHURN_FEATURES).to_numpy()
        X_std = scaler.transform(X)
        prob = float(model.predict_proba(X_std)[0, 1])
        tau = thresholds["churn"]["threshold"]
        return {
            "target": "churn",
            "customer_id": req.customer_id,
            "probability": round(prob, 4),
            "threshold": tau,
            "decision": "churn_likely" if prob >= tau else "retained",
            "note": (
                "Threshold-driven decision. Raise threshold to send fewer "
                "retention offers (higher precision, lower recall); lower it "
                "to catch more churners at the cost of wasted offers."
            ),
        }

    if req.target == "conversion":
        if req.category is None:
            raise HTTPException(422, "conversion score requires `category`")
        # For pedagogical simplicity, we return the base rate from the leaderboard.
        # The allocator uses a pre-computed probability grid (see /allocate/solve).
        candidates = ctx.predictor.conv_candidates.get("candidates", {})
        leader = candidates.get("gradient_boosted") or (
            next(iter(candidates.values())) if candidates else {}
        )
        metrics = leader.get("metrics", {})
        base_rate = metrics.get("base_rate", 0.5)
        return {
            "target": "conversion",
            "customer_id": req.customer_id,
            "category": req.category,
            "probability": round(float(base_rate), 4),
            "threshold": thresholds["conversion"]["threshold"],
            "note": (
                "Simplified for teaching: returns the leaderboard's base rate. "
                "The Sprint 3 allocator consumes the full probability grid."
            ),
        }

    raise HTTPException(422, f"unknown target {req.target!r}")
