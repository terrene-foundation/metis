<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# PDPA Basics

> **One-line hook:** Singapore's Personal Data Protection Act — the legal constraint that makes under-18 browsing history a hard exclusion in the Arcadia allocator.

## The gist

The **Personal Data Protection Act (PDPA)** is Singapore's primary data privacy law, governing how organisations collect, use, and disclose personal data. For Arcadia Retail, one provision is directly load-bearing in Sprint 3:

**Section 13 (Purpose Limitation)**: Personal data collected for one purpose cannot be used for a materially different purpose without fresh consent. Under-18 customers' browsing history may have been collected for "improving the shopping experience" (a service purpose) but using it to personalise marketing campaigns (a commercial targeting purpose) is arguably a different purpose — and for minors, the bar is higher because they cannot give meaningful consent.

This is the PDPA injection that fires at ~4:30 in the workshop: Legal classifies the use of under-18 browsing history in the campaign allocator as a **Section 13 hard exclusion** with a **$220 per-record exposure** (from `PRODUCT_BRIEF.md §2`). "Hard exclusion" means: no under-18 browsing history in any feature vector, any model, or any allocator constraint — period. Not "reduce its weight". Not "cap the segment size". Exclude it entirely.

The correct response to the PDPA injection is:

1. Re-classify the under-18 browsing feature as a **hard constraint** in `journal/phase_11_postpdpa.md`.
2. Re-run the LP allocator with the new hard exclusion to produce a new `data/allocator_last_plan.json` — the Phase 12 re-solve.
3. Report the **shadow price** of the PDPA constraint in dollars — this is the cost of compliance made visible to the CMO.

The most common rubric failure: writing the Phase 11 re-classification but not re-running the LP (Phase 12). The journal says "PDPA is now a hard constraint" but the allocator plan still uses under-18 browsing data. The plan and the journal are inconsistent.

## Why it matters for ML orchestrators

PDPA violations are not "accept the risk and move on." The $220 per-record exposure is a real regulatory penalty, and shipping a plan that violates it is not a trade-off decision — it's a legal failure. Phase 11 is where you classify it; Phase 12 is where you prove the allocation respects the classification.

## Common confusions

- **"PDPA is a soft constraint with a penalty"** — Under the specific injection scenario in Week 5, Legal explicitly classifies it as a hard constraint. Hard means infeasible plans that violate it are rejected; it does not mean "penalise violations by $220 and solve".
- **"The shadow price is just a theoretical number"** — The shadow price of the PDPA constraint quantifies the cost of compliance: how much expected revenue does the allocator forgo by excluding under-18 data? That's a number the CMO needs to understand the business impact of the legal constraint.

## When you'll hit it

Used in: Phase 11 (Constraints — PDPA injection re-classification), Phase 12 (Solver Acceptance — PDPA re-solve; `data/allocator_last_plan.json` must change), workflow-05 (Sprint 3 boot pre-announces the injection)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Singapore PDPA 2012 (as amended 2021) — primary legislation
- PDPC Advisory Guidelines on the PDPA for Selected Topics — practical interpretation
