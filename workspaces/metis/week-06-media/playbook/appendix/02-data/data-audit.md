<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Data Audit

> **One-line hook:** A structured six-category inspection of your data before any model runs — dispositions required, not just observations.

## The gist

A data audit is not "describe the data". It is a systematic check in six categories, each requiring a written disposition (what you will do about it):

1. **Completeness** — what fraction of rows have nulls in each key field? If more than 5% of your behavioural features are missing, your model is learning on a biased subsample. Disposition: impute, drop the column, or document the missingness as a known bias.

2. **Correctness** — are values plausible? Negative transaction amounts, timestamps in the future, product IDs that don't exist in the SKU catalogue. Disposition: filter, cap, or flag as bad data.

3. **Consistency** — do the same customers, SKUs, or stores appear under multiple identifiers across tables? A customer who is "C001" in transactions and "CUST-001" in the demographics table is a join failure waiting to happen. Disposition: normalise identifiers before joining.

4. **Leakage** — does any feature contain information from after the prediction horizon? A "days since last purchase" feature computed on the full timeline leaks the future into the past. Disposition: hard-cut the feature at the train/test split.

5. **Proxy for a protected class** — does any feature act as a stand-in for age, gender, ethnicity, or religion without being labelled as such? Postal district and age_band are the Arcadia candidates. Disposition: run a proxy test, drop or document.

6. **Sampling** — is the scaffold sample representative? 5,000 customers drawn from 18,000 active — by what method? Disposition: confirm the sample was drawn to preserve the full distribution of spend tiers, store locations, and tenure bands.

Each category needs a one-sentence disposition. "Noted" is not a disposition. "Capped at 99th percentile and documented in `journal/phase_2_data_audit.md`" is.

## Why it matters for ML orchestrators

You cannot commission a model and then be surprised by what it learned. If the data was dirty going in, the model learned the dirt. A Phase 2 audit with written dispositions is the artefact that proves you knew what you were working with — and the audit is what the rubric checks under D1 (harm framing).

## Common confusions

- **"Claude Code will clean the data automatically"** — It can, but it needs instructions. If you don't specify a missingness strategy, the default is usually "drop rows with nulls" — which silently biases your training set toward customers with complete records (typically higher-value ones).
- **"The audit is just documentation"** — The audit produces dispositions that Claude Code executes. It is not passive documentation; it drives what data actually enters the model.

## When you'll hit it

Used in: Phase 2 (Data Audit), workflow-03 (Sprint 1 USML boot — audit runs before any clustering)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Gebru et al., "Datasheets for Datasets" — structured data documentation standard
- Breck et al., "The ML Test Score" — systematic data validation checklist
