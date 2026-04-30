<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Hard vs Soft Constraints

> **One-line hook:** Hard constraints cannot be violated under any circumstances; soft constraints can be violated at a dollar cost — and classifying which is which is a Trust Plane decision.

## The gist

Every LP (linear program) has constraints — rules the allocator's solution must respect. Your Phase 11 job is to classify each constraint as hard or soft.

**Hard constraints** make certain solutions infeasible. The LP solver will not return a plan that violates them, regardless of how much revenue it would generate. Examples for Arcadia:

- PDPA under-18 exclusion: no under-18 browsing records in any model feature or allocation
- Total budget cap: total spend ≤ monthly budget
- Inventory constraints: cannot recommend more units than are in stock

If the hard constraints cannot all be satisfied simultaneously, the LP returns "infeasible" — no plan is produced. That infeasibility is itself a signal (a Phase 12 pathology) that something upstream changed.

**Soft constraints** are preferences with a dollar penalty for violation. The solver may violate them if the revenue gain outweighs the penalty. Examples for Arcadia:

- Per-segment fatigue cap: "don't touch the same segment more than 3 times a month" — violating this costs $X per excess touch in customer fatigue and unsubscribe risk
- Diversity floor: "at least 30% of budget goes to non-top-3 segments" — violating this costs $Y in lost long-tail segment engagement

The penalty dollar value IS a Trust Plane decision. Setting fatigue-cap penalty at $5 vs $50 changes the LP's willingness to violate it significantly. Ground the penalty in the business consequence: if one excess touch costs $3 in unsubscribe risk (from `PRODUCT_BRIEF.md §2`), the penalty is $3 per touch.

Misclassifying a hard constraint as soft (e.g., treating PDPA as a $220 penalty rather than a hard exclusion) produces a plan that legally cannot be shipped. That's the PDPA injection failure mode. Misclassifying a soft constraint as hard over-tightens the LP and may cause infeasibility when a softer solution was perfectly acceptable.

## Why it matters for ML orchestrators

The hard/soft classification is entirely a business and legal judgment — the solver has no opinion. It will optimise against whatever objective and constraints you give it. The CMO's "this segment can't be touched more than twice" is soft (business preference). Legal's "no under-18 personal data in the model" is hard (regulatory requirement). Knowing the difference is what Phase 11 teaches.

## Common confusions

- **"Everything should be hard to be safe"** — Over-tightening with hard constraints produces infeasible plans. A plan with no solution is less useful than a plan that slightly violates a preference.
- **"Soft means optional"** — Soft means "violate at a cost." The cost must be grounded in real dollar consequences; zero-penalty soft constraints are effectively ignored by the solver.

## When you'll hit it

Used in: Phase 11 (Constraints — classify every constraint in the allocator), Phase 12 (Solver Acceptance — infeasibility signals a hard constraint problem), workflow-05 (Sprint 3 boot; PDPA injection is a hard-constraint reclassification event)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Williams, "Model Building in Mathematical Programming" — LP constraint design
- Hillier & Lieberman, "Introduction to Operations Research" ch. 3 — constraint classification in LP
