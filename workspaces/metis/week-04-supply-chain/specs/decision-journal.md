# Decision Journal — Data Model + CLI

This spec is the authority on the decision journal: the entry schema, the `metis journal` CLI, the PDF export, rubric-dimension embedding, and auto-linkage to `ExperimentTracker` run IDs and `ModelRegistry` versions.

The journal is the 60% of the workshop grade (see `rubric-grader.md`). It is also the student's portfolio artefact — by Week 8 it is a ~50-page record of ML decision-making that stands as evidence when the student pitches a CEO or a VC.

## 1. Entry schema

Every journal entry is a Markdown file at `journal/phase_<N>_<slug>.md`. The filename encodes the phase number (1..13, plus `postunion` / `postdrift` suffixes for re-runs). Contents follow a fixed schema — hand-written or produced by `metis journal add`.

### 1.1 Canonical filename patterns

```
journal/phase_1_frame.md
journal/phase_2_data_audit.md
journal/phase_5_model_selection.md
journal/phase_5_postdrift.md
journal/phase_6_metric_threshold.md
journal/phase_6_postdrift.md
journal/phase_7_red_team.md
journal/phase_8_gate.md
journal/phase_8_postunion.md
journal/phase_9_codify.md
journal/phase_10_objective.md
journal/phase_11_constraints.md
journal/phase_11_postunion.md
journal/phase_12_solver.md
journal/phase_12_postunion.md
journal/phase_13_retrain.md
```

The grader and the Viewer Panel's Playbook Progress bar match against these exact patterns. `phase_8_postunion.md` is the Sprint 2 Phase-8 re-run entry (deployment gate on the post-union plan) — noted explicitly so the Viewer's chip matcher does not miss it.

### 1.2 Frontmatter (required)

Every entry begins with YAML frontmatter:

```yaml
---
phase: 6
phase_name: "Metric + Threshold"
sprint: 1
timestamp: 2026-04-16T14:32:18+08:00
experiment_run_ids: ["<tracker-run-uuid>"] # ExperimentTracker run UUIDs (library native)
experiment_run_names: ["forecast_sprint1_GradientBoostingRegressor"] # human-readable run_name (cosmetic)
model_version_ids: ["forecast_sprint1_v3"] # derived string of form {name}_v{version}
scenario_tag: null # "preunion", "postunion", "postdrift" for re-runs
---
```

- `phase` and `phase_name` are authoritative for the grader's phase attribution.
- `sprint` is 1, 2, 3, or `close` (for Phase 9).
- `timestamp` is ISO-8601 with timezone. Auto-filled by `metis journal add`.
- `experiment_run_ids` is a list of `ExperimentTracker` run UUIDs the entry references. Auto-populated from `ExperimentTracker.list_runs(created_after=<last_entry_timestamp>)` when the student adds the entry via CLI. The UUID is the library's native primary key; the `experiment_run_names` field is an optional cosmetic alias.
- `model_version_ids` is a list of derived `{model_name}_v{version}` strings (NOT opaque `mv_007` strings). Auto-populated from the most recent `ModelRegistry.list_models()` call — each yields a `(name, version)` pair that's joined into the derived string by `ml_context.derive_model_version_id`.
- `scenario_tag` distinguishes re-run entries from their originals.

Auto-linkage (populating `experiment_run_ids` and `model_version_ids`) runs only through the CLI. Students who write markdown files by hand in their editor MUST fill these manually; the grader treats `experiment_run_ids: []` on a Phase 5 / 8 entry as a 0 on the Trade-off honesty dimension because the run isn't cited.

### 1.3 Body schema

The body is phase-specific. Each phase's body fields are listed in `playbook-universal.md` under the phase's "Journal schema" heading. The 5 rubric dimensions are embedded as headings so the grader can parse them deterministically:

```markdown
## Harm framing

Named cost: \_**\_
Cost asymmetry: $** (under) vs $** (over) = **:1

## Metric-cost linkage

Metric: \_**\_
Reason in dollars: \_\_**

## Trade-off honesty

Chosen: \_**\_ (run ID: \_\_**)
Sacrificed: \_**\_ (quantified: \_\_**)

## Constraint classification

Hard: \_**\_ (reason: \_\_**)
Soft: \_**\_ (penalty: \_\_**)

## Reversal condition

Signal: \_**\_
Threshold: \_\_**
Duration window: \_**\_
Human-in-the-loop: yes / no (why: \_\_**)
```

Phases where a dimension does not apply (see `rubric-grader.md` §1.3 applicability matrix) can omit the corresponding heading. The grader's dimension-applicability matrix controls the denominator; omitting an applicable heading scores 0 on that dimension.

### 1.4 Free-form section

After the five dimension headings, an optional `## Notes` section captures anything that doesn't fit the rubric (context, the student's reasoning chain, what they'd ask Claude Code next). The grader ignores `## Notes` for scoring but it appears in the PDF export.

## 2. Template — `journal/_template.md`

Pre-built skeleton copied by `metis journal add`. Contents:

```markdown
---
phase: <N>
phase_name: "<filled by CLI>"
sprint: <1|2|3|close>
timestamp: <ISO-8601>
experiment_run_ids: []
model_version_ids: []
scenario_tag: null
---

# Phase <N> — <phase_name>

> Rubric dimensions applied to this phase: <list from applicability matrix>

## Harm framing

…

## Metric-cost linkage

…

## Trade-off honesty

…

## Constraint classification

…

## Reversal condition

…

## Notes

…
```

The CLI populates `<N>`, `phase_name`, `sprint`, `timestamp`, auto-linked IDs, and the rubric-dimensions-applied list, leaving the body content for the student.

## 3. Worked examples — `journal/_examples.md`

`[PRE-BUILT]`. Contains three entries scored 4/4 and three scored 1/4, side-by-side per phase. The 4/4 examples anchor what "good" looks like; the 1/4 examples make the gap visible before the student writes their first entry. One 4/4 / 1/4 pair from Phase 6 is reproduced in `rubric-grader.md` §1.1 and §1.2.

## 4. CLI — `metis journal`

The `metis` CLI is a thin wrapper around `scripts/journal_export.py` and a template-filler. The three subcommands:

### 4.0 Journal lifecycle state machine

Journal entries move through four states driven by the `metis journal` subcommands. Transitions outside the table are rejected.

```
(no file)
   │
   │  metis journal add --phase N [--scenario tag]
   ▼
drafted  ──metis journal add (same phase, --scenario)──→ drafted (new file at phase_N_<scenario>.md)
   │                                                              │
   │  metis journal add --phase N  (same phase, same scenario)     │
   │  → append `## Previous draft` section with old content;       │
   │    timestamp updates; entry stays in `drafted`                │
   │                                                              │
   │  (student's editor saves + closes)                            │
   ▼                                                              │
listed    (shows via `metis journal list`)                        │
   │                                                              │
   │  metis journal export → compiles all drafted/listed entries  │
   ▼                                                              │
exported  (present in journal.pdf / journal.md)                   │
   │                                                              │
   │  metis journal add (same phase, same scenario) on a NEW      │
   │  concern → adds new `## Previous draft` section (rollback-   │
   │  like: previous content is preserved, not lost)              │
   └───────────────────────────── loops back to drafted ──────────┘
```

The add/list/export transitions are LEGAL. "Delete a journal entry" is NOT a legal transition — entries are append-only. Rollback-style edits preserve prior content as `## Previous draft` sections (the same content is the rollback target; there is no destructive operation).

### 4.1 `metis journal add [--phase <N>] [--scenario <tag>]`

- Copies `journal/_template.md` → `journal/phase_<N>_<slug>.md`.
- Fills the frontmatter:
  - `phase` and `phase_name` from a hard-coded table (1..13 + close).
  - `sprint` derived from phase number.
  - `timestamp` from the system clock.
  - `experiment_run_ids` via `ExperimentTracker.list_runs(created_after=<last_entry_timestamp>)` — any run logged since the last journal entry is a candidate for citation.
  - `model_version_ids` via `ModelRegistry.list_models()` filtered to stages `{staging, shadow, production}`, then each `(name, version)` joined via `ml_context.derive_model_version_id(name, version)` into the `{name}_v{version}` string form.
  - `scenario_tag` = `--scenario` value if provided.
- Opens the file in `$EDITOR` (defaults to `${VISUAL:-${EDITOR:-vi}}`).
- On editor close, validates the frontmatter parses and the required rubric-dimension headings are present.
- Updates `journal/.last_entry_timestamp` (plain-text file, ISO-8601) so the next `add` call's `created_after` query excludes already-cited runs.
- Prompts the student with: "Which dimensions did you cover? The grader applies dimensions <applicable list>; missing headings score 0."

`<last_entry_timestamp>` is persisted in `journal/.last_entry_timestamp`. On first `add`, the file doesn't exist — the CLI falls back to epoch-0 (all runs are candidates). The file is updated atomically on every successful `add` (write to `.tmp` + rename). If a student writes entries by hand without going through the CLI, `.last_entry_timestamp` stays stale; the next `add` will re-offer runs the student already cited, which is a safe over-offer (the student edits to remove duplicates).

If the student runs `metis journal add` without `--phase`, the CLI infers from the most recent Claude Code activity (checks `.scenario_log.jsonl` + recent `/api/workspace/state` changes) and asks to confirm.

### 4.2 `metis journal list [--phase <N>] [--scenario <tag>]`

- Walks `journal/*.md` in phase-then-timestamp order.
- Prints a one-line summary per entry: `phase_7_red_team.md   14:42   runs=[<uuid-short>]   models=[forecast_sprint1_v3]   [Phase 7 — Red-Team]`.
- `--phase` and `--scenario` filter.

### 4.3 `metis journal export [--output journal.pdf]`

- Wraps `scripts/journal_export.py`.
- Compiles all `journal/*.md` entries into a single PDF.
- Run at the Close block (~03:25) by the student as part of their deliverables.

## 5. PDF export format

`journal.pdf` is the student's final deliverable for the 60% grade layer.

### 5.1 Layout

- **Cover page**: student name (from `$USER` or `--student-id`), workshop date, total score (if `grade_report.json` is present), Viewer Pane screenshot (optional).
- **Table of contents**: phase → page number.
- **Per-entry pages**:
  - Header: "Phase N — phase_name — sprint X — timestamp".
  - Frontmatter cited runs + models displayed as a cited-sources box.
  - Rubric-dimension headings rendered as `h2` with a dimension-score badge (if grader has scored) showing 0/2/4 dots colour-coded green/yellow/red.
  - Body markdown rendered with a readable serif font.
- **Appendix**: auto-generated "cited artefacts" index — every `experiment_run_id` referenced with a one-line summary from `ExperimentTracker.get_run`; every `model_version_id` referenced with a one-line summary from `ModelRegistry.get`.

### 5.2 Tech stack

- `pandoc` (via subprocess) as the markdown → PDF engine.
- A small LaTeX template (`scripts/journal_template.tex`) for the cover and table of contents.
- Graceful fallback: if `pandoc` or `latex` is missing, the CLI emits `journal.md` (concatenated) and `journal.html` via a pure-Python markdown → HTML pass. The grader accepts `.pdf` OR `.md`; the Viewer Panel's Journal Panel reads the individual `.md` files directly regardless.

### 5.3 Reproducibility

Same journal files + same grader state → byte-identical PDF (modulo the timestamp header, which is frozen to the export time). This keeps the grade deterministic if the instructor re-runs the export.

## 6. Auto-linkage contract

The frontmatter fields `experiment_run_ids` and `model_version_ids` are the only mechanical link between a journal entry and the underlying framework state. Two rules govern them:

### 6.1 Populated at creation

`metis journal add` queries the tracker and registry at the moment of creation and fills the lists with candidate runs / versions. The student edits to remove uncited ones. Empty lists on phases where the rubric requires citation (Phase 5 selection, Phase 8 gate) score 0 on the affected dimensions.

### 6.2 Validated at export

`metis journal export` validates every listed `experiment_run_id` resolves in `ExperimentTracker.get_run(id)` and every `model_version_id` resolves in `ModelRegistry.get(id)`. Unresolvable IDs are flagged in red on the PDF page with "referenced run ID not found in tracker — fabrication?" — this is a deterrent against hand-forging frontmatter to chase the rubric.

## 7. Reversal condition requirement

Every journal entry at phases 1, 2, 5, 6, 7, 8, 12, 13 MUST include a non-trivial reversal condition under the `## Reversal condition` heading. Non-trivial means: names a signal AND a threshold AND (for Phase 13) a duration window. "If data changed" is explicitly 0/4 — the anti-pattern is named in `rubric-grader.md` §5.

The template embeds the reversal-condition fields as `Signal: ____`, `Threshold: ____`, `Duration window: ____`. A student who leaves any of those blank scores partial credit at best.

## 8. Journal hygiene

- Entries are append-only per phase. If a student re-writes an entry, the timestamp updates but prior content is not lost — the CLI appends a `## Previous draft` section with the superseded content.
- No PII beyond the student's own identifier (from `$USER` or `--student-id`).
- No secrets — the auto-linkage populates IDs only, never credentials.
- `.gitignore` the `journal/` directory in shared scaffolds so students don't accidentally commit their journal to a public fork.

## Open questions

- **Offline export** — if a student's laptop has neither `pandoc` nor LaTeX, the fallback path produces HTML + MD but not PDF. The grader accepts that; the 50-page-portfolio narrative is weaker. Flag for future: pre-install `pandoc` via the `scripts/preflight.py` remediation.
- **Hand-typed frontmatter** — a student who writes markdown in an editor without going through `metis journal add` must fill `experiment_run_ids` and `model_version_ids` manually. The grader has no way to distinguish "student forgot to cite" from "student cited but the ID is wrong" — both score 0 on Trade-off honesty. This is intentional but worth making explicit in student docs.
