# Phase 10 — Objective Function

**Sprint:** 3 (Optimization) · **Time:** **_:_**

## Mode chosen

Single-objective / Multi-objective: \_\_\_

## Terms and weights

| Term                 | Weight | Dollar interpretation                    |
| -------------------- | ------ | ---------------------------------------- |
| expected_revenue     | \_\_\_ | $18 per converted click / $14 per wasted |
| reach                | \_\_\_ | $\_\_\_/customer-touched                 |
| diversity / coverage | \_\_\_ | long-tail-protection proxy ($\_\_\_)     |
| _other_              | \_\_\_ | \_\_\_                                   |

Weights sum to **1.0**: \_\_\_ (yes/no — the LP requires this)

## Business justification for weights

<Why these numbers, grounded in PRODUCT_BRIEF.md §2 costs and Arcadia's current CTR baseline.>

## Shadow prices (marginal $ of relaxing each constraint by 1 unit)

- Touch budget: $\_\_\_
- PDPA under-18 (if hard): $\_\_\_
- Other: $\_\_\_

## What this framing sacrifices (D3)

<Honest trade-off. "Single-objective sacrifices Pareto visibility; multi costs the CMO a simpler story.">

## Reversal (D5)

<When would I switch framings? "If quarterly ESG review demands explicit diversity tracking, switch to multi-objective.">
