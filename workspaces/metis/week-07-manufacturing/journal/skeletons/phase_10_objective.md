<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 10 — Objective Function

**Decision moment:** What does the inspector queue allocator optimise, and against what budget?
**Sprint:** 3 (Queue + RL composition)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_10_objective.md` + `POST /queue/solve`

## Five dimensions

- **D1 Harm framing** — wrong objective ships throughput at the cost of recall, dollars on the table.
- **D2 Metric → cost linkage** — objective = sum_t (FN catch value − FP cost) under inspector-min budget.
- **D3 Trade-off honesty** — inspector hours × $35/min vs FN value caught.
- **D4 Constraint classification** — inspector head-count is hard for tonight; tier mean-review-times are soft.
- **D5 Reversal condition** — net value < $0 / day for 7 days → re-tune tier weights.

## What I decided

<Objective: maximise net catch value. Budget: 6 inspectors × 8 hr × 60 min = 2,880 inspector-min/shift.>

## Why

<Reviewer cost ($35/min) vs FN cost ($4,200) drives the tier prioritisation table.>

## What I rejected

<Single tier-blind throughput maximisation — under-prices the critical tier.>

## Reversal condition

<Net value < $0/day for 7 days → re-tune tier_config.>

## Risks I am accepting

<Tier review-time means are estimates; real distribution has tail.>
