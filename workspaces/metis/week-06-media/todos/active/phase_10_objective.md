<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 10 — Objective (Queue allocator LP)

**Sprint:** Sprint 3 · Fusion + Queue · Decide
**Playbook phase:** Phase 10 — Objective
**Trust-plane decision:** Set the LP objective weights for the reviewer-queue allocator: `minimise_sla_breach` and `minimise_reviewer_cost` must sum to 1.0. Defend the split in dollars (FN $320 vs reviewer-time $22/min, both quoted from `PRODUCT_BRIEF.md §2`).
**Paste prompt:** `playbook/phase-10-objective.md` §1
**Evaluation checklist:** `playbook/phase-10-objective.md` §2
**Endpoints touched:** `GET /queue/state` to read tier catalogue + headcount + capacity; `GET /queue/objective` for current weights; `POST /queue/objective` (route enforces sum-to-1 with 422).
**Skeleton to copy:** `journal/skeletons/phase_10_objective.md` → `journal/phase_10_objective.md`
**Acceptance criterion:** `journal/phase_10_objective.md` names the two weights, defends the ratio in $-of-FN-cost vs $-of-reviewer-cost (both verbatim from §2), `POST /queue/objective` returns 200 and `queue_objective.json` reflects the weights.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — weights POSTed
- [ ] Journal cites $320 / $22 from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
