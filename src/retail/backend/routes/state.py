# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Workshop state — what the viewer's progress banner reads.

The state advances explicitly: Claude Code calls POST /state/advance at the
start of each Playbook phase (the prompt templates include this as boilerplate).
Viewer polls GET /state/current and renders the value-chain banner.

State is persisted to .workshop_state.json in the workspace so restarts don't
lose progress.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import load_settings

router = APIRouter()


# ----------------------------- canonical pipeline ---------------------------
# Order matters — this is the value-chain the banner renders left-to-right.
PIPELINE = [
    {"id": "open", "label": "Open", "coc": None, "sprint": None, "clock": "2:00"},
    {"id": "analyze", "label": "Analyze", "coc": "/analyze", "sprint": None, "clock": "2:10"},
    {"id": "todos", "label": "Todos", "coc": "/todos", "sprint": None, "clock": "2:25"},
    {
        "id": "usml",
        "label": "USML · Discover",
        "coc": "/implement",
        "sprint": 1,
        "clock": "2:30→3:15",
    },
    {"id": "sml", "label": "SML · Predict", "coc": "/implement", "sprint": 2, "clock": "3:15→4:00"},
    {"id": "opt", "label": "Opt · Decide", "coc": "/implement", "sprint": 3, "clock": "4:00→4:40"},
    {
        "id": "mlops",
        "label": "MLOps · Monitor",
        "coc": "/implement",
        "sprint": 4,
        "clock": "4:40→5:00",
    },
    {"id": "redteam", "label": "Red-team", "coc": "/redteam", "sprint": None, "clock": "5:00→5:15"},
    {"id": "codify", "label": "Codify", "coc": "/codify", "sprint": None, "clock": "5:15→5:30"},
]

PIPELINE_IDS = [s["id"] for s in PIPELINE]

# Canonical phase metadata (for the mini-bar inside a sprint)
PHASE_META = {
    1: {"name": "Frame", "levers": "scope · horizon · ceiling · cost asymmetry"},
    2: {"name": "Data Audit", "levers": "outliers · missingness · contamination · sampling"},
    3: {
        "name": "Feature Framing",
        "levers": "availability · leakage · proxy check · engineered derivation",
    },
    4: {"name": "Candidates", "levers": "model family mix · sweep breadth · CV · baseline"},
    5: {
        "name": "Implications",
        "levers": "complexity/interpretability · stability/accuracy · speed",
    },
    6: {
        "name": "Metric + Threshold",
        "levers": "primary metric · threshold · class imbalance · calibration",
    },
    7: {"name": "Red-team", "levers": "subgroups · adversarial · proxy tests · acceptance"},
    8: {"name": "Deployment Gate", "levers": "monitoring cadence · rollback · alerts · promotion"},
    9: {"name": "Codify", "levers": "transferable lessons · domain-specific lessons"},
    10: {"name": "Objective", "levers": "single/multi · weights · proxies · coverage floor"},
    11: {"name": "Constraints", "levers": "hard/soft · penalties · demotion · regulatory triggers"},
    12: {
        "name": "Solver Acceptance",
        "levers": "held-out · pathology · accept/retune/redesign · rollback",
    },
    13: {"name": "Drift", "levers": "signal · threshold grounding · duration · HITL/auto"},
    14: {"name": "Fairness", "levers": "deferred to Week 7"},
}

# The 5 decision moments students must hit — universal framing
DECISION_MOMENTS = [
    {
        "id": 1,
        "label": "Primary operating point defended in unit of harm",
        "sprint": 1,
        "phase": 6,
        "retail": "K and segment count defended in $",
    },
    {
        "id": 2,
        "label": "Distinct downstream action per output class",
        "sprint": 1,
        "phase": 5,
        "retail": "One campaign per segment",
    },
    {
        "id": 3,
        "label": "Model strategy with explicit cold/low-confidence fallback",
        "sprint": 2,
        "phase": 6,
        "retail": "Churn + conversion thresholds + cold-start disposition",
    },
    {
        "id": 4,
        "label": "Hard/soft constraint classification under regulatory change",
        "sprint": 3,
        "phase": 11,
        "retail": "PDPA under-18 as hard line",
    },
    {
        "id": 5,
        "label": "Retrain rule with signal + threshold + duration",
        "sprint": 4,
        "phase": 13,
        "retail": "Drift rules per model",
    },
]


# ----------------------------- persistence ----------------------------------


def _state_path() -> Path:
    return load_settings().workspace_root / ".workshop_state.json"


def _default_state() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "stage": "open",
        "sprint": None,
        "phase": None,
        "phase_name": None,
        "started_at": now,
        "stage_started_at": now,
        "phase_started_at": now,
        "completed_stages": [],
        "completed_phases": [],
        "completed_decisions": [],
        "notes": [],
    }


def _load() -> dict:
    p = _state_path()
    if p.exists():
        return json.loads(p.read_text())
    p.parent.mkdir(parents=True, exist_ok=True)
    state = _default_state()
    p.write_text(json.dumps(state, indent=2))
    return state


def _save(state: dict) -> None:
    _state_path().write_text(json.dumps(state, indent=2))


# ----------------------------- request models ------------------------------


class AdvanceRequest(BaseModel):
    stage: str | None = Field(
        default=None,
        description="pipeline stage id (open | analyze | todos | usml | sml | opt | mlops | redteam | codify)",
    )
    sprint: int | None = Field(default=None, ge=1, le=4)
    phase: int | None = Field(default=None, ge=1, le=14)
    note: str | None = None


class DecisionRequest(BaseModel):
    decision_id: int = Field(ge=1, le=5)
    resolution: str
    evidence: str | None = None


# ----------------------------- endpoints ------------------------------------


@router.get("/current")
def get_current() -> dict:
    s = _load()
    now = datetime.now(timezone.utc)
    started = datetime.fromisoformat(s["started_at"])
    phase_started = datetime.fromisoformat(s.get("phase_started_at") or s["started_at"])

    current_stage = next((p for p in PIPELINE if p["id"] == s["stage"]), PIPELINE[0])
    phase_meta = PHASE_META.get(s.get("phase")) if s.get("phase") else None

    return {
        "pipeline": PIPELINE,
        "current": {
            "stage": s["stage"],
            "stage_label": current_stage["label"],
            "sprint": s.get("sprint"),
            "phase": s.get("phase"),
            "phase_name": phase_meta["name"] if phase_meta else s.get("phase_name"),
            "phase_levers": phase_meta["levers"] if phase_meta else None,
            "clock": current_stage.get("clock"),
        },
        "elapsed": {
            "workshop_seconds": int((now - started).total_seconds()),
            "phase_seconds": int((now - phase_started).total_seconds()),
        },
        "completed_stages": s.get("completed_stages", []),
        "completed_phases": s.get("completed_phases", []),
        "decision_moments": [
            {
                **dm,
                "completed": dm["id"] in s.get("completed_decisions", []),
            }
            for dm in DECISION_MOMENTS
        ],
        "notes": s.get("notes", [])[-5:],
    }


@router.post("/advance")
def advance(req: AdvanceRequest) -> dict:
    s = _load()
    now = datetime.now(timezone.utc).isoformat()

    if req.stage is not None:
        if req.stage not in PIPELINE_IDS:
            raise HTTPException(422, f"unknown stage {req.stage!r}; must be one of {PIPELINE_IDS}")
        # Mark previous stage complete
        prev = s.get("stage")
        if prev and prev != req.stage and prev not in s.get("completed_stages", []):
            s.setdefault("completed_stages", []).append(prev)
        s["stage"] = req.stage
        s["stage_started_at"] = now
    if req.sprint is not None:
        s["sprint"] = req.sprint
    if req.phase is not None:
        prev_phase = s.get("phase")
        if (
            prev_phase
            and prev_phase != req.phase
            and prev_phase not in s.get("completed_phases", [])
        ):
            s.setdefault("completed_phases", []).append(prev_phase)
        s["phase"] = req.phase
        s["phase_name"] = PHASE_META.get(req.phase, {}).get("name")
        s["phase_started_at"] = now
    if req.note:
        s.setdefault("notes", []).append({"ts": now, "note": req.note})
    _save(s)
    return s


@router.post("/decision/resolved")
def resolve_decision(req: DecisionRequest) -> dict:
    s = _load()
    completed = s.setdefault("completed_decisions", [])
    if req.decision_id not in completed:
        completed.append(req.decision_id)
    s.setdefault("notes", []).append(
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "note": f"decision_{req.decision_id}: {req.resolution}",
            "evidence": req.evidence,
        }
    )
    _save(s)
    return {"decision_id": req.decision_id, "resolved": True, "count": len(completed)}


@router.post("/reset")
def reset() -> dict:
    _save(_default_state())
    return {"reset": True}
