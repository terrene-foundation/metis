<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 7 — Red-Team · Predictive Maintenance

**Decision moment:** Probe the predmaint classifier for failure modes before promoting to shadow.
**Sprint:** 2 (PredMaint)
**Time:** 18:30
**Artefact produced:** `journal/phase_7_predmaint.md`

## Five dimensions

- **D1 Harm framing** — failure modes that slip past Phase 6 cost $12K/incident × N missed/year. Common modes: machine-specific calibration drift, novel failure modes (e.g. servo amplifier failure not in training set).
- **D2 Metric → cost linkage** — robustness probes drive Phase 13 retrain rules. Each surfaced failure mode = a daily-cadence drift signal we know to monitor.
- **D3 Trade-off honesty** — perfect F1 on synthetic data is a confidence trap. The probe must distinguish "classifier is robust" from "synthetic features are too easy."
- **D4 Constraint classification** — Q4 ramp seasonal exclusion is HARD; mid-Q4 retrain mistakes the seasonality for drift.
- **D5 Reversal condition** — any probed failure mode that exceeds 5% prevalence on the live shadow window → freeze chosen family + retrain.

## What I probed

1. **Window-stability across seeds.** Re-ran `/predict/maintenance/train` at seeds 99, 42, 20260504 — LightGBM holds f1=1.000 across all three seeds at 7d window; LSTM/Survival vary (0.000–0.667). Confidence: chosen family is robust on 7d.
2. **Per-machine cohort skew.** No per-machine FN/FP imbalance on the 4 failing machines — all 4 caught at threshold 0.50.
3. **Bogus inputs.** `POST /predict/maintenance/score {machine_id:"smt_99"}` (unknown id) → 404. `POST /predict/maintenance/window {window_days:5}` (off-allowlist) → 422. Defenses hold.
4. **Adversarial scenario.** Q4 demand drift scenario (`/drift/check {model_id:"predmaint", window:"q4_demand_drift"}`) returns PSI ~0.96 vs recent_30d PSI ~0.74 — the drift signal is differentiable. Phase 13 retrain rule must include `Q4 ramp` as a seasonal exclusion or it will auto-trigger every Q4.
5. **Cold-start mode.** Novel failure mode (e.g. servo-amplifier short) is not in the 7-defect-mode training set — chosen family will route it to `monitor` with high confidence, masking the failure.

## What surfaced

LightGBM is robust across seeds at 7d window. Cold-start exposure on novel failure modes is the residual risk. Q4 seasonal drift is differentiable from real drift but Phase 13 must encode the exclusion. Bogus-input defenses hold at the API boundary.

## What I am promoting anyway

LightGBM/7d to shadow. The 6.7:1 asymmetry is satisfied at f1=1.000 on holdout; the cold-start risk is monitored at Phase 13 daily cadence.

## Reversal condition

Per-machine FN rate > 0.10 over 14-day shadow → freeze + retrain on a fresh seed. Q4 demand drift PSI > 0.50 → re-tune retrain threshold.

## Risks I am accepting

Cold-start exposure on novel failure modes (~$12K/missed-event); mitigation = drift monitor + new-mode label injection cadence. Synthetic-feature perfect separability may overstate live-data robustness; revisit at 14-day shadow checkpoint.
