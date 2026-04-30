<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Cold Start

> **One-line hook:** What happens when a new customer or product arrives with no history — a product decision, not a bug to be fixed.

## The gist

**Cold start** is the condition where a model cannot make a meaningful prediction because it has no historical data for that customer or product.

**User cold start**: A new customer creates an account. They have no transaction history. A collaborative filtering recommender ("customers like you also bought X") has nothing to work with — there are no similar customers to reference because this customer's purchase patterns are unknown. The model falls back to a default.

**Item cold start**: A new SKU is added to the catalogue. No customer has ever bought it, so there's no purchase co-occurrence data. A collaborative filtering recommender cannot rank this SKU because it has no interaction history.

The cold-start fallback is a **product decision you own**. Options for Arcadia:

- **Segment modal basket** (recommended): Use the Sprint 1 segmentation. A new customer without purchase history still has demographics or browsing signals that can assign them to a segment. Recommend the most popular items in that segment. This is the warmest fallback because it uses the structural knowledge from Sprint 1.
- **Catalogue popularity**: Recommend the top-10 most purchased items across all customers. Simple, but produces the same recommendation for every cold-start customer — low diversity.
- **Editorial curation**: A human-curated "new customer" list. Most personalised intent but least scalable.

For Arcadia: the scaffold pre-wires the cold-start fallback at `/recommend/*`. You declare which fallback to use in Phase 5, and the Phase 7 red-team checks that the cold-start rate (fraction of sessions that triggered the fallback) is at an acceptable level.

The cost of a bad cold-start fallback: `$8 per cold-start session` if it defaults to catalogue popularity (from `PRODUCT_BRIEF.md §2`). That's the cost the Arcadia team assigned to catalogue-popularity cold-starts, presumably because catalogue popularity has low conversion for new customers.

## Why it matters for ML orchestrators

Cold start is most of your mobile signups in Singapore. A recommender that is brilliant for tenured customers but defaults to a bad experience for new ones is a net-negative product. The cold-start decision belongs in the journal: what fallback, and what's the reversal condition if the cold-start rate climbs above an acceptable threshold?

## Common confusions

- **"Cold start only affects recommenders"** — Cold start affects any model that relies on historical data. A churn classifier for customers with fewer than 3 purchases has minimal signal. The population definition (Phase 1) should exclude customers below a purchase threshold if the model cannot serve them meaningfully.
- **"We can fix cold start later"** — Cold start affects new users from day one. If you ship without a declared fallback, the default is whatever the framework does — often catalogue popularity. Declare it explicitly.

## When you'll hit it

Used in: Phase 5 (Implications — declare the cold-start fallback), Phase 7 (Red-Team — check cold-start rate), Phase 10 (Objective — cold-start rate may enter the LP objective), workflow-04 (Sprint 2 includes recommender evaluation)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Schein et al., "Methods and Metrics for Cold-Start Recommendations" — foundational survey
- Lam et al., "Addressing the Cold Start Problem in Recommender Systems Using Social Data" — hybrid approaches
