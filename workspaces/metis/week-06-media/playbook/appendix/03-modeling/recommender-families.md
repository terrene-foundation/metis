<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Recommender Families

> **One-line hook:** Three approaches for suggesting products to customers — and why "hybrid is always best" is not the right answer without an offline evaluation.

## The gist

Recommender systems suggest items (products, articles, campaigns) to users (customers, readers). Three families are relevant for Arcadia:

**Content-based filtering**: Recommends items similar to what the customer has already bought, based on product attributes (category, brand, price tier, tags). Works for new SKUs that have attributes but no purchase history yet. Handles the "new product cold-start" well. Produces conservative recommendations — you're suggesting things the customer would probably have found anyway. Low serendipity, decent precision.

**Collaborative filtering**: Recommends items that customers similar to this one have bought, based on purchase patterns. "Customers like you also bought X." High serendipity — can surface items the customer has never seen. Struggles with new customers who have no purchase history (user cold-start) and new products with no purchase history (item cold-start). The scaffold pre-trains a matrix factorisation model (NMF — non-negative matrix factorisation) at startup, which is why there's a ~17s warm-up time.

**Hybrid**: Blends content-based and collaborative signals, often with a segment-aware cold-start fallback (use the segment's modal basket when a customer has no history). Higher complexity and more to tune, but not automatically better. For a 400-SKU catalogue, hybrid is plausible — but whether it beats content-based or collaborative depends on the offline evaluation.

The offline evaluation (Phase 4 for the recommender) compares all three on: precision@k (how many of your top-k recommendations did the customer actually engage with?), catalogue coverage (what fraction of SKUs ever appear in a top-10?), cold-start rate (what fraction of sessions fell back to the cold-start?), and diversity within a top-10 (average distinct categories per recommendation list).

For Arcadia: the scaffold pre-wires all three variants behind `/recommend/compare`. Your Phase 5 decision is which family wins — and what the cold-start fallback is for new customers.

## Why it matters for ML orchestrators

Cold-start is a product decision, not a bug. Every new mobile signup starts with no history. Your choice of cold-start fallback (segment modal basket vs catalogue popularity vs editorial curation) determines the experience for a large share of your user base. That choice belongs in your journal.

## Common confusions

- **"Hybrid is always better"** — Only if it outperforms on your offline metrics. On a small catalogue (400 SKUs), content-based may be more precise and less noisy.
- **"Precision@10 is the only metric"** — Coverage and diversity matter for the long tail of the catalogue. A recommender with high precision@10 but 2% catalogue coverage is effectively recommending the same 10 products to everyone.

## When you'll hit it

Used in: Phase 4 (Candidates — recommender offline eval), Phase 5 (Implications — pick the family and declare cold-start fallback), Phase 7 (Red-Team — cold-start rate check)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Ricci, Rokach & Shapira, "Recommender Systems Handbook" — comprehensive reference
- Lee & Seung, "Learning the Parts of Objects by Non-Negative Matrix Factorization" — NMF paper underlying collaborative filtering
