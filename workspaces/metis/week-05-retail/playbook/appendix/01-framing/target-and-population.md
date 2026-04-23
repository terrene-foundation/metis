<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Target and Population

> **One-line hook:** Who the model predicts for — and who it deliberately ignores — stated explicitly before any code runs.

## The gist

The **target** is what the model predicts, stated in the form: _what × per whom × over what window_. "Discover patterns" is not a target. "Assign a behavioural segment to each active customer over the last 90 days" is.

The **population** is the full list of who counts and — equally important — who is excluded. Inclusions are easy. Exclusions take discipline: staff accounts, bot accounts, test transactions, customers with fewer than three purchases (too sparse for reliable behaviour). Every exclusion you skip comes back as noise that muddies your model and confuses the people who have to act on it.

For Arcadia Retail, the active population is ~18,000 customers with at least one transaction in the last 90 days, from the full book of ~50,000. The scaffold sample ships 5,000 of these. That 18,000 number is the one you cite in your frame; the 5,000 is the scaffold number you cite in your journal when reporting actual model outputs.

Why does the exclusion list matter so much? Because a staff account that buys 200 items a week looks like a hyper-loyalist to any clustering algorithm — and "hyper-loyalist" becomes a real segment label that marketing plans campaigns against. You excluded it by writing it down, not by hoping the model would ignore it.

## Why it matters for ML orchestrators

If your population definition is fuzzy, every downstream metric is questionable — "what share of active customers are in Segment A?" depends on whether "active" is defined the same way everywhere. Write it once in Phase 1 Frame and cite that definition in every later phase.

## Common confusions

- **"The model will filter outliers automatically"** — Clustering and classification algorithms don't know which accounts are bots; they find patterns, including bot patterns. Exclusions are your job, not the algorithm's.
- **"The 5,000 scaffold sample is the real Arcadia population"** — No. It's a representative sample. Frame decisions using the 18,000 active number from `PRODUCT_BRIEF.md §2`; report model outputs using the 5,000 scaffold number.

## When you'll hit it

Used in: Phase 1 (Frame), Phase 2 (Data Audit), workflow-03 (Sprint 1 USML boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Sculley et al., "Machine Learning: The High-Interest Credit Card of Technical Debt" — on hidden dependencies in population definitions
- Google PAIR Guidebook, "Designing Datasets" — on systematic exclusion review
