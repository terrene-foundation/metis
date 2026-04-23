#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Scenario injection — Sprint-2 and Sprint-3 mid-session events.

Scenarios:
  - pdpa_redline   (Sprint 2, Phase 11) — legal blocks under-18 browse data
  - catalog_drift  (Sprint 3, Phase 13) — new wellness category triggers drift

Usage (from repo root):

    .venv/bin/python src/retail/scripts/scenario_inject.py <scenario_id> [--undo]

The scenario prints the event + expected Trust-Plane response so the student
has the context to re-run the affected Playbook phase.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCEN_DIR = REPO_ROOT / "src" / "retail" / "data" / "scenarios"
WORKSPACE = REPO_ROOT / "workspaces" / "metis" / "week-05-retail"


def inject(scenario_id: str) -> int:
    path = SCEN_DIR / f"{scenario_id}.json"
    if not path.exists():
        print(f"✗ unknown scenario {scenario_id!r}. Available:", file=sys.stderr)
        for p in sorted(SCEN_DIR.glob("*.json")):
            print(f"    - {p.stem}", file=sys.stderr)
        return 2
    payload = json.loads(path.read_text())
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    marker = WORKSPACE / f".scenario_{scenario_id}.json"
    marker.write_text(json.dumps(payload, indent=2))

    print(f"\n  SCENARIO INJECTED: {scenario_id}")
    print(f"  Sprint {payload.get('sprint')}, Phase {payload.get('phase')}\n")
    print(f"  EVENT:\n    {payload['event']}\n")
    print(f"  EXPECTED TRUST-PLANE RESPONSE:\n    {payload['expected_trust_plane_response']}\n")
    print(f"  (marker: {marker.relative_to(REPO_ROOT)})")
    return 0


def undo(scenario_id: str) -> int:
    marker = WORKSPACE / f".scenario_{scenario_id}.json"
    if marker.exists():
        marker.unlink()
        print(f"✓ scenario {scenario_id!r} undone.")
        return 0
    print(f"(scenario {scenario_id!r} was not active)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("scenario_id", help="pdpa_redline | catalog_drift")
    p.add_argument("--undo", action="store_true", help="remove the scenario marker")
    args = p.parse_args()
    return undo(args.scenario_id) if args.undo else inject(args.scenario_id)


if __name__ == "__main__":
    sys.exit(main())
