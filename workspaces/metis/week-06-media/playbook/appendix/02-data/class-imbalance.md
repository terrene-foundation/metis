<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Class Imbalance

> **One-line hook:** When the event you're predicting is rare, standard accuracy is meaningless — and your evaluation metric and threshold strategy must change.

## The gist

Class imbalance occurs when one class in your training data is much rarer than the other. In a churn dataset where 5% of customers churn per month, a model that always predicts "no churn" achieves 95% accuracy — and catches zero churners. That accuracy number looks impressive and is completely useless.

Churn and conversion are both rare-positive problems. Churn rates in retail are typically 3–8% per month. Conversion rates on targeted campaigns are often 8–15%. When your positive class is rare, you need evaluation metrics that are sensitive to performance on the rare class:

- **Precision** (of the customers you flagged, how many actually churned?) — relevant when false positives are expensive (you're spending $3 per touch on people who aren't really churning)
- **Recall** (of all the customers who actually churned, how many did you catch?) — relevant when false negatives are expensive (you lost a customer worth $120 CAC to reacquire)
- **PR curve** (precision vs recall across all possible thresholds) — the right tool for rare-positive problems; gives you a curve from which to pick the operating point that best fits your cost asymmetry
- **ROC-AUC** tells you how well the model ranks, but is relatively insensitive to class imbalance — a model can have high AUC but terrible performance on the positive class specifically

Imbalance also affects training: if 5% of your training data is positive, gradient descent will optimise heavily for the 95% negative class. Techniques like oversampling the positive class (SMOTE), undersampling the negative, or class-weighting compensate for this — Claude Code applies these in Sprint 2 when it trains the classifiers.

## Why it matters for ML orchestrators

Your Phase 6 evaluation decision — which metric to use, where to set the threshold — depends on whether your problem is balanced or imbalanced. For Arcadia's churn and conversion classifiers, the PR curve is the right instrument because both are rare-positive problems with asymmetric costs.

## Common confusions

- **"Accuracy is the natural metric"** — Only when classes are roughly balanced. For rare events, accuracy is a vanity metric that hides zero positive-class performance.
- **"The model with the highest AUC is the best model"** — AUC measures ranking quality; for rare positives, the model with the best precision-recall trade-off at your chosen operating point is more relevant.

## When you'll hit it

Used in: Phase 4 (Candidates — family selection for SML), Phase 6 (Metric + Threshold — SML variant uses PR curve), Phase 7 (Red-Team — per-subgroup performance check)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- He & Garcia, "Learning from Imbalanced Data" — survey of imbalance handling techniques
- Saito & Rehmsmeier, "The Precision-Recall Plot Is More Informative than the ROC Plot" — direct comparison for rare-positive settings
