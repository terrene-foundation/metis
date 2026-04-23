<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Shadow Prices

> **One-line hook:** The dollar cost of tightening a constraint by one unit — the LP's way of making regulatory and business constraints legible to stakeholders.

## The gist

When the LP solver finds an optimal plan, it also computes a **shadow price** (also called dual value or marginal value) for each binding constraint. The shadow price answers: if I relaxed this constraint by one unit, how much more revenue could the allocator generate?

Example for Arcadia: the budget cap is $50,000/month. The LP allocates all $50,000 and returns an expected revenue of $180,000. The shadow price of the budget constraint might be $3.60 — meaning if the budget were $50,001 instead of $50,000, the allocator could generate $180,003.60. Extrapolating (carefully): each additional $1,000 of budget generates approximately $3,600 in expected revenue. That's a number the CMO can act on.

For the PDPA constraint: the shadow price of the under-18 exclusion tells you how much expected revenue the allocator forgets by not using under-18 browsing data. If the shadow price is $50,000/month, that's the business cost of PDPA compliance — and the CMO needs that number to understand the trade-off between legal compliance and revenue. This doesn't mean you violate PDPA (it's a hard constraint — infeasible by design); it means you can tell the CMO exactly what compliance costs in revenue terms.

Constraints with zero shadow price are **non-binding**: the LP didn't hit them. A zero-shadow-price constraint means you could tighten it further at no cost — or that it was unnecessarily loose.

Constraints with high shadow prices are **tight** and should be reviewed: are they correctly specified? Is the high cost of the constraint intentional (regulatory) or accidental (overly conservative business rule)?

Shadow prices are reported by the allocator at Phase 12 after the solve. They are a key element of your Phase 12 journal entry and your conversation with the CMO and E-com Ops Lead.

## Why it matters for ML orchestrators

Shadow prices convert "the model respects this constraint" into "this constraint costs the business $X/month." That translation is what makes compliance decisions legible to non-technical stakeholders. The CMO can decide whether to lobby for a higher budget based on the budget shadow price; Legal can quantify the revenue cost of PDPA compliance.

## Common confusions

- **"Shadow price = the penalty for violating the constraint"** — No. Shadow price is the gain from relaxing the constraint, not the cost of violation. Violation cost is the penalty you set in Phase 11 for soft constraints. Hard constraints have no violation — they're infeasible if violated.
- **"Shadow price extrapolates linearly forever"** — Shadow prices are marginal values: they hold exactly at the margin and approximately in a local range. A budget increase of $1,000 at a shadow price of $3.60 gives ≈ $3,600 more revenue. A budget increase of $500,000 will not give $1.8M more revenue — the LP will hit other binding constraints.

## When you'll hit it

Used in: Phase 10 (Objective — shadow prices inform whether the objective weights are reasonable), Phase 11 (Constraints — PDPA shadow price is the dollar cost of compliance), Phase 12 (Solver Acceptance — report shadow prices as part of plan validation), workflow-05 (Sprint 3 boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Hillier & Lieberman, "Introduction to Operations Research" ch. 6 — sensitivity analysis and shadow prices
- Williams, "Model Building in Mathematical Programming" — interpreting dual values in business context
