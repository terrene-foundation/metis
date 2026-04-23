<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Precision@k

> **One-line hook:** Of the top-k items you recommended to a customer, how many did they actually engage with? The primary offline metric for recommender evaluation.

## The gist

**Precision@k** answers: if we show a customer their top-k recommended items, what fraction of those items will they actually click, purchase, or engage with?

Concretely: you show a customer their top-10 recommended SKUs. They engage with 3. Precision@10 for that customer = 3/10 = 0.30.

You compute this across all customers in a held-out test set (sessions where you know what they actually bought) and average. The result is your recommender's offline precision@k.

Why k matters: precision@5 and precision@10 can tell different stories. A recommender that packs the top 5 with high-confidence items and trails off for slots 6–10 will have precision@5 > precision@10. Report both; the UI shows top-10 to Arcadia customers, so precision@10 is the primary metric.

Precision@k for recommenders plays the same role as AUC for classifiers: it's a comparative metric for ranking candidates in Phase 4. The current rule-based recommender converts at 12% click-through — that's approximately precision@10 = 0.12. Any new recommender must beat 0.12 to justify the complexity.

**Important caveat**: precision@k is computed on historical data where you know what the customer actually bought. It measures performance on items the customer was exposed to. Items they were never shown (but might have loved) don't count as hits or misses. This is an **exposure bias** inherent to all offline recommender evaluation.

## Why it matters for ML orchestrators

Phase 5 asks you to pick the recommender variant (content-based, collaborative, hybrid). Precision@k is the primary signal for that choice, but it must be evaluated alongside coverage (are you recommending a wide range of SKUs or always the same 20?) and cold-start rate (how often does the recommender fall back?).

## Common confusions

- **"High precision@k is all that matters"** — A recommender that only recommends the 10 most popular items achieves decent precision@k but zero personalisation and 2% catalogue coverage. Diversity and coverage matter.
- **"Precision@k measures revenue impact"** — It measures engagement rate on offline data. Revenue impact requires A/B testing in production, which is a live experiment, not an offline metric.

## When you'll hit it

Used in: Phase 4 (Candidates — recommender leaderboard reports precision@5 and precision@10), Phase 5 (Implications — pick the winning recommender variant), Phase 7 (Red-Team — check cold-start session precision@k)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Herlocker et al., "Evaluating Collaborative Filtering Recommender Systems" — foundational evaluation paper
- Cremonesi, Koren & Turrin, "Performance of Recommender Algorithms on Top-N Recommendation Tasks" — precision@k in practice
