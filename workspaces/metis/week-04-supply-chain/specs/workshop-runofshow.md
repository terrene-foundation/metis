# Workshop Run-of-Show — Minute-by-Minute Script

This spec is the authority on the 210-minute instructor script for the Week 4 Supply Chain workshop. The schedule is derived from `approach.md` §"Rebudgeted schedule" — Opening 10 + Sprint 1 (Forecast) 75 + Break 10 + Sprint 2 (Optimize) 60 + Sprint 3 (Monitor) 40 + Close 15 = 210 min = 3.5 h.

Each block specifies: instructor actions, student actions, any scenario injections, checkpoints the instructor uses to detect the failure modes in `failure-points.md`, and common hiccups with their mitigations.

Clock format: `HH:MM` measured from workshop start (T+0). Adjust for wall-clock start time in the instructor's brief.

## 0. Pre-class (T−30 to T+0)

### Instructor actions

- Run `scripts/preflight.py` on the shared machine AND on a student machine sample.
- Project `SCAFFOLD_MANIFEST.md` on main screen.
- Confirm Viewer Pane (`:3000`) and Nexus API (`:8000/health`) are up.
- Stage `scripts/scenario_inject.py` with `--dry-run union-cap` and `--dry-run drift-week-78` to confirm both events load.
- Open `scripts/instructor_brief.md` for the announcement cues.

### Student actions

- Log in to workspace.
- Run `scripts/preflight.py` — green bar appears in Viewer Pane via `.preflight.json`.
- Open terminal + Viewer + `START_HERE.md`.

### Failure modes this block catches

- F4 (`[xgb]` missing) — preflight fails loudly with the remediation one-liner.
- F10 (FeatureStore ingest skipped) — `fs_preload.py` runs on Nexus startup; preflight probes `/health` which confirms `feature_store_populated: true`.

## 1. Opening block (00:00 – 00:10, 10 min)

### 00:00 — Kickoff

- **Instructor**: 60-second welcome + the Trust Plane / Execution Plane split. "If the question is _what_ or _how_, let Claude Code answer. If it's _which_ / _whether_ / _who wins_ / _is it good enough to ship_, that's yours."
- **Students**: read `SCAFFOLD_MANIFEST.md`.

### 00:03 — Opening prompt

- **Students**: paste the opening prompt from `START_HERE.md` §9 into Claude Code.
- **Claude Code**: verifies every file in `SCAFFOLD_MANIFEST.md` exists at the stated path with the stated state; flags any discrepancy; stops before `/analyze`.
- **Students**: read Claude Code's scaffold confirmation, flag any discrepancy on a volunteer student's machine.

### 00:08 — Transition to Sprint 1

- **Instructor**: announces the Sprint 1 goal — "by 01:25, ship `/forecast/*` endpoints with a defensible model + threshold + deployment gate."

### Checkpoint at 00:10

- ≥ 95% of students have scaffold confirmation on-screen.
- Viewer Pane preflight banner green for all.
- If > 3 students have red preflight, delay Sprint 1 start by 5 min.

## 2. Sprint 1 — Forecast (00:10 – 01:25, 75 min)

Seven phases (1, 2, 4, 5, 6, 7, 8) at ~10 min each average. Phase 3 is folded into Phase 2.

### 00:10 — Phase 1 (Frame, ~7 min)

- **Students**: type the Phase 1 prompt from `PLAYBOOK.md`; write `journal/phase_1_frame.md`.
- **Instructor**: walk the room for the first 5 min — flag any student writing "forecast demand" without the target-variable precision.
- **Hiccup**: student's framing is vague. Mitigation: instructor points them at `specs/business-costs.md` and says "name the ratio in dollars, not a ratio alone."

### 00:17 — Phase 2 (Data Audit + folded Feature Framing, ~10 min)

- **Students**: run the `DataExplorer` prompt; write `journal/phase_2_data_audit.md` with the 6-category audit AND feature classification.
- **Instructor**: circulate. Flag any student who accepts DataExplorer output verbatim without making a call.

### 00:27 — Phase 4 (Model Candidates, ~12 min of wall-clock, ~10 min of student work)

- **Instructor announcement (at 00:15, ahead of this phase)**: "When you hit Phase 4, use `search_n_trials=5, families=3, search_strategy='random'`. If AutoML exceeds 3 minutes wall-clock, kill it and pivot to the pre-baked leaderboard at `data/leaderboard_prebaked.json`."
- **Students**: run AutoML. Live run target ~90 s; write live results to `data/leaderboard.json`.
- **Viewer Pane**: Leaderboard panel populates as the run completes.
- **Hiccup**: student's machine is slow; AutoML running past 3 min. Mitigation: instructor says "kill the run, use the pre-bake — phases 5-8 still run on real artefacts." No rubric penalty; this is what the pre-bake exists for (F1 mitigation).

### 00:39 — Phase 5 (Model Implications, ~10 min)

- **Students**: compare live leaderboard against pre-baked; pick one model; write `journal/phase_5_model_selection.md` with the `ExperimentTracker` run ID cited.
- **Instructor announcement at 00:45**: live "challenge this entry" demo — grab a volunteer's Phase 1 journal entry, project it, ask "how would you score this on Harm framing?" Cohort scores it out loud. Demonstrates the rubric gap.
- **Hiccup**: student picks top of leaderboard without examining fold variance. Mitigation: instructor asks "what does the fold-to-fold variance tell you about robustness?" — pushes the student into the 4/4 reasoning.

### 00:49 — Phase 6 (Metric + Threshold, ~10 min)

- **Students**: cost-curve prompt; write `journal/phase_6_metric_threshold.md`.
- **Hiccup**: reversal condition = "if data changes" — 0/4. Mitigation: instructor projects the worked 4/4 example from `journal/_examples.md`.

### 00:59 — Phase 7 (Red-Team with AI Verify dimensions, ~10 min)

- **Students**: run the three-dimension red-team (Transparency / Robustness / Safety); note Fairness deferral. Write `journal/phase_7_red_team.md`.
- **Hiccup**: Safety dimension skipped as "abstract". Mitigation: instructor points at the $220 SLA cost — "what's the dollar cost of the worst 1% of predictions?"

### 01:09 — Phase 8 (Deployment Gate, ~8 min)

- **Students**: go/no-go memo; transition in `ModelRegistry` from `staging` → `shadow`. Write `journal/phase_8_gate.md`.
- **Hiccup**: illegal stage transition attempted. Mitigation: grader's helper error prints the transition table; no stack trace reaches the student.

### 01:17 — Sprint 1 buffer (~8 min)

- Catch-up time for students who fell behind by 3–5 min across phases.
- Instructor does a floor check: "how many of you have six journal entries?" Should be ≥ 80%.

### Checkpoint at 01:25

- ≥ 80% of students have `/forecast/*` endpoints live (contract grader's `train`, `compare`, `predict` pass).
- ≥ 80% have 6 journal entries.
- Leaderboard panel renders for ≥ 80%.
- Cohort-average journal rubric (estimated) ≥ 3.0 — informal sampling, not full grading yet.

## 3. Break (01:25 – 01:35, 10 min)

- **Students**: hydrate, stretch.
- **Instructor**: triage the 1–3 students who fell furthest behind in Sprint 1. Offer: "continue solo OR adopt the pre-baked leaderboard AND my worked Phase 5 example as your baseline, and we'll sprint on Phase 6-8 now."
- **Common hiccup**: a student's Viewer Pane stopped updating. Mitigation: `cat data/leaderboard.json` in terminal — textual fallback is a valid evaluation surface; journal either way (F5 mitigation).

## 4. Sprint 2 — Optimize (01:35 – 02:35, 60 min)

Phases 10, 11, 12 + scenario injection + re-run 11, 12 + re-run 8.

### 01:35 — Phase 10 (Objective Function, ~12 min)

- **Students**: single-objective + multi-objective prompt; write `journal/phase_10_objective.md`.
- **Hiccup**: carbon term dropped. Mitigation: "the deck emphasises ESG; drop it if you defend the drop — but don't silently skip it."

### 01:47 — Phase 11 (Constraint Classification, ~10 min, pre-injection)

- **Students**: classify every constraint; write `journal/phase_11_constraints.md`.

### 01:57 — Phase 12 (Solver Acceptance, ~10 min, pre-injection)

- **Students**: run `/optimize/solve`; write `journal/phase_12_solver.md`; SAVE `data/route_plan.json`.
- **Instructor reminder**: "Before the scenario fires at 02:05, make sure `route_plan.json` is written — the injection needs it to exist to snapshot."

### 02:05 — SCENARIO INJECTION: `union-cap`

- **Instructor**: runs `metis scenario fire union-cap` (see `scenario-injection.md` §2.1). Drops the three-line chat snippet in the class chat.
- **Students**: save prior plan as `route_plan_preunion.json`; re-run Phase 11 with the new constraint classification (overtime = hard); re-solve with `/optimize/solve` and `scenario_tag: "postunion"`; save as `route_plan_postunion.json`. Write `journal/phase_11_postunion.md` + `journal/phase_12_postunion.md`.
- **Hiccup**: student overwrites `route_plan.json` without the snapshot. Mitigation: instructor's `--undo` path restores from `preunion`; if `preunion` is also gone, the student regenerates from the seed run.
- **Hiccup**: student leaves overtime as soft, only raises penalty. Mitigation: instructor projects the rubric's D4 worked example — "this is a contractual hard constraint; a penalty of any size is a 1/4."

### 02:25 — Phase 8 re-run (Deployment Gate, ~10 min)

- **Students**: sign off on the post-union plan via another `staging → shadow` transition (or reject and document).
- **Hiccup**: infeasible post-injection. Mitigation: re-classify one other constraint as soft; document the trade-off in the journal.

### Checkpoint at 02:35

- ≥ 70% of students have both `_preunion` and `_postunion` route plans on disk (F6 state-hygiene).
- ≥ 70% have Phase 11-postunion + Phase 12-postunion journal entries.
- `/optimize/solve` contract assertion passing for ≥ 70%.

## 5. Sprint 3 — Monitor (02:35 – 03:15, 40 min)

Phase 13 + drift injection + re-run Phases 5 and 6 on post-drift data.

### 02:35 — Lead-in (~5 min)

- **Instructor**: quick 90-second context: "Drift is what separates a 'deployed demo' from a 'living product'. Today's injection is the week-78 event — a realistic distribution shift."

### 02:40 — SCENARIO INJECTION: `drift-week-78`

- **Instructor**: runs `metis scenario fire drift-week-78` (see `scenario-injection.md` §2.2). Drops the scenario chat snippet.
- **Students**: run `/drift/check` via the Phase 13 prompt; surface severity + per-feature statistical tests; write `journal/phase_13_retrain.md`.
- **Hiccup**: `set_reference_data` not called. Mitigation: `drift_wiring.py` auto-wires this. If it still fires, grader's actionable message tells the student exactly which call to make.
- **Hiccup**: "retrain when MAPE > 15%" (agent-reasoning violation). Mitigation: instructor demonstrates the reframing in a 60-s aside — "signals and thresholds for operator monitoring, human decides to retrain."

### 02:55 — Re-run Phase 5 and Phase 6 on post-drift data (~20 min)

- **Students**: re-interpret the leaderboard against the drifted holdout; write `journal/phase_5_postdrift.md` and `journal/phase_6_postdrift.md`. Does the chosen model still stand? Does the threshold need to shift?

### Checkpoint at 03:15

- ≥ 70% of students have `/drift/check` contract passing.
- ≥ 70% have Phase 13 journal entry with a signal + threshold + duration window (not "if data changes").
- Cohort-average journal rubric (informal) ≥ 3.0 across Sprint 3 entries.

## 6. Close (03:15 – 03:30, 15 min)

### 03:15 — Phase 9 Codify (~8 min)

- **Students**: run `/codify` prompt; write `journal/phase_9_codify.md` with 3 transferable + 2 domain-specific lessons; append `Week 4 delta` to `PLAYBOOK.md`.

### 03:20 — PUBLIC GRADER RUN

- **Instructor announcement**: "I'm running the grader now on the shared projector."
- **Instructor**: runs `scripts/grade_product.py --base-url http://<each_student>:8000` against each student's backend. Projects the colour-coded per-endpoint table live.
- **Students**: see their 40% product score in real time.
- **Hiccup**: endpoint failing 1/3 assertions. Mitigation: grader prints actionable fix; instructor decides whether to allow a 2-minute fix attempt (within Close block) or lock the score.

### 03:25 — Journal export (~5 min)

- **Students**: run `metis journal export --output journal.pdf`. Verify the PDF renders.
- **Hiccup**: `pandoc` missing. Mitigation: fallback to `journal.md` + `journal.html` is accepted; noted in preflight for future.

### 03:30 — Close

- **Instructor**: 30-second close. "By 03:30 you shipped a product and defended a page of decisions. Next week, new domain, same Playbook. See you then."

## 7. Timing contingencies

| Slip                                          | Recovery                                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Sprint 1 overruns by 5–10 min                 | Compress Sprint 2 buffer; drop Phase 8 re-run ceremony to 5 min instead of 10                     |
| Sprint 1 overruns by > 15 min                 | Collapse to "critique pre-bake only" path for the bottom half of the cohort; flag in wrap-up      |
| Scenario injection missed (instructor forgot) | Fire with 5-min apology; student budget still recovers because injections add state not remove it |
| Grader run blocked by one student's crash     | Skip that student; return at end of block; do not pause public projector                          |

## 8. Post-workshop

- **Instructor**: archives `grade_report.json` from each student.
- **Instructor**: reviews session-notes for Week 5 prep; the `Week 4 delta` section of each student's `PLAYBOOK.md` becomes Week 5 opening's "what we learned last week" segment.
- **Failure-mode audit**: which of F1–F10 actually fired? Update `failure-points.md` and `risk-assessment.md` with the observed probabilities for Week 5 planning.

## Open questions

- **Shared-screen grader run (03:20) privacy** — projecting per-student scores live is high-stakes and public. The analysis artefacts assume the cohort norms accept this ("no post-hoc regrade"); if the cohort norms differ, a private-per-student grader run is a compatible alternative that loses the collective-accountability signal.
- **Failure-mode feedback into next week** — `approach.md` mentions "Week 5 opens with 'what we learned'" but doesn't specify whether the instructor's post-workshop failure-mode audit feeds into a written artefact. Flag for future: add a `post-workshop-debrief.md` artefact to the codify phase.
