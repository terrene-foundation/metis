<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Coverage and Diversity

> **One-line hook:** Whether the recommender surfaces the full catalogue (coverage) and whether each recommendation list contains varied items (diversity) — the long-tail metrics.

## The gist

Precision@k measures how good the recommendations are for each individual customer. Coverage and diversity measure whether the system is healthy at a population level.

**Catalogue coverage**: What fraction of all SKUs ever appear in a top-10 recommendation across the full customer base? A recommender with 5% coverage recommends the same 20 items to everyone — the other 380 SKUs in Arcadia's 400-SKU catalogue are invisible. That's bad for the business (categories with zero recommendations die) and bad for customers (they never discover items outside the algorithm's comfort zone).

Typical targets: >40% coverage is reasonable for a retail recommender. Below 20% signals a popularity bias — the system has learned that recommending popular items is "safe" and is essentially just showing everyone the bestseller list.

**Within-list diversity**: For each customer's top-10 list, how many distinct product categories are represented? A top-10 that is 9 "yoga pants" and 1 "yoga mat" is not diverse. A top-10 that spans athletic wear, outdoor gear, accessories, and footwear is diverse.

Low within-list diversity means customers see a monoculture and stop browsing. It also means the recommender has overfit to the customer's most recent purchase category (recency bias).

For Arcadia Phase 4: the scaffold reports coverage and within-list diversity alongside precision@k in the recommender leaderboard at `/recommend/compare`. You use all four metrics (precision@5, precision@10, coverage, diversity) to compare the three variants in Phase 5.

## Why it matters for ML orchestrators

Phase 10 (Objective) for the LP allocator may include a coverage floor as a constraint: "at least 30% of SKUs must appear in at least one recommended top-10 per week." This ensures the long-tail of the catalogue gets exposure. Without this constraint, the LP optimises purely for expected revenue and recommends only the highest-P(convert) items, which are usually the bestsellers.

## Common confusions

- **"High coverage means the recommender is good"** — Coverage can be gamed by recommending random items. High precision@k AND high coverage together indicate a genuinely useful recommender.
- **"Diversity lowers precision"** — Often true: more diverse lists include items the customer is less likely to engage with. The trade-off is between short-term engagement (precision) and long-term discovery (diversity). Declare the trade-off explicitly in Phase 5.

## When you'll hit it

Used in: Phase 4 (Candidates — recommender leaderboard metrics), Phase 5 (Implications — declare the coverage/diversity vs precision trade-off), Phase 10 (Objective — coverage floor as LP constraint candidate)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Adomavicius & Kwon, "Improving Aggregate Recommendation Diversity Using Ranking-Based Techniques"
- McNee, Riedl & Konstan, "Being Accurate is Not Enough: How Accuracy Metrics Have Hurt Recommender Systems"
