# Phase 10 — Objective Function (queue allocator LP)

**Sprint:** 3 · **Time:** **_:_** · **Artefact:** `journal/phase_10_objective.md`

## Decision variables

- `x[tier, queue]` = number of posts of each (tier, queue) pair
- Tiers: auto-allow / low-confidence-allow / mid-confidence-review / high-confidence-review / auto-remove
- Queues: expedited (60s SLA) / standard (90min SLA) / bulk (24hr SLA)

## Objective formula

minimise: sum over (tier, queue) [
expected_FN_at(tier) × $320 // FN cost (PRODUCT_BRIEF.md §2)

- expected_FP_at(tier) × $15 // FP cost (PRODUCT_BRIEF.md §2)
- expected_reviewer_minutes_at(queue) × $22 // reviewer cost
- expected_GPU_inferences × $0.03/1000 // inference cost
  ]

## Per-term defense (D2)

- **FN term** ($320): \_\_\_
- **FP term** ($15): \_\_\_
- **Reviewer-minute term** ($22): \_\_\_
- **GPU inference term** ($0.03/1k): \_\_\_

## Trade-off discussion (D3)

<Pure FN-minimisation drives everything to expedited queue → reviewer cost explodes. Pure cost-minimisation under-staffs queues → FN escapes regulator. The objective balances; Phase 11 hard constraints make IMDA non-negotiable.>

## Endpoint call

- POST /queue/objective with the formula above

## Reversal condition (D5)

<When would I re-tune objective weights? "If reviewer headcount drops by 30% for 30+ days, reduce reviewer-minute weight from $22 to reflect overtime cost.">
