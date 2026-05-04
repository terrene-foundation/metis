# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""GET /health — liveness + load-bearing baseline summary."""

from __future__ import annotations

from fastapi import APIRouter

from ..ml_context import get_context

router = APIRouter()


@router.get("/health")
def health() -> dict:
    ctx = get_context()
    chosen_pm_window = ctx.predmaint_baseline.chosen_window
    chosen_pm_family = ctx.predmaint_baseline.chosen_family
    pm_entry = ctx.predmaint_baseline.leaderboard[chosen_pm_window][chosen_pm_family]
    return {
        "status": "ok",
        "boards": int(len(ctx.boards)),
        "sensor_rows": int(len(ctx.sensor_stream)),
        "rl_episodes": {p: len(ctx.rl_episodes.get(p, [])) for p in ctx.rl_baseline.policies},
        "vision_baseline_arch": ctx.vision_baseline.chosen_arch,
        "vision_baseline_f1": ctx.vision_baseline.macro_f1,
        "predmaint_baseline_family": chosen_pm_family,
        "predmaint_baseline_window_days": chosen_pm_window,
        "predmaint_baseline_brier": pm_entry.brier,
        "rl_baseline_policy": ctx.rl_baseline.chosen_policy,
        "drift_refs_active": ctx.drift_baselines_registered,
        "agent_mom_mandate_active": ctx.agent_policy.mom_mandate_active,
    }
