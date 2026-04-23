<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# PSI — Population Stability Index

> **One-line hook:** A single number measuring how far a feature's current distribution has shifted from its training distribution — above 0.25 is severe.

## The gist

**PSI** (Population Stability Index) compares the distribution of a feature today against the distribution at training time. It asks: has the mix of values in this column changed significantly since we trained the model?

The calculation bins the feature into 10 buckets, computes the percentage of the population in each bucket at training time (baseline) and today, and sums a weighted log-ratio across buckets. The result is a single positive number:

- **PSI < 0.10**: No significant shift. Model is likely still valid for this feature.
- **0.10 ≤ PSI < 0.25**: Moderate shift. Worth monitoring; some model performance degradation is possible.
- **PSI ≥ 0.25**: Severe shift. The feature distribution has moved substantially from training. Investigate and likely retrain.

Example for Arcadia: if the `days_since_last_purchase` feature had a median of 14 days at training time, but a post-Black-Friday spike pushes the current median to 3 days, PSI will flag this as a severe shift. The model trained on normal shopping cadence is now receiving inputs from the holiday sprint — its predictions are unreliable.

PSI is most useful as an early warning signal before performance metrics degrade. You can observe PSI rising before the model's AUC or calibration visibly worsens — because it takes time for mispredictions to accumulate into statistically significant performance drops. PSI catches the leading indicator.

For Arcadia Phase 13: PSI is one of the signals in the churn classifier monitoring rule (alongside AUC decay and calibration drift). The `/drift/check` endpoint reports PSI per feature.

## Why it matters for ML orchestrators

PSI gives you a feature-level view of drift. When PSI is high for `days_since_last_purchase` but low for `total_spend_90d`, you know the cadence dimension of customer behaviour shifted but the spending dimension hasn't. That informs whether a full retrain is needed or whether targeted recalibration is sufficient.

## Common confusions

- **"PSI above 0.25 means I must retrain immediately"** — PSI is a warning signal, not a mandatory trigger. Confirm with performance metrics (AUC, Brier) before triggering retraining. The retrain decision is yours.
- **"PSI works for any feature type"** — PSI is designed for continuous and ordinal features that can be meaningfully binned. For low-cardinality categorical features (e.g., segment labels), different statistics apply.

## When you'll hit it

Used in: Phase 13 (Drift — churn classifier monitoring includes PSI on key features), workflow-06 (Sprint 4 MLOps boot, the `/drift/check` endpoint returns PSI)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Yurdakul, "Statistical Properties of Population Stability Index" — PSI methodology
- Klinkenberg, "Learning Drifting Concepts: Example Selection vs. Example Weighting" — drift detection alternatives
