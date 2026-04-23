<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Bootstrap Jaccard

> **One-line hook:** A stability measure for clustering — do the same customers stay together when you re-cluster on a different random sample?

## The gist

Silhouette tells you how crisp the clusters are on one sample. Bootstrap Jaccard tells you whether those clusters are stable across different samples — which is the thing that actually matters for a marketing team building quarterly campaigns.

The protocol:

1. Draw 10–20 bootstrap samples from your data (each sample is the same size as your original, drawn with replacement — some customers appear twice, some not at all).
2. Re-cluster each bootstrap sample with the same algorithm and the same K.
3. For each pair of customers who both appear in a bootstrap sample: did they land in the same cluster in the bootstrap as they did in the original clustering?
4. The **Jaccard index** for one bootstrap sample is: (pairs that stayed together) / (pairs that stayed together + pairs that split up + pairs that were together in bootstrap but apart originally).
5. Average across all 20 bootstraps. That's your stability score.

Interpretation: ≥ 0.80 is conventionally "shippable" for a marketing segmentation. Below 0.80, the segmentation reshuffles too much between runs to support stable campaigns.

For Arcadia: the Phase 6 USML pre-registration requires you to write down your stability floor before running the sweep. If the winning K from the silhouette leaderboard has bootstrap Jaccard below your floor, it doesn't pass — even if it has the highest silhouette.

## Why it matters for ML orchestrators

A segmentation with bootstrap Jaccard 0.68 means roughly 1 in 3 customer pairs ends up in different segments when you re-cluster on fresh data. The CMO builds a "frequent weekend shoppers" campaign in February; the March re-cluster reshuffles 30% of them out of that segment. The campaign runs against the wrong people. Stability is the ML property that prevents this.

## Common confusions

- **"Bootstrap Jaccard is like cross-validation"** — Similar spirit, different mechanism. Cross-validation tests predictive accuracy on held-out data. Bootstrap Jaccard tests structural stability of the clustering solution.
- **"I need to compute this myself"** — Claude Code computes it during the Phase 4 sweep and reports it in the leaderboard. Your job is to read it and compare it to your pre-registered floor.

## When you'll hit it

Used in: Phase 4 (Candidates — reported in the clustering leaderboard), Phase 6 (Metric + Threshold — pre-register stability floor), Phase 7 (Red-Team — re-seed stability test uses same principle), Phase 8 (Deployment Gate — stability is one of the PASS/FAIL checks)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Hennig, "Cluster-wise Assessment of Cluster Stability" — bootstrap Jaccard methodology
- Ben-David et al., "Stability of k-Means Clustering" — theoretical foundations
