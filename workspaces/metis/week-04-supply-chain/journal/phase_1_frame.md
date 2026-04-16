---
phase: 1
phase_name: Frame
sprint: 1
timestamp: 2026-04-17T09:30:00+08:00
---

## Harm framing
Northwind stockouts cost $40 per unit shortage vs $12 per overstock — a 3.3:1 ratio. Stockouts harm B2B customers (missed commitments); overstocks harm ops margin.

## Metric-cost linkage
MAPE over RMSE because peak-day errors dominate revenue, not outlier magnitude.

## Trade-off honesty
Choosing MAPE trades tail-risk visibility for consistent relative error measurement. I accept this.

## Constraint classification
Forecast horizon = 1 day (hard: optimizer needs tomorrow's plan).

## Reversal condition
I would change my mind if a single-day stockout could cost >$500 — then RMSE wins.
