<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Calibration Decay

> **One-line hook:** The gradual divergence between a classifier's stated probability and actual real-world outcomes — critical to detect when probabilities feed a downstream optimizer.

## The gist

A newly trained classifier might be well-calibrated: when it outputs P(churn) = 0.30 for a group of customers, roughly 30% of them actually churn in the next 30 days. Over time, as customer behaviour shifts, the relationship can drift: the same P(churn) = 0.30 now corresponds to only 15% actual churn. The model's probability outputs are now systematically overconfident — it thinks customers are churning at twice the actual rate.

**Calibration decay** is this gradual divergence between stated probability and real-world rate. It's measured by:

- **Brier score drift**: comparing the current period's Brier score against the training-period baseline. A rising Brier score indicates worsening calibration.
- **Calibration plot shift**: the actual-vs-predicted diagonal from Phase 6 now curves away from the diagonal in the current data.

Why does calibration decay matter more than AUC decay for Arcadia? Because Sprint 3's LP allocator uses the churn and conversion probabilities directly in its objective: `expected_revenue = P(convert) × $18`. If P(convert) is miscalibrated — say, systematically inflated by 50% — the allocator targets a fantasy revenue figure and misallocates budget. AUC decay would show that the model's ranking deteriorated; calibration decay shows that even if the ranking is still okay, the probabilities the allocator uses are wrong.

For Arcadia Phase 13: the churn classifier monitoring rule includes weekly Brier score computation on a rolling held-out sample. The threshold and duration window for triggering recalibration (vs full retrain) are set in Phase 13 grounded in the Phase 6 Brier score baseline.

## Why it matters for ML orchestrators

Calibration decay is often invisible if you only monitor AUC. A model can maintain its ranking quality (AUC stable) while its probability outputs drift significantly. For any product where probabilities feed downstream decisions (as in Sprint 3), calibration monitoring is non-negotiable.

## Common confusions

- **"If AUC is stable, calibration is fine"** — AUC measures rank order; calibration measures probability accuracy. Both can degrade independently.
- **"Calibration decay requires full retraining"** — Often, Platt scaling or isotonic regression on recent data recalibrates without a full retrain. Recalibration is faster and cheaper; try it before committing to a full retrain.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — Brier score at training time is the baseline), Phase 13 (Drift — churn classifier monitoring rule; Brier drift triggers recalibration or retrain), workflow-06 (Sprint 4 MLOps boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Niculescu-Mizil & Caruana, "Predicting Good Probabilities with Supervised Learning" — calibration methods
- Guo et al., "On Calibration of Modern Neural Networks" — calibration measurement and recalibration
