<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Unsupervised Families

> **One-line hook:** Four algorithm families for finding structure when you have no labels — and why the "right" family depends on what shape you expect the clusters to be.

## The gist

Unsupervised learning means you have no ground-truth label. There is no "this customer belongs to Segment A" column in your training data. The algorithm finds structure by looking for patterns in the feature space. Your job is to decide whether the structure the algorithm found is real and useful.

**K-means** (and variants): Groups customers into K round blobs by minimising the distance between each customer and their cluster center. Fast, simple, and widely used. Works well when your clusters are roughly equal in size and round in shape. Breaks when clusters are elongated, nested, or unequal in size. You specify K up front — choosing the wrong K is the most common failure in Sprint 1.

**Density-based** (DBSCAN, HDBSCAN): Finds dense regions of customers separated by sparse regions. Automatically flags customers who don't fit any cluster as unassigned (outliers). Does not require you to specify K. Fails when clusters have varying densities and can leave 10–25% of customers unassigned — which means 10–25% of Arcadia's customers have no segment label, which the marketing team cannot handle.

**Hierarchical** (agglomerative clustering): Builds a tree from the bottom up (merge the two closest customers, then the two closest groups, etc.) and lets you cut the tree at any level to get any K. Useful when you're unsure of K and want to explore the structure visually (dendrogram). Slow on large data; the cut decision is somewhat arbitrary.

**Gaussian Mixture Models (GMM)**: Like K-means but allows soft (probabilistic) membership — a customer can be 70% Segment A and 30% Segment B. Useful when segments genuinely overlap. Slower to converge and can find spurious components on small data.

For Arcadia: the scaffold's baseline is K-means (K=3). The Phase 4 sweep should include at least K-means (at multiple K values), HDBSCAN, and hierarchical, so you have a genuine comparison before choosing in Phase 5.

## Why it matters for ML orchestrators

Choosing the wrong family means your "segments" reflect the algorithm's assumptions, not the data's actual structure. K-means on non-blob-shaped data produces segments that look neat on a chart but don't correspond to real customer patterns. The Phase 4 comparison exists to surface this.

## Common confusions

- **"K-means is the standard so I'll use it"** — K-means is a reasonable starting point, but it's not always the best. Run at least one alternative and compare.
- **"HDBSCAN is better because it doesn't require K"** — Only if the resulting unassigned fraction is acceptable. 20% unassigned customers means 20% of Arcadia's customers have no campaign, which the CMO may not accept.

## When you'll hit it

Used in: Phase 4 (Candidates — USML sweep), Phase 5 (Implications — pick the clustering approach), workflow-03 (Sprint 1 USML boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Ester et al., "A Density-Based Algorithm for Discovering Clusters" — original DBSCAN paper
- Campello et al., "Density-Based Clustering Based on Hierarchical Density Estimates" — HDBSCAN paper
