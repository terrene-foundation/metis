<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Dimensionality Reduction

> **One-line hook:** Collapsing many features into fewer dimensions — either for preprocessing (before clustering) or for visualisation — with two distinct purposes that must not be conflated.

## The gist

Dimensionality reduction takes a dataset with many features (columns) and produces a smaller number of features that capture most of the information. For Arcadia's 40+ behavioural features, this matters for two separate reasons:

**Preprocessing for clustering**: Distance-based clustering algorithms (K-means, hierarchical) calculate distances between customers in feature space. With 40 features, two customers who are genuinely similar on 5 core behavioural dimensions may appear "far apart" in 40-dimensional space because of noise in the other 35 features. Reducing to 5–10 principal components (PCA) or non-negative factors (NMF) before clustering removes noise and tightens the distance calculation. The resulting clusters are usually cleaner.

**Visualisation**: You cannot plot customers in 40 dimensions. Reducing to 2 dimensions (t-SNE or UMAP) lets you plot a scatter chart where each dot is a customer and proximity on the chart represents feature similarity. This is useful for understanding whether the clusters are visually coherent — do Segment A customers form a blob, or are they scattered everywhere? But t-SNE and UMAP are for visualisation only; their 2D coordinates do not preserve distances accurately enough for use as model inputs.

The two purposes use different techniques: PCA and NMF for preprocessing (preserve linear structure, interpretable components); t-SNE and UMAP for visualisation (preserve neighbourhood structure, not interpretable as coordinates).

Do not use t-SNE coordinates as features for clustering — you will be clustering on a distortion of the original space.

## Why it matters for ML orchestrators

When Claude Code proposes "reduce to N components before clustering", you need to ask: is this for preprocessing or visualisation? If preprocessing, are the components interpretable — can you tell the CMO "this component captures transaction frequency and another captures spend-tier"? Uninterpretable components make segment narratives harder.

## Common confusions

- **"t-SNE shows clear clusters, so the clustering must be good"** — t-SNE is designed to show local neighbourhood structure; it may create apparent visual clusters even in random data. Use the silhouette score and bootstrap Jaccard as your quantitative signals.
- **"PCA loses information"** — PCA retains the directions of maximum variance. You choose how many components to keep (typically enough to explain 80–90% of variance). The information "lost" is mostly noise.

## When you'll hit it

Used in: Phase 3 (Feature Framing — decide whether to reduce before clustering), Phase 4 (Candidates — the sweep may include runs with and without reduction), Phase 7 (Red-Team — visualise segment structure)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- van der Maaten & Hinton, "Visualizing Data using t-SNE" — original t-SNE paper
- McInnes et al., "UMAP: Uniform Manifold Approximation and Projection" — UMAP paper
