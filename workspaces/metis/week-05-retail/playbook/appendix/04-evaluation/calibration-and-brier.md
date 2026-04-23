<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Calibration and Brier Score

> **One-line hook:** Whether the model's probability outputs are honest — if it says 30% churn risk, do 30% of those customers actually churn?

## The gist

A **well-calibrated** model produces probabilities that match real-world frequencies. If the model outputs a 30% churn probability for 1,000 customers, roughly 300 of them should actually churn. If only 100 churn (the model is overconfident) or 600 churn (the model is underconfident), the probabilities are miscalibrated.

Why does this matter? Because Sprint 3's campaign allocator uses the churn and conversion probabilities directly in its LP objective: `expected_revenue = P(convert) × $18`. If P(convert) is systematically inflated (the model says 40% but true rate is 15%), the allocator optimises against a fantasy and produces a plan that wastes budget.

The **calibration plot** (reliability diagram) visualises this: it bins predictions by probability range (0–10%, 10–20%, etc.) and plots the actual positive rate in each bin. A perfect calibration plot is a diagonal line from bottom-left to top-right. Curves above the diagonal mean underconfidence (the model is too modest about positive cases); curves below mean overconfidence.

The **Brier score** is the mean squared error of predicted probabilities. Lower is better. A perfectly calibrated model with AUC 0.87 might still have a poor Brier score if its probability outputs are systematically biased.

Recalibration via **Platt scaling** (logistic regression on the raw scores) or **isotonic regression** (non-parametric) can fix systematic miscalibration after training without retraining the underlying model.

For Arcadia Phase 6 SML: after picking the threshold from the PR curve, check calibration with the Brier score. If calibration is poor, recalibrate before handing off to Sprint 3.

## Why it matters for ML orchestrators

The allocator's LP objective is only as good as the probabilities it consumes. Miscalibrated probabilities produce a plan that is mathematically optimal against the wrong numbers. Checking calibration in Phase 6 catches this before Sprint 3.

## Common confusions

- **"Good AUC means good calibration"** — AUC measures ranking; calibration measures probability accuracy. A model can rank perfectly and be wildly miscalibrated.
- **"Calibration is a nice-to-have"** — Not when probabilities are consumed downstream by an LP solver. It's a hard requirement in the Arcadia cascade.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — SML variant: check Brier score after threshold selection), Phase 7 (Red-Team — per-subgroup calibration), Phase 13 (Drift — calibration decay is the churn classifier drift signal)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Guo et al., "On Calibration of Modern Neural Networks" — calibration analysis
- Platt, "Probabilistic Outputs for Support Vector Machines" — Platt scaling method
