# Phase 13 — Drift / Retrain Rules (× 3 models)

**Sprint:** 4 · **Time:** **_:_** · **Artefact:** 3× `POST /drift/retrain_rule` + this entry

## Rule 1 — Segmentation (USML)

- **Primary signal:** segment-membership churn (% customers moving segments month-over-month)
- **Threshold:** **_% (grounded in historical variance: 95th percentile of weekly churn in training window = _**%)
- **Secondary signal:** per-segment size drift (PSI on segment_sizes)
- **Duration window:** \_\_\_ months of sustained drift
- **HITL on first trigger:** yes
- **Re-train cadence after first trigger:** \_\_\_

## Rule 2 — Churn classifier (SML)

- **Primary signal:** calibration error (Brier delta from baseline)
- **Threshold:** Brier delta > \_\_\_
- **Secondary signal:** AUC decay > \_\_\_ points
- **Duration window:** \_\_\_ consecutive weeks
- **HITL on first trigger:** yes

## Rule 3 — Campaign allocator (Opt)

- **Primary signal:** constraint-violation rate (% plans producing infeasibility)
- **Threshold:** > \_\_\_%
- **Secondary signal:** expected-revenue decay > \_\_\_% vs historical
- **Duration window:** \_\_\_ consecutive days
- **HITL on first trigger:** yes

## Seasonal exclusions

<Windows to exclude from the drift baseline. "Nov 25 – Jan 5 (Black Friday + Year-End), ~2 weeks around Chinese New Year.">

## Historical variance grounding (how I picked the thresholds)

<"Churn threshold = 12% because weekly membership churn in the training window has 95th percentile at 9.8%, so 12% is ~1.2σ above normal.">

## Reversal condition (D5)

<When would I re-calibrate the thresholds themselves? "If 3 months of ops feedback show false-positive retraining rate > 2× genuine drift rate, widen the threshold.">
