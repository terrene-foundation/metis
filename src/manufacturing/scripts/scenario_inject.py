#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Mid-session scenario injection for the LumenCircuit workshop.

Two scenarios:
  - mom_wsh_shadow_mandate (Sprint 3) — forces agent autonomy ladder for
    WSH-affecting task classes to "shadow" until --undo
  - q4_demand_drift (Sprint 4) — flags the predictive-maintenance signal as
    drifting; students re-run /drift/check to see severity rise

Usage:
    .venv/bin/python src/manufacturing/scripts/scenario_inject.py mom_wsh_shadow_mandate
    .venv/bin/python src/manufacturing/scripts/scenario_inject.py mom_wsh_shadow_mandate --undo
    .venv/bin/python src/manufacturing/scripts/scenario_inject.py q4_demand_drift
    .venv/bin/python src/manufacturing/scripts/scenario_inject.py q4_demand_drift --undo

The mandate marker file lives in the workspace, not the scaffold — students see
it in `git status` and document the trigger in their journal.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKSPACE = ROOT / "workspaces" / "metis" / "week-07-manufacturing"
DATA = ROOT / "src" / "manufacturing" / "data"

SCENARIOS = {
    "mom_wsh_shadow_mandate": {
        "marker": WORKSPACE / "mom_wsh_shadow_mandate.active",
        "scenario_payload": DATA / "scenarios" / "mom_wsh_shadow_mandate.json",
    },
    "q4_demand_drift": {
        "marker": WORKSPACE / "q4_demand_drift.active",
        "scenario_payload": DATA / "scenarios" / "q4_demand_drift.json",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=list(SCENARIOS.keys()))
    parser.add_argument("--undo", action="store_true", help="Remove the marker")
    args = parser.parse_args()

    cfg = SCENARIOS[args.scenario]
    marker: Path = cfg["marker"]

    if args.undo:
        if marker.exists():
            marker.unlink()
            print(f"removed marker {marker.relative_to(ROOT)}")
        else:
            print(f"no marker at {marker.relative_to(ROOT)}")
        return 0

    payload = json.loads(cfg["scenario_payload"].read_text())
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(
            {
                "injected_at": datetime.now(timezone.utc).isoformat(),
                "scenario": args.scenario,
                "payload_path": str(cfg["scenario_payload"].relative_to(ROOT)),
                "payload_summary": {
                    k: payload.get(k)
                    for k in (
                        "trigger",
                        "mandate",
                        "rationale",
                        "estimated_compliance_shadow_price_dollars_per_day",
                        "modality_affected",
                        "expected_psi_lift",
                    )
                    if k in payload
                },
            },
            indent=2,
        )
    )
    print(f"injected {args.scenario} -> {marker.relative_to(ROOT)}")
    print(f"  trigger: {payload.get('trigger', 'N/A')}")
    if "mandate" in payload:
        print(f"  mandate: {payload['mandate']}")
    if "estimated_compliance_shadow_price_dollars_per_day" in payload:
        print(
            f"  est. compliance shadow price: "
            f"${payload['estimated_compliance_shadow_price_dollars_per_day']:,}/day"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
