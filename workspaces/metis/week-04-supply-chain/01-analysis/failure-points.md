# Failure Points — Week 4 Supply Chain Workshop

**Workshop**: 3.5-hour Applied ML workshop for MBA students (zero-code).
**Ships**: tomorrow (2026-04-17, morning session).
**Reviewer**: `analyst` agent.
**Target audience**: 20-30 MBA students, terminal + Viewer Pane, prompting Claude Code.

This is the ranked list of the top 10 things most likely to break the workshop, scored by `Severity x Likelihood`. Severity is scored against the course promise ("by 3:30 pm every student ships a product and defends a page of decisions"); Likelihood reflects that we have never run Week 4 with this specific tool stack on this cohort.

## Ranking

| #   | Failure                                           | Sev | Like | Score |
| --- | ------------------------------------------------- | --- | ---- | ----- |
| F1  | AutoML wall-clock overrun kills Sprint 1          | 5   | 5    | 25    |
| F2  | Stub-200 rubric gaming collapses product grade    | 5   | 4    | 20    |
| F3  | Scaffold ambiguity -> Claude Code fabricates      | 4   | 5    | 20    |
| F4  | `[xgb]` extra missing on student machines         | 4   | 4    | 16    |
| F5  | Viewer Pane never receives data -> blind students | 4   | 4    | 16    |
| F6  | Scenario injection mid-sprint corrupts state      | 4   | 3    | 12    |
| F7  | Shallow journal entries all score <=2.5           | 3   | 4    | 12    |
| F8  | DriftMonitor reference-data step forgotten        | 4   | 3    | 12    |
| F9  | ModelRegistry stage transition illegal -> throw   | 3   | 4    | 12    |
| F10 | FeatureStore ingest skipped -> all training fails | 5   | 2    | 10    |

Each row below follows the template requested: trigger, symptom, blast radius, mitigation-before (what we do tonight / at scaffold time), mitigation-during (what instructor does live).

---

## F1 — AutoML wall-clock overrun kills Sprint 1 (Score 25)

**Trigger.** A student runs the Phase 4 prompt as written: `search_n_trials=30`, 5 model families, Bayesian, time-series CV. On a laptop the run takes 4-8 minutes wall-clock; on a weak machine with XGBoost compiling trees it can take 15+.

**Symptom.** Student sits watching a progress bar. Sprint 1 budget (50 min covering phases 1-9) dies the moment AutoML alone burns 10 min. Student arrives at Phase 5 (model implications) with no leaderboard to reason over.

**Blast radius.** ALL students hit this simultaneously because the prompt is identical. Sprint 1 slips by 15-30 min; Sprint 2 (already tight at 50 min for 4 phases) gets crushed; Sprint 3 (optimize + drift + journal) gets abandoned. The entire "you shipped a product" promise collapses in Hour 1.

**Mitigation-before** (tonight):

1. Adopt the pre-baked-leaderboard strategy (`approach.md` Issue 1, Option A+B hybrid): ship `data/leaderboard_prebaked.json` with 5 runs in a real ExperimentTracker database. Students run AutoML with `search_n_trials=5, families=3` (~90s) for the live-build muscle-memory moment, then pivot to critiquing the pre-baked 30-trial leaderboard.
2. Pin `search_n_trials` and family count in the scaffolded Phase 4 prompt; students cannot accidentally trigger a 30-trial run.
3. Workspace includes a `.env` containing `KAILASH_ML_AUTOML_QUICK=1` that caps trials at 5 if the env var is set, as a defense-in-depth.

**Mitigation-during**: instructor announces at 00:15 "if your AutoML run exceeds 3 min wall-clock, kill it and use the pre-baked leaderboard at `data/leaderboard_prebaked.json` — you will still run phases 5-9 against real artifacts."

---

## F2 — Stub-200 rubric gaming collapses product grade (Score 20)

**Trigger.** Current rubric awards 20% per endpoint for returning HTTP 200. A student (or Claude Code under pressure) returns `{"status": "ok"}` and passes. `zero-tolerance.md` Rule 2 forbids stubs but the rubric does not enforce it.

**Symptom.** Student finishes the workshop with 40% product grade against zero real ML work, and the journal score is uncorrelated to product quality. The "one-person unicorn" promise is visibly unearned; next week's instructor has to re-teach every concept.

**Blast radius.** Approximately 20-40% of students (the ones who fall behind in Sprint 1) will reach for stubs rather than ship nothing. Without contract assertions, they all succeed at rubric-gaming.

**Mitigation-before**: rewrite the rubric per `approach.md` Issue 2. Each endpoint MUST assert a non-trivial contract, graded by automated checker script (`scripts/grade_product.py`) that the student runs and that the instructor re-runs at close:

- `/forecast/train` -> response includes `experiment_run_id`; `ExperimentTracker.get_run(id)` returns params + metrics
- `/forecast/compare` -> returns >=3 rows with distinct `params_hash`
- `/forecast/predict` -> returns `model_version_id` matching a `ModelRegistry` entry at stage in {staging, shadow, production}
- `/optimize/solve` -> returns `feasibility: true`, `optimality_gap: <float>`, hard-constraint satisfaction table
- `/drift/check` -> returns >=1 statistical test name + p-value/statistic + severity in {none,low,moderate,severe}

Grader script imports each endpoint's payload and runs the assertions as pytest-style checks. Pre-built and included in scaffold. Student sees pass/fail per endpoint before journal export.

**Mitigation-during**: instructor runs `scripts/grade_product.py` publicly at 3:20 pm so students see live whether their product passed.

---

## F3 — Scaffold ambiguity -> Claude Code fabricates (Score 20)

**Trigger.** Opening prompt (Section 9 of `START_HERE.md`) asks Claude Code to "summarize what's scaffolded." No canonical manifest exists. Claude Code hallucinates one.

**Symptom.** Student believes Feature X is pre-built when it is not, or re-builds a component that already exists, or writes into a file that Claude Code invented. Every downstream prompt inherits that fabrication.

**Blast radius.** Universal — every student runs the opening prompt. A wrong scaffold summary wastes 10-20 min per student in Sprint 1 alone.

**Mitigation-before**: ship `SCAFFOLD_MANIFEST.md` (see `scaffold-manifest.md`) in the workspace root. Opening prompt changes to "read `@SCAFFOLD_MANIFEST.md` and confirm you see exactly these files — flag any discrepancy before we start." Claude Code cannot fabricate what is pinned.

**Mitigation-during**: instructor projects the manifest on the main screen for the first 2 min of the workshop.

---

## F4 — `[xgb]` extra missing on student machines (Score 16)

**Trigger.** Phase 4 prompt mentions `XGBoostRegressor` as a candidate. `kailash-ml[xgb]` is an optional extra. A student on a fresh install without `[xgb]` gets `ImportError` mid-AutoML.

**Symptom.** AutoML run dies halfway with a stack trace; student does not understand; Claude Code tries to "fix" by installing, which fails behind a corporate proxy.

**Blast radius.** ~20% of students (the ones who did not run the pre-class `pip install kailash-ml[full]`). Loses 10-20 min per affected student.

**Mitigation-before**:

1. Pre-class setup script `scripts/preflight.py` verifies `kailash-ml[xgb]` AND `[explain]` AND `ortools` AND `pulp` are present, fails loudly with remediation. Run at student login.
2. Phase 4 prompt (scaffolded in `PLAYBOOK.md`) states "use XGBoostRegressor if available, else GradientBoostingRegressor" so the AutoML config degrades gracefully.
3. `scripts/preflight.py` writes `.preflight.json` the Viewer reads; the dashboard header shows a red strip if preflight failed.

**Mitigation-during**: instructor has a one-liner ready: `pip install 'kailash-ml[full]' --upgrade` with a backup offline wheel folder for no-internet students.

---

## F5 — Viewer Pane never receives data -> blind students (Score 16)

**Trigger.** Viewer Pane (Next.js) polls `/api/workspace/state` for file changes. If the Nexus backend returns CORS errors, or the Viewer points at `:3001` while Nexus is on `:8000`, the Viewer loads but shows empty panels.

**Symptom.** Student stares at an empty dashboard. Every evaluation step ("is the leaderboard decision-ready?") is impossible because the leaderboard panel is blank.

**Blast radius.** Up to 50% of students if CORS or port binding is fragile. Average loss: 5-15 min of troubleshooting per student.

**Mitigation-before**:

1. Scaffolded Viewer reads from the filesystem (`workspaces/metis/week-04-supply-chain/data/*.json`) via a pre-built `VIEWER_STATE.md` contract — no cross-origin HTTP. Nexus writes JSON to disk; Viewer watches the directory.
2. `scripts/preflight.py` curls `http://localhost:3000` and `http://localhost:8000/health` at startup; fails loudly if either is down.
3. Include a `data/README.md` listing every JSON file the Viewer expects.

**Mitigation-during**: if Viewer is broken for >30s, instructor instructs student to `cat data/leaderboard.json` in the terminal — the text-mode read is a valid fallback evaluation surface. Students journal either way.

---

## F6 — Scenario injection mid-sprint corrupts state (Score 12)

**Trigger.** Instructor fires "driver union caps overtime at 5h/week" at Sprint 2 minute 25. Student must re-run Phase 11 and Phase 12. The current doc says "re-run 11 AND 12" but does not specify what artifacts to preserve vs. overwrite.

**Symptom.** Student overwrites `route_plan.json` losing the comparison baseline; or Claude Code creates `route_plan_v2.json` and the Viewer keeps showing v1; or ExperimentTracker runs from before and after the injection get mixed.

**Blast radius.** ~30% of students confuse themselves. The scenario-injection is meant to teach "I re-classified a soft constraint as hard and my plan changed in these ways" — if the before/after can't be compared, the lesson fails.

**Mitigation-before**:

1. `PLAYBOOK.md` Sprint 2 section specifies: after injection, save prior state as `route_plan_preunion.json`, new run as `route_plan_postunion.json`, journal entry MUST cite both.
2. ExperimentTracker runs are tagged with `scenario=preunion` or `scenario=postunion` — the grader script counts both buckets.
3. Viewer Pane has a "scenario" toggle pre-built: swaps between `_preunion` and `_postunion` JSON files.

**Mitigation-during**: instructor drops a 3-line prompt-template snippet in chat at injection time.

---

## F7 — Shallow journal entries all score <=2.5 (Score 12)

**Trigger.** Students under time pressure write one-sentence journal entries. The rubric awards 0 for "if data changed" reversal conditions, 2 for named signals, 4 for signal + threshold.

**Symptom.** Cohort-average journal score drops below 3.0 (passing threshold). The 60% grade layer fails en masse.

**Blast radius.** Systemic. This threatens the course's primary learning outcome: ML decision-making discipline.

**Mitigation-before**:

1. PLAYBOOK.md includes a worked 4-out-of-4 journal example per phase, anchored in the Northwind numbers ($40 stockout, $12 overstock, $220 SLA, $45 overtime).
2. Scaffold `workspaces/metis/week-04-supply-chain/journal/_rubric_examples.md` with 3 entries at 4/4 and 3 at 1/4, side by side. Students see the gap before they write.
3. The journal-add command auto-prompts the student with the rubric dimensions before accepting the entry.

**Mitigation-during**: instructor does a live "challenge this entry" example with a volunteer at minute 30 of Sprint 1.

---

## F8 — DriftMonitor reference-data step forgotten (Score 12)

**Trigger.** Kailash-ml `DriftMonitor` requires `await monitor.set_reference_data(model_id, reference_df)` before `check_drift` can be called. Phase 13 prompt does include this per red-team H7 fix, but a tired student at minute 180 drops it.

**Symptom.** `/drift/check` returns an error like "reference_data not set for model_id". Sprint 3's deliverable fails the grader.

**Blast radius.** ~20% of students; loss is Sprint 3 (the last 35 min).

**Mitigation-before**: the scaffolded `InferenceServer` auto-calls `set_reference_data` on first training completion (post-Phase 4). The drift check is then a pure `check_drift` call. Students cannot forget what the framework does for them. Code shim: `src/backend/drift_wiring.py` (scaffold, NOT a stub — actually calls `set_reference_data` when a training run completes).

**Mitigation-during**: grader script emits a specific error message "run `drift setup <model_id>` first" if reference data is missing, so the fix is obvious.

---

## F9 — ModelRegistry stage transition illegal -> throw (Score 12)

**Trigger.** Student in Phase 8 tries to promote `staging -> shadow`. That is legal. Student then tries `shadow -> staging` (rollback). That is also legal. Student then tries `production -> staging` — NOT legal (must go production -> shadow or production -> archived).

**Symptom.** Promotion throws; student panics; time bleeds.

**Blast radius.** ~15% of students. Loses 5-10 min.

**Mitigation-before**:

1. Transition table shipped in `PLAYBOOK.md` Phase 8 (already present in START_HERE §3.5 per C3 fix — verify it made it into PLAYBOOK too).
2. `scripts/grade_product.py` catches the illegal-transition exception and prints the transition table instead of the stack trace.

**Mitigation-during**: none needed beyond the helper error message.

---

## F10 — FeatureStore ingest skipped -> all training fails (Score 10)

**Trigger.** Phase 4 prompt per the C5 fix already starts with `fs.ingest(...)`. Severity is 5 because if ingest is skipped, every subsequent training call errors, but likelihood is low (2) because the scaffolded prompt is explicit.

**Symptom.** `TrainingPipeline.train` returns "schema not found in feature store." Cascade failure across Phases 4, 5, 6, 7, 8.

**Blast radius.** If it hits, it hits hard — kills Sprint 1. But unlikely to hit given the fix.

**Mitigation-before**: scaffold `src/backend/fs_preload.py` that ingests `data/northwind_demand.csv` on Nexus startup. Student's first Phase 4 prompt confirms ingest succeeded rather than triggering it. Downgrades likelihood to ~1.

**Mitigation-during**: grader script has a fast "is feature store populated?" check that runs first.

---

## Irreversible vs. Recoverable

Of the top 10, these are **recoverable within-session** (instructor can unblock in <5 min):

- F4 (preflight), F5 (Viewer), F8 (DriftMonitor), F9 (transition), F10 (ingest)

These are **irreversible within-session** (if they fire, the workshop is materially degraded):

- F1 (AutoML overrun — can't recover Sprint 1 time once lost)
- F2 (rubric gaming — grading is done; post-hoc regrading is politically ugly)
- F3 (scaffold fabrication — student worldview corrupted for the full session)
- F6 (state corruption — the re-solve lesson is destroyed; no second scenario injection scheduled)
- F7 (shallow journals — the primary learning outcome fails)

All irreversibles get `before`-mitigations with defense-in-depth. The three `Score >= 20` failures (F1, F2, F3) are all structural; they are the three that `approach.md` resolves.
