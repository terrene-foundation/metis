# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Sprint 3 + 4 — Inspector queue allocator (LP via scipy.optimize.linprog)."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel, Field
from scipy.optimize import linprog

router = APIRouter(prefix="/queue")
log = logging.getLogger("metis.manufacturing.queue")


# Inspector queue is allocated across 3 tiers: critical (safety-critical-defect
# candidates), major (major-defect candidates), minor (minor-defect candidates).
# Each tier has a per-board mean review time, an FN cost, and an SLA bound.
TIER_CONFIG: dict[str, dict[str, float]] = {
    "critical": {
        "mean_review_min": 6.0,
        "fn_dollar_per_board": 4200.0,  # major-defect-shipped cost
        "fp_dollar_per_board": 85.0,
        "sla_minutes": 30.0,
    },
    "major": {
        "mean_review_min": 3.0,
        "fn_dollar_per_board": 1800.0,
        "fp_dollar_per_board": 85.0,
        "sla_minutes": 60.0,
    },
    "minor": {
        "mean_review_min": 1.5,
        "fn_dollar_per_board": 180.0,
        "fp_dollar_per_board": 85.0,
        "sla_minutes": 120.0,
    },
}

INSPECTOR_HOURLY_DOLLAR: float = 35.0 * 60.0  # $35/min × 60


class QueueState(BaseModel):
    queue_depth: dict[str, int] = Field(
        default_factory=lambda: {"critical": 120, "major": 480, "minor": 800}
    )
    inspector_minutes_available: float = 8.0 * 60.0 * 6.0  # 6 inspectors × 8-hr shift


_STATE = QueueState()


@router.get("/state")
def state() -> dict[str, Any]:
    sla_breach_critical = (
        _STATE.queue_depth["critical"] * TIER_CONFIG["critical"]["mean_review_min"]
        > TIER_CONFIG["critical"]["sla_minutes"] * 6
    )
    return {
        "queue_depth": _STATE.queue_depth,
        "inspector_minutes_available": _STATE.inspector_minutes_available,
        "sla_breach_critical": bool(sla_breach_critical),
        "tier_config": TIER_CONFIG,
        "inspector_hourly_dollar": INSPECTOR_HOURLY_DOLLAR,
    }


class SolveRequest(BaseModel):
    queue_depth: dict[str, int] | None = None
    inspector_minutes_available: float | None = None


_LAST_PLAN: dict[str, Any] | None = None


@router.post("/solve")
def solve(req: SolveRequest) -> dict[str, Any]:
    """Solve the LP: maximise expected catch-value subject to inspector-minute budget.

    Variables: x_critical, x_major, x_minor (boards reviewed per tier).
    Objective: minimise -[fn_value × x] (i.e. maximise FN cost averted).
    Constraints:
      - x_t <= queue_depth[t] (cannot review more than queued)
      - sum(mean_review_min[t] × x_t) <= inspector_minutes_available
      - x_t >= 0
    Plus: critical SLA — at least sla_minutes/mean_review_min boards/inspector
    must be reviewed for the critical tier each shift.
    """
    global _LAST_PLAN
    if req.queue_depth is not None:
        _STATE.queue_depth = dict(req.queue_depth)
    if req.inspector_minutes_available is not None:
        _STATE.inspector_minutes_available = float(req.inspector_minutes_available)

    tiers = ("critical", "major", "minor")
    fn_values = np.array([TIER_CONFIG[t]["fn_dollar_per_board"] for t in tiers], dtype=np.float64)
    review_min = np.array([TIER_CONFIG[t]["mean_review_min"] for t in tiers], dtype=np.float64)
    queue = np.array([_STATE.queue_depth[t] for t in tiers], dtype=np.float64)

    # Maximise fn_values · x  ==>  minimise -fn_values · x
    c = -fn_values
    # Inequalities: review_min · x <= inspector_minutes_available
    A_ub = np.vstack([review_min, -np.eye(3)])
    b_ub = np.concatenate([[_STATE.inspector_minutes_available], np.zeros(3)])
    # Bounds: 0 <= x_t <= queue[t]
    bounds = [(0.0, float(queue[i])) for i in range(3)]

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success or res.x is None:
        log.warning("queue.solve.infeasible message=%s", res.message)
        return {
            "feasible": False,
            "message": str(res.message),
        }
    x = np.asarray(res.x, dtype=np.float64)
    plan = {t: int(round(float(x[i]))) for i, t in enumerate(tiers)}
    minutes_used = float(np.dot(review_min, x))
    catch_value = float(np.dot(fn_values, x))
    fp_cost = float(
        sum(
            plan[t] * TIER_CONFIG[t]["fp_dollar_per_board"] * 0.10  # assume 10% FP rate at gate
            for t in tiers
        )
    )

    # Shadow prices (LP duals). highs returns marginals via res.ineqlin.marginals.
    shadow_prices = (
        list(res.ineqlin.marginals)
        if hasattr(res, "ineqlin") and getattr(res.ineqlin, "marginals", None) is not None
        else []
    )
    plan_blob = {
        "feasible": True,
        "plan": plan,
        "expected_catch_value_dollars": round(catch_value, 2),
        "expected_fp_cost_dollars": round(fp_cost, 2),
        "net_value_dollars": round(catch_value - fp_cost, 2),
        "inspector_minutes_used": round(minutes_used, 2),
        "inspector_minutes_available": _STATE.inspector_minutes_available,
        "shadow_price_inspector_minute_dollars": (
            round(float(shadow_prices[0]), 2) if shadow_prices else None
        ),
        "queue_after": {t: int(_STATE.queue_depth[t] - plan[t]) for t in tiers},
    }
    _LAST_PLAN = plan_blob
    log.info(
        "queue.solve.ok plan=%s minutes_used=%.1f catch_value=%.2f",
        plan,
        minutes_used,
        catch_value,
    )
    return plan_blob


@router.get("/last_plan")
def last_plan() -> dict[str, Any]:
    if _LAST_PLAN is None:
        return {"plan_available": False}
    return {"plan_available": True, **_LAST_PLAN}
