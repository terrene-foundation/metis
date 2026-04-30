# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Reviewer queue allocator — Sprint 3 of the Playbook (Optimisation · Decide).

Linear-programming reviewer-minute allocator. Given T queue tiers × R
reviewer pools, per-tier expected backlog, per-tier per-post minutes, and
constraints (reviewer headcount, SLA, IMDA priority routing), returns an
allocation plan that minimises (SLA breach cost + reviewer-time cost).

Mid-Sprint-3 IMDA injection (~4:30pm in the workshop): IMDA mandates that
posts scoring > 0.40 on csam_adjacent route to mandatory human review
within 60 seconds AND get auto-blurred. This forces re-classification of
the imda_priority tier from "soft prefer" to "hard required" AND re-solves
the LP with the new constraint shape. Phase 11 + Phase 12 BOTH re-run.

Endpoints
---------
- `GET  /queue/state`            — current backlog, reviewer headcount, SLA
- `GET  /queue/tiers`            — tier catalogue + per-tier per-post minutes
- `GET  /queue/objective`        — current objective weights
- `POST /queue/objective`        — set objective weights with justification
- `GET  /queue/constraints`      — current constraint set
- `POST /queue/constraints`      — set hard/soft constraints
- `POST /queue/solve`            — run the LP; return plan + pathologies
- `GET  /queue/last_plan`        — viewer reads this
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from scipy.optimize import linprog

from ..config import load_settings
from ..ml_context import get_context

router = APIRouter()


# Queue tiers — five priority lanes the queue allocator splits across.
# minutes_per_post is the wall-clock reviewer time for one decision in that
# tier. sla_seconds is the SLA the Reviewer Ops Lead targets; 60 seconds for
# imda_priority is an IMDA-driven hard ceiling, others are operational.
TIERS = [
    {
        "id": "imda_priority",
        "label": "IMDA priority (CSAM-adjacent + terrorism)",
        "minutes_per_post": 4.0,
        "sla_seconds": 60,
        "fn_cost": 320.0,
        "imda_critical": True,
    },
    {
        "id": "self_harm_review",
        "label": "Self-harm encouragement",
        "minutes_per_post": 3.5,
        "sla_seconds": 600,
        "fn_cost": 320.0,
        "imda_critical": False,
    },
    {
        "id": "threats_review",
        "label": "Threats / harassment escalation",
        "minutes_per_post": 3.0,
        "sla_seconds": 1800,
        "fn_cost": 320.0,
        "imda_critical": False,
    },
    {
        "id": "hate_speech_review",
        "label": "Hate-speech review",
        "minutes_per_post": 2.5,
        "sla_seconds": 5400,
        "fn_cost": 320.0,
        "imda_critical": False,
    },
    {
        "id": "general_review",
        "label": "General gray-zone review",
        "minutes_per_post": 2.0,
        "sla_seconds": 5400,
        "fn_cost": 80.0,
        "imda_critical": False,
    },
]

# Reviewer pools — three skill tiers, three cost rates ($/minute).
REVIEWER_POOLS = [
    {
        "id": "senior",
        "label": "Senior reviewers (CSAM-adjacent qualified)",
        "cost_per_min": 32.0,
        "headcount": 12,
        "qualified_tiers": [
            "imda_priority",
            "self_harm_review",
            "threats_review",
            "hate_speech_review",
            "general_review",
        ],
    },
    {
        "id": "standard",
        "label": "Standard reviewers",
        "cost_per_min": 22.0,
        "headcount": 50,
        "qualified_tiers": [
            "self_harm_review",
            "threats_review",
            "hate_speech_review",
            "general_review",
        ],
    },
    {
        "id": "surge",
        "label": "Surge / contractor overflow",
        "cost_per_min": 18.0,
        "headcount": 38,
        "qualified_tiers": ["hate_speech_review", "general_review"],
    },
]

# Default expected backlog (posts/day awaiting review per tier).
DEFAULT_BACKLOG = {
    "imda_priority": 80,
    "self_harm_review": 240,
    "threats_review": 460,
    "hate_speech_review": 1800,
    "general_review": 5500,
}

# Reviewer-minute working budget per reviewer per shift (8h shift × 60 min × 0.83
# tooling utilisation ≈ 400 effective minutes/day).
WORKING_MINUTES_PER_REVIEWER = 400


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #


def _obj_path() -> Path:
    return load_settings().workspace_root / "queue_objective.json"


def _con_path() -> Path:
    return load_settings().workspace_root / "queue_constraints.json"


def _plan_path() -> Path:
    return load_settings().workspace_root / "queue_last_plan.json"


def _default_objective() -> dict:
    return {
        "weights": {
            "minimise_sla_breach": 0.7,
            "minimise_reviewer_cost": 0.3,
        },
        "justification": "default — student has not set",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _default_constraints() -> dict:
    return {
        "hard": [
            # imda_priority hard-required is OFF by default; flips ON post-injection.
            {
                "rule": "imda_priority_must_clear_within_sla",
                "enabled": False,
                "reason": "IMDA mandate clarification (Sprint 3 injection)",
            }
        ],
        "soft": [
            {
                "rule": "max_minutes_per_pool",
                "value": "headcount × WORKING_MINUTES_PER_REVIEWER",
                "penalty_per_excess": 5.0,
                "reason": "reviewer fatigue cap",
            }
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
    _obj_path().parent.mkdir(parents=True, exist_ok=True)
    _obj_path().write_text(json.dumps(d, indent=2))


def _save_con(d: dict) -> None:
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    _con_path().parent.mkdir(parents=True, exist_ok=True)
    _con_path().write_text(json.dumps(d, indent=2))


# --------------------------------------------------------------------------- #
# Request models
# --------------------------------------------------------------------------- #


class ObjectiveRequest(BaseModel):
    weights: dict[str, float] = Field(
        description="keys: minimise_sla_breach, minimise_reviewer_cost — must sum to 1.0",
    )
    justification: str = Field(min_length=10)


class ConstraintsRequest(BaseModel):
    hard: list[dict] = Field(default_factory=list)
    soft: list[dict] = Field(default_factory=list)


class SolveRequest(BaseModel):
    backlog: dict[str, int] | None = Field(
        default=None,
        description="optional override of expected per-tier backlog (posts/day)",
    )
    seed: int = Field(default=20260430)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@router.get("/state")
def state() -> dict:
    """Current queue depth, reviewer headcount, SLA targets per tier."""
    ctx = get_context()
    total_headcount = sum(p["headcount"] for p in REVIEWER_POOLS)
    total_minutes_available = total_headcount * WORKING_MINUTES_PER_REVIEWER
    return {
        "tiers": [
            {
                "id": t["id"],
                "expected_backlog": DEFAULT_BACKLOG[t["id"]],
                "minutes_per_post": t["minutes_per_post"],
                "sla_seconds": t["sla_seconds"],
                "imda_critical": t["imda_critical"],
            }
            for t in TIERS
        ],
        "reviewer_pools": [
            {
                "id": p["id"],
                "headcount": p["headcount"],
                "cost_per_min": p["cost_per_min"],
                "qualified_tiers": p["qualified_tiers"],
            }
            for p in REVIEWER_POOLS
        ],
        "total_headcount": total_headcount,
        "total_minutes_available": total_minutes_available,
        "working_minutes_per_reviewer": WORKING_MINUTES_PER_REVIEWER,
        "n_posts_in_corpus": len(ctx.posts),
        "note": (
            "Backlog values are the expected per-day inflow per tier. "
            "Post-IMDA-injection, the imda_priority tier's SLA is structurally "
            "hard at 60s; the LP must allocate enough senior-reviewer minutes "
            "to clear backlog × minutes_per_post within the SLA."
        ),
    }


@router.get("/tiers")
def get_tiers() -> dict:
    return {"tiers": TIERS, "reviewer_pools": REVIEWER_POOLS}


@router.get("/objective")
def get_objective() -> dict:
    return _load_obj()


@router.post("/objective")
def set_objective(req: ObjectiveRequest) -> dict:
    keys = {"minimise_sla_breach", "minimise_reviewer_cost"}
    if set(req.weights.keys()) != keys:
        raise HTTPException(422, f"weights must have exactly these keys: {sorted(keys)}")
    total = sum(req.weights.values())
    if abs(total - 1.0) > 1e-3:
        raise HTTPException(422, f"weights must sum to 1.0 (got {total})")
    state = {"weights": req.weights, "justification": req.justification}
    _save_obj(state)
    return _load_obj()


@router.get("/constraints")
def get_constraints() -> dict:
    return _load_con()


@router.post("/constraints")
def set_constraints(req: ConstraintsRequest) -> dict:
    _save_con(req.model_dump())
    return _load_con()


@router.post("/solve")
def solve(req: SolveRequest) -> dict:
    """Run the LP allocator across (tier × reviewer-pool) cells.

    Variables  : x[t,r] = reviewer-minutes allocated to (tier t, pool r)
    Objective  : minimise α·sla_breach_penalty + β·reviewer_cost
    Hard       :
      - x[t,r] >= 0
      - x[t,r] = 0  if pool r is not qualified for tier t
      - sum_t x[t,r] <= pool_r.headcount × WORKING_MINUTES_PER_REVIEWER
      - if IMDA active: sum_r x[imda_priority, r]
                          >= backlog[imda_priority] × minutes_per_post[imda_priority]
        AND only senior pool counts (the qualified pool for imda_priority)
    Soft       : exceeding pool cap is penalised in the objective via the
                 reviewer_cost term — pools at cap are simply unavailable.

    Pathology checks: tier starvation, pool over-utilisation, infeasible.
    """
    obj = _load_obj()
    con = _load_con()
    backlog = dict(DEFAULT_BACKLOG)
    if req.backlog:
        backlog.update(req.backlog)

    T = len(TIERS)
    R = len(REVIEWER_POOLS)

    minutes_required = np.array(
        [backlog[t["id"]] * t["minutes_per_post"] for t in TIERS], dtype=float
    )
    cost_per_min = np.array([p["cost_per_min"] for p in REVIEWER_POOLS], dtype=float)
    headcount = np.array([p["headcount"] for p in REVIEWER_POOLS], dtype=float)
    pool_capacity_min = headcount * WORKING_MINUTES_PER_REVIEWER

    # SLA-breach penalty per minute SHORT of required (per tier). Tighter SLA
    # tiers have proportionally higher penalty so the solver prioritises them.
    sla_penalty = np.array(
        [
            t["fn_cost"]
            * (1.0 if t["imda_critical"] else 1.0)
            / max(t["sla_seconds"], 1)
            * 60.0  # convert per-second penalty to per-minute coefficient
            for t in TIERS
        ],
        dtype=float,
    )

    alpha = obj["weights"]["minimise_sla_breach"]
    beta = obj["weights"]["minimise_reviewer_cost"]

    # We parameterise: x[t,r] in [0, pool_capacity_min[r]]; shortfall = required - allocated_per_tier.
    # Objective per (t, r): cost = β * cost_per_min[r] - α * sla_penalty[t]
    # (allocating one extra minute REDUCES SLA breach by sla_penalty[t]).
    # linprog minimises c @ x, so this is direct.
    c_vec = np.zeros(T * R)
    for ti, t in enumerate(TIERS):
        for ri, p in enumerate(REVIEWER_POOLS):
            qualified = t["id"] in p["qualified_tiers"]
            if not qualified:
                # Disqualify by making the cost prohibitive — also enforced by
                # an explicit equality below.
                c_vec[ti * R + ri] = 1e9
            else:
                c_vec[ti * R + ri] = beta * cost_per_min[ri] - alpha * sla_penalty[ti]

    # Inequality A_ub @ x <= b_ub
    A_rows: list[np.ndarray] = []
    b_rows: list[float] = []

    # Per-pool capacity: sum_t x[t,r] <= pool_capacity_min[r]
    for ri in range(R):
        row = np.zeros(T * R)
        for ti in range(T):
            row[ti * R + ri] = 1.0
        A_rows.append(row)
        b_rows.append(float(pool_capacity_min[ri]))

    # Per-tier ceiling: sum_r x[t,r] <= minutes_required[t] (don't over-allocate)
    for ti in range(T):
        row = np.zeros(T * R)
        for ri in range(R):
            row[ti * R + ri] = 1.0
        A_rows.append(row)
        b_rows.append(float(minutes_required[ti]))

    # Equality A_eq @ x = b_eq — disqualified cells must be exactly 0
    A_eq_rows: list[np.ndarray] = []
    b_eq_rows: list[float] = []
    for ti, t in enumerate(TIERS):
        for ri, p in enumerate(REVIEWER_POOLS):
            if t["id"] not in p["qualified_tiers"]:
                row = np.zeros(T * R)
                row[ti * R + ri] = 1.0
                A_eq_rows.append(row)
                b_eq_rows.append(0.0)

    # IMDA-priority hard constraint: when active, the imda_priority tier MUST be
    # 100% covered (sum_r x[imda_priority, r] >= minutes_required[imda_priority]).
    # We add a >= constraint by negating both sides for the linprog A_ub form.
    imda_active = any(
        r.get("rule") == "imda_priority_must_clear_within_sla" and r.get("enabled", False)
        for r in con.get("hard", [])
    )
    if imda_active:
        ti = next(i for i, t in enumerate(TIERS) if t["id"] == "imda_priority")
        row = np.zeros(T * R)
        for ri in range(R):
            row[ti * R + ri] = -1.0  # -sum >= -required  ⇔  sum <= required (ceiling above already)
        A_rows.append(row)
        b_rows.append(-float(minutes_required[ti]))

    A_ub = np.array(A_rows)
    b_ub = np.array(b_rows)
    A_eq = np.array(A_eq_rows) if A_eq_rows else None
    b_eq = np.array(b_eq_rows) if b_eq_rows else None
    bounds = [(0.0, None)] * (T * R)

    try:
        result = linprog(
            c_vec,
            A_ub=A_ub,
            b_ub=b_ub,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method="highs",
        )
    except Exception as exc:
        raise HTTPException(500, f"solver failed: {exc}") from exc

    if not result.success:
        return {
            "feasibility": False,
            "status": int(result.status),
            "message": result.message,
            "imda_active": imda_active,
            "hint": (
                "Infeasible — most commonly because the IMDA hard constraint demands "
                "more senior-reviewer minutes than the senior pool capacity can "
                "supply. Demote imda_priority to soft-prefer, or expand senior "
                "headcount, or accept that backlog will grow on lower tiers."
            ),
        }

    assert result.x is not None  # narrowed by `result.success` check above
    x = np.asarray(result.x).reshape(T, R)
    allocation: dict[str, dict[str, int]] = {}
    for ti, t in enumerate(TIERS):
        tier_alloc: dict[str, int] = {}
        for ri, p in enumerate(REVIEWER_POOLS):
            mins = int(round(float(x[ti, ri])))
            if mins > 0:
                tier_alloc[p["id"]] = mins
        allocation[t["id"]] = tier_alloc

    minutes_allocated_per_tier = x.sum(axis=1)
    minutes_used_per_pool = x.sum(axis=0)
    sla_breach_minutes = np.maximum(minutes_required - minutes_allocated_per_tier, 0)
    total_breach_minutes = float(sla_breach_minutes.sum())
    reviewer_cost = float((x * cost_per_min[None, :]).sum())

    pathologies: list[str] = []
    # Tier starvation: any tier > 25% short
    for ti, t in enumerate(TIERS):
        if minutes_required[ti] > 0:
            shortfall_frac = sla_breach_minutes[ti] / minutes_required[ti]
            if shortfall_frac > 0.25:
                pathologies.append(
                    f"{t['id']}: {shortfall_frac*100:.1f}% of required minutes unmet "
                    f"(SLA breach risk)"
                )
    # Pool over-utilisation: any pool > 95% of capacity
    for ri, p in enumerate(REVIEWER_POOLS):
        if pool_capacity_min[ri] > 0:
            util = minutes_used_per_pool[ri] / pool_capacity_min[ri]
            if util > 0.95:
                pathologies.append(
                    f"{p['id']}: {util*100:.1f}% pool utilisation (reviewer-burnout risk)"
                )

    # Compliance cost (IMDA): if IMDA active, the marginal cost of the senior
    # pool spent above what we'd have spent absent the mandate is the shadow
    # price of compliance.
    senior_idx = next(i for i, p in enumerate(REVIEWER_POOLS) if p["id"] == "senior")
    senior_cost = float(x[:, senior_idx].sum() * cost_per_min[senior_idx])
    compliance_cost = senior_cost if imda_active else 0.0

    plan = {
        "solved_at": datetime.now(timezone.utc).isoformat(),
        "feasibility": True,
        "imda_active": imda_active,
        "allocation_minutes": allocation,
        "minutes_required_per_tier": {
            t["id"]: int(round(float(minutes_required[ti]))) for ti, t in enumerate(TIERS)
        },
        "minutes_allocated_per_tier": {
            t["id"]: int(round(float(minutes_allocated_per_tier[ti]))) for ti, t in enumerate(TIERS)
        },
        "sla_breach_minutes_per_tier": {
            t["id"]: int(round(float(sla_breach_minutes[ti]))) for ti, t in enumerate(TIERS)
        },
        "total_sla_breach_minutes": int(round(total_breach_minutes)),
        "reviewer_cost_total": round(reviewer_cost, 2),
        "compliance_cost_imda": round(compliance_cost, 2),
        "pathologies": pathologies,
        "objective_weights": obj["weights"],
        "interpretation": (
            "Feasible plan. Phase 12: ACCEPT, RE-TUNE (objective weights), "
            "FALL BACK (demote imda_priority hard constraint), or REDESIGN "
            "(expand senior headcount / shift SLA). The compliance_cost_imda "
            "is the shadow price of the IMDA mandate — quantify in "
            "phase_12_postimda.md."
        ),
    }
    _plan_path().parent.mkdir(parents=True, exist_ok=True)
    _plan_path().write_text(json.dumps(plan, indent=2))
    return plan


@router.get("/last_plan")
def last_plan() -> dict:
    p = _plan_path()
    if not p.exists():
        return {"plan_exists": False, "note": "no plan solved yet — run /queue/solve"}
    return json.loads(p.read_text())
