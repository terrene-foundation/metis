<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · Predictive Maintenance ★

**Decision moment:** Which family + which prediction window?
**Sprint:** 2 (PredMaint)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_5_predmaint.md` + `POST /predict/maintenance/{window,promote}`

## Five dimensions

- **D1 Harm framing** — missed unplanned line stop = $12,000; false alarm = $1,800 planned-maintenance overhead.
- **D2 Metric → cost linkage** — F1 + window choice trades FN against FP at the $12K/$1.8K = 6.7:1 ratio.
- **D3 Trade-off honesty** — shorter window catches less, longer window catches more but with more FP.
- **D4 Constraint classification** — Q4 ramp cadence is hard (operations cannot accept shutdown).
- **D5 Reversal condition** — base-rate shift > 30% over 30 days → retrain.

## What I decided

<Family: lightgbm_features. Window: 7 days. Threshold: <X>. Brier: <Y>.>

## Why

<7-day window is the operations sweet spot. LightGBM > LSTM > Survival Forest at 10-machine scale on hand-engineered features.>

## What I rejected

<14-day window — by the time we act, throughput already lost.>

## Reversal condition

<Brier > 0.20 on chosen family for 7 consecutive days → retrain.>

## Risks I am accepting

<10-machine sample is small; LightGBM overfits to current failure-mode distribution.>
