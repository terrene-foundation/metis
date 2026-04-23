<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# ROC-AUC

> **One-line hook:** A measure of how well a classifier ranks positives above negatives — useful for comparing models, but not the right metric for setting a threshold on rare-positive problems.

## The gist

The **ROC curve** (Receiver Operating Characteristic) plots the true positive rate (recall — fraction of actual churners caught) against the false positive rate (fraction of non-churners incorrectly flagged) across all possible classification thresholds.

**AUC** (Area Under the Curve) is a single number summary: 0.5 means the model is no better than random; 1.0 means perfect — every actual churner is ranked above every non-churner. In practice, a good tabular classification model lands in the 0.75–0.90 range.

AUC is useful for **comparing model families** in Phase 4: if the gradient-boosted model has AUC 0.87 and logistic regression has 0.79, the GBM is a better ranker. That's a meaningful comparison.

AUC is **not** the right metric for **setting the threshold** on churn or conversion — because it averages performance across all threshold values, including thresholds you'd never use. It's also relatively insensitive to class imbalance: a model can have high AUC while performing badly on the (small) positive class specifically.

For rare-positive problems like churn (5% of customers) and conversion (10–15%), the **PR curve** is more informative than the ROC curve for threshold selection. The PR curve shows what happens to precision and recall as you move the threshold — and the cost-asymmetry tells you where to land on that curve.

For Arcadia Sprint 2: report AUC for model comparison in Phase 4, but use the PR curve for threshold selection in Phase 6 SML.

## Why it matters for ML orchestrators

If Claude Code recommends a threshold using AUC, push back: "AUC compares models; PR curve sets the threshold. Please show me the PR curve and compute the expected cost at each operating point using the churn cost asymmetry ($120 vs $3)."

## Common confusions

- **"High AUC means the model is calibrated"** — AUC measures ranking quality. Calibration (are the probabilities honest?) is separate. A model can have AUC 0.88 and wildly miscalibrated probabilities. Sprint 2 Phase 6 checks calibration separately via the Brier score.
- **"AUC below 0.7 is bad"** — Depends on the problem. Rare events with noisy signals can produce AUCs of 0.65 that are still better than chance and operationally useful.

## When you'll hit it

Used in: Phase 4 (Candidates — SML leaderboard reports AUC for model comparison), Phase 6 (Metric + Threshold — SML uses PR curve, not ROC, for threshold selection), Phase 13 (Drift — AUC decay is one of the churn classifier drift signals)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Fawcett, "An Introduction to ROC Analysis" — foundational ROC tutorial
- Davis & Goadrich, "The Relationship Between Precision-Recall and ROC Curves" — when to use which
