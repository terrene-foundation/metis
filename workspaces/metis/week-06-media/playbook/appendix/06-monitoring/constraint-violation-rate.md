<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Constraint Violation Rate

> **One-line hook:** The fraction of allocator runs that produce infeasible plans or require ops overrides — the primary drift signal for the LP campaign allocator.

## The gist

Supervised models drift when their predictions become wrong. Optimization models (like Arcadia's LP allocator) drift differently: they drift when the problem they are solving no longer matches reality — when the constraints become infeasible, or when the solved plan is technically feasible but operationally overridden by the ops team.

Two signals form the **constraint violation rate** for the allocator:

**Infeasibility rate**: The fraction of allocator runs that return no feasible solution. Infeasibility means the hard constraints (PDPA exclusions, budget cap, inventory limits) cannot all be satisfied simultaneously. This can happen when the customer population eligible under PDPA constraints shrinks (e.g., more under-18 accounts added), when budget is cut mid-month, or when inventory constraints tighten. A rising infeasibility rate signals that the constraint set needs review.

**Ops override rate**: The fraction of allocator plans that the E-com Ops Lead overrides manually before execution. Overrides are a leading indicator: if ops regularly overrides the plan, either the objective is wrong (not capturing what ops actually optimises for), the constraints are wrong (missing a real-world constraint that ops knows about), or upstream data is drifting (segments have shifted, probabilities are stale). High override rate is a Phase 10/11 signal, not just a Phase 13 signal.

Monitoring cadence for the allocator is **daily** — allocator plans run daily (or weekly for campaigns), so the violation rate can accumulate quickly.

For Arcadia Phase 13: the `/drift/check` endpoint returns infeasibility and override counts for the specified window. Your retrain rule should specify: at what infeasibility rate over what window you trigger a Phase 10/11/12 re-run vs a Phase 8 rollback.

## Why it matters for ML orchestrators

The allocator is the business's decision engine. If it is producing infeasible plans or plans that ops systematically rejects, the campaign allocation is broken — but it may not look broken from the outside because ops is compensating manually. The constraint violation rate makes the operational failure visible.

## Common confusions

- **"Infeasible plan means the software is broken"** — Usually not. Infeasibility means the constraint set is too tight for the available population and budget. The fix is often a constraint relaxation decision (Phase 11), not a code fix.
- **"Ops overrides are just ops being difficult"** — Systematic overrides usually signal a model or constraint problem that ops has learned to compensate for. Each override is a data point; a pattern of overrides is a product problem.

## When you'll hit it

Used in: Phase 12 (Solver Acceptance — you check for pathologies including incipient feasibility issues), Phase 13 (Drift — allocator retrain rule uses constraint violation rate), workflow-06 (Sprint 4 MLOps boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Kleppmann, "Designing Data-Intensive Applications" ch. 12 — on monitoring derived data systems
- Sculley et al., "Machine Learning: The High-Interest Credit Card of Technical Debt" — on feedback loops in production ML
