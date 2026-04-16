#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Scenario injection CLI — `metis scenario fire <event>`.

Authoritative spec: `specs/scenario-catalog.md` (5 events) and
`specs/scenario-injection.md` (CLI mechanics, exit codes).

Usage (from workspace root):

    python scripts/scenario_inject.py fire union-cap
    python scripts/scenario_inject.py fire drift-week-78
    python scripts/scenario_inject.py fire union-cap --undo
    python scripts/scenario_inject.py fire union-cap --dry-run
    python scripts/scenario_inject.py list

Exit codes (per specs/scenario-injection.md):
  0  fired successfully
  1  unknown event
  2  workspace not detected
  3  pre-condition not met
  4  already fired (pass --re-fire)
  5  rollback target missing
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Workspace resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
DATA_DIR = WORKSPACE_ROOT / "data"
SCENARIO_DIR = DATA_DIR / "scenarios"
SCENARIO_LOG = WORKSPACE_ROOT / ".scenario_log.jsonl"


def _detect_workspace() -> None:
    """Exit 2 if we're not in the Week 4 workspace."""
    markers = [WORKSPACE_ROOT / "PLAYBOOK.md", WORKSPACE_ROOT / "specs" / "_index.md"]
    if not all(m.exists() for m in markers):
        print(f"ERROR: workspace not detected at {WORKSPACE_ROOT}", file=sys.stderr)
        sys.exit(2)
    SCENARIO_DIR.mkdir(parents=True, exist_ok=True)


def _log_event(payload: dict[str, Any]) -> None:
    """Append a structured log line for audit."""
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    with SCENARIO_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload) + "\n")


# ---------------------------------------------------------------------------
# Event handlers — one per scenario
# ---------------------------------------------------------------------------


def fire_union_cap(undo: bool, dry_run: bool, re_fire: bool) -> int:
    """MOM Employment Act tightens driver OT cap to 5 hr/week."""
    marker = SCENARIO_DIR / "active_union_cap.json"
    route_plan = DATA_DIR / "route_plan.json"
    snapshot = DATA_DIR / "route_plan_preunion.json"

    if undo:
        if not marker.exists():
            print("Nothing to undo — union-cap is not active.", file=sys.stderr)
            return 5
        if not snapshot.exists():
            # Fall back — if we don't have a snapshot, student's route_plan
            # would be stuck in postunion state. Write an empty snapshot so
            # the Viewer can at least fall back to "no pre-union plan".
            snapshot.write_text(json.dumps({"stops": [], "note": "no snapshot"}, indent=2))
        marker.unlink()
        if route_plan.exists() and snapshot.exists():
            shutil.copy(snapshot, route_plan)
        _log_event({"event": "union-cap", "action": "undo"})
        print("UNDONE: union-cap marker removed; route_plan.json restored from snapshot.")
        return 0

    if marker.exists() and not re_fire:
        print("Already fired. Pass --re-fire to replay.", file=sys.stderr)
        return 4

    if not route_plan.exists():
        print(
            "Pre-condition not met: /optimize/solve has not written route_plan.json yet.",
            file=sys.stderr,
        )
        return 3

    payload = {
        "event": "union-cap",
        "constraint": "driver_overtime_hours_max",
        "new_cap": 5,
        "unit": "hours_per_week",
        "classification_hint": "hard",
        "reason": "MOM Employment Act circular tightens OT ceiling for logistics sector",
        "fired_at": datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        print(f"DRY RUN — would write {marker} and snapshot {route_plan} -> {snapshot}")
        print(json.dumps(payload, indent=2))
        return 0

    shutil.copy(route_plan, snapshot)
    marker.write_text(json.dumps(payload, indent=2) + "\n")
    _log_event({"event": "union-cap", "action": "fire", "payload": payload})
    print(f"SCENARIO FIRED: union-cap. Prior plan saved as {snapshot.name}.")
    print("Re-run POST /optimize/solve with scenario_tag='postunion' to see the new plan.")
    return 0


def fire_drift_week78(undo: bool, dry_run: bool, re_fire: bool) -> int:
    """Post-CNY demand distribution shift (week 78 onward)."""
    marker = SCENARIO_DIR / "active_drift.json"
    fixture = DATA_DIR / "week78_drift.json"

    if undo:
        if not marker.exists():
            print("Nothing to undo — drift-week-78 is not active.", file=sys.stderr)
            return 5
        marker.unlink()
        _log_event({"event": "drift-week-78", "action": "undo"})
        print("UNDONE: drift marker removed. Fixture week78_drift.json preserved.")
        return 0

    if marker.exists() and not re_fire:
        print("Already fired. Pass --re-fire to replay.", file=sys.stderr)
        return 4

    if not fixture.exists():
        print(f"Pre-condition not met: {fixture.name} missing.", file=sys.stderr)
        return 3

    payload = {
        "event": "drift-week-78",
        "scenario": "week78",
        "window_start": "2025-06-23",
        "window_days": 30,
        "cultural_anchor": "post_CNY_week_8",
        "fired_at": datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        print(f"DRY RUN — would write {marker}")
        print(json.dumps(payload, indent=2))
        return 0

    marker.write_text(json.dumps(payload, indent=2) + "\n")
    _log_event({"event": "drift-week-78", "action": "fire", "payload": payload})
    print(
        "SCENARIO FIRED: drift-week-78. Re-run POST /drift/check — severity should flip to 'moderate' or 'severe'."
    )
    return 0


def fire_lta_carbon_levy(undo: bool, dry_run: bool, re_fire: bool) -> int:
    """LTA introduces $0.18/km carbon levy on diesel fleet."""
    marker = SCENARIO_DIR / "active_lta_carbon_levy.json"

    if undo:
        if not marker.exists():
            return 5
        marker.unlink()
        _log_event({"event": "lta-carbon-levy", "action": "undo"})
        print("UNDONE: LTA carbon levy marker removed.")
        return 0

    if marker.exists() and not re_fire:
        print("Already fired. Pass --re-fire to replay.", file=sys.stderr)
        return 4

    payload = {
        "event": "lta-carbon-levy",
        "levy_per_km_sgd": 0.18,
        "fleet_scope": "diesel",
        "reason": "LTA Budget 2026 carbon pricing — takes effect mid-month",
        "fired_at": datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    marker.write_text(json.dumps(payload, indent=2) + "\n")
    _log_event({"event": "lta-carbon-levy", "action": "fire", "payload": payload})
    print("SCENARIO FIRED: lta-carbon-levy. Objective should gain a 4th term (+$0.18 × km).")
    return 0


def fire_dry_run_only(event: str, _undo: bool, dry_run: bool, _re_fire: bool) -> int:
    """`hdb-loading-curfew` and `mas-climate-disclosure` are Week 5+ shells."""
    if not dry_run:
        print(f"Scenario '{event}' is dry-run only for Week 4. Pass --dry-run.", file=sys.stderr)
        return 3
    payload = {"event": event, "status": "dry-run", "week": "5+"}
    print(json.dumps(payload, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

EVENTS: dict[str, Callable[[bool, bool, bool], int]] = {
    "union-cap": fire_union_cap,
    "drift-week-78": fire_drift_week78,
    "lta-carbon-levy": fire_lta_carbon_levy,
    "hdb-loading-curfew": lambda u, d, r: fire_dry_run_only("hdb-loading-curfew", u, d, r),
    "mas-climate-disclosure": lambda u, d, r: fire_dry_run_only("mas-climate-disclosure", u, d, r),
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scenario_inject", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    fire = sub.add_parser("fire", help="Fire a scenario event")
    fire.add_argument("event", help=f"One of: {', '.join(EVENTS)}")
    fire.add_argument("--undo", action="store_true", help="Reverse the event")
    fire.add_argument("--dry-run", action="store_true", help="Print payload without writing")
    fire.add_argument("--re-fire", action="store_true", help="Overwrite an already-fired event")

    sub.add_parser("list", help="List available events")

    args = parser.parse_args(argv)
    _detect_workspace()

    if args.command == "list":
        print("Available scenarios:")
        for name in EVENTS:
            print(f"  - {name}")
        return 0

    if args.event not in EVENTS:
        print(
            f"ERROR: unknown event '{args.event}'. Try one of: {', '.join(EVENTS)}", file=sys.stderr
        )
        return 1

    handler = EVENTS[args.event]
    return handler(args.undo, args.dry_run, args.re_fire)


if __name__ == "__main__":
    sys.exit(main())
