<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Silhouette Score

> **One-line hook:** A per-customer crispness measure for clustering — how much closer is each customer to their own cluster vs the nearest other cluster?

## The gist

The **silhouette score** measures how well each customer fits their assigned cluster. For one customer it asks: how far am I from my own cluster's center (cohesion) vs how far am I from the nearest other cluster's center (separation)? A customer who is tightly packed with their own cluster and far from others gets a score near +1. A customer right on the boundary between two clusters gets a score near 0. A customer who would fit better in another cluster gets a negative score.

The overall silhouette score is the average across all customers. Near +1 = tight, well-separated clusters. Near 0 = overlapping clusters. Negative = the clustering is worse than random for those customers.

For Arcadia: the scaffold baseline (K=3) reports a silhouette of ≈0.3422. That's the number you see when you hit `/segment/baseline` on startup. It's your inherited starting point, not your target — you may or may not beat it with a different K.

Silhouette is useful for **comparing K values**: if K=5 silhouette is 0.41 and K=3 silhouette is 0.34, K=5 has tighter clusters on this sample. But silhouette alone does not determine the right K — your operational ceiling and stability (bootstrap Jaccard) both constrain the choice.

One caution: silhouette measures crispness on the training sample. A high silhouette on one sample does not guarantee stability across different samples — that's what bootstrap Jaccard tests.

## Why it matters for ML orchestrators

You pre-register a silhouette floor in Phase 6 before seeing the leaderboard. If no K on the leaderboard clears the floor, you either revisit the floor (with explicit rationale) or go back to Phase 4 and try different algorithm families. The silhouette number is not a target to optimise — it's a minimum bar.

## Common confusions

- **"Higher silhouette always means better segmentation"** — Silhouette can be high for clusters that are statistically crisp but operationally meaningless (e.g., clusters split purely by spend-tier that map to the same marketing action). Always complement with actionability assessment.
- **"Silhouette of 0.3 is bad"** — In real-world behavioural data with many overlapping patterns, 0.3–0.5 is often the realistic range. Context matters more than absolute value.

## When you'll hit it

Used in: Phase 4 (Candidates — silhouette is reported per K on the leaderboard), Phase 6 (Metric + Threshold — USML three floors; pre-register separation floor), Phase 7 (Red-Team — stability re-runs also report silhouette)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Rousseeuw, "Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis" — original paper
- Kaufman & Rousseeuw, "Finding Groups in Data" — broader cluster validation context
