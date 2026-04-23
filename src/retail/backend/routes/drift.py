# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Drift endpoints — Sprint 3 of the Playbook.

Segmentation-drift signal: re-cluster a recent window and measure how many
customers change segment assignment (segment churn %). Feature-level drift
uses a PSI proxy against the drift_baseline reference distribution.

Endpoints
---------
- `GET  /drift/status/<model_id>`    — whether reference is registered
- `POST /drift/check`                — run a drift check against a named window
- `POST /drift/retrain_rule`         — student proposes the retrain trigger
- `GET  /drift/retrain_rule`         — current retrain rule
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sklearn.preprocessing import StandardScaler

from ..config import load_settings
from ..ml_context import CLUSTER_FEATURES, get_context

router = APIRouter()


def _retrain_rule_path() -> Path:
    return load_settings().data_dir / "retrain_rule.json"


def _load_retrain_rule() -> dict:
    p = _retrain_rule_path()
    if p.exists():
        return json.loads(p.read_text())
    return {
        "signals": [],
        "thresholds": {},
        "duration_window_days": None,
        "human_in_the_loop": None,
        "justification": None,
        "updated_at": None,
    }


def _psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf
    e_counts, _ = np.histogram(expected, bins=breakpoints)
    a_counts, _ = np.histogram(actual, bins=breakpoints)
    e_pct = e_counts / max(e_counts.sum(), 1)
    a_pct = a_counts / max(a_counts.sum(), 1)
    # avoid log(0)
    e_pct = np.where(e_pct == 0, 1e-6, e_pct)
    a_pct = np.where(a_pct == 0, 1e-6, a_pct)
    return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))


class DriftCheckRequest(BaseModel):
    window: str = Field(
        default="recent_30d",
        description="recent_30d | catalog_drift | custom",
    )


class RetrainRuleRequest(BaseModel):
    signals: list[str]
    thresholds: dict[str, float]
    duration_window_days: int
    human_in_the_loop: bool
    justification: str


@router.get("/status/{model_id}")
def drift_status(model_id: str) -> dict:
    ctx = get_context()
    return {
        "model_id": model_id,
        "reference_set": True,
        "reference_window": ctx.drift_reference.get("window"),
        "n_reference_rows": ctx.drift_reference.get("n_customers"),
        "feature_columns": list(ctx.drift_reference.get("features", {}).keys()),
    }


def _simulate_catalog_drift(customers: pl.DataFrame, rng: np.random.Generator) -> pl.DataFrame:
    """Inject the Sprint-3 catalog-drift scenario.

    Wellness-category launch: 12 % of customers shift to higher luxury fraction
    and higher visit frequency; new seasonal purchase patterns.
    """
    n = len(customers)
    mask = rng.random(n) < 0.12
    out = customers.with_columns(
        [
            pl.when(pl.Series(mask))
            .then(pl.col("luxury_category_fraction") + 0.15)
            .otherwise(pl.col("luxury_category_fraction"))
            .clip(0.0, 1.0)
            .alias("luxury_category_fraction"),
            pl.when(pl.Series(mask))
            .then(pl.col("visits_per_week") * 1.25)
            .otherwise(pl.col("visits_per_week"))
            .alias("visits_per_week"),
        ]
    )
    return out


@router.post("/check")
def check_drift(req: DriftCheckRequest) -> dict:
    ctx = get_context()
    rng = np.random.default_rng(7)

    if req.window == "recent_30d":
        # Use customers who signed up in last 30 days as the "current" window
        current = ctx.customers.filter(pl.col("days_since_last_visit") <= 30)
    elif req.window == "catalog_drift":
        current = _simulate_catalog_drift(ctx.customers, rng)
    else:
        raise HTTPException(422, f"unknown window {req.window!r}")

    ref_features = ctx.drift_reference["features"]
    per_feature = {}
    for feat in CLUSTER_FEATURES:
        if feat not in current.columns:
            continue
        # Generate synthetic reference values from the summary stats we stored
        stats = ref_features.get(feat)
        if stats is None:
            continue
        ref_sim = rng.normal(stats["mean"], max(stats["std"], 1e-6), size=2000)
        cur_vals = current[feat].to_numpy()
        psi = _psi(ref_sim, cur_vals)
        per_feature[feat] = {
            "psi": round(psi, 4),
            "severity": "severe" if psi > 0.25 else "moderate" if psi > 0.10 else "none",
        }

    # Segment churn: re-cluster current window with baseline model, compare assignments
    X_cur = current.select(CLUSTER_FEATURES).to_numpy()
    X_cur_std = ctx.baseline.scaler.transform(X_cur)
    new_labels = ctx.baseline.model.predict(X_cur_std)

    if req.window == "recent_30d":
        # Restrict baseline labels to the same customers
        cust_id_idx = {c: i for i, c in enumerate(ctx.baseline.customer_ids)}
        relevant = [cust_id_idx.get(c) for c in current["customer_id"].to_list()]
        if None in relevant:
            churn = None
        else:
            L0 = ctx.baseline.labels[np.array(relevant)]
            churn = float(np.mean(L0 != new_labels))
    else:
        L0 = ctx.baseline.labels
        churn = float(np.mean(L0 != new_labels))

    max_psi = max((v["psi"] for v in per_feature.values()), default=0.0)
    overall = (
        "severe"
        if max_psi > 0.25 or (churn or 0) > 0.20
        else "moderate" if max_psi > 0.10 or (churn or 0) > 0.10 else "none"
    )

    report = {
        "window": req.window,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "per_feature_psi": per_feature,
        "segment_membership_churn": round(churn, 4) if churn is not None else None,
        "overall_severity": overall,
        "interpretation": (
            "PSI >0.25 is severe drift (retrain signal). Churn >20 % means "
            "cluster assignments are moving faster than the model can keep up."
        ),
    }

    # Persist to disk for viewer
    out = load_settings().data_dir / "drift_report.json"
    out.write_text(json.dumps(report, indent=2))
    return report


@router.get("/retrain_rule")
def get_retrain_rule() -> dict:
    return _load_retrain_rule()


@router.post("/retrain_rule")
def set_retrain_rule(req: RetrainRuleRequest) -> dict:
    rule = {
        "signals": req.signals,
        "thresholds": req.thresholds,
        "duration_window_days": req.duration_window_days,
        "human_in_the_loop": req.human_in_the_loop,
        "justification": req.justification,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _retrain_rule_path().write_text(json.dumps(rule, indent=2))
    return rule
