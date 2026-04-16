# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace the handler body (the 501 stub
# below) with the real implementation described in SCAFFOLD_MANIFEST.md and
# PLAYBOOK.md Phase 13. The route registration is PRE-BUILT and stays put.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoint:
#   POST /drift/check — DriftMonitor.check_drift call. Accept a request body
#                       with {model_name: str, window_days: int}. Before first
#                       check, call DriftMonitor.set_reference_data(model_name,
#                       reference_df) exactly once (initialized at startup).
#                       Return {overall_severity, features: [...],
#                               recommendations: [...], checked_at}.
#                       overall_severity ∈ {"none","moderate","severe"} — the
#                       library NEVER emits "low" (canonical-values.md §1).
#
# Required call sites (for orphan-detection):
#   - DriftMonitor.set_reference_data (startup, once per model)
#   - DriftMonitor.check_drift (per request)
"""Drift routes (501 stubs — student-commissioned).

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
log = logging.getLogger("metis.routes.drift")

_TODO_STUDENT_BANNER = (
    "TODO-STUDENT: POST /drift/check is a scaffold placeholder. Replace "
    "the handler body by prompting Claude Code with the Phase 13 prompt "
    "template from specs/playbook-phases-mlops.md: 'For the Northwind "
    "forecast model, first call "
    "DriftMonitor.set_reference_data(model_id, reference_df) on the training "
    "window (once at startup), then run check_drift against the last 30 "
    "days. From the severity + per-feature scores + recommendations, "
    "propose the signals and thresholds the operator should monitor: "
    "7-day rolling MAPE, customer_mix PSI (from DriftMonitor), and "
    "actual-vs-predicted bias. Show the historical variance of each signal "
    "so thresholds are grounded in data, not guesses. Recommend whether "
    "the retrain decision should be made by a human reviewer or by a "
    "policy the operator pre-approves. Severity enum is 3 values — "
    'NEVER emit "low".\' '
    "See scaffold-contract.md §4 for the full call-site list."
)


def _stub_payload(endpoint: str) -> dict[str, Any]:
    """Shape the 501 body so graders parse the TODO marker."""
    return {
        "error": "not implemented — prompt Claude Code to commission this endpoint",
        "endpoint": endpoint,
        "hint": "see PLAYBOOK.md Phase 13 for /drift/check",
        "todo_student": _TODO_STUDENT_BANNER,
    }


def _bind_log(request: Request) -> tuple[logging.Logger, str]:
    """Return a logger bound with a correlation ID for this request."""
    request_id = request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:12]}"
    return log, request_id


@router.post("/check")
async def drift_check(request: Request) -> dict[str, Any]:
    logger, request_id = _bind_log(request)
    t0 = time.monotonic()
    logger.info(
        "drift_check.start",
        extra={"request_id": request_id, "route": "/drift/check"},
    )
    body = _stub_payload("POST /drift/check")
    logger.warning(
        "drift_check.stub",
        extra={
            "request_id": request_id,
            "latency_ms": (time.monotonic() - t0) * 1000.0,
            "status": 501,
        },
    )
    raise HTTPException(status_code=501, detail=body)
