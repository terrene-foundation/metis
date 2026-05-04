<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 10 — Objective Function · Inspector Queue Allocator

**Decision moment:** What does the inspector queue allocator optimise, and against what budget?
**Sprint:** 3 (Queue + RL composition)
**Time:** 18:42
**Artefact produced:** `journal/phase_10_objective.md` + `POST /queue/solve`

## Five dimensions

- **D1 Harm framing** — wrong objective ships throughput at the cost of recall. Per-tier FN cost: critical $4,200 / major $1,800 / minor $180.
- **D2 Metric → cost linkage** — objective = sum_t (FN catch value − FP cost) × x_t under inspector-min budget. Solver returns shadow price (LP dual) per inspector-minute = marginal $/min for adding capacity.
- **D3 Trade-off honesty** — inspector hours × $35/min vs FN value caught. The LP picks the optimal allocation; the policy choice is the tier weights, not the math.
- **D4 Constraint classification** — inspector head-count is HARD for tonight (6 inspectors × 8 hr × 60 min = 2,880 inspector-min/shift). Tier mean-review-times are SOFT (estimates).
- **D5 Reversal condition** — net value < $0 / day for 7 days → re-tune tier weights.

## What I decided (live evidence from `POST /queue/solve {}`)

| Field                                          | Value                  |
| ---------------------------------------------- | ---------------------- |
| Objective                                      | maximise net catch value |
| Inspector budget                               | 2,880 min/shift (6 × 8 × 60) |
| Tier weights (FN $/board)                      | critical $4,200 / major $1,800 / minor $180 |
| Tier mean review minutes                       | critical 6 / major 3 / minor 1.5 |
| Plan (boards/shift)                            | critical 120 / major 480 / minor 480 |
| Inspector minutes used                         | 2,880 / 2,880 (binding) |
| Expected catch value                           | $1,454,400 |
| Expected FP cost (10% FP rate at gate × $85)   | $9,180 |
| **Net value**                                  | **$1,445,220** |
| Shadow price per inspector-minute              | -$120 (LP dual; binding constraint) |
| Queue after shift                              | critical 0 / major 0 / minor 320 (residual) |

## Why

The LP allocates 2,880 inspector-minutes optimally: critical tier (120 boards × 6 min = 720 min) catches $4,200/board; major tier (480 boards × 3 min = 1,440 min) catches $1,800/board; minor tier (480 boards × 1.5 min = 720 min) catches $180/board. Total: 2,880 min, all spent. The shadow price -$120/min says each marginal inspector-minute would catch $120 more in averted FN cost — a 7th inspector at $35/min × 480 min = $16,800 cost would catch additional $57,600 → net +$40,800/shift.

## What I rejected

Single tier-blind throughput maximisation — under-prices the critical tier. Cost-balanced threshold per tier (mirroring vision Phase 6) — already encoded in the FN $/board weights; the LP picks the allocation, not a per-tier threshold.

## Reversal condition

Net value < $0/day for 7 days → re-tune tier_config (likely the FN $/board weights have shifted). Shadow price flips positive (queue is no longer the binding constraint) → reduce inspector head-count.

## Risks I am accepting

Tier review-time means are estimates with real-world tail (e.g. 95th percentile critical review = ~12 min, not 6). LP solution is brittle to per-tier mean shifts. Mitigation: re-solve daily; if shadow price drifts > 50%, re-tune.
