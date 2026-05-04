<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# `/todos` Output — Week 7 Playbook

The 14-phase ML Decision Playbook unfolds here as ~21 active todos (Phase 14 is deferred). `/todos` creates one file per phase per sprint. The instructor clears the gate before `/implement` starts.

## File naming

```
todos/active/phase_1.md                    # Sprint 1 boot — shared framing across all sprints
todos/active/phase_2.md                    # Sprint 1 — shared data audit
todos/active/phase_3.md                    # Sprint 1 — shared feature framing
todos/active/phase_4_vision.md             # Sprint 1 — Vision QC candidates
todos/active/phase_5_vision.md             # Sprint 1 ★ Vision architecture pick
todos/active/phase_6_vision.md             # Sprint 1 ★ Vision per-class thresholds × 4
todos/active/phase_7_vision.md             # Sprint 1 — Vision red-team
todos/active/phase_8_vision.md             # Sprint 1 — Vision deployment gate
todos/active/phase_4_predmaint.md          # Sprint 2 — PredMaint candidates
todos/active/phase_5_predmaint.md          # Sprint 2 ★ PredMaint family + window
todos/active/phase_6_predmaint.md          # Sprint 2 — PredMaint threshold + held-out calibration
todos/active/phase_7_predmaint.md          # Sprint 2 — PredMaint red-team
todos/active/phase_8_predmaint.md          # Sprint 2 — PredMaint deployment gate
todos/active/phase_5_rl.md                 # Sprint 3 — RL policy pick
todos/active/phase_7_rl.md                 # Sprint 3 ★ RL reward function weights
todos/active/phase_10_objective.md         # Sprint 3 — Inspector queue LP objective
todos/active/phase_11_constraints.md       # Sprint 3 — Queue + agent constraints (first pass)
todos/active/phase_12_acceptance.md        # Sprint 3 — Queue + agent acceptance (first pass)
todos/active/phase_11_postwsh.md           # Sprint 3 ★ MOM/WSH re-classification (post-injection)
todos/active/phase_12_postwsh.md           # Sprint 3 ★ MOM/WSH acceptance + RL simulate re-run
todos/active/phase_13_drift.md             # Sprint 4 — 3 retrain rules at 3 cadences
todos/active/phase_99_close.md             # /redteam + /codify + /wrapup
```

## Per-todo template

```
# Phase N — <name>

**Sprint:** 1 (Vision/Transfer Learning) / 2 (PredMaint/Time-series) / 3 (RL+Queue) / 4 (Agent+MLOps)
**Trust-plane question:** <the single decision; ★ if Trust-Plane decision moment>
**Prompt template (from PLAYBOOK.md):** see §Phase N
**Evaluation checklist:** see §Phase N
**Endpoints touched:** see SCAFFOLD_MANIFEST.md
**Skeleton to copy:** journal/skeletons/phase_N_<sprint>.md
**Acceptance criterion:** journal/phase_N_<sprint>.md ≥ 500 bytes (auto-detection threshold)

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites dollar figures from PRODUCT_BRIEF.md §2 / specs/business-costs.md
- [ ] Moved to todos/completed/ on human approval
```

## Instructor gate

Before `/implement` begins, the instructor verifies:

1. All ~21 todos exist.
2. Each todo names its Trust-plane question (not paraphrased from the Playbook — in the student's own words).
3. The student can name which phases are REPLAYED for the four modules: Phase 4–8 run THREE times (Vision then PredMaint then RL via Phase 5/7 only), Phase 11–12 run TWICE (first-pass then post-WSH).
4. The five ★ Trust Plane decision moments from `PRODUCT_BRIEF.md §5` are represented: D-07 vision arch, D-09 vision thresholds, D-14 predmaint window, D-19 RL reward weights, D-23 agent autonomy + MOM hard-shadow.
5. The student can name the three drift cadences (vision-weekly / predmaint-daily / rl-per-deployment) and why each differs.
6. The student can name the WSH hard floor (0.40 on safety_critical_defect) AND the RL safety_penalty hard floor AND what the MOM mandate does to which endpoints.

Fails any of the above → `/todos` reruns. No Sprint 1 start until the gate passes.
