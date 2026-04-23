<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Naive Baselines

> **One-line hook:** The simplest possible model you compare every other model against — if you can't beat the baseline, don't ship the complex one.

## The gist

A **naive baseline** is the simplest approach that could plausibly solve your problem. Its job is to set a floor: any model you propose must beat it, or the complexity isn't earning its keep.

For **clustering (USML)**: the naive baseline is the existing rule-based segmentation — in Arcadia's case, the 5 hand-authored customer segments from the 2020 segmentation playbook. If your K-means clustering doesn't produce more distinct, stable, and actionable segments than the 2020 rule-book, you should recommend keeping the rule-book and saving the retraining cost.

For **classification (SML)**: the naive baseline is either a majority-class classifier (always predicts the most common class — achieves 95% accuracy on a 5% churn rate by always predicting "no churn") or a logistic regression with raw features and no feature engineering. Every more complex model must beat both.

For **recommender**: the naive baseline is the current rule-based recommender (Arcadia's existing system), which converts at 12% click-through. Any new recommender system must exceed 12% to justify the complexity, retraining cost, and new failure modes it introduces.

Baselines are not just pedagogical — they are the most honest form of cost-benefit analysis. If your gradient-boosted model improves AUC from 0.82 to 0.84 but costs $3,000/month more in compute and requires monthly retraining, is the gain worth it? The baseline comparison makes that trade-off concrete.

## Why it matters for ML orchestrators

Phase 5 (Implications) requires you to pick a winning candidate from the Phase 4 leaderboard. But "pick the winner" always means "pick the winner vs the baseline". If the baseline is competitive, the honest recommendation is: keep the baseline.

## Common confusions

- **"Baselines are just teaching exercises"** — In industry, baselines sometimes win. Rule-based systems are interpretable, fast, and don't require retraining. Complex models should earn their place.
- **"The highest AUC model wins"** — AUC vs the baseline must account for operational cost, interpretability, and retraining burden. A 2% AUC lift might not justify a monthly retraining pipeline.

## When you'll hit it

Used in: Phase 4 (Candidates — baseline included in every sweep), Phase 5 (Implications — compare winner to baseline), Phase 8 (Deployment Gate — ship only if winner beats baseline by a defensible margin)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Amershi et al., "Software Engineering for Machine Learning: A Case Study" — Microsoft study on baseline practice
- Sculley et al., "Hidden Technical Debt in Machine Learning Systems" — on the cost of skipping baselines
