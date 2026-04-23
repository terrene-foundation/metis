<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Confusion Matrix

> **One-line hook:** A 2×2 table showing exactly how many times your classifier was right and wrong in each direction — at a specific threshold.

## The gist

The **confusion matrix** shows four counts at a chosen classification threshold:

|                      | Predicted: Positive | Predicted: Negative |
| -------------------- | ------------------- | ------------------- |
| **Actual: Positive** | TP (True Positive)  | FN (False Negative) |
| **Actual: Negative** | FP (False Positive) | TN (True Negative)  |

For churn: TP = caught a real churner; FN = missed a real churner (they left); FP = flagged a non-churner (wasted touch); TN = correctly left a loyal customer alone.

From the confusion matrix you derive:

- **Precision** = TP / (TP + FP) — of everyone you flagged, what fraction was right?
- **Recall** = TP / (TP + FN) — of everyone who actually churned, what fraction did you catch?
- **Accuracy** = (TP + TN) / total — misleading for rare positives; avoid as primary metric.

The confusion matrix is threshold-specific: change the threshold and all four cells change. The PR curve is what you get when you compute a confusion matrix at every possible threshold.

For Arcadia: you pick a threshold in Phase 6 SML, and Claude Code reports the confusion matrix at that threshold. You translate it into dollars: FN × $120 CAC + FP × $3 touch cost = total cost of errors per period. That's the Phase 6 cost linkage (D2) the rubric scores.

## Why it matters for ML orchestrators

The confusion matrix is the translation layer between "model performance" and "business impact". Don't let Claude Code report only AUC or accuracy — ask for the confusion matrix at your chosen threshold and compute the dollar cost of errors.

## Common confusions

- **"Accuracy is the right summary statistic"** — Only for balanced classes. For 5% churn rate, a model that always predicts "no churn" has 95% accuracy and zero TP. The confusion matrix exposes this; accuracy hides it.
- **"FP is just as bad as FN"** — Not always. The cost asymmetry determines which is worse in your specific context.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — ask for the confusion matrix at your chosen threshold and compute dollar cost), Phase 7 (Red-Team — per-subgroup confusion matrices for bias detection)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Powers, "Evaluation: From Precision, Recall and F-Factor to ROC, Informedness, Markedness and Correlation" — comprehensive confusion matrix metrics
- Provost & Fawcett, "Data Science for Business" ch. 7 — business-context confusion matrix use
