<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 13 — Drift × 3 Cadences

**Decision moment:** Three retrain rules — one per model — with cadence-specific signal/threshold/duration.
**Sprint:** 4 (MLOps)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_13_drift.md` + `POST /drift/retrain_rule` (× 3)

## Five dimensions

- **D1 Harm framing** — silent drift → AOI 78% recall floor returns; $4,200/board exposure rises.
- **D2 Metric → cost linkage** — retrain cost ($0.40/hr cloud) vs FN cost averted by detected drift.
- **D3 Trade-off honesty** — universal "weekly retrain" wastes compute AND misses fast drift.
- **D4 Constraint classification** — Q4 ramp + medical certification cycles are hard seasonal exclusions.
- **D5 Reversal condition** — false-positive retrain rate > 1/quarter → tighten threshold.

## What I decided

<Three rules: vision (weekly, PSI > 0.25, 7-day window, HITL first trigger), predmaint (daily, calibration_decay > 0.05, 1-day window), rl (per-deployment, safety_violations > 0, immediate halt).>

## Why

<Different data-generating processes → different cadences. Vision drifts on equipment + supplier; sensor drifts on temperature + calibration; RL changes per-deployment.>

## What I rejected

<Universal weekly retrain — wastes compute on stable models AND misses fast text/sensor drift.>

## Reversal condition

<False-positive retrain rate > 1/quarter on any model → tighten threshold.>

## Risks I am accepting

<Q4 seasonal exclusion may mask a real drift event during ramp.>
