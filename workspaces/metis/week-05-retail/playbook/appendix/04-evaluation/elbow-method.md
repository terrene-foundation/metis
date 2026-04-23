<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Elbow Method

> **One-line hook:** A visual heuristic for picking K in clustering — useful for ruling out bad values but not sufficient on its own.

## The gist

The **elbow method** plots within-cluster sum of squared distances (inertia) against K. As K increases, inertia always decreases — more clusters means each cluster is tighter. The plot looks like a curve that drops steeply at first, then flattens. The "elbow" is the point where the curve bends: adding more clusters beyond that point gives diminishing returns.

Example: K=2 inertia is 10,000. K=3 is 6,000. K=4 is 5,200. K=5 is 4,900. K=6 is 4,750. The big drops are K=2→3 and K=3→4. After K=4, improvements are small. The elbow is around K=3 or K=4.

**Limitations**: The elbow method is a visual heuristic, not a rigorous criterion. In practice, the "elbow" is often not obvious — the curve is smooth without a clear bend. It also says nothing about stability or actionability. A K that looks good on the elbow plot may still produce unstable or non-actionable clusters.

For Arcadia: the elbow plot is one signal among several. Silhouette score and bootstrap Jaccard are more principled; the operational ceiling constrains the upper bound of K. The elbow is useful for quickly ruling out extreme values — if the elbow is at K=3, then K=9 is unlikely to be justified. But the elbow doesn't decide; it narrows.

Your Phase 6 pre-registration is the three floors (separation, stability, actionability), not an elbow plot. The elbow is informational, not a gate.

## Why it matters for ML orchestrators

You'll see elbow plots referenced in Claude Code's output during Phase 4. They're a quick sanity check on K range, not a substitute for rigorous evaluation. If Claude Code says "the elbow is at K=5", your follow-up is: "and what's the bootstrap Jaccard at K=5?"

## Common confusions

- **"The elbow picks K"** — The elbow narrows the range of plausible K values. You pick K, informed by elbow + silhouette + Jaccard + operational ceiling.
- **"If there's no clear elbow, clustering doesn't work"** — A smooth curve just means the data doesn't have an obvious number of natural clusters. You still choose a K based on the other signals and your operational ceiling.

## When you'll hit it

Used in: Phase 4 (Candidates — elbow plot may appear in the clustering leaderboard output), Phase 6 (Metric + Threshold — used informally to set K range before pre-registration)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Thorndike, "Who Belongs in the Family?" — original elbow method paper (1953)
- Tibshirani, Walther & Hastie, "Estimating the Number of Clusters in a Data Set via the Gap Statistic" — more principled alternative
