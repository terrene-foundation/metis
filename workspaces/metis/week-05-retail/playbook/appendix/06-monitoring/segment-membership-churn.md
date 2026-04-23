<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Segment Membership Churn

> **One-line hook:** The fraction of customers who move between segments month-over-month — the primary drift signal for unsupervised segmentation models.

## The gist

Supervised models have prediction accuracy — you can compare predicted vs actual labels and compute AUC or Brier. Unsupervised segmentation has no ground truth label, so you cannot compute "accuracy drift" directly. Instead, you monitor **segment membership churn**: the fraction of customers who land in a different segment when you re-cluster this month vs last month.

Low churn (< 5–10%) means the segmentation is stable — customers are reliably in the same segments and marketing campaigns built on those segments remain valid.

High churn (> 20–30%) means the segmentation is reshuffling. Campaigns that targeted "Segment A: weekend athleisure buyers" last month are now reaching a different mix of customers this month. The segment label has drifted from its original meaning. At some threshold of churn, the segmentation needs to be re-run with fresh data.

The monitoring cadence for segmentation is **monthly** — monthly re-cluster, monthly comparison. This is slower than classifier monitoring (weekly) because segment structure changes more slowly than individual purchase behaviour.

**Seasonal exclusion**: The Nov–Dec (Black Friday, Year-End) period produces abnormal shopping patterns that should not be treated as drift. A 30% segment-membership churn in December likely reflects holiday shopping behaviour, not structural change in customer segments. Your Phase 13 retrain rule must explicitly exclude this window from the drift baseline.

For Arcadia Phase 13: the `/drift/check` endpoint (window: `recent_30d`) returns the segment-membership churn rate for the current period vs the training reference. You set the threshold and duration window in Phase 13, grounded in the historical variance from `/drift/check` (window: `catalog_drift`).

## Why it matters for ML orchestrators

Segment-membership churn is the primary answer to "how do I know when to re-cluster?" without a ground-truth label. It's a structural health metric for the segmentation layer — and because Sprint 2 classifiers and Sprint 3 allocator both consume segment labels, high segment churn propagates instability into every downstream sprint.

## Common confusions

- **"Some churn is always bad"** — Some churn is expected and healthy (customers genuinely change behaviour month to month). The question is whether churn is within the historical variance established on your training window.
- **"I should re-cluster whenever segment churn is high"** — High churn in a seasonal window (Nov–Dec) is seasonality, not drift. Re-clustering on a seasonal spike produces a holiday-optimised segmentation that breaks in January.

## When you'll hit it

Used in: Phase 13 (Drift — segmentation retrain rule uses segment-membership churn as its signal), workflow-06 (Sprint 4 MLOps boot, the drift endpoint returns this metric)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Xu & Wunsch, "Survey of Clustering Algorithms" — includes discussion of cluster stability over time
- Hennig, "Cluster-wise Assessment of Cluster Stability" — bootstrap-based stability methodology adaptable for temporal drift
