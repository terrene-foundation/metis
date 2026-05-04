# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Sprint 3 — Process-optimization RL controller (3-policy leaderboard, reward function)."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..ml_context import (
    RL_HARD_FLOOR_SAFETY_PENALTY,
    RL_LINE_SPEED_CEILING,
    RL_POLICIES,
    RL_REFLOW_TEMP_CEILING,
    RewardFunction,
    get_context,
)

router = APIRouter(prefix="/optimize/rl")
log = logging.getLogger("metis.manufacturing.rl")


def _serialise_policy(entry: Any) -> dict[str, Any]:
    return {
        "policy": entry.policy,
        "why": entry.policy_why,
        "n_episodes": entry.n_episodes,
        "throughput_boards_per_min": entry.throughput_boards_per_min,
        "defect_rate": entry.defect_rate,
        "energy_kwh_per_board": entry.energy_kwh_per_board,
        "safety_violations": entry.safety_violations,
        "avg_return": entry.avg_return,
        "return_under_chosen_weights": entry.return_under_chosen_weights,
    }


def _re_score_under_weights(
    rl_episodes: dict[str, list[dict[str, float]]],
    rf: RewardFunction,
) -> dict[str, float]:
    """Re-compute per-policy mean return under given reward weights.

    return = throughput * w_thr
           - defect_rate * w_def
           - energy_per_board * w_eng
           - safety_violation * w_safety_penalty
    """
    out: dict[str, float] = {}
    for policy, eps in rl_episodes.items():
        if not eps:
            out[policy] = 0.0
            continue
        rets = []
        for e in eps:
            r = (
                rf.throughput * float(e["throughput"])
                - rf.defect_cost * float(e["defect_rate"])
                - rf.energy_cost * float(e["energy_per_board"])
                - rf.safety_penalty * float(e["safety_violation"])
            )
            rets.append(r)
        out[policy] = float(np.mean(rets))
    return out


@router.get("/leaderboard")
def leaderboard() -> dict[str, Any]:
    ctx = get_context()
    rl = ctx.rl_baseline
    re_scored = _re_score_under_weights(ctx.rl_episodes, rl.reward_function)
    rows = []
    for policy in RL_POLICIES:
        entry = rl.leaderboard.get(policy)
        if entry is None:
            continue
        entry.return_under_chosen_weights = round(re_scored.get(policy, 0.0), 3)
        rows.append(_serialise_policy(entry))
    rows.sort(key=lambda r: r["return_under_chosen_weights"] or r["avg_return"], reverse=True)
    return {
        "policies": list(RL_POLICIES),
        "chosen_policy": rl.chosen_policy,
        "stage": rl.stage,
        "reward_function": {
            "throughput": rl.reward_function.throughput,
            "defect_cost": rl.reward_function.defect_cost,
            "energy_cost": rl.reward_function.energy_cost,
            "safety_penalty": rl.reward_function.safety_penalty,
            "hard_floors": rl.reward_function.hard_floors,
        },
        "leaderboard": rows,
    }


@router.get("/reward_function")
def get_reward_function() -> dict[str, Any]:
    ctx = get_context()
    rf = ctx.rl_baseline.reward_function
    return {
        "throughput": rf.throughput,
        "defect_cost": rf.defect_cost,
        "energy_cost": rf.energy_cost,
        "safety_penalty": rf.safety_penalty,
        "hard_floors": rf.hard_floors,
        "hard_floor_safety_penalty_minimum": RL_HARD_FLOOR_SAFETY_PENALTY,
    }


class RewardFunctionRequest(BaseModel):
    throughput: float = Field(ge=0.0)
    defect_cost: float = Field(ge=0.0)
    energy_cost: float = Field(ge=0.0)
    safety_penalty: float = Field(ge=0.0)


@router.post("/reward_function")
def set_reward_function(req: RewardFunctionRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.safety_penalty < RL_HARD_FLOOR_SAFETY_PENALTY:
        raise HTTPException(
            status_code=422,
            detail=(
                f"safety_penalty {req.safety_penalty} below hard floor "
                f"{RL_HARD_FLOOR_SAFETY_PENALTY}. Cached rollouts at this weight "
                f"produce ≥1 hard-floor violation across the 10,000-episode bench. "
                f"WSH Act + $50K equipment-damage envelope are non-optimisable."
            ),
        )
    ctx.rl_baseline.reward_function = RewardFunction(
        throughput=req.throughput,
        defect_cost=req.defect_cost,
        energy_cost=req.energy_cost,
        safety_penalty=req.safety_penalty,
    )
    log.info(
        "rl.reward_function.ok throughput=%.3f defect_cost=%.3f energy_cost=%.3f safety_penalty=%.3f",
        req.throughput,
        req.defect_cost,
        req.energy_cost,
        req.safety_penalty,
    )
    return get_reward_function()


class SimulateRequest(BaseModel):
    policy: str
    n_episodes: int = Field(default=200, ge=1, le=10000)
    seed: int = 20260504


@router.post("/simulate")
def simulate(req: SimulateRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.policy not in RL_POLICIES:
        raise HTTPException(status_code=404, detail=f"unknown policy {req.policy}")
    eps = ctx.rl_episodes.get(req.policy, [])
    if not eps:
        raise HTTPException(status_code=404, detail=f"no cached episodes for {req.policy}")
    rng = np.random.default_rng(req.seed)
    sample_idx = rng.choice(len(eps), size=min(req.n_episodes, len(eps)), replace=False)
    sample = [eps[int(i)] for i in sample_idx]
    rf = ctx.rl_baseline.reward_function
    rets = [
        rf.throughput * float(e["throughput"])
        - rf.defect_cost * float(e["defect_rate"])
        - rf.energy_cost * float(e["energy_per_board"])
        - rf.safety_penalty * float(e["safety_violation"])
        for e in sample
    ]
    safety_violations = int(sum(int(e["safety_violation"]) for e in sample))
    line_speed_violations = int(
        sum(int(float(e.get("line_speed", 0.0)) > RL_LINE_SPEED_CEILING) for e in sample)
    )
    temp_violations = int(
        sum(int(float(e.get("max_zone_temp", 0.0)) > RL_REFLOW_TEMP_CEILING) for e in sample)
    )
    # Per `specs/compliance-floors.md`: line_speed and reflow_temp ceilings are HARD
    # only when the MOM/WSH mandate is active. Pre-mandate they are soft envelope
    # (workshop targets, not pass/fail). The WSH-notifiable safety_violation count
    # is HARD always.
    mom_active = ctx.agent_policy.mom_mandate_active
    if mom_active:
        hard_active = (safety_violations + line_speed_violations + temp_violations) > 0
    else:
        hard_active = safety_violations > 0
    log.info(
        "rl.simulate.ok policy=%s n=%d mean_return=%.3f safety_violations=%d "
        "line_speed_violations=%d temp_violations=%d mom_active=%s hard_floor=%s",
        req.policy,
        len(sample),
        float(np.mean(rets)),
        safety_violations,
        line_speed_violations,
        temp_violations,
        mom_active,
        hard_active,
    )
    return {
        "policy": req.policy,
        "n_episodes": len(sample),
        "mean_return": round(float(np.mean(rets)), 3),
        "mean_throughput": round(float(np.mean([e["throughput"] for e in sample])), 3),
        "mean_defect_rate": round(float(np.mean([e["defect_rate"] for e in sample])), 4),
        "mean_energy_per_board": round(float(np.mean([e["energy_per_board"] for e in sample])), 4),
        "safety_violations": safety_violations,
        "line_speed_violations": line_speed_violations,
        "reflow_temp_violations": temp_violations,
        "mom_mandate_active": mom_active,
        "hard_floor_active": hard_active,
    }


class PromoteRequest(BaseModel):
    policy: str
    to_stage: str


@router.post("/promote")
def promote(req: PromoteRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.policy not in RL_POLICIES:
        raise HTTPException(status_code=404, detail=f"unknown policy {req.policy}")
    legal_transitions = {
        "staging": {"shadow", "archived"},
        "shadow": {"production", "archived", "staging"},
        "production": {"archived", "shadow"},
        "archived": {"staging"},
    }
    current_stage = ctx.rl_baseline.stage
    if req.to_stage not in legal_transitions.get(current_stage, set()):
        raise HTTPException(
            status_code=409,
            detail=f"illegal transition {current_stage} -> {req.to_stage}",
        )
    # Defensive WSH gate: cannot promote a policy whose simulated rollouts
    # have ANY hard-floor violations.
    sim_check = simulate(SimulateRequest(policy=req.policy, n_episodes=500, seed=42))
    if sim_check["hard_floor_active"]:
        raise HTTPException(
            status_code=409,
            detail=(
                f"refused promotion: policy {req.policy} produces hard-floor "
                f"violations on the 500-episode simulate bench "
                f"(safety={sim_check['safety_violations']}, "
                f"speed={sim_check['line_speed_violations']}, "
                f"temp={sim_check['reflow_temp_violations']})"
            ),
        )
    ctx.rl_baseline.chosen_policy = req.policy
    ctx.rl_baseline.stage = req.to_stage
    log.info(
        "rl.promote.ok policy=%s from=%s to=%s",
        req.policy,
        current_stage,
        req.to_stage,
    )
    return {
        "policy": req.policy,
        "from_stage": current_stage,
        "to_stage": req.to_stage,
    }


@router.get("/registry")
def registry() -> dict[str, Any]:
    ctx = get_context()
    rl = ctx.rl_baseline
    return {
        "current": {
            "policy": rl.chosen_policy,
            "stage": rl.stage,
        },
        "candidates": {
            policy: {
                "avg_return": entry.avg_return,
                "throughput": entry.throughput_boards_per_min,
                "defect_rate": entry.defect_rate,
                "safety_violations": entry.safety_violations,
                "why": entry.policy_why,
            }
            for policy, entry in rl.leaderboard.items()
        },
    }
