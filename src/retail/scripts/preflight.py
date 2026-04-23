#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Pre-flight check — run BEFORE class starts.

Green-lights every precondition so the instructor knows the workspace is
ready. Check-only — does not mutate state.

Usage (from repo root):

    .venv/bin/python src/retail/scripts/preflight.py

Exit codes:
  0  all green
  1  warnings present — class can start degraded
  2  critical failures — instructor must fix
"""

from __future__ import annotations

import json
import socket
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
RETAIL_ROOT = REPO_ROOT / "src" / "retail"
WORKSPACE = REPO_ROOT / "workspaces" / "metis" / "week-05-retail"

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
        self.rows: list[tuple[str, str, str]] = []
        self.critical = 0
        self.warnings = 0

    def ok(self, label: str, detail: str = "") -> None:
        self.rows.append((CHECK, label, detail))

    def warn(self, label: str, detail: str) -> None:
        self.rows.append((WARN, label, detail))
        self.warnings += 1

    def fail(self, label: str, detail: str) -> None:
        self.rows.append((FAIL, label, detail))
        self.critical += 1

    def render(self) -> None:
        print(f"\n{BOLD}Metis Week 5 — Arcadia Retail Preflight{RESET}\n")
        for icon, label, detail in self.rows:
            line = f"  {icon}  {label}"
            if detail:
                line += f"  — {detail}"
            print(line)
        print()
        if self.critical:
            print(f"{RED}{BOLD}NO-GO:{RESET} {self.critical} critical failure(s).")
        elif self.warnings:
            print(f"{YELLOW}{BOLD}DEGRADED:{RESET} {self.warnings} warning(s).")
        else:
            print(f"{GREEN}{BOLD}GO:{RESET} all green.")


def check_layout(r: Report) -> None:
    r.ok("repo root", str(REPO_ROOT)) if REPO_ROOT.exists() else r.fail("repo root missing", "")
    (
        r.ok("src/retail/", str(RETAIL_ROOT))
        if RETAIL_ROOT.exists()
        else r.fail("src/retail/ missing", "run `scripts/generate_data.py`?")
    )
    (
        r.ok("workspace", str(WORKSPACE))
        if WORKSPACE.exists()
        else r.fail("workspace missing", f"expected {WORKSPACE}")
    )


def check_data(r: Report) -> None:
    required = [
        ("arcadia_customers.csv", 5000),
        ("arcadia_products.csv", 400),
        ("arcadia_transactions.csv", 50_000),  # lower bound
        ("segment_baseline.json", None),
        ("segment_candidates.json", None),
        ("drift_baseline.json", None),
        ("scenarios/pdpa_redline.json", None),
        ("scenarios/catalog_drift.json", None),
    ]
    for name, min_rows in required:
        path = RETAIL_ROOT / "data" / name
        if not path.exists():
            r.fail(f"data/{name}", "missing — run generate_data.py")
            continue
        if min_rows is not None:
            n = sum(1 for _ in path.open()) - 1  # minus header
            if n < min_rows:
                r.warn(f"data/{name}", f"{n} rows (expected ≥ {min_rows})")
            else:
                r.ok(f"data/{name}", f"{n:,} rows")
        else:
            try:
                json.loads(path.read_text())
                r.ok(f"data/{name}", "valid JSON")
            except Exception as exc:
                r.fail(f"data/{name}", f"invalid JSON: {exc}")


def check_port(r: Report, port: int = 8000) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind(("127.0.0.1", port))
            r.ok(f"port {port} free", "")
        except OSError:
            r.warn(f"port {port} in use", "backend will fail to bind; set METIS_API_PORT")


def check_python_imports(r: Report) -> None:
    try:
        import polars  # noqa: F401
        import sklearn  # noqa: F401
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401

        r.ok("python imports", "polars, sklearn, fastapi, uvicorn")
    except ImportError as exc:
        r.fail("python imports", f"missing: {exc}")


def check_workspace_scaffolding(r: Report) -> None:
    for sub in ("briefs", "01-analysis", "todos/active", "journal", "specs"):
        p = WORKSPACE / sub
        if p.exists():
            r.ok(f"workspace/{sub}", "")
        else:
            r.warn(f"workspace/{sub} missing", "will be created on first use")
    for doc in ("PRODUCT_BRIEF.md", "PLAYBOOK.md", "START_HERE.md"):
        p = WORKSPACE / doc
        if p.exists():
            r.ok(f"workspace/{doc}", "")
        else:
            r.fail(f"workspace/{doc} missing", "student manual not yet written")


def main() -> int:
    r = Report()
    check_layout(r)
    check_python_imports(r)
    check_data(r)
    check_port(r, 8000)
    check_workspace_scaffolding(r)
    r.render()
    if r.critical:
        return 2
    if r.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
