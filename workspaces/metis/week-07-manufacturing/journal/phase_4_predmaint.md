<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 4 — Candidate Models · Predictive Maintenance

**Decision moment:** Which 3 family candidates × 3 prediction windows are on the leaderboard for Sprint 2?
**Sprint:** 2 (PredMaint)
**Time:** 18:21
**Artefact produced:** `journal/phase_4_predmaint.md`

## Five dimensions

- **D1 Harm framing** — picking too few candidates risks under-exploration. The 6.7:1 unplanned-vs-planned cost ratio ($12K / $1.8K) sets the search bar.
- **D2 Metric → cost linkage** — each candidate scored on per-window F1 + Brier. F1 differential at the chosen window × 4 failing machines/30d × $12K-$1.8K averted = $/quarter at stake.
- **D3 Trade-off honesty** — what didn't make the leaderboard: GRU sequence model (data-hungry, 10 machines too few); XGBoost (effectively a duplicate of LightGBM at this scale); Cox proportional-hazards (continuous-survival shape, doesn't fit the binary-window task).
- **D4 Constraint classification** — Q4 ramp + medical certification cycles are HARD seasonal exclusions for retrain. Audit-trail retention 7 years is HARD.
- **D5 Reversal condition** — sample > 30 machines AND LSTM macro_f1 stabilises across seeds → re-evaluate.

## What I decided (live evidence from `/predict/maintenance/leaderboard`)

Three families × three prediction windows on the leaderboard:

| Family                | 3-day F1 / Brier | 7-day F1 / Brier | 14-day F1 / Brier |
| --------------------- | ---------------- | ---------------- | ----------------- |
| `lightgbm_features`   | 1.000 / 0.000    | 1.000 / 0.000    | 1.000 / 0.000     |
| `lstm_sequence`       | 0.667 / 0.061    | 0.000 / 0.057    | 0.000 / 0.054     |
| `survival_forest_tte` | 0.667 / 0.071    | 0.000 / 0.047    | 0.000 / 0.063     |

LightGBM cleanly wins across all three windows. LSTM-shaped and Survival-shaped surrogates have high seed variance at 10-machine scale (per `journal/0002-RISK-predmaint-strict-ordering-overstated.md`) — the defendable claim is "tabular ML on hand-engineered features wins at small data" not "LSTM > Survival".

## Why these three

LightGBM on hand-engineered features (mean / std / max / min / linear-trend per channel = 20 features) is the practical default at 10-machine scale; the inductive bias of gradient boosting on tabular features is matched to the data shape. LSTM is on the leaderboard because students need to see explicitly that sequence models lose at 10-machine scale (the canonical "data hungry" lesson). Survival Forest (time-to-event framing) is on the leaderboard as the third inductive bias — students see that the framing matters, not just the family.

## What I rejected

XGBoost — duplicate of LightGBM at this scale. Cox PH — continuous-survival shape; binary-window task fits gradient boosting cleaner.

## Reversal condition

Sample > 30 machines AND LSTM-shape stabilises (macro_f1 std < 0.10 across 5 seeds) → add to candidate set or replace Survival Forest.

## Risks I am accepting

3-candidate × 3-window leaderboard at 10-machine scale has variance noise on the simpler-classifier rows. LightGBM's perfect F1 on the synthetic dataset reflects the engineered features being separable; real-world features will be noisier.
