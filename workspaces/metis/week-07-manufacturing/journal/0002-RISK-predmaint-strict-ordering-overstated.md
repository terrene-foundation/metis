---
type: RISK
date: 2026-05-04
created_at: 2026-05-04T13:32:00+08:00
author: agent
session_id: 0b709081-dc57-4817-a9fe-8bae014f9294
project: metis-week-07-manufacturing
topic: PRODUCT_BRIEF claimed strict LightGBM > LSTM > Survival ordering that the data does not support
phase: redteam
tags: [pedagogy, predmaint, leaderboard, sample-size, risk]
---

# PRODUCT_BRIEF strict-ordering claim contradicted by 10-machine seed variance

## Context

Original PRODUCT*BRIEF.md §4.2 (Predictive Maintenance Classifier) committed to: *"Pedagogy: LightGBM > LSTM > Survival Forest at 10-machine scale on hand-engineered features."\_

`/redteam` R2 ran the smoke test against the modified backend at the canonical seed `20260504` and observed the actual leaderboard at the chosen 7-day window:

| Family                | macro_f1 | brier |
| --------------------- | -------- | ----- |
| `lightgbm_features`   | 1.000    | 0.000 |
| `lstm_sequence`       | 0.000    | 0.057 |
| `survival_forest_tte` | 0.000    | 0.047 |

LightGBM clearly wins. **But Survival's Brier (0.047) is _better_ than LSTM's (0.057)** — directly contradicting the brief's strict "LSTM > Survival" claim. By Brier, Survival is second. By F1, both tied at zero.

A retrain at seed=99 produced a different ranking: LightGBM=1.000, LSTM=0.667, Survival=0.667 — both tied, Brier-comparable.

## Risk

If a student defends "LSTM is structurally second-best because it's a sequence model" in their Phase 5 PredMaint journal, the rubric grader will look at the leaderboard and see the claim is **not supported by the data the student is looking at**. The student loses credit on D2 (metric → cost linkage) and D3 (trade-off honesty) for a claim the brief told them to make.

The root cause: at 10-machine sample size with the hand-engineered features, the simpler classifiers (RF surrogates with `n_estimators=20` and `n_estimators=8`) are noise-dominated. Their ranking depends on the seed.

## Mitigation

PRODUCT_BRIEF §4.2 amended with a "Pedagogical leaderboard" subsection explicitly naming the variance:

> LightGBM consistently wins at 10-machine scale on hand-engineered features. LSTM-shaped and Survival-Forest-shaped surrogates have high seed-variance at this sample size — depending on the run they may tie, invert, or both score zero. The defendable takeaway is that **tabular ML on hand-engineered features is the right tool for small-data time-series prediction**, not that LSTM is structurally second-best. Students who re-run `/predict/maintenance/train` with a new seed will see the LSTM/Survival ranking move; they should NOT defend a strict ordering between the two.

This converts the failure mode from "student writes a defendable-sounding claim that contradicts the data" into "student is told the variance is real and defends only the LightGBM win."

## Residual risk

Students who skip the amended brief paragraph and follow only Week 6's pattern (which DID have a strict 3-family ordering) may still write a strict-ordering claim. The Phase 5 PredMaint todo + the playbook phase-05-implications file should both reinforce this — currently only PRODUCT_BRIEF carries the variance note.

## What was NOT done

I did not re-tune the `n_estimators` / `max_depth` / `min_samples_leaf` parameters of the LSTM-shaped and Survival-shaped surrogates to produce a stable LSTM > Survival ordering, because:

- The pedagogical contract is "tabular wins at small data" not "sequence > survival at small data".
- Tuning to force a strict ordering would mask exactly the variance the brief now teaches.
- A re-tuned ordering at seed=20260504 would still flip at other seeds — the underlying issue (10 machines is too few to discriminate between two underfit classifiers) is structural, not a parameter choice.

## For Discussion

1. Counterfactual: had we generated 30 machines instead of 10 (still small but enough to discriminate), would LSTM and Survival rankings stabilise? Would the pedagogical lesson "tabular wins at small data" survive at 30-machine scale, or would it require dropping back to 5? The answer changes the recommended `n_machines` for next year's scaffold.

2. Specific data: at default seed `20260504`, predmaint Brier values are LSTM=0.057, Survival=0.047, LightGBM=0.000. The Brier delta between Survival and LSTM is 0.010 — within the noise floor of the synthetic-feature scaffold (per-feature noise is `rng.normal(0, 0.01)` in `synthesise_sensor_window_features`). Should the scaffold widen the per-feature noise so both surrogates land farther from each other and from LightGBM, increasing the discriminability and reducing the chance of a tied leaderboard?

3. The Phase 5 PredMaint rubric scores D3 (trade-off honesty) on whether the student names what was sacrificed. With LSTM and Survival both at f1=0, what trade-off is there to name? The student honestly has nothing to defend in choosing LightGBM. Does this devalue the Phase 5 deliverable for Sprint 2 specifically, and should the rubric weight Sprint 2 lower than Sprint 1 / 3 to compensate?
