#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""LumenCircuit preflight — green-light check before the workshop opens.

Usage:
    .venv/bin/python src/manufacturing/scripts/preflight.py

Exit code 0 = all green; non-zero = a step failed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = "✓" if ok else "✗"
    line = f"  [{mark}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    print("metis.manufacturing.preflight starting")
    failures = 0

    # 1. Data files
    for f in (
        "boards_labelled.csv",
        "sensor_stream.csv",
        "rl_episodes.json",
        "baseline_vision_metrics.json",
        "baseline_predmaint_metrics.json",
        "baseline_rl_metrics.json",
        "drift_baseline.json",
        "safety_labelled.csv",
    ):
        p = DATA / f
        ok = p.exists() and p.stat().st_size > 0
        if not check(f"data file {f}", ok, f"{p.stat().st_size:,} B" if ok else "missing"):
            failures += 1

    # 2. Image directories
    pcb_count = (
        len(list((DATA / "images_pcb").glob("*.png"))) if (DATA / "images_pcb").exists() else 0
    )
    if not check("PCB images >= 800", pcb_count >= 800, f"{pcb_count} found"):
        failures += 1
    safety_count = (
        len(list((DATA / "images_safety").glob("*.png")))
        if (DATA / "images_safety").exists()
        else 0
    )
    if not check("safety images >= 200", safety_count >= 200, f"{safety_count} found"):
        failures += 1

    # 3. Scenarios
    for s in ("mom_wsh_shadow_mandate.json", "q4_demand_drift.json"):
        p = DATA / "scenarios" / s
        if not check(f"scenario {s}", p.exists()):
            failures += 1

    # 4. Backend imports OK (the backend lives at src/manufacturing/, so we
    # need src/ on sys.path so `import manufacturing.backend.app` resolves;
    # this matches how `run_backend.sh` boots uvicorn from src/.)
    try:
        sys.path.insert(0, str(ROOT.parent))
        from manufacturing.backend.app import create_app  # noqa: F401
        from manufacturing.backend.startup import run_startup_sync  # noqa: F401

        check("backend imports", True)
    except Exception as e:
        check("backend imports", False, str(e))
        failures += 1

    # 5. RL episodes shape
    try:
        eps = json.loads((DATA / "rl_episodes.json").read_text())
        ok = all(
            p in eps and len(eps[p]) >= 1000
            for p in ("ppo_continuous", "dqn_discrete", "random_baseline")
        )
        if not check("RL episodes (≥1000 each policy)", ok):
            failures += 1
    except Exception as e:
        check("RL episodes", False, str(e))
        failures += 1

    # 6. Cost / compliance specs are loadable
    workspace = ROOT.parent.parent / "workspaces" / "metis" / "week-07-manufacturing"
    for spec in (
        "specs/_index.md",
        "specs/business-costs.md",
        "specs/api-surface.md",
        "specs/compliance-floors.md",
    ):
        p = workspace / spec
        if not check(f"spec {spec}", p.exists()):
            failures += 1

    print(
        "metis.manufacturing.preflight " + ("ok" if failures == 0 else f"FAIL ({failures} issues)")
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
