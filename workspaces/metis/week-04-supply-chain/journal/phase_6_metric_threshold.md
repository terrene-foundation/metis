---
phase: 6
phase_name: Metric + Threshold
sprint: 1
timestamp: 2026-04-17T10:45:00+08:00
experiment_run_ids: [xgb_007]
---

## Harm framing
Threshold determines stock levels per depot-day.

## Metric-cost linkage
80th-percentile interval minimizes expected cost given 3.3:1 asymmetry.

## Trade-off honesty
Wider intervals protect against stockouts at the cost of ~20% higher carrying cost.

## Constraint classification
Interval bound (hard: solver needs a point estimate).

## Reversal condition
Change to 90th percentile if Q4 stockout cost spikes above $60/unit.
