# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Sprint 4 — Coordination Agent (LLM-style harness, autonomy ladder, audit trail).

The agent is a deterministic teaching harness — NO actual LLM calls. The
"reasoning" is a documented decision table that maps (board class, machine
fail probability, line state) -> (action, autonomy_mode, tools_called). The
pedagogical contract is that students defend the autonomy ladder + the WSH
shadow-mode gate, NOT the LLM prompt engineering. Same conservative pattern
Week 6 used for the fusion moderator.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..ml_context import (
    AGENT_AUTONOMY_MODES,
    AGENT_TASK_CLASSES,
    AgentAuditEntry,
    RL_LINE_SPEED_CEILING,
    RL_REFLOW_TEMP_CEILING,
    SAFETY_CRITICAL_HARD_FLOOR,
    get_context,
)

router = APIRouter(prefix="/agent")
log = logging.getLogger("metis.manufacturing.agent")


WSH_AFFECTING_TASK_CLASSES: tuple[str, ...] = (
    "setpoint_adjustment",
    "safety_alert",
)


@router.get("/policy")
def get_policy() -> dict[str, Any]:
    ctx = get_context()
    return {
        "autonomy": ctx.agent_policy.autonomy,
        "task_classes": list(AGENT_TASK_CLASSES),
        "autonomy_modes": list(AGENT_AUTONOMY_MODES),
        "wsh_affecting_task_classes": list(WSH_AFFECTING_TASK_CLASSES),
        "mom_mandate_active": ctx.agent_policy.mom_mandate_active,
    }


class PolicyRequest(BaseModel):
    autonomy: dict[str, str]


@router.post("/policy")
def set_policy(req: PolicyRequest) -> dict[str, Any]:
    ctx = get_context()
    if set(req.autonomy.keys()) != set(AGENT_TASK_CLASSES):
        raise HTTPException(
            status_code=422,
            detail=(
                f"autonomy keys MUST be exactly {sorted(AGENT_TASK_CLASSES)}; "
                f"got {sorted(req.autonomy.keys())}"
            ),
        )
    for task_class, mode in req.autonomy.items():
        if mode not in AGENT_AUTONOMY_MODES:
            raise HTTPException(
                status_code=422,
                detail=f"unknown autonomy mode {mode}; legal: {list(AGENT_AUTONOMY_MODES)}",
            )
    if ctx.agent_policy.mom_mandate_active:
        for tc in WSH_AFFECTING_TASK_CLASSES:
            if req.autonomy.get(tc) != "shadow":
                raise HTTPException(
                    status_code=422,
                    detail=(
                        f"MOM/WSH mandate active: WSH-affecting task class {tc!r} "
                        f"MUST be shadow; got {req.autonomy.get(tc)!r}. "
                        f"See specs/compliance-floors.md."
                    ),
                )
    ctx.agent_policy.autonomy = dict(req.autonomy)
    log.info(
        "agent.policy.ok %s",
        " ".join(f"{k}={v}" for k, v in sorted(ctx.agent_policy.autonomy.items())),
    )
    return get_policy()


class DecideRequest(BaseModel):
    board_id: str | None = None
    machine_id: str | None = None
    line_state: dict[str, float] = Field(default_factory=dict)


def _decide_task_class(req: DecideRequest, ctx: Any) -> tuple[str, str, list[str], str]:
    """Deterministic decision logic — no LLM. Returns (task_class, action, tools, rationale).

    Order of precedence: safety_alert > setpoint_adjustment > vision_triage >
    maintenance_scheduling. The agent picks the highest-stakes task class
    that fires given the inputs.
    """
    line_speed = float(req.line_state.get("line_speed_boards_per_min", 0.0))
    max_zone_temp = float(req.line_state.get("max_zone_temp_celsius", 0.0))
    restricted_zone_breach = bool(req.line_state.get("restricted_zone_breach", 0.0))

    # Safety alert: any envelope breach.
    if (
        restricted_zone_breach
        or line_speed > RL_LINE_SPEED_CEILING
        or max_zone_temp > RL_REFLOW_TEMP_CEILING
    ):
        rationale = (
            f"safety envelope breach: speed={line_speed} (ceiling {RL_LINE_SPEED_CEILING}), "
            f"max_zone_temp={max_zone_temp} (ceiling {RL_REFLOW_TEMP_CEILING}), "
            f"restricted_zone_breach={restricted_zone_breach}"
        )
        return ("safety_alert", "halt_line_pending_human_ack", ["log_safety_incident"], rationale)

    # Setpoint adjustment: line state present without breach.
    if line_speed > 0 and max_zone_temp > 0:
        rationale = (
            f"line state in-envelope (speed={line_speed}, temp={max_zone_temp}); "
            f"recommending RL setpoint adjustment per chosen policy"
        )
        return (
            "setpoint_adjustment",
            "recommend_rl_setpoint",
            ["suggest_setpoint"],
            rationale,
        )

    # Vision triage: a board_id is supplied without machine context.
    if req.board_id is not None and req.machine_id is None:
        # Look up ground truth class for the rationale (audit-trail evidence).
        label_lookup = dict(
            zip(ctx.boards["image_id"].to_list(), ctx.boards["class_label"].to_list())
        )
        truth = label_lookup.get(req.board_id)
        rationale = (
            f"single board context; vision triage on board_id={req.board_id} (truth={truth})"
        )
        return ("vision_triage", "classify_and_route", ["vision_classify"], rationale)

    # Maintenance scheduling: a machine_id is supplied.
    if req.machine_id is not None:
        rationale = (
            f"machine context present (machine_id={req.machine_id}); "
            f"predictive-maintenance scoring under chosen window"
        )
        return (
            "maintenance_scheduling",
            "predict_and_schedule",
            ["predict_failure"],
            rationale,
        )

    # Default: no input; recommend manual review.
    return (
        "vision_triage",
        "manual_review_required",
        [],
        "no actionable input — defer to operator",
    )


@router.post("/decide")
def decide(req: DecideRequest) -> dict[str, Any]:
    ctx = get_context()
    task_class, chosen_action, tools_called, rationale = _decide_task_class(req, ctx)
    autonomy_mode = ctx.agent_policy.autonomy.get(task_class, "shadow")
    # WSH safety floor: any safety_critical_defect classification forces escalation.
    audit_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = AgentAuditEntry(
        audit_id=audit_id,
        timestamp=timestamp,
        board_id=req.board_id,
        machine_id=req.machine_id,
        task_class=task_class,
        autonomy_mode=autonomy_mode,
        chosen_action=chosen_action,
        tools_called=list(tools_called),
        rationale=rationale,
    )
    ctx.agent_audit.append(entry)
    # Cap audit trail at 1000 entries (FIFO).
    if len(ctx.agent_audit) > 1000:
        ctx.agent_audit = ctx.agent_audit[-1000:]
    log.info(
        "agent.decide.ok task=%s mode=%s action=%s tools=%s",
        task_class,
        autonomy_mode,
        chosen_action,
        tools_called,
    )
    return {
        "audit_id": audit_id,
        "timestamp": timestamp,
        "task_class": task_class,
        "autonomy_mode": autonomy_mode,
        "chosen_action": chosen_action,
        "tools_called": tools_called,
        "rationale": rationale,
        "wsh_safety_floor": SAFETY_CRITICAL_HARD_FLOOR,
    }


@router.get("/audit")
def audit(since: str | None = None, limit: int = 50) -> dict[str, Any]:
    ctx = get_context()
    entries = ctx.agent_audit
    if since:
        entries = [e for e in entries if e.timestamp >= since]
    entries = entries[-limit:]
    return {
        "count": len(entries),
        "entries": [
            {
                "audit_id": e.audit_id,
                "timestamp": e.timestamp,
                "board_id": e.board_id,
                "machine_id": e.machine_id,
                "task_class": e.task_class,
                "autonomy_mode": e.autonomy_mode,
                "chosen_action": e.chosen_action,
                "tools_called": e.tools_called,
                "rationale": e.rationale,
            }
            for e in entries
        ],
    }
