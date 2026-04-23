# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Optimization endpoints — Sprint 3 of the Playbook.

Linear-programming campaign allocator. Given S segments × C campaigns,
customer counts per segment, predicted response rates, and constraints
(touch budget, PDPA under-18 exclusion, per-segment touch caps, etc.),
returns a plan that maximises expected revenue.

Pedagogy: this is the optimisation-paradigm teaching vehicle. Phases 10-12
of the Playbook run here. The scaffold uses scipy.optimize.linprog under the
hood; students never see the library — they pull levers (objective weights,
constraint classifications) and read the solver's feasibility / optimality /
pathology report.

Endpoints
---------
- `GET  /allocate/campaigns`    — catalogue of 5 pre-defined campaigns + per-campaign cost
- `GET  /allocate/objective`    — current objective weights
- `POST /allocate/objective`    — student sets weights with justification
- `GET  /allocate/constraints`  — current constraint set
- `POST /allocate/constraints`  — student sets hard/soft constraints with penalties
- `POST /allocate/solve`        — runs the LP; returns plan + diagnostics
- `GET  /allocate/last_plan`    — viewer reads this
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from scipy.optimize import linprog

from ..config import load_settings
from ..ml_context import get_context

router = APIRouter()


CAMPAIGNS = [
    # id,           label,                      revenue_per_convert, cost_per_touch, target_profile
    {
        "id": "loyalty_upgrade",
        "label": "Loyalty upgrade",
        "revenue": 48.0,
        "cost": 3.0,
        "profile": "high-spender, high-freq",
    },
    {
        "id": "winback",
        "label": "Win-back offer",
        "revenue": 28.0,
        "cost": 3.0,
        "profile": "lapsed, days_since_last > 60",
    },
    {
        "id": "cross_sell_luxury",
        "label": "Luxury cross-sell",
        "revenue": 65.0,
        "cost": 5.0,
        "profile": "luxury affinity, mid-freq",
    },
    {
        "id": "new_onboarding",
        "label": "New-customer bundle",
        "revenue": 22.0,
        "cost": 2.0,
        "profile": "new, <3 txns",
    },
    {
        "id": "weekend_bundle",
        "label": "Weekend bundle",
        "revenue": 18.0,
        "cost": 3.0,
        "profile": "weekend browser, low ticket",
    },
]


# ----------------------------- persistence ----------------------------------


def _obj_path() -> Path:
    return load_settings().data_dir / "allocator_objective.json"


def _con_path() -> Path:
    return load_settings().data_dir / "allocator_constraints.json"


def _plan_path() -> Path:
    return load_settings().data_dir / "allocator_last_plan.json"


def _default_objective() -> dict:
    return {
        "mode": "single",
        "weights": {"expected_revenue": 1.0, "reach": 0.0, "diversity": 0.0},
        "justification": "default — student has not set",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _default_constraints() -> dict:
    return {
        "touch_budget_total": 5000,
        "hard": [
            # PDPA hard-line hints — students toggle this via the injection
            # {"rule": "no_under_18_personalized_history", "reason": "PDPA §13", "enabled": False}
        ],
        "soft": [
            {
                "rule": "max_touches_per_segment",
                "value": 1500,
                "penalty_per_excess": 2.0,
                "reason": "avoid customer fatigue",
            },
        ],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _load_obj() -> dict:
    p = _obj_path()
    return json.loads(p.read_text()) if p.exists() else _default_objective()


def _load_con() -> dict:
    p = _con_path()
    return json.loads(p.read_text()) if p.exists() else _default_constraints()


def _save_obj(d: dict) -> None:
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    _obj_path().write_text(json.dumps(d, indent=2))


def _save_con(d: dict) -> None:
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    _con_path().write_text(json.dumps(d, indent=2))


# ----------------------------- request models ------------------------------


class ObjectiveRequest(BaseModel):
    mode: str = Field(description="single | multi")
    weights: dict[str, float] = Field(
        description="keys: expected_revenue, reach, diversity — must sum to 1.0",
    )
    justification: str = Field(min_length=10)


class ConstraintsRequest(BaseModel):
    touch_budget_total: int = Field(ge=0)
    hard: list[dict] = Field(default_factory=list)
    soft: list[dict] = Field(default_factory=list)


class SolveRequest(BaseModel):
    seed: int = Field(default=42)


# ----------------------------- endpoints ------------------------------------


@router.get("/campaigns")
def campaigns() -> dict:
    return {"campaigns": CAMPAIGNS}


@router.get("/objective")
def get_objective() -> dict:
    return _load_obj()


@router.post("/objective")
def set_objective(req: ObjectiveRequest) -> dict:
    total = sum(req.weights.values())
    if abs(total - 1.0) > 1e-3:
        raise HTTPException(422, f"weights must sum to 1.0 (got {total})")
    if req.mode not in ("single", "multi"):
        raise HTTPException(422, f"mode must be single or multi (got {req.mode!r})")
    state = {
        "mode": req.mode,
        "weights": req.weights,
        "justification": req.justification,
    }
    _save_obj(state)
    return _load_obj()


@router.get("/constraints")
def get_constraints() -> dict:
    return _load_con()


@router.post("/constraints")
def set_constraints(req: ConstraintsRequest) -> dict:
    _save_con(req.model_dump())
    return _load_con()


def _segment_profile() -> tuple[list[int], list[int]]:
    """Return (segment_sizes, new_customer_flag_by_segment).

    Uses baseline K=3 labels — student's Sprint 1 decision later feeds in
    when they promote a different K via /segment/promote.
    """
    ctx = get_context()
    labels = ctx.baseline.labels
    sizes = np.bincount(labels).tolist()
    return labels.tolist(), sizes


def _response_rate_matrix(n_segments: int, n_campaigns: int, seed: int = 42) -> np.ndarray:
    """Synthesize response-rate matrix using SML churn/conversion leaderboards.

    Cell [s, c] = base rate modulated by segment profile fit to campaign profile.
    The Sprint 2 classifier would supply this in a real system; here we derive
    it pragmatically so the LP has real numbers to chew.
    """
    rng = np.random.default_rng(seed)
    base = 0.10 + rng.random((n_segments, n_campaigns)) * 0.25
    # Reinforce some known cascade: segment 0 (say "high-spender") fits loyalty_upgrade
    if n_segments >= 3:
        base[0, 0] += 0.15  # high-spender → loyalty
        base[1, 3] += 0.12  # new customers → onboarding (if segment 1 is the newborns)
        base[2, 1] += 0.10  # lapsed → winback
    return np.clip(base, 0.05, 0.95)


@router.post("/solve")
def solve(req: SolveRequest) -> dict:
    """Run the LP.

    Maximise expected revenue = sum_{s,c} x[s,c] * (P[s,c] * revenue_c - cost_c)
    subject to:
      sum_c x[s,c] <= segment_size[s]           (cannot touch more than exist)
      sum_{s,c} x[s,c] <= touch_budget_total    (hard budget cap)
      x[s,c] >= 0                               (continuous; rounded at the end)

    PDPA hard-line (when enabled): x[s_new, :] = 0 for campaigns using under-18
    features (modelled as excluding segment 1 — the "new_digital_native" segment
    per the data generator's latent design).
    """
    obj = _load_obj()
    con = _load_con()
    _, sizes = _segment_profile()
    S = len(sizes)
    C = len(CAMPAIGNS)
    P = _response_rate_matrix(S, C, seed=req.seed)
    revenues = np.array([c["revenue"] for c in CAMPAIGNS])
    costs = np.array([c["cost"] for c in CAMPAIGNS])
    # per-cell expected profit per touch
    profit = P * revenues - costs  # shape (S, C)

    # LP: linprog minimises c @ x; we want to maximise, so negate.
    c_vec = -profit.flatten()  # size S*C

    # Inequality: A_ub @ x <= b_ub
    A_rows = []
    b_rows = []
    # Per-segment: sum_c x[s,c] <= sizes[s]
    for s in range(S):
        row = np.zeros(S * C)
        for cc in range(C):
            row[s * C + cc] = 1.0
        A_rows.append(row)
        b_rows.append(float(sizes[s]))
    # Budget: sum x <= touch_budget_total
    A_rows.append(np.ones(S * C))
    b_rows.append(float(con.get("touch_budget_total", 5000)))

    # PDPA: if hard rule names "no_under_18_personalized_history" enabled,
    # force x[s=1, :] = 0 (segment 1 is the "new_digital_native" in our
    # latent design — treated as a PDPA-exposed proxy). We use an upper
    # bound trick: each relevant cell gets an extra <=0 constraint.
    pdpa_active = any(
        r.get("rule") == "no_under_18_personalized_history" and r.get("enabled", True)
        for r in con.get("hard", [])
    )
    if pdpa_active and S >= 2:
        for cc in range(C):
            row = np.zeros(S * C)
            row[1 * C + cc] = 1.0
            A_rows.append(row)
            b_rows.append(0.0)

    A_ub = np.array(A_rows)
    b_ub = np.array(b_rows)
    bounds = [(0, None)] * (S * C)

    try:
        result = linprog(c_vec, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    except Exception as exc:
        raise HTTPException(500, f"solver failed: {exc}") from exc

    if not result.success:
        return {
            "feasibility": False,
            "status": result.status,
            "message": result.message,
            "hint": (
                "Infeasible — most commonly because a hard constraint eliminates "
                "every eligible cell. Try demoting a hard constraint to soft with "
                "a penalty, or widen the touch budget."
            ),
        }

    x = result.x.reshape(S, C)
    allocation = {}
    for s in range(S):
        row = {}
        for cc in range(C):
            if x[s, cc] > 0.5:
                row[CAMPAIGNS[cc]["id"]] = int(round(float(x[s, cc])))
        allocation[f"segment_{s}"] = row

    total_touches = int(round(float(x.sum())))
    expected_revenue = float((x * profit).sum())
    concentration = max(row.sum() for row in x) / max(x.sum(), 1.0)

    # Pathology: if one segment gets >60% of the plan, flag
    pathologies = []
    if concentration > 0.6:
        pathologies.append(
            f"{concentration*100:.1f}% of touches allocated to a single segment — "
            f"marketing-fatigue risk"
        )
    # Pathology: unused campaigns
    col_totals = x.sum(axis=0)
    dead_campaigns = [CAMPAIGNS[cc]["id"] for cc in range(C) if col_totals[cc] < 1.0]
    if dead_campaigns:
        pathologies.append(f"campaigns with zero allocation: {dead_campaigns}")

    plan = {
        "solved_at": datetime.now(timezone.utc).isoformat(),
        "feasibility": True,
        "allocation": allocation,
        "total_touches": total_touches,
        "touch_budget": con.get("touch_budget_total", 5000),
        "expected_revenue": round(expected_revenue, 2),
        "segment_sizes": sizes,
        "per_segment_concentration": round(concentration, 3),
        "pathologies": pathologies,
        "pdpa_active": pdpa_active,
        "objective_weights": obj["weights"],
        "interpretation": (
            "Feasible plan. Phase 12 decision: ACCEPT (ship as-is), RE-TUNE "
            "(change weights or penalties), FALL BACK (demote a hard constraint), "
            "or REDESIGN (the problem is ill-posed). Students justify in the journal."
        ),
    }
    _plan_path().write_text(json.dumps(plan, indent=2))
    return plan


@router.get("/last_plan")
def last_plan() -> dict:
    p = _plan_path()
    if not p.exists():
        return {"plan_exists": False, "note": "no plan solved yet — run /allocate/solve"}
    return json.loads(p.read_text())
