<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Proxy for a Protected Class

> **One-line hook:** A feature that encodes race, age, gender, or religion indirectly — and must be tested and documented, not silently left in.

## The gist

A **proxy** is a feature that correlates strongly with a legally protected characteristic (age, gender, ethnicity, religion, disability) without being labelled as such. The model learns the correlation and effectively makes decisions on the basis of the protected characteristic, without anyone having explicitly included it.

In Singapore, postal district is a well-known proxy for ethnicity. The HDB (Housing Development Board) managed ethnic quotas in public housing estates for decades, which means where you live correlates with your ethnicity to a statistically detectable degree. Age_band is a direct age proxy; if PDPA §13 constrains what data you can use for under-18 individuals, then age_band embedded in a segmentation model may create segments that are partially defined by age in a way that violates the constraint.

The test is simple: drop the suspected proxy feature, re-run the model, and count how many customers change segment (or change predicted class). If a lot move — say, more than 15% — the model was encoding the proxy heavily. That doesn't automatically mean you must drop the feature, but it does mean you must document it and decide explicitly.

For the Arcadia Phase 7 red-team: you drop `postal_district` AND `age_band` together, re-cluster, and report the fraction of customers who change segment. If that fraction is high and the resulting segments are less interpretable, you have a choice: keep the feature with documented risk, or build segments on behavioural features only.

## Why it matters for ML orchestrators

PDPA §13 in Singapore restricts the processing of personal data relating to protected characteristics without explicit consent. Proxy features can create de facto processing of protected characteristics. The $220 per-record PDPA exposure (from `PRODUCT_BRIEF.md §2`) applies to under-18 records specifically, but the broader principle — you are responsible for what your features encode — applies to all protected classes.

## Common confusions

- **"We didn't include ethnicity as a feature, so we're fine"** — If you included postal district, you may have effectively included ethnicity. The label on the column doesn't determine its information content.
- **"The proxy test is just about compliance"** — It's also about product quality. A segment whose defining characteristic is "customers who live in Tampines" is less useful for marketing than one defined by "customers who buy weekend athleisure". Proxy removal often improves interpretability.

## When you'll hit it

Used in: Phase 3 (Feature Framing — proxy axis), Phase 7 (Red-Team — mandatory proxy drop and re-cluster), Phase 11 (Constraints — PDPA proxy-risk re-classification if needed)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Barocas & Selbst, "Big Data's Disparate Impact" — foundational paper on proxy discrimination
- Singapore PDPA 2012 (as amended) — Personal Data Protection Act, Section 13
