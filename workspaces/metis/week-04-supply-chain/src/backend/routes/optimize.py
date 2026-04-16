# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace the handler body (the 501 stub
# below) with the real implementation described in SCAFFOLD_MANIFEST.md and
# PLAYBOOK.md Phases 10-12. The route registration is PRE-BUILT and stays put.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoint:
#   POST /optimize/solve — OR-Tools VRP solver call. Accept a request body with
#                          `objective_terms` (list of {kind, weight}), hard
#                          constraints (capacity, driver_hours_max), and soft
#                          constraints (time_windows, overtime_penalty). Return
#                          {plan_id, routes: [...], objective_value,
#                           optimality_gap, solver_status, feasible: bool,
#                           scenario_tag}. When scenario_tag ∈ {"preunion",
#                           "postunion"}, write data/route_plan_<tag>.json.
#
# Required call sites (for orphan-detection):
#   - ortools.constraint_solver.pywrapcp (real solver; no mocks per testing.md Tier 2)
#   - ml_context.resolve_experiment_run_id (if forecast ID is supplied)
#   - ExperimentTracker.log_run (tag phase=optimize)
"""Optimize routes (501 stubs — student-commissioned).

Registration lives from commit 1 so orphan-detection Rule 1 is satisfied
the moment the scaffold lands. Students replace the handler body, not
the registration.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()
log = logging.getLogger("metis.routes.optimize")

_TODO_STUDENT_BANNER = (
    "TODO-STUDENT: POST /optimize/solve is a scaffold placeholder. Replace "
    "the handler body by prompting Claude Code with the Phase 10-12 prompt "
    "template from specs/playbook-phases-prescribe.md: 'Using OR-Tools VRP "
    "(ortools.constraint_solver.pywrapcp), solve tomorrow's route plan over "
    "the forecast output. Objective: minimize "
    "(fuel_cost × distance) + ($220 × late_deliveries) + ($45 × "
    "overtime_hours). Hard constraints: vehicle capacity 40 pallets, driver "
    "hours <= 9/day. Soft constraints: prefer deliveries before 5pm "
    "(penalty $15/hour late). Time budget 30 seconds. Log the plan + "
    "solver gap to data/route_plan.json and the OR-Tools run to "
    "ExperimentTracker (tag phase=optimize). When scenario_tag='postunion' "
    "(MOM Employment Act hard cap), re-classify overtime from soft to hard "
    "and write to data/route_plan_postunion.json.' "
    "See scaffold-contract.md §3 for the full call-site list."
)


def _stub_payload(endpoint: str) -> dict[str, Any]:
    """Shape the 501 body so graders parse the TODO marker."""
    return {
        "error": "not implemented — prompt Claude Code to commission this endpoint",
        "endpoint": endpoint,
        "hint": "see PLAYBOOK.md Phases 10-12 for /optimize/solve",
        "todo_student": _TODO_STUDENT_BANNER,
    }


def _bind_log(request: Request) -> tuple[logging.Logger, str]:
    """Return a logger bound with a correlation ID for this request."""
    request_id = request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:12]}"
    return log, request_id


@router.post("/solve")
async def optimize_solve(request: Request) -> dict[str, Any]:
    logger, request_id = _bind_log(request)
    t0 = time.monotonic()
    logger.info(
        "optimize_solve.start",
        extra={"request_id": request_id, "route": "/optimize/solve"},
    )
    body = _stub_payload("POST /optimize/solve")
    logger.warning(
        "optimize_solve.stub",
        extra={
            "request_id": request_id,
            "latency_ms": (time.monotonic() - t0) * 1000.0,
            "status": 501,
        },
    )
    raise HTTPException(status_code=501, detail=body)
