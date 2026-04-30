#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Pre-flight check — run BEFORE class starts.

Green-lights every precondition so the instructor knows the workspace is
ready. Check-only — does not mutate state.

Usage (from repo root):

    .venv/bin/python src/media/scripts/preflight.py

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
MEDIA_ROOT = REPO_ROOT / "src" / "media"
WORKSPACE = REPO_ROOT / "workspaces" / "metis" / "week-06-media"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"
CHECK = f"{GREEN}{RESET}"
WARN = f"{YELLOW}{RESET}"
FAIL = f"{RED}{RESET}"


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
        print(f"\n{BOLD}Metis Week 6 — MosaicHub Content Moderation Preflight{RESET}\n")
        for icon, label, detail in self.rows:
            line = f"  {icon}  {label}"
            if detail:
                line += f"  {detail}"
            print(line)
        print()
        if self.critical:
            print(f"{RED}{BOLD}NO-GO:{RESET} {self.critical} critical failure(s).")
        elif self.warnings:
            print(f"{YELLOW}{BOLD}DEGRADED:{RESET} {self.warnings} warning(s).")
        else:
            print(f"{GREEN}{BOLD}GO:{RESET} all green.")


def check_layout(r: Report) -> None:
    if REPO_ROOT.exists():
        r.ok("repo root", str(REPO_ROOT))
    else:
        r.fail("repo root missing", "")
    if MEDIA_ROOT.exists():
        r.ok("src/media/", str(MEDIA_ROOT))
    else:
        r.fail("src/media/ missing", "scaffold not generated")
    if WORKSPACE.exists():
        r.ok("workspace", str(WORKSPACE))
    else:
        r.fail("workspace missing", f"expected {WORKSPACE}")


def check_data(r: Report) -> None:
    required = [
        ("posts_labelled.csv", 80_000),
        ("baseline_image_metrics.json", None),
        ("baseline_text_metrics.json", None),
        ("fusion_baseline.json", None),
        ("drift_baseline.json", None),
        ("scenarios/imda_csam_mandate.json", None),
        ("scenarios/election_cycle_drift.json", None),
    ]
    for name, min_rows in required:
        path = MEDIA_ROOT / "data" / name
        if not path.exists():
            r.fail(f"data/{name}", "missing  run generate_data.py")
            continue
        if min_rows is not None:
            n = sum(1 for _ in path.open()) - 1  # minus header
            if n < min_rows:
                r.warn(f"data/{name}", f"{n} rows (expected {min_rows})")
            else:
                r.ok(f"data/{name}", f"{n:,} rows")
        else:
            try:
                json.loads(path.read_text())
                r.ok(f"data/{name}", "valid JSON")
            except Exception as exc:
                r.fail(f"data/{name}", f"invalid JSON: {exc}")


def check_images(r: Report) -> None:
    images_dir = MEDIA_ROOT / "data" / "images"
    if not images_dir.exists():
        r.warn(
            "data/images/",
            "directory missing  run generate_data.py (or accept synthesised-embedding mode)",
        )
        return
    n = sum(1 for _ in images_dir.glob("*.png"))
    if n == 0:
        r.warn("data/images/", "0 PNG files  --no-images was used; backend still works")
    elif n < 24_000:
        r.warn(f"data/images/", f"{n:,} PNGs (expected 24,000)")
    else:
        r.ok(f"data/images/", f"{n:,} PNG files")


def check_port(r: Report, port: int = 8000) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind(("127.0.0.1", port))
            r.ok(f"port {port} free", "")
        except OSError:
            r.warn(f"port {port} in use", "backend will fail to bind; set METIS_API_PORT")


def check_python_imports(r: Report) -> None:
    missing: list[str] = []
    for mod_name in ("polars", "sklearn", "scipy", "fastapi", "uvicorn", "PIL", "pydantic"):
        try:
            __import__(mod_name)
        except ImportError:
            missing.append(mod_name)
    if missing:
        r.fail("python imports", f"missing: {', '.join(missing)}")
    else:
        r.ok("python imports", "polars, sklearn, scipy, fastapi, uvicorn, PIL, pydantic")


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


def check_backend_imports(r: Report) -> None:
    """Smoke-test the backend Python package imports cleanly."""
    import importlib.util

    src_media = str(MEDIA_ROOT)
    if src_media not in sys.path:
        sys.path.insert(0, src_media)
    try:
        spec = importlib.util.find_spec("backend.app")
        if spec is None:
            r.fail("backend imports", "backend.app spec not found  PYTHONPATH issue")
            return
        # Don't actually import — that would invoke startup. Just check the
        # spec resolves and the source file is parseable.
        import ast

        ast.parse(Path(MEDIA_ROOT, "backend", "app.py").read_text())
        ast.parse(Path(MEDIA_ROOT, "backend", "ml_context.py").read_text())
        ast.parse(Path(MEDIA_ROOT, "backend", "startup.py").read_text())
        r.ok("backend imports", "app + ml_context + startup parse cleanly")
    except Exception as exc:
        r.fail("backend imports", f"parse error: {exc}")


def main() -> int:
    r = Report()
    check_layout(r)
    check_python_imports(r)
    check_data(r)
    check_images(r)
    check_port(r, 8000)
    check_backend_imports(r)
    check_workspace_scaffolding(r)
    r.render()
    if r.critical:
        return 2
    if r.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
