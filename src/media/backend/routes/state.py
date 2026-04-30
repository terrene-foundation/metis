# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Workshop state — what the viewer's progress banner reads.

State advances explicitly via POST /state/advance (Claude Code calls this
at the start of each Playbook phase). The viewer polls GET /state/current
and renders the value-chain banner. Auto-detection of completed phases
also runs on every read by scanning `journal/phase_*.md` for files
authored beyond the skeleton template — so the banner lights up even if
the student forgets to advance explicitly.

State is persisted to `.workshop_state.json` in the workspace so backend
restarts don't lose progress.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import load_settings

router = APIRouter()


# ----------------------------- canonical pipeline ---------------------------
# Order matters — the value-chain banner renders left-to-right.
PIPELINE: list[dict[str, Any]] = [
    {"id": "open", "label": "Open", "coc": None, "sprint": None, "clock": "2:00"},
    {"id": "analyze", "label": "Analyze", "coc": "/analyze", "sprint": None, "clock": "2:10"},
    {"id": "todos", "label": "Todos", "coc": "/todos", "sprint": None, "clock": "2:25"},
    {
        "id": "vision",
        "label": "Sprint 1 · Vision · See",
        "coc": "/implement",
        "sprint": 1,
        "clock": "2:30→3:15",
    },
    {
        "id": "text",
        "label": "Sprint 2 · Text · Read",
        "coc": "/implement",
        "sprint": 2,
        "clock": "3:15→4:00",
    },
    {
        "id": "fusion",
        "label": "Sprint 3 · Fusion · Decide",
        "coc": "/implement",
        "sprint": 3,
        "clock": "4:00→4:40",
    },
    {
        "id": "mlops",
        "label": "Sprint 4 · MLOps · Monitor",
        "coc": "/implement",
        "sprint": 4,
        "clock": "4:40→5:00",
    },
    {"id": "redteam", "label": "Red-team", "coc": "/redteam", "sprint": None, "clock": "5:00→5:15"},
    {"id": "codify", "label": "Codify", "coc": "/codify", "sprint": None, "clock": "5:15→5:30"},
]
PIPELINE_IDS = [s["id"] for s in PIPELINE]

# Phase 1-14 metadata (same Playbook as Week 5, swapped lever vocabulary)
PHASE_META = {
    1: {"name": "Frame", "levers": "scope · horizon · IMDA ceiling · cost asymmetry $320/$15"},
    2: {"name": "Data Audit", "levers": "label noise · proxy class leakage · class imbalance"},
    3: {"name": "Feature Framing", "levers": "modality coverage · joint-feature derivation"},
    4: {
        "name": "Candidates",
        "levers": "frozen vs partial vs full fine-tune · 3-family leaderboard",
    },
    5: {"name": "Implications", "levers": "compute cost · per-class F1 · 3× fusion penalty"},
    6: {
        "name": "Metric + Threshold",
        "levers": "per-class threshold · CSAM IMDA hard floor · cost-balanced for soft classes",
    },
    7: {
        "name": "Red-team",
        "levers": "adversarial cohort · CSAM near-miss · joint-meaning attacks",
    },
    8: {"name": "Deployment Gate", "levers": "shadow stage · per-modality monitoring · rollback"},
    9: {"name": "Codify", "levers": "transferable lessons · domain-specific lessons"},
    10: {"name": "Objective", "levers": "minimise SLA breach + reviewer cost weights"},
    11: {"name": "Constraints", "levers": "IMDA hard tier · headcount cap · regulatory triggers"},
    12: {
        "name": "Solver Acceptance",
        "levers": "feasibility · pathology · accept/retune/redesign · rollback",
    },
    13: {
        "name": "Drift × 3",
        "levers": "image weekly · text daily · fusion per-incident · seasonal exclusions",
    },
    14: {"name": "Fairness", "levers": "deferred to Week 7"},
}

# 5 Trust-Plane decision moments for Week 6 (per PRODUCT_BRIEF §5)
DECISION_MOMENTS: list[dict[str, Any]] = [
    {
        "id": 1,
        "label": "Define what counts as harmful (auto-remove vs review vs creator-warn)",
        "sprint": 1,
        "phase": 1,
        "media": "5 image classes + 5 text classes mapped to 3 reviewer dispositions",
    },
    {
        "id": 2,
        "label": "Set per-class auto-remove threshold defended in $",
        "sprint": 1,
        "phase": 6,
        "media": "$320 FN / $15 FP cost-balanced for soft classes; CSAM hard floor 0.40",
    },
    {
        "id": 3,
        "label": "Choose fusion architecture (early/late/joint)",
        "sprint": 3,
        "phase": 5,
        "media": "Coverage gain vs 3× compute cost",
    },
    {
        "id": 4,
        "label": "Re-classify CSAM-adjacent threshold as hard when IMDA fires",
        "sprint": 3,
        "phase": 11,
        "media": "Phase 11 + Phase 12 BOTH re-run; quantify compliance cost",
    },
    {
        "id": 5,
        "label": "Set retrain rules × 3 (image weekly / text daily / fusion per-incident)",
        "sprint": 4,
        "phase": 13,
        "media": "Three rules, three cadences, three signals — universal rule BLOCKED",
    },
]

# Phase → sprint mapping (for auto-detection from journal entries)
PHASE_TO_SPRINT = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,  # Sprint 1 base
    10: 3,
    11: 3,
    12: 3,  # Optimisation in Sprint 3
    13: 4,  # MLOps in Sprint 4
    14: 4,  # Fairness deferred → Sprint 4 slot
}


# ----------------------------- persistence ----------------------------------


def _state_path() -> Path:
    return load_settings().workspace_root / ".workshop_state.json"


def _journal_dir() -> Path:
    return load_settings().workspace_root / "journal"


def _default_state() -> dict[str, Any]:
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


def _load() -> dict[str, Any]:
    p = _state_path()
    if p.exists():
        return json.loads(p.read_text())
    p.parent.mkdir(parents=True, exist_ok=True)
    state = _default_state()
    p.write_text(json.dumps(state, indent=2))
    return state


def _save(state: dict) -> None:
    _state_path().parent.mkdir(parents=True, exist_ok=True)
    _state_path().write_text(json.dumps(state, indent=2))


# ----------------------------- auto-detection -------------------------------

# Phase entries are filename-keyed: phase_1_frame.md, phase_11_postimda.md, etc.
# Skeletons live under journal/skeletons/ — those don't count as "completed".
_PHASE_FILE_RE = re.compile(r"^phase_(\d{1,2})_[a-z0-9_]+\.md$")
_SKELETON_BYTES_THRESHOLD = 500  # files larger than this are considered "authored"


def _detect_completed_phases() -> dict[str, Any]:
    """Scan workspace journal/ for non-skeleton phase entries.

    Returns:
        {
          "completed_phases": [1, 2, 6, ...],      # phase numbers found
          "imda_postimda_present": bool,           # phase_11_postimda + phase_12_postimda
          "phase_files_seen": [...],               # filenames that were counted
        }
    """
    j = _journal_dir()
    completed: set[int] = set()
    imda_files: set[str] = set()
    seen: list[str] = []
    if not j.exists():
        return {"completed_phases": [], "imda_postimda_present": False, "phase_files_seen": []}
    for f in sorted(j.iterdir()):
        if f.is_dir():
            continue
        m = _PHASE_FILE_RE.match(f.name)
        if not m:
            continue
        try:
            size = f.stat().st_size
        except OSError:
            continue
        if size < _SKELETON_BYTES_THRESHOLD:
            # Treat tiny stubs as "not authored" — same heuristic the rubric uses.
            continue
        phase_n = int(m.group(1))
        if 1 <= phase_n <= 14:
            completed.add(phase_n)
            seen.append(f.name)
        if f.name == "phase_11_postimda.md" or f.name == "phase_12_postimda.md":
            imda_files.add(f.name)
    return {
        "completed_phases": sorted(completed),
        "imda_postimda_present": (
            "phase_11_postimda.md" in imda_files and "phase_12_postimda.md" in imda_files
        ),
        "phase_files_seen": seen,
    }


def _sprint_progress(completed_phases: list[int]) -> dict[int, str]:
    """Per-sprint status: not_started | in_progress | done.

    Sprint 1 (vision)  needs phases 1-9 with at least 5 complete to be done.
    Sprint 2 (text)    is a thin layer — implicitly done when text-related
                       phases (1-9 again, on text moderator) are journaled.
    Sprint 3 (fusion)  needs phases 10-12 + a revisit of 5/6/11.
    Sprint 4 (mlops)   needs phase 13.

    For pedagogical simplicity (the manifest doesn't separate per-modality
    journals), we report:
        Sprint 1 done when ≥ 5 of phases 1..9 present
        Sprint 2 done when ≥ 7 of phases 1..9 present (a denser pass over the loop)
        Sprint 3 done when phases 10, 11, 12 ALL present
        Sprint 4 done when phase 13 present
    """
    s = set(completed_phases)
    s1_count = len(s & set(range(1, 10)))
    sprint1 = "done" if s1_count >= 5 else ("in_progress" if s1_count > 0 else "not_started")
    sprint2 = "done" if s1_count >= 7 else ("in_progress" if s1_count >= 3 else "not_started")
    s3_required = {10, 11, 12}
    s3_inter = s & s3_required
    sprint3 = "done" if s3_required.issubset(s) else ("in_progress" if s3_inter else "not_started")
    sprint4 = "done" if 13 in s else "not_started"
    return {
        1: sprint1,
        2: sprint2,
        3: sprint3,
        4: sprint4,
    }


def _decision_moments_completed(state: dict[str, Any], detected: dict[str, Any]) -> list[int]:
    """Auto-resolve decision moments from journal evidence + queue/drift state.

    1. Phase 1 journaled → decision 1 done
    2. Phase 6 journaled → decision 2 done
    3. Phase 5 journaled → decision 3 done
    4. phase_11_postimda + phase_12_postimda BOTH present → decision 4 done
    5. Phase 13 journaled AND `drift_retrain_rules.json` has 3 set rules → decision 5 done

    Explicit /state/decision/resolved POSTs OR the journal evidence — either
    one resolves the moment. Union semantics.
    """
    explicit = set(state.get("completed_decisions", []))
    completed = set(detected["completed_phases"])
    auto: set[int] = set()
    if 1 in completed:
        auto.add(1)
    if 6 in completed:
        auto.add(2)
    if 5 in completed:
        auto.add(3)
    if detected["imda_postimda_present"]:
        auto.add(4)
    # Decision 5: phase 13 journaled AND retrain rules complete
    if 13 in completed:
        rules_path = load_settings().workspace_root / "drift_retrain_rules.json"
        if rules_path.exists():
            try:
                rules = json.loads(rules_path.read_text())
                set_count = sum(1 for r in rules.values() if r.get("updated_at"))
                if set_count >= 3:
                    auto.add(5)
            except (json.JSONDecodeError, OSError):
                pass
    return sorted(explicit | auto)


# ----------------------------- request models ------------------------------


class AdvanceRequest(BaseModel):
    stage: str | None = Field(
        default=None,
        description=f"pipeline stage id; one of: {', '.join(PIPELINE_IDS)}",
    )
    sprint: int | None = Field(default=None, ge=1, le=4)
    phase: int | None = Field(default=None, ge=1, le=14)
    note: str | None = None


class DecisionRequest(BaseModel):
    decision_id: int = Field(ge=1, le=5)
    resolution: str = Field(min_length=10)
    evidence: str | None = None


# ----------------------------- endpoints ------------------------------------


@router.get("/current")
def get_current() -> dict:
    s = _load()
    detected = _detect_completed_phases()
    decisions_completed = _decision_moments_completed(s, detected)
    sprint_progress = _sprint_progress(detected["completed_phases"])

    now = datetime.now(timezone.utc)
    started = datetime.fromisoformat(s["started_at"])
    phase_started = datetime.fromisoformat(s.get("phase_started_at") or s["started_at"])

    current_stage = next((p for p in PIPELINE if p["id"] == s["stage"]), PIPELINE[0])
    phase_n = s.get("phase")
    phase_meta = PHASE_META.get(int(phase_n)) if phase_n else None

    # Merge explicit completed_stages with sprint-derived ones.
    completed_stages: list[str] = list(s.get("completed_stages", []))
    for stage_id, sprint_n in (
        ("vision", 1),
        ("text", 2),
        ("fusion", 3),
        ("mlops", 4),
    ):
        if sprint_progress[sprint_n] == "done" and stage_id not in completed_stages:
            completed_stages.append(stage_id)

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
        "completed_stages": completed_stages,
        "completed_phases": sorted(
            set(s.get("completed_phases", [])) | set(detected["completed_phases"])
        ),
        "sprint_progress": sprint_progress,
        "imda_postimda_present": detected["imda_postimda_present"],
        "phase_files_seen": detected["phase_files_seen"],
        "decision_moments": [
            {**dm, "completed": dm["id"] in decisions_completed} for dm in DECISION_MOMENTS
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
