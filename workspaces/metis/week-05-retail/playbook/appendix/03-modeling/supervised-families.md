<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Supervised Families

> **One-line hook:** Four algorithm families for problems where you have labels — and why ensemble methods win on tabular data almost every time.

## The gist

Supervised learning means you have a **label** — the right answer for each training row. A churn dataset where each customer row has a "churned: yes/no" column is supervised. You train a model to predict that label for future customers.

Four families matter for tabular retail data:

**Linear** (logistic regression, linear regression): Fast, interpretable, always include as a baseline. It can only fit a straight-line decision boundary — if the relationship between features and outcome is non-linear, linear models underfit. But they are fast, explainable ("this weight on recency means X"), and often competitive on small datasets.

**Tree** (decision tree, random forest): A decision tree splits the data on feature values ("if recency < 30 AND spend > $100, predict churn"). Single trees overfit easily; random forests grow many trees on different subsets and average them. Much better at non-linear patterns than linear models, and moderately interpretable (feature importances tell you which features matter).

**Ensemble** (gradient-boosted trees — XGBoost, LightGBM, sklearn GBM): The default winner for tabular data. Builds trees sequentially, each correcting the previous one's errors. Handles missing values, non-linear interactions, and class imbalance gracefully. Not as interpretable as a single tree, but feature importances are available. The Phase 4 sweep always includes one gradient-boosted model.

**Neural networks**: Overkill for tabular data unless you have millions of rows, complex heterogeneous inputs (text + image + tabular), or very high-dimensional feature spaces. Too slow to train for a 3.5-hour workshop, and offers no interpretability benefit.

For Arcadia Sprint 2: the scaffold runs all three non-neural families (logistic regression + random forest + gradient-boosted). Your Phase 5 decision is which family wins — usually gradient-boosted, but check.

## Why it matters for ML orchestrators

Phase 4 produces a leaderboard of candidates; Phase 5 asks you to pick one. Understanding the families' trade-offs (linear = interpretable but limited; ensemble = accurate but opaque) is what makes that pick defensible rather than arbitrary.

## Common confusions

- **"Ensemble always wins, so I don't need to run the baseline"** — The baseline (logistic regression) exists to show you what you gain from the more complex model. If ensemble is only 2% better, the simpler model may be the better production choice given its interpretability.
- **"Feature importance from a GBM means the feature causes churn"** — Importance means the model used the feature heavily. Causation requires a different analysis.

## When you'll hit it

Used in: Phase 4 (Candidates — SML sweep), Phase 5 (Implications — pick the winning family), workflow-04 (Sprint 2 SML boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Chen & Guestrin, "XGBoost: A Scalable Tree Boosting System" — the canonical ensemble paper
- Hastie, Tibshirani & Friedman, "The Elements of Statistical Learning" ch. 10 — boosting theory
