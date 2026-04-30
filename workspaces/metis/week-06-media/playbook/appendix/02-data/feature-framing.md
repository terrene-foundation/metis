<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Feature Framing

> **One-line hook:** Classifying every input feature on four axes — availability, leakage, proxy risk, derivation — before any model sees it.

## The gist

Feature framing is the step where you decide which columns are allowed to enter the model, and why. It uses four axes:

**1. Availability at prediction time** — will this feature exist when the model runs in production? "Last week's transactions" is available if you re-compute it weekly. "The customer's final purchase in the dataset" is available during training but not in production — the model will look for it and find nothing.

**2. Leakage** — does this feature contain information from after the prediction horizon? A feature built on future data makes the model look brilliant during training and useless in production. Leakage is the single most common cause of "our model had 0.95 AUC in testing and 0.52 in production".

**3. Proxy for a protected class** — does this feature encode age, gender, ethnicity, or religion indirectly? In Singapore, postal district correlates strongly with ethnicity (the legacy of HDB allocation policies). Age_band is directly age. If you segment customers by postal_district, you may be segmenting them by ethnicity without realising it — and directing different marketing treatment to different ethnic groups, which is both legally and ethically problematic under PDPA and broader anti-discrimination norms.

**4. Engineered derivation** — is this a raw column or a derived feature? Derived features (recency × frequency, RFM scores, days-since-last-visit) can encode leakage or proxies invisibly. Document derivation steps so the audit can trace the chain.

For Arcadia Week 5, the Playbook unfolds Phase 3 (Feature Framing) as a separate phase because pre-cluster feature selection has higher stakes than pre-model feature selection. A feature that creates a segment that is really a proxy for a protected class is harder to unwind after the segment has a name and a marketing plan.

## Why it matters for ML orchestrators

Every decision in Phases 4–8 is downstream of the features that enter the model. A bad feature inclusion in Phase 3 creates a systematic bias that no threshold choice, no model family, and no red-team sweep will fix — because the model will have learned the bias deeply.

## Common confusions

- **"More features is always better"** — Dimensionality curse: on 40+ features, distance-based clustering finds noise rather than signal. Feature selection and dimensionality reduction before clustering is often worth more than adding another column.
- **"The model will just ignore useless features"** — Tree models can ignore uninformative features, but clustering algorithms cannot. K-means is especially sensitive to irrelevant columns, which add noise to distance calculations.

## When you'll hit it

Used in: Phase 3 (Feature Framing), Phase 7 (Red-Team — proxy leakage sweep drops postal_district and age_band to test)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Kuhn & Johnson, "Feature Engineering and Selection" — practical guide to feature construction
- Nisbet, Elder & Miner, "Handbook of Statistical Analysis and Data Mining" — on feature leakage detection
