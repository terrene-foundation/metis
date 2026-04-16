#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Journal export — concatenate `journal/phase_*.md` into a single PDF.

Authoritative spec: `specs/decision-journal.md` §3 (PDF export format).

Usage (from workspace root):

    python scripts/journal_export.py           # → journal.pdf (and .md)
    python scripts/journal_export.py --md-only # concatenated markdown only
    python scripts/journal_export.py --out /tmp/my-submission.pdf

Behavior:
  - Reads every `journal/phase_*.md` matching `phase_<N>_*.md` (e.g.
    `phase_1_frame.md`, `phase_6_metric_threshold.md`).
  - Sorts by phase number ascending, then by suffix (so `phase_5_postdrift`
    follows `phase_5_model_selection`).
  - Skips files whose names start with `_` (template, examples).
  - Concatenates with separator + cited-artefacts appendix.
  - Tries pandoc for PDF; falls back to cleanly-named markdown if pandoc
    or a LaTeX engine is missing (lesson grader reads markdown).

Exit codes:
  0  export succeeded (PDF or fallback MD)
  1  no journal entries found
  2  workspace not detected
  3  pandoc failed AND fallback MD also failed
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
JOURNAL_DIR = WORKSPACE_ROOT / "journal"
ALIAS_FILE = WORKSPACE_ROOT / "data" / ".experiment_aliases.json"

PHASE_RE = re.compile(r"^phase_(\d+)_([a-z0-9_]+)\.md$")


def _detect_workspace() -> None:
    if not (WORKSPACE_ROOT / "PLAYBOOK.md").exists():
        print(f"ERROR: workspace not detected at {WORKSPACE_ROOT}", file=sys.stderr)
        sys.exit(2)


def _discover_entries() -> list[tuple[int, str, Path]]:
    """Return (phase_number, suffix, path) for every journal entry."""
    if not JOURNAL_DIR.exists():
        return []
    entries: list[tuple[int, str, Path]] = []
    for p in sorted(JOURNAL_DIR.iterdir()):
        if not p.is_file() or p.name.startswith("_"):
            continue
        m = PHASE_RE.match(p.name)
        if not m:
            continue
        phase_num = int(m.group(1))
        suffix = m.group(2)
        entries.append((phase_num, suffix, p))
    entries.sort(key=lambda t: (t[0], t[1]))
    return entries


def _build_appendix() -> str:
    """Cited-artefacts index — every experiment_run_id / model_version_id from
    decision-journal.md §6. Simplified: just list the alias file contents."""
    lines = ["## Appendix — Cited Artefacts", ""]
    if ALIAS_FILE.exists():
        try:
            aliases = json.loads(ALIAS_FILE.read_text())
            if aliases:
                lines.append("### ExperimentTracker runs referenced")
                lines.append("")
                for alias, uuid in sorted(aliases.items()):
                    lines.append(f"- **{alias}** → `{uuid}`")
            else:
                lines.append("_No aliases recorded (alias file is empty)._")
        except json.JSONDecodeError:
            lines.append("_Alias file malformed; see `data/.experiment_aliases.json`._")
    else:
        lines.append(
            "_No alias file yet — students who have not run /forecast/train have nothing to cite._"
        )
    lines.append("")
    return "\n".join(lines)


def _concat_markdown(entries: list[tuple[int, str, Path]]) -> str:
    header = [
        "---",
        "title: Metis Week 4 — Decision Journal Submission",
        f"date: {datetime.now(timezone.utc).isoformat()}",
        "author: (student)",
        "---",
        "",
        "# Metis Week 4 — Northwind Control Tower Decision Journal",
        "",
        "> Submission artefact. Graded on the 5-dimension rubric in",
        "> `specs/rubric-grader.md` §1 (Harm framing, Metric-cost linkage,",
        "> Trade-off honesty, Constraint classification, Reversal condition).",
        "",
    ]
    parts = ["\n".join(header)]
    for phase_num, suffix, path in entries:
        parts.append(f"\n---\n\n## Phase {phase_num} — {suffix.replace('_', ' ').title()}\n")
        parts.append(f"*Source: `journal/{path.name}`*\n")
        parts.append(path.read_text(encoding="utf-8"))
    parts.append("\n---\n")
    parts.append(_build_appendix())
    return "\n".join(parts)


def _try_pandoc(md_path: Path, pdf_path: Path) -> bool:
    """Return True if pandoc produced the PDF."""
    if not _have_binary("pandoc"):
        print("INFO: pandoc not found — shipping markdown instead.", file=sys.stderr)
        return False
    # Prefer typst (fast, no TeX dependency) if available; fall back to the
    # default PDF engine (LaTeX) or html (wkhtmltopdf). Last resort: leave MD.
    engines = ["typst", "xelatex", "pdflatex", "tectonic"]
    for engine in engines:
        if not _have_binary(engine):
            continue
        try:
            subprocess.run(
                ["pandoc", str(md_path), "-o", str(pdf_path), f"--pdf-engine={engine}"],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return True
        except subprocess.CalledProcessError as err:
            print(f"WARN: pandoc with {engine} failed: {err.stderr[:300]}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            print(f"WARN: pandoc with {engine} timed out.", file=sys.stderr)
    return False


def _have_binary(name: str) -> bool:
    from shutil import which

    return which(name) is not None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="journal_export", description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=WORKSPACE_ROOT / "journal.pdf",
        help="Output path for the PDF (default: ./journal.pdf)",
    )
    parser.add_argument(
        "--md-only", action="store_true", help="Emit concatenated markdown only; skip PDF"
    )
    args = parser.parse_args(argv)

    _detect_workspace()
    entries = _discover_entries()
    if not entries:
        print(
            "No journal entries found in journal/. Expected files: phase_N_<slug>.md",
            file=sys.stderr,
        )
        return 1

    md_body = _concat_markdown(entries)
    md_out = args.out.with_suffix(".md")
    md_out.write_text(md_body, encoding="utf-8")
    print(f"Wrote {md_out} ({len(entries)} phases).")

    if args.md_only:
        return 0

    pdf_out = args.out if args.out.suffix == ".pdf" else args.out.with_suffix(".pdf")
    if _try_pandoc(md_out, pdf_out):
        print(f"Wrote {pdf_out}.")
        return 0

    # Fallback — md_out is the submission artefact.
    print(
        f"PDF export unavailable; submit {md_out} instead (grader accepts markdown).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
