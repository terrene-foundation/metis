<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 8 — Deployment Gate · Predictive Maintenance

**Decision moment:** Is the predmaint classifier ready to promote from staging → shadow?
**Sprint:** 2 (PredMaint)
**Time:** 18:33
**Artefact produced:** `journal/phase_8_predmaint.md` + `POST /predict/maintenance/promote {family:"lightgbm_features", window_days:7, to_stage:"shadow"}`

## Gate checklist

| Criterion                                   | Floor  | Actual                 | Pass |
| ------------------------------------------- | ------ | ---------------------- | ---- |
| F1 on chosen (LightGBM, 7d)                 | ≥ 0.85 | 1.0000                 | ✓    |
| Brier on chosen (LightGBM, 7d)              | ≤ 0.20 | 0.0000                 | ✓    |
| Counterfactual lift vs reactive maintenance | > 0    | +100% catch on holdout | ✓    |
| Per-machine cohort F1 spread                | ≤ 0.10 | 0.00                   | ✓    |
| 7d window vs 14d (operational lever)        | yes    | yes                    | ✓    |
| Bogus-input gates (404 / 422)               | hold   | hold                   | ✓    |

## What I decided

Promoted `lightgbm_features` at window 7d from `staging` to `shadow` via `POST /predict/maintenance/promote`. Stage transition recorded; subsequent score calls return chosen family + window.

## Why

All gate criteria pass. F1=1.000 on the holdout is the result of synthetic-feature perfect separability; the honest defense is "robust on the 30-day window we have data for, with cold-start risk on novel modes monitored at Phase 13." 7-day shadow window will surface any per-machine variance the synthetic dataset masks.

## What I rejected

Promote to production directly — bypasses shadow validation. Rolling 14-day window for production — too slow to schedule maintenance.

## Reversal condition

Brier > 0.20 over 7 days OR FN rate > 0.10 over 14-day shadow → demote.

## Risks I am accepting

Cold-start cost on novel failure modes ($12K/incident); shadow period validates pre-production. Sensor stream may have gaps the synthetic dataset doesn't model.
