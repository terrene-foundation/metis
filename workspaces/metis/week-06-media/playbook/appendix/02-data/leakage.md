<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Leakage

> **One-line hook:** When future information contaminates training data, producing a model that looks brilliant in testing and useless in production.

## The gist

Leakage is when the model learns from information it won't have at the moment of prediction. The training data contains a signal from after the horizon, the model bakes that signal in as a feature weight, and then in production — where that future signal doesn't yet exist — the model's performance collapses.

The classic shape: you are training a churn classifier to predict whether a customer will leave in the next 30 days. If you include "number of customer-service contacts in the last 30 days" as a feature, you are leaking: you computed that number looking forward from the training date, not from the prediction date. At prediction time, you don't know next month's service contacts. The model trained on this feature will score 0.94 AUC in testing (where the feature exists) and 0.57 AUC in production (where it doesn't).

Leakage can also be structural, not just temporal. If you split customers into train and test randomly but the same customer's sessions appear in both (because one customer can have 30 rows in a transactional dataset), the model learns that customer's pattern from training and "discovers" it again in the test set. This is group leakage. The fix is customer-level splitting, not row-level splitting.

For Arcadia: the scaffold's feature set is pre-selected, but any derived feature you add (e.g., "spend in the last 7 days of the dataset window") must be inspected for leakage at Phase 3.

One rule of thumb: if one feature has much higher importance than all others, and that feature is computed on a timeline that overlaps your prediction window, check for leakage first.

## Why it matters for ML orchestrators

Leakage produces fraudulent test results. You will show an AUC to the CX Lead, she will approve the classifier for production, and then the model will be wrong in production without anyone understanding why. The cost is both operational (wrong predictions) and political (trust breakdown between ML and the business).

## Common confusions

- **"High feature importance means it's a good feature"** — High importance on a leaking feature means the model found the shortcut through future information, not genuine signal.
- **"The model did well on holdout — no leakage"** — Only if the holdout was constructed without leakage. If the holdout split has the same structural problem as training (e.g., row-level split on a customer dataset), holdout performance is still inflated.

## When you'll hit it

Used in: Phase 2 (Data Audit — leakage check), Phase 3 (Feature Framing — availability and leakage axes), Phase 7 (Red-Team — feature-drop test as proxy for leakage check)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Kaufman et al., "Leakage in Data Mining: Formulation, Detection, and Avoidance" — foundational paper
- Géron, "Hands-On Machine Learning" ch. 2 — practical leakage detection in pipelines
