<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# `/todos` Output — Week 6 Playbook

The 14-phase ML Decision Playbook unfolds here as 13 active todos (Phase 14 is deferred to Week 7). `/todos` creates one file per phase. The instructor clears the gate before `/implement` starts.

## File naming

```
todos/active/phase_01_frame.md
todos/active/phase_02_data_audit.md
todos/active/phase_03_feature_framing.md           # unfolded in Week 6 (multi-modal feature surface is large)
todos/active/phase_04_candidates.md                # REPLAYED Vision (Sprint 1) → Text (Sprint 2)
todos/active/phase_05_implications.md
todos/active/phase_06_metric_threshold.md          # REPLACED for per-class (5 image + 5 text + 1 fusion)
todos/active/phase_07_red_team.md
todos/active/phase_08_gate.md
todos/active/phase_09_codify.md
todos/active/phase_10_objective.md                 # REPLACED for queue allocator (FN-cost / FP-cost / queue-time / GPU)
todos/active/phase_11_constraints.md
todos/active/phase_12_solver_acceptance.md         # REPLACED for queue allocator (SLA / reviewer load / IMDA)
todos/active/phase_13_drift.md                     # × 3 cadences (image weekly / text daily / fusion per-incident)
```

## Per-todo template

```
# Phase N — <name>

**Sprint:** 1 (Vision/CNN) / 2 (Text/Transformer) / 3 (Fusion/Multi-Modal) / 4 (MLOps)
**Trust-plane question:** <the single decision>
**Prompt template (from PLAYBOOK.md):** see §Phase N
**Evaluation checklist:** see §Phase N
**Journal artefact:** journal/phase_N_<name>.md

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites dollar figures from PRODUCT_BRIEF.md §2
- [ ] Moved to todos/completed/ on human approval
```

## Instructor gate

Before `/implement` begins, the instructor verifies:

1. All 13 todos exist.
2. Each todo names its Trust-plane question (not paraphrased from the Playbook — in the student's own words).
3. The student can name which 3 phases are REPLACED for deep-learning content (Phase 6 per-class thresholds × 11, Phase 10 queue-allocator objective, Phase 12 queue-allocator acceptance) and why.
4. The five Trust Plane decision moments from `PRODUCT_BRIEF.md` are represented.
5. The student can name the three drift cadences (image weekly / text daily / fusion per-incident) and why each differs.

Fails any of the above → `/todos` reruns. No Sprint 1 start until the gate passes.
