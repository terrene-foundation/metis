#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Pre-flight check — run BEFORE class starts.

Green-lights every precondition so the instructor knows the workspace is
ready. Check-only — does not mutate state.

Usage (from workspace root):

    python scripts/preflight.py

Exit codes:
  0  all green — class can start
  1  warnings present — class can start degraded
  2  critical failures — instructor must fix
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

CHECK = f"{GREEN}✓{RESET}"
WARN = f"{YELLOW}⚠{RESET}"
FAIL = f"{RED}✗{RESET}"


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []  # (icon, label, detail)
        self.critical_failures = 0
        self.warnings = 0

    def ok(self, label: str, detail: str = "") -> None:
        self.rows.append((CHECK, label, detail))

    def warn(self, label: str, detail: str) -> None:
        self.rows.append((WARN, label, detail))
        self.warnings += 1

    def fail(self, label: str, detail: str) -> None:
        self.rows.append((FAIL, label, detail))
        self.critical_failures += 1

    def render(self) -> None:
        print(f"\n{BOLD}Metis Week 4 — Preflight Report{RESET}\n")
        for icon, label, detail in self.rows:
            line = f"  {icon}  {label}"
            if detail:
                line += f"  — {detail}"
            print(line)
        print()
        if self.critical_failures:
            print(
                f"{RED}{BOLD}NO-GO:{RESET} {self.critical_failures} critical failure(s). Fix before class."
            )
        elif self.warnings:
            print(f"{YELLOW}{BOLD}DEGRADED:{RESET} {self.warnings} warning(s). Class can start.")
        else:
            print(f"{GREEN}{BOLD}GO:{RESET} all green.")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def _port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def check_workspace(r: Report) -> None:
    for path, desc in [
        (WORKSPACE_ROOT / "PLAYBOOK.md", "PLAYBOOK.md"),
        (WORKSPACE_ROOT / "START_HERE.md", "START_HERE.md"),
        (WORKSPACE_ROOT / "PRODUCT_BRIEF.md", "PRODUCT_BRIEF.md"),
        (WORKSPACE_ROOT / "SCAFFOLD_MANIFEST.md", "SCAFFOLD_MANIFEST.md"),
        (WORKSPACE_ROOT / "specs" / "_index.md", "specs/_index.md"),
    ]:
        if path.exists():
            r.ok(f"Doc present: {desc}")
        else:
            r.fail(f"Doc missing: {desc}", f"expected at {path}")


def check_env(r: Report) -> None:
    env_file = WORKSPACE_ROOT / ".env"
    env_example = WORKSPACE_ROOT / ".env.example"
    if env_file.exists():
        r.ok(".env present")
    elif env_example.exists():
        r.warn(".env missing", "falling back to .env.example — copy it to .env for overrides")
    else:
        r.fail(".env and .env.example both missing", "cannot start backend")


def check_data(r: Report) -> None:
    data_dir = WORKSPACE_ROOT / "data"
    required = [
        "northwind_demand.csv",
        "northwind_customers.csv",
        "northwind_fleet.csv",
        "northwind_depots.csv",
        "week78_drift.json",
        "leaderboard_prebaked.json",
    ]
    for name in required:
        p = data_dir / name
        if p.exists():
            size_kb = p.stat().st_size // 1024
            r.ok(f"Data: {name}", f"{size_kb} KB")
        else:
            r.fail(f"Data missing: {name}", "run scripts/regenerate_data.py (shard 07)")


def check_ports(r: Report) -> None:
    # Load env overrides if present — only read, do not export.
    port_backend = int(os.environ.get("KAILASH_NEXUS_PORT", "8000"))
    # Viewer binds on 3000 per canonical-values §7 (not env-overridable today).
    if _port_free(port_backend):
        r.ok(f"Port {port_backend} free (backend)")
    else:
        r.warn(f"Port {port_backend} in use", "backend may fail to bind; set KAILASH_NEXUS_PORT")
    if _port_free(3000):
        r.ok("Port 3000 free (viewer)")
    else:
        r.warn("Port 3000 in use", "viewer may fail to bind")


def check_backend_imports(r: Report) -> None:
    try:
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "from src.backend.app import app; "
                "routes = [r.path for r in app.routes if hasattr(r, 'path')]; "
                "need = {'/health', '/forecast/train', '/forecast/compare', "
                "'/forecast/predict', '/optimize/solve', '/drift/check'}; "
                "missing = need - set(routes); "
                "assert not missing, f'missing: {missing}'; print('ok')",
            ],
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and "ok" in result.stdout:
            r.ok("Backend imports + all 6 routes registered")
        else:
            detail = (
                (result.stderr or result.stdout or "").strip().splitlines()[-1]
                if (result.stderr or result.stdout)
                else "unknown"
            )
            r.fail("Backend import failed", detail[:200])
    except FileNotFoundError:
        r.fail("`uv` not found", "install uv or activate .venv manually")
    except subprocess.TimeoutExpired:
        r.fail("Backend import timed out", "check for blocking imports")


def check_viewer(r: Report) -> None:
    pkg = WORKSPACE_ROOT / "apps" / "web" / "package.json"
    node_modules = WORKSPACE_ROOT / "apps" / "web" / "node_modules"
    if not pkg.exists():
        r.fail("Viewer package.json missing", str(pkg))
        return
    r.ok("Viewer package.json present")
    if node_modules.exists():
        r.ok("Viewer node_modules installed")
    else:
        r.warn("Viewer node_modules not installed", "run `cd apps/web && npm install` before class")


def check_journal(r: Report) -> None:
    journal_dir = WORKSPACE_ROOT / "journal"
    template = journal_dir / "_template.md"
    examples = journal_dir / "_examples.md"
    if template.exists():
        r.ok("Journal template present")
    else:
        r.warn("Journal template missing", str(template))
    if examples.exists():
        r.ok("Journal examples present")
    else:
        r.warn("Journal examples missing", str(examples))


def check_scripts(r: Report) -> None:
    for name in ["run_backend.sh", "scenario_inject.py", "journal_export.py", "preflight.py"]:
        p = WORKSPACE_ROOT / "scripts" / name
        if p.exists():
            r.ok(f"Script: {name}")
        else:
            r.warn(f"Script missing: {name}", "instructor may need manual fallback")


def main() -> int:
    r = Report()
    check_workspace(r)
    check_env(r)
    check_data(r)
    check_ports(r)
    check_backend_imports(r)
    check_viewer(r)
    check_journal(r)
    check_scripts(r)
    r.render()
    if r.critical_failures:
        return 2
    if r.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
