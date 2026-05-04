# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""GET /state/current — viewer aggregator.

Reads the workspace journal/ directory + scenarios/ directory + retrain_rules.json
and returns a single blob the viewer polls every 5 s. Sprints light up green
as students journal phases; ★ decision moments resolve from journal evidence.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from ..config import load_settings
from ..ml_context import get_context

router = APIRouter(prefix="/state")
log = logging.getLogger("metis.manufacturing.state")


SPRINT_PHASE_GROUPS: dict[str, list[str]] = {
    "sprint_1_vision": [
        "phase_1",
        "phase_2",
        "phase_3",
        "phase_4_vision",
        "phase_5_vision",
        "phase_6_vision",
        "phase_7_vision",
        "phase_8_vision",
    ],
    "sprint_2_predmaint": [
        "phase_4_predmaint",
        "phase_5_predmaint",
        "phase_6_predmaint",
        "phase_7_predmaint",
        "phase_8_predmaint",
    ],
    "sprint_3_rl": [
        "phase_5_rl",
        "phase_7_rl",
        "phase_10_objective",
        "phase_11_constraints",
        "phase_12_acceptance",
        "phase_11_postwsh",
        "phase_12_postwsh",
    ],
    "sprint_4_agent": ["phase_13_drift", "phase_99_close"],
}

DECISION_MOMENTS: list[dict[str, str]] = [
    {"id": "vision_arch", "name": "Vision QC base architecture", "evidence": "phase_5_vision"},
    {
        "id": "vision_threshold",
        "name": "Per-class auto-pass thresholds (incl. WSH floor)",
        "evidence": "phase_6_vision",
    },
    {
        "id": "predmaint_window",
        "name": "Predictive-maintenance prediction window",
        "evidence": "phase_5_predmaint",
    },
    {"id": "rl_reward", "name": "RL reward function weights", "evidence": "phase_7_rl"},
    {
        "id": "agent_autonomy",
        "name": "Agent autonomy ladder + WSH safety floor",
        "evidence": "phase_12_acceptance",
    },
]

JOURNAL_MIN_BYTES = 500


def _detect_completed_phases(journal_dir: Path) -> set[str]:
    """A phase is considered complete if `phase_<id>.md` exists and is > 500 bytes."""
    if not journal_dir.exists():
        return set()
    completed: set[str] = set()
    for f in journal_dir.glob("phase_*.md"):
        try:
            if f.stat().st_size >= JOURNAL_MIN_BYTES:
                stem = f.stem  # phase_5_vision
                completed.add(stem)
        except OSError:
            continue
    return completed


def _detect_mom_mandate_active(scenarios_marker_dir: Path) -> bool:
    marker = scenarios_marker_dir / "mom_wsh_shadow_mandate.active"
    return marker.exists()


@router.get("/current")
def current() -> dict[str, Any]:
    settings = load_settings()
    ctx = get_context()
    journal_dir = settings.workspace_root / "journal"
    completed = _detect_completed_phases(journal_dir)

    sprints: dict[str, dict[str, Any]] = {}
    for sprint, phases in SPRINT_PHASE_GROUPS.items():
        done_count = sum(1 for p in phases if p in completed)
        sprints[sprint] = {
            "phases_total": len(phases),
            "phases_done": done_count,
            "complete": done_count == len(phases),
            "phases_done_list": sorted([p for p in phases if p in completed]),
        }

    # Resolve decision moments from journal evidence presence.
    decisions = []
    for d in DECISION_MOMENTS:
        decisions.append(
            {
                "id": d["id"],
                "name": d["name"],
                "evidence_phase": d["evidence"],
                "resolved": d["evidence"] in completed,
            }
        )

    # MOM mandate marker (workspace-side flag set by scenario_inject.py)
    mom_active = _detect_mom_mandate_active(settings.workspace_root)
    # Side-effect: keep the agent_policy in sync so /agent/decide honours it.
    ctx.agent_policy.mom_mandate_active = mom_active

    # Retrain rules registered count (for Phase 13 readout)
    retrain_rules_path = settings.workspace_root / "retrain_rules.json"
    retrain_rules: dict[str, Any] = {}
    if retrain_rules_path.exists():
        try:
            retrain_rules = json.loads(retrain_rules_path.read_text())
        except Exception:
            retrain_rules = {}

    return {
        "sprints": sprints,
        "decisions": decisions,
        "mom_mandate_active": mom_active,
        "retrain_rules_registered": list(retrain_rules.keys()),
        "vision_chosen_arch": ctx.vision_baseline.chosen_arch,
        "vision_macro_f1": ctx.vision_baseline.macro_f1,
        "predmaint_chosen_family": ctx.predmaint_baseline.chosen_family,
        "predmaint_chosen_window_days": ctx.predmaint_baseline.chosen_window,
        "rl_chosen_policy": ctx.rl_baseline.chosen_policy,
        "agent_autonomy": ctx.agent_policy.autonomy,
    }
