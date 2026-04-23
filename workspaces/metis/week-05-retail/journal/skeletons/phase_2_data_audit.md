# Phase 2 — Data Audit

**Sprint:** 1 · **Time:** **_:_** · **Artefact:** `journal/phase_2_data_audit.md`

## Accepted?

Yes / Conditional / No: \_\_\_

## Audit findings (six categories)

- **Duplicates:** <count + disposition (dedupe / keep)>
- **Contamination (bots/staff/test):** <count + disposition (exclude / flag / keep)>
- **Singletons / low-observation rows:** <count + disposition (exclude / cold-start branch)>
- **Outliers:** <which feature + disposition (cap / log / exclude / own-cluster)>
- **Label-in-disguise candidates:** <columns + reason they look like an older rule>
- **Missingness:** <per-feature disposition (impute / drop / leave / mask-flag)>

## Conditions applied before fitting

<List the transformations — e.g. "log-transform total_spend_24mo, cap visits_per_week at 95th percentile">

## Known risks I am accepting (D3)

<What trade-off did this audit take? e.g. "Excluding top-1% spenders loses $X/month of attention but prevents the segmentation from collapsing into wealth tiers.">

## Reversal condition (D5)

<Signal + threshold that would make me re-run the audit. e.g. "If next month's contamination rate > 3%, re-audit.">
