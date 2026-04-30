#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Scenario injection — Sprint-3 and Sprint-4 mid-session events.

Scenarios:
  - imda_csam_mandate    (Sprint 3, Phase 11+12) — IMDA mandate forces CSAM-adjacent
                          threshold to hard, queue allocator re-solves with hard tier.
  - election_cycle_drift (Sprint 4, Phase 13)  — adversarial drift on the text
                          moderator.

Usage (from repo root):

    .venv/bin/python src/media/scripts/scenario_inject.py <scenario_id> [--undo]

The injection writes a marker file under the active workspace AND, for the
IMDA scenario, ALSO toggles the queue allocator's hard constraint by writing
queue_constraints.json in the workspace. The backend reads this file at
each /queue/solve, so the next solve naturally re-runs with the new
constraint shape (Phase 12 re-run trigger).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCEN_DIR = REPO_ROOT / "src" / "media" / "data" / "scenarios"
WORKSPACE = REPO_ROOT / "workspaces" / "metis" / "week-06-media"


def _activate_imda_queue_constraint() -> Path:
    """Flip queue_constraints.json::hard.imda_priority_must_clear_within_sla=True."""
    from typing import Any

    cpath = WORKSPACE / "queue_constraints.json"
    state: dict[str, Any]
    if cpath.exists():
        state = json.loads(cpath.read_text())
    else:
        state = {"hard": [], "soft": []}
    hard = state.get("hard", [])
    found = False
    for rule in hard:
        if rule.get("rule") == "imda_priority_must_clear_within_sla":
            rule["enabled"] = True
            found = True
            break
    if not found:
        hard.append(
            {
                "rule": "imda_priority_must_clear_within_sla",
                "enabled": True,
                "reason": "IMDA mandate clarification (scenario_inject)",
            }
        )
    state["hard"] = hard
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    cpath.parent.mkdir(parents=True, exist_ok=True)
    cpath.write_text(json.dumps(state, indent=2))
    return cpath


def _deactivate_imda_queue_constraint() -> None:
    cpath = WORKSPACE / "queue_constraints.json"
    if not cpath.exists():
        return
    state = json.loads(cpath.read_text())
    for rule in state.get("hard", []):
        if rule.get("rule") == "imda_priority_must_clear_within_sla":
            rule["enabled"] = False
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    cpath.write_text(json.dumps(state, indent=2))


def inject(scenario_id: str) -> int:
    path = SCEN_DIR / f"{scenario_id}.json"
    if not path.exists():
        print(f" unknown scenario {scenario_id!r}. Available:", file=sys.stderr)
        for p in sorted(SCEN_DIR.glob("*.json")):
            print(f"    - {p.stem}", file=sys.stderr)
        return 2
    payload = json.loads(path.read_text())
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    marker = WORKSPACE / f".scenario_{scenario_id}.json"
    marker.write_text(json.dumps(payload, indent=2))

    side_effects: list[str] = []
    if scenario_id == "imda_csam_mandate":
        cpath = _activate_imda_queue_constraint()
        side_effects.append(
            f"flipped imda_priority_must_clear_within_sla to True in {cpath.relative_to(REPO_ROOT)}"
        )

    print(f"\n  SCENARIO INJECTED: {scenario_id}")
    print(f"  Sprint {payload.get('sprint')}, Phase {payload.get('phase')}\n")
    print(f"  EVENT:\n    {payload['event']}\n")
    print(f"  EXPECTED TRUST-PLANE RESPONSE:\n    {payload['expected_trust_plane_response']}\n")
    if side_effects:
        print("  SIDE EFFECTS:")
        for s in side_effects:
            print(f"    - {s}")
        print()
    print(f"  (marker: {marker.relative_to(REPO_ROOT)})")
    return 0


def undo(scenario_id: str) -> int:
    marker = WORKSPACE / f".scenario_{scenario_id}.json"
    if scenario_id == "imda_csam_mandate":
        _deactivate_imda_queue_constraint()
    if marker.exists():
        marker.unlink()
        print(f" scenario {scenario_id!r} undone.")
        return 0
    print(f"(scenario {scenario_id!r} was not active)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("scenario_id", help="imda_csam_mandate | election_cycle_drift")
    p.add_argument("--undo", action="store_true", help="remove the scenario marker")
    args = p.parse_args()
    return undo(args.scenario_id) if args.undo else inject(args.scenario_id)


if __name__ == "__main__":
    sys.exit(main())
