# Risk Assessment — Week 4 Supply Chain Workshop

**Workshop**: 3.5-hour Applied ML workshop.
**Cohort**: 20-30 MBA students (non-coders).
**Ships**: tomorrow.
**Framing**: scenarios are expressed in **autonomous execution cycles** (one scaffolding cycle ~= 1 session of one autonomous coder-agent working in parallel), NOT human-days.

## Scenario 1 — Best case (probability ~15%)

**What happens.** Tonight's scaffolding sprint (1 cycle, ~4-6 hrs of agent time) delivers: locked `SCAFFOLD_MANIFEST.md`, pre-baked leaderboard, contract-grading script, Viewer Pane reading from filesystem JSON, preflight script, rubric examples, PLAYBOOK.md with all 13 phases. Every student logs in with preflight green. Sprint 1 runs within its 55-min budget because AutoML pivots to critique-the-pre-bake by minute 25. Sprint 2 and 3 finish on time. Grader script runs publicly at 3:20 pm.

**Outcomes.**

- ~85% of students pass the product grade (>=60% of 40%) because the contract grader fails fast with actionable errors and students fix forward.
- Cohort-average journal score ~3.3 because the rubric examples in scaffolding anchor the 4/4 target.
- Scenario injections (Sprint 2 union cap, Sprint 3 week-78 drift) land correctly; ~60% of students produce before/after journal entries.
- One "hero" student finishes Sprint 3 with 10 min to spare and goes deeper on drift-per-segment. That student becomes the exemplar for Week 5's opening.
- Zero students hit F1 (AutoML overrun) because it's architecturally prevented.

**What can still go wrong even in best case.** Instructor scenario injection timing slips by 5-10 min. One or two students with corporate-laptop lockdowns cannot install `[xgb]` and run the fallback path. That's acceptable noise.

**Signals we are on this path at minute 60**: >=80% of students have ExperimentTracker runs logged; Viewer Pane shows a leaderboard for >=80%; journal has >=2 entries per student averaging >=3.0.

## Scenario 2 — Modal case (probability ~60%)

**What happens.** Scaffolding sprint delivers core artifacts but two of {pre-baked leaderboard in real tracker DB, filesystem-watching Viewer, grader script} land in a partially-working state. Specifically: the Viewer filesystem watcher has a cache-lag issue (shows stale data for ~15s after a file write), and the grader script has a false-negative on `/optimize/solve` feasibility parsing. Rubric examples land but without the 1/4 counter-examples that make the gap visceral.

**Outcomes.**

- ~65% of students pass the product grade. The Viewer lag confuses ~8 students for ~5 min each; the instructor announces "refresh manually" at minute 45 and the issue is contained.
- Sprint 1 runs 5-10 min long; Sprint 2 gets compressed to 45 min; Sprint 3 gets compressed to 30 min. Phase 13's historical-variance grounding suffers — about half the students skip the `check_drift` result-grounding step and journal guesses instead of data-backed thresholds.
- Cohort-average journal score ~2.9-3.1. Borderline pass. The reversal-condition dimension is the weakest (most students write "if data changes" rather than a signal+threshold).
- Scenario injection hits ~40% of students correctly; the rest end up with overwritten state (F6 fires moderately) and no before/after comparison.
- AI Verify dimensions (Transparency/Robustness/Safety per Option A recommendation) get touched in Phase 7 red-team but only ~30% of students internalize the framework — they see the words but not the structure.
- 2-3 students (~10%) submit a stub-shaped product that passes the contract grader's loose checks and fails the spot-check.

**What this means for Week 5.** Week 5 opens with a 10-min "what we learned last week" that re-teaches the reversal-condition rubric and the scenario-injection state hygiene. Net course delivery is intact; the Playbook survives.

**Signals we are on this path at minute 60**: 50-80% of students have leaderboards; Viewer Pane works but laggy; journals average 2.5-3.0.

## Scenario 3 — Worst case (probability ~25%)

**What happens.** Scaffolding sprint collides with a SDK version mismatch — tonight's `kailash-ml` wheel on PyPI differs from the one the scaffold was authored against, and `AutoMLEngine(feature_store=..., model_registry=..., config=...)` kwargs fail validation on some students' machines. Preflight script catches it but the mitigation (downgrade) takes 15 min per affected student. Meanwhile the Viewer filesystem watcher fails on Windows (path separator bug) and ~6 students see an empty dashboard the whole workshop.

**Outcomes.**

- ~35% of students pass the product grade; the rest ship partial products (one or two endpoints failing the contract grader).
- Sprint 1 overruns by 20 min; Sprint 2 by 15 min; Sprint 3 effectively does not happen for the bottom half of the cohort. Phase 13 drift rule is journaled as "I would retrain when MAPE is high" — no thresholds, no data.
- Cohort-average journal score drops to ~2.4. Product grade average ~50%. Overall cohort-pass rate (>=60% overall) ~55%.
- Scenario injections fail because nobody has state to inject into.
- Rubric gaming fires for 4-6 students — they ship `{"status":"ok"}` endpoints and a one-line journal. The contract grader catches them but the instructor has to decide live whether to hard-fail or credit partial.
- The "one-person unicorn" narrative loses credibility with the cohort. Students who were going to drop the course accelerate their decision.

**What this means for Week 5-8.** Significant damage control. Instructor opens Week 5 with an explicit acknowledgment ("we asked too much of the environment; here's the reset") and a rebuilt rubric. Playbook shifts from 13 phases to 9 phases as a forced simplification. Risk: the MBA cohort learns "AI coding tools are fragile" — the exact anti-lesson the course was designed to prevent.

**Signals we are on this path at minute 60**: <50% of students have leaderboards; preflight errors still on-screen; >3 students have raised hands simultaneously.

## Irreversible failure modes

- **Cohort trust loss** (Scenario 3) — cannot be recovered mid-session; only via a honest reset next week. Mitigation is scaffold rigor.
- **Rubric gaming shipped at scale** — once students learn stubs pass, they teach each other for the rest of the course. Mitigation is the contract-grading script and public run at 3:20 pm.
- **Stub code in scaffold mistaken for real work** (`zero-tolerance.md` Rule 2) — if any scaffolded file looks like implementation but is actually `pass`, students will not re-implement it and the endpoint will fail at grade time. MUST be marked `# TODO-STUDENT:` with a banner comment that the file is a scaffold and the student's prompt to Claude Code must fill it.
- **Scenario-injection state corruption** (F6) — cannot be retried within session; instructor only has one union-cap moment. Mitigation is the pre-declared `_preunion` / `_postunion` file naming contract in PLAYBOOK.md.

## Recoverable failure modes (mid-session instructor actions)

- Individual preflight failures (F4) — one-liner install.
- Viewer lag (Scenario 2) — "refresh manually" announcement; fall back to `cat data/*.json`.
- Illegal ModelRegistry transition (F9) — helper error message with the transition table.
- Forgotten `set_reference_data` (F8) — auto-wired at training-complete; even if forgotten, grader script emits a specific fix instruction.
- Individual AutoML overrun (F1) — kill and pivot to pre-baked leaderboard.

## Confidence intervals

The 15/60/25 split assumes:

- Scaffolding is delivered in 1 autonomous cycle tonight with parallel agent specializations (backend-scaffold, frontend-scaffold, data-scaffold, grader-script, preflight, manifest).
- No SDK-version surprise beyond what preflight catches.
- Instructor is coached on the three announcements (00:15 AutoML pivot, 00:45 rubric challenge demo, 03:20 public grader run).

If the scaffold sprint misses `SCAFFOLD_MANIFEST.md` or the contract grader, shift Scenario 2 down by 15 points and Scenario 3 up by 15 points. If scaffold misses the pre-baked leaderboard, Scenario 1 drops to <5%.

The critical-path scaffold artifacts (in decreasing order of P1 risk if missing):

1. **Contract grader script** — no substitute. If missing, F2 (rubric gaming) fires universally.
2. **Pre-baked leaderboard** — no substitute. If missing, F1 fires universally.
3. **SCAFFOLD_MANIFEST.md** — no substitute. If missing, F3 fires universally.
4. **Preflight script** — partial substitute (instructor pre-class email). If missing, F4 fires for ~20%.
5. **Rubric examples in PLAYBOOK** — partial substitute (live walkthrough). If missing, F7 probability rises.
6. **Filesystem-watching Viewer** — partial substitute (cat-on-terminal). If missing, F5 consumes 5-10 min per student.
