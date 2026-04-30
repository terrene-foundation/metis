<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Stability Protocols

> **One-line hook:** Checking whether your model's outputs hold up on new data — not just the specific sample it was trained on.

## The gist

A model can look excellent on one dataset by accident. Stability protocols test whether the structure the model found is repeatable — does it show up on different samples, different seeds, or different time windows?

For clustering (USML), the canonical stability test is **bootstrap Jaccard**:

1. Draw a new sample of customers (bootstrap sample — sampling with replacement)
2. Re-cluster with the same algorithm and K
3. For each pair of customers in both samples, check: were they in the same cluster both times? The fraction of pairs that stay together is the Jaccard index.
4. A Jaccard ≥ 0.80 across 10–20 bootstraps is the conventional "shippable" threshold for segmentation.

Why does this matter? Because a segmentation that assigns Segment A one month and then reshuffles 40% of customers to Segment B next month is operationally useless: marketing cannot build a "loyal high-value customers" campaign if "loyal high-value" is a different set of people every month.

For classification (SML), stability tests typically involve re-training with different random seeds or on different temporal windows and checking whether the top feature importances stay consistent. A classifier whose most important feature changes from "recency" to "average spend" between two random seeds is learning noise, not signal.

**Protocol for Arcadia Phase 7 red-team**: re-seed the K-means clustering 3 times with different random seeds, measure bootstrap Jaccard, and report the percentage of customers who change segments across seeds. This is the STABILITY section of the Phase 7 red-team.

## Why it matters for ML orchestrators

You pre-register a stability floor (e.g., Jaccard ≥ 0.80) in Phase 6 before seeing the leaderboard. The Phase 7 red-team measures actual stability and compares to your floor. If actual Jaccard is 0.74, that's below your floor — it's a Phase 8 deployment gate failure, not a reason to lower the floor.

## Common confusions

- **"Good silhouette = stable"** — Not necessarily. Silhouette measures separation quality on the specific sample; stability measures repeatability across samples. A high silhouette low-stability segmentation looks clean in training and reshuffles in production.
- **"Re-seeding is just for K-means"** — Any algorithm with stochastic initialisation (K-means, GMM, some versions of HDBSCAN) should be tested for seed sensitivity. Hierarchical clustering is deterministic given the same data.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — pre-register the stability floor), Phase 7 (Red-Team — run the stability protocol), Phase 8 (Deployment Gate — pass/fail against the floor)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Hennig, "Cluster-wise Assessment of Cluster Stability" — bootstrap Jaccard methodology
- Von Luxburg, "Clustering Stability: An Overview" — broader survey of stability approaches
