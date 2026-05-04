<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 10 — Objective (Inspector queue allocator LP)

**Sprint:** Sprint 3 · Process Optimization + Inspector Queue · Decide
**Playbook phase:** Phase 10 — Objective
**Trust-plane decision:** Frame the inspector-queue LP objective: maximise expected catch-value (FN avoidance) subject to inspector-minute budget (6 inspectors × 8 hour shift = 2,880 minutes). Defend the per-tier FN cost weights from `routes/queue.py::TIER_CONFIG` against `PRODUCT_BRIEF.md §2`: critical tier $4,200 (major-defect-shipped); major tier $1,800 (planned-stop scaffold proxy); minor tier $180 (minor-defect-shipped). Inspector cost $35/min × 60 = $2,100/hr per `INSPECTOR_HOURLY_DOLLAR`.
**Paste prompt:** `playbook/phase-10-objective.md` §1
**Evaluation checklist:** `playbook/phase-10-objective.md` §2
**Endpoints touched:** `GET /queue/state` to read tier catalogue + headcount + capacity; `POST /queue/solve` with chosen `queue_depth` and `inspector_minutes_available` to read the LP objective coefficients.
**Skeleton to copy:** `journal/skeletons/phase_10_objective.md` → `journal/phase_10_objective.md`
**Acceptance criterion:** `journal/phase_10_objective.md` exists ≥ 500 bytes, names the LP objective (maximise catch-value) and the tier-FN-cost weights, defends each weight in $ verbatim from `PRODUCT_BRIEF.md §2` ($4,200 / $1,800 / $180), inspector-minute budget arithmetic shown (6 × 8 × 60 = 2,880), $35/min cost cited.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — objective and tier weights documented
- [ ] Journal cites $4,200 / $1,800 / $180 / $35/min from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
