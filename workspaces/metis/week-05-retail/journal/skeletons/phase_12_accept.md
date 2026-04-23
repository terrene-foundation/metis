# Phase 12 — Solver Acceptance (first pass)

**Sprint:** 3 · **Time:** **_:_** · **Artefact:** `data/allocator_last_plan.json` + this entry

## Feasibility per hard constraint

- touch_budget: ✓ / ✗ (used **_/_**)
- inventory_availability: ✓ / ✗
- \_\_\_ : ✓ / ✗

## Optimality gap

- Solver status: \_\_\_ (optimal / feasible sub-optimal / infeasible)
- Gap: \_\_\_% (if reported)

## Pathologies

- **Concentration:** \_\_\_% on one segment (flag if > 60%)
- **Dead campaigns (0 allocation):** \_\_\_
- **Boundary solutions (100% of a variable):** \_\_\_

## Sensitivity analysis

- Perturb weight_revenue ± 5%: plan changes \_\_\_% of touches → stable / knife-edge
- Perturb touch_budget ± 10%: expected revenue changes $\_\_\_

## Decision

**Accept / Re-tune / Fall back / Redesign:** \_\_\_

## Reason (D3)

<Honest trade-off. "Accept — plan is concentrated at 62% on segment 2 but their campaign is Loyalty Upgrade which has highest $18 lift; sensitivity stable.">

## Prior-plan comparison

- Expected lift vs incumbent 2020 rulebook: $\_\_\_/month
- Actual gain from solver vs baseline: $\_\_\_/month
- Delta: \_\_\_

## Reversal (D5)

<What would reclassify as "redesign"? "If PDPA injection fires and removes segment 1 from reach, revisit.">
