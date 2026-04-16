# Recommended Approach — Week 4 Supply Chain Workshop

**Purpose**: resolve the four structural issues surfaced by the red-team review and define the workshop design that ships tomorrow. This document is the authoritative decision record; `PLAYBOOK.md` and the edited `START_HERE.md` follow from it.

## Design constraints (anchors)

- **Promise**: student ships a full product (forecast + optimizer + drift monitor) in one 3.5-hour session and defends a page of decisions. One-person unicorn framing is non-negotiable.
- **Audience**: non-coder MBAs. Plain language (`communication.md`), no unexplained jargon, decisions framed as impact.
- **Tool stack**: kailash-ml (TrainingPipeline, AutoMLEngine, ExperimentTracker, ModelRegistry, InferenceServer, DriftMonitor), kailash-nexus (endpoints), OR-Tools / PuLP (optimizer), Next.js Viewer Pane (read-only).
- **Terrene framing**: trust plane = human judgment; execution plane = Claude Code + frameworks (`terrene-naming.md`).
- **Zero tolerance**: scaffold files that look like implementation but contain placeholders MUST be banner-marked `# TODO-STUDENT:` or they violate `zero-tolerance.md` Rule 2.
- **Agent reasoning**: retrain rule stays in the trust plane; no `if X > Y` encoded in agent logic (`agent-reasoning.md`).
- **Orphan detection**: every component named in the doc has a production call site in scaffolded code (`orphan-detection.md`).

## Issue 1 — Time budget

### Decision: Option A + B hybrid (cut phases AND pre-bake leaderboard). Keep total at 3.5 hours.

Rationale: Option C (extend to 4.5h) loses institutional slot; Option D (shrink AutoML to 10 trials/3 families) still takes ~90s but does not solve the 13-phases-in-135-min problem. Option A alone leaves Sprint 1 with 5 phases each needing ~8 min; Option B alone keeps 9 phases but the critique-of-prebaked path is shallower than the run-your-own path. Hybrid (A+B) gets the muscle-memory of "I ran AutoML" AND the time to reason over a richer leaderboard.

### Rebudgeted schedule

| Block             | Minutes | Cumulative | What happens                                                                                   |
| ----------------- | ------- | ---------- | ---------------------------------------------------------------------------------------------- |
| Opening           | 10      | 10         | Read `SCAFFOLD_MANIFEST.md`, preflight runs, instructor sets expectations, opening prompt      |
| Sprint 1 Forecast | 75      | 85         | Phases 1, 2, 4, 5, 6, 7, 8. Phase 3 folded into 2. Phase 9 (codify) moved to end-of-class      |
| Break             | 10      | 95         | Hydrate, troubleshoot                                                                          |
| Sprint 2 Optimize | 60      | 155        | Phases 10, 11, 12 + union-cap injection at min 30 -> re-run 11+12 + re-run 8 (deployment gate) |
| Sprint 3 Monitor  | 40      | 195        | Phase 13 + drift-event injection + re-run 5+6 on post-drift data                               |
| Close             | 15      | 210        | Phase 9 codify, public grader run, journal export                                              |

Total = 210 min = 3.5 hours.

### Phases per sprint after the cut

- **Sprint 1 (Forecast, 75 min)**: phases 1, 2, 4, 5, 6, 7, 8. Seven phases, ~10 min each. Phase 3 (feature framing) is folded into Phase 2 (data audit) — the same dataset interrogation produces both artifacts.
- **Sprint 2 (Optimize, 60 min)**: phases 10, 11, 12, plus mid-sprint re-run of 11+12, plus re-run 8 (deployment gate for the new plan). Five phase-passes in 60 min.
- **Sprint 3 (Monitor, 40 min)**: phase 13, plus re-runs of 5 and 6 against post-drift data. Three phase-passes in 40 min.
- **Phase 9 (Codify)**: moved to the 15-min Close block — the last ~8 min of class. It is the `/codify` command over the session's journal; it is compact by design.

Net: 13 phases reduced to **12 phases** (3 folded), spread over 175 min of sprint time (+ 25 min bookend blocks) — average ~14 min per phase-pass counting re-runs.

### Pre-bake vs. live-build split

**Live-built** (student prompts Claude Code, real wall-clock execution):

- Data ingest to FeatureStore (Phase 2, ~30s)
- AutoMLEngine run with `search_n_trials=5, families=3, search_strategy="random"` (~60-90s)
- Model promotion staging -> shadow in Phase 8 (~5s)
- OR-Tools VRP solve in Sprint 2 (~20-45s)
- Second VRP solve post-injection (~20-45s)
- DriftMonitor `set_reference_data` auto-fires at training complete, then `check_drift` in Phase 13 (~5s)

**Pre-baked** (shipped in scaffold; student critiques existing artifact):

- `data/leaderboard_prebaked.json` — a 30-trial / 5-family Bayesian AutoML run persisted to the ExperimentTracker DB. Students compare their 5-trial run against this richer leaderboard and reason about the jump.
- `data/drift_baseline.json` — DriftMonitor reference distribution for the training window.
- `data/scenarios/union_cap.json` — the Sprint 2 injection payload.
- `data/scenarios/week78_drift.json` — the Sprint 3 injection payload (synthesized drifted data).

Rationale for the split: the live-built items are short enough (60-90s max) to preserve agency without blowing the budget, and the pre-baked items provide the depth of real production artifacts. The student sees "I ran AutoML and got these 5 runs; the pre-baked 30-trial leaderboard beats my best by 1.8% MAPE — why is that, is the lift worth it?" That is a trust-plane question.

## Issue 2 — Rubric gaming

### Decision: contract-based endpoint assertions, enforced by a pre-shipped grader script.

The product grade stays at 40% of the total (journal 60%). It stays at 5 endpoint checks but each check now asserts a non-trivial contract:

| Endpoint            | Contract asserted by grader                                                                                                                                      | Point weight |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `/forecast/train`   | Response contains `experiment_run_id`; `ExperimentTracker.get_run(id)` returns params AND >=2 metrics AND a non-null training timestamp                          | 8%           |
| `/forecast/compare` | Response is a list of >=3 runs; each run has distinct `params_hash`; metric column is present and numeric                                                        | 8%           |
| `/forecast/predict` | Response contains `model_version_id`; `ModelRegistry.get(id).stage` in {`staging`, `shadow`, `production`}; prediction is a number or list of numbers (not null) | 8%           |
| `/optimize/solve`   | Response contains `feasibility: true`, `optimality_gap` as float >=0, `hard_constraints_satisfied` as dict where every value is true                             | 8%           |
| `/drift/check`      | Response contains >=1 named statistical test (`ks` / `chi2` / `psi` / `js`) with a numeric statistic, and `severity` in {`none`, `low`, `moderate`, `severe`}    | 8%           |

Grader script `scripts/grade_product.py` is shipped in scaffold, imports each endpoint's live response, and runs these assertions as pytest-style checks. Script prints per-endpoint pass/fail with actionable messages ("run Phase 8 to promote a model to staging", "re-run Phase 12 with solver feasibility reporting enabled").

Instructor runs `scripts/grade_product.py` publicly at 3:20 pm on a projector. Students see the score live. No post-hoc regrade.

### Why this survives rubric gaming

A student who ships `{"status":"ok"}` gets 0% on `/forecast/train` because no `experiment_run_id` is present. A student who hardcodes a fake run ID gets 0% because `ExperimentTracker.get_run(id)` fails. A student who returns a fake `model_version_id` gets 0% because `ModelRegistry.get(id)` fails. Gaming would require reimplementing ExperimentTracker and ModelRegistry to fake-accept the grader's queries — at which point the student has done more work than the honest path and has no ML decisions to show for it.

## Issue 3 — AI Verify framework

### Decision: Option A — expand Phase 7 red-team to cover Transparency + Robustness + Safety. Fairness stays in Week 7.

Rationale: Options B (Phase 7.5) and C (drop entirely) are bad. Option C loses an anchor from the Week 4 deck and leaves students who read the deck believing the course dropped the framework. Option B crams a 14th phase into an already-tight sprint and fragments Phase 7's red-team spine. Option A threads the three applicable dimensions into the existing Phase 7, so the student learns AI Verify as "the structure of a good red-team" rather than as "yet another gate."

### Phase 7 rewrite (applies to Sprint 1 and Sprint 3 re-run)

Phase 7 red-team checklist expands from the current 4-item list to a 3-dimension structured scan:

1. **Transparency**
   - Which feature does the model rely on most heavily? (ModelExplainer global importance)
   - If that feature were removed, how does headline MAPE change? (feature-ablation test)
   - Can you explain to the Ops Manager in one sentence why the model predicted X?
2. **Robustness**
   - Which calendar weeks does the model fail on? (per-week MAPE)
   - Which customer segments have worst MAPE? (subgroup audit)
   - What happens on the week-78 drift event? (adversarial input test)
3. **Safety**
   - What is the cost of the model's worst 1% of predictions? (tail-risk in dollars)
   - What does the model predict on zero-demand days, or days missing upstream features? (degenerate-input test)
   - Who is harmed if this model silently fails for a week? (blast-radius memo)

Fairness (the 4th AI Verify dimension) is explicitly deferred: Phase 14 in the Playbook, covered in Week 7 (healthcare + credit). The Phase 7 journal entry ends with a one-line "fairness audit deferred to Week 7 per Playbook" so the student internalizes that the deferral is deliberate, not absent.

Phase 7 evaluation checklist is now a rubric row per dimension rather than a flat list. Phase 7 journal schema gains one-line fields for Transparency / Robustness / Safety dispositions.

### Why this resolves the red-team H1 finding

The deck covers all 4 AI Verify dimensions. The doc now covers 3, defers 1, and labels the deferral. No dimension is silently dropped. Transparency maps onto ModelExplainer (already scaffolded). Robustness maps onto per-segment / per-week MAPE (already produced by AutoML holdout evaluation). Safety maps onto the cost-asymmetry numbers ($40/$12/$220/$45) already in the brief. All three fit within the existing Phase 7 budget.

## Issue 4 — Scaffold manifest

### Decision: ship `SCAFFOLD_MANIFEST.md` as a workspace-root file, read by the opening prompt.

The full manifest is in `scaffold-manifest.md` (this workspace, `01-analysis/`). It enumerates every file across `apps/web/`, `src/`, `data/`, `specs/`, `scripts/`, and CI. Each file is marked:

- `[PRE-BUILT]` — scaffold ships a complete, working file. The student never edits it.
- `[STUDENT-COMMISSIONED]` — scaffold ships a placeholder with `# TODO-STUDENT:` banner. The student's prompt to Claude Code produces the real file. Grader runs against the student's version.
- `[PRE-BUILT + STUDENT-EXTENDED]` — scaffold ships a skeleton with a named extension point; student adds to named slot.

### Banner contract for placeholder files

Every `[STUDENT-COMMISSIONED]` file begins with the exact banner:

```
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace this file with the real
# implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.
# Do NOT edit manually — prompt Claude Code.
```

This satisfies `zero-tolerance.md` Rule 2 (no stubs mistaken for real work) and makes the hand-off unambiguous.

### Opening prompt rewrite

Old prompt asks Claude Code to summarize what's scaffolded. New prompt asks Claude Code to confirm it sees exactly the files listed in `SCAFFOLD_MANIFEST.md` and to flag any discrepancy:

```
Read @SCAFFOLD_MANIFEST.md, @PRODUCT_BRIEF.md, @PLAYBOOK.md, @START_HERE.md.

For each file in SCAFFOLD_MANIFEST.md, confirm the file exists at the
stated path AND matches the stated state (PRE-BUILT / STUDENT-COMMISSIONED /
PRE-BUILT + STUDENT-EXTENDED). Report any file that is missing, or any file
whose current contents do not match its stated state.

Then summarize, in plain language a non-coder can read:
  1. Which parts of the product are already wired
  2. Which parts I will commission from you today
  3. The 12 decision phases I will run across today's three sprints
  4. What output you produce vs. what output I produce

Stop and wait for me to run /analyze.
```

Claude Code cannot fabricate the manifest because it is a file, not a memory. Discrepancies surface in the first 2 minutes of class.

## Workshop design summary

One paragraph for the instructor brief: Week 4 ships a Northwind Control Tower in 3.5 hours, split into 10-min opening + 75-min Sprint 1 (Forecast, phases 1/2/4/5/6/7/8) + 10-min break + 60-min Sprint 2 (Optimize, phases 10/11/12 + scenario injection + re-run 8) + 40-min Sprint 3 (Monitor, phase 13 + drift injection + re-run 5/6) + 15-min close (phase 9 + public grader run). Students prompt Claude Code for every execution step; they never write code. Phase 7 red-team covers 3 of 4 AI Verify dimensions (Transparency, Robustness, Safety); Fairness is deferred to Week 7. Product grade (40%) is 5 endpoint contract checks graded by `scripts/grade_product.py` against real framework state (ExperimentTracker, ModelRegistry, solver output, DriftMonitor). Journal grade (60%) uses the 5-dimension rubric with worked 4/4 and 1/4 examples in `PLAYBOOK.md`. Every file students interact with is enumerated in `SCAFFOLD_MANIFEST.md`; placeholder files carry a `# TODO-STUDENT:` banner so they cannot be mistaken for real work.
