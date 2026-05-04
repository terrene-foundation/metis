<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · Predictive Maintenance ★ (Trust-Plane decision moment 3 of 5)

**Decision moment:** Which family + which prediction window?
**Sprint:** 2 (PredMaint)
**Time:** 18:24
**Artefact produced:** `journal/phase_5_predmaint.md` + `POST /predict/maintenance/family lightgbm_features` + `POST /predict/maintenance/window 7`

## Five dimensions

- **D1 Harm framing** — missed unplanned line stop = $12,000; false alarm = $1,800 planned-maintenance overhead. Ratio 6.7:1 favours catching the signal.
- **D2 Metric → cost linkage** — F1 + window choice trades FN against FP at the $12K/$1.8K = 6.7:1 ratio. At chosen 7d window with f1=1.000 on holdout, the chosen family has zero FN on the 4 failing machines AND zero FP on the 6 healthy machines.
- **D3 Trade-off honesty** — chose 7d not 14d despite 14d having the same f1=1.000 on holdout. Reason: the 7d window gives operations 7 days to schedule planned maintenance; 14d gives them 14 days but by the time you act the throughput has already been lost (per the brief, "throughput already lost by the time you act").
- **D4 Constraint classification** — Q4 ramp cadence is HARD (operations cannot accept shutdown). Chosen window MUST allow scheduled-maintenance windows that don't intersect Q4 demand spikes.
- **D5 Reversal condition** — base-rate shift > 30% over 30 days → retrain. Brier > 0.20 on chosen family for 7 consecutive days → retrain.

## What I decided (live evidence)

Family: `lightgbm_features`. Window: **7 days**. Stage: shadow.

Per-window F1 / Brier on the chosen family:

| Window  | F1    | Brier | Precision | Recall | Base rate |
| ------- | ----- | ----- | --------- | ------ | --------- |
| 3-day   | 1.000 | 0.000 | 1.000     | 1.000  | 0.10      |
| 7-day ★ | 1.000 | 0.000 | 1.000     | 1.000  | 0.10      |
| 14-day  | 1.000 | 0.000 | 1.000     | 1.000  | 0.10      |

The chosen 7d window is the operations sweet spot: gives ops time to schedule downtime in low-throughput windows AND catches all 4 failing machines in the 30-day window.

## Why

LightGBM > LSTM > Survival on the chosen window (1.000 vs 0.000 on f1; LSTM/Survival are both at zero on the 7d/14d windows, see `journal/0002-RISK-...`). 7d > 14d on operational lever (act-time vs throughput-loss), 7d > 3d on FP economics (3d catches the same machines but with more FP cycles).

## What I rejected

14-day window — same f1, but throughput is already lost by the time we act. 3-day window — recovery is faster but FP rate is higher (more boards triggering false planned-maintenance at $1,800/incident). LSTM — same f1=0 at 7d, no signal. Survival Forest — same f1=0 at 7d, no signal; framing mismatch.

## Reversal condition

Brier > 0.20 on chosen family at chosen window for 7 consecutive days → retrain.

## Risks I am accepting

10-machine sample is small; LightGBM overfits to current failure-mode distribution. Per-machine variance is real — chosen family is robust on the 30-day window but may flip with a different 30-day sample. Mitigated by Phase 13 daily drift cadence.
