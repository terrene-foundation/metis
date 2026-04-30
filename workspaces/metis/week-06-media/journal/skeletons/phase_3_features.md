# Phase 3 — Feature Framing

**Sprint:** 1 · **Time:** **_:_** · **Artefact:** `journal/phase_3_features.md`

## Feature table

| Feature                      | At decision time? | Proxy risk | Source       | Decision (drop/keep/monitor) | Rationale                                    |
| ---------------------------- | ----------------- | ---------- | ------------ | ---------------------------- | -------------------------------------------- |
| raw RGB image (224x224)      | YES               | low        | raw          | KEEP                         | The model needs it                           |
| EXIF metadata                | YES               | medium     | metadata     | DROP                         | GPS proxy risk                               |
| random horizontal flip       | training only     | low        | augmentation | KEEP                         | Standard, safe                               |
| mixup augmentation           | training only     | medium     | augmentation | MONITOR                      | Memes break under blend; review with Phase 7 |
| account_country              | YES               | HIGH       | metadata     | DROP                         | Ethnicity proxy in SEA                       |
| account_age_days             | YES               | medium     | metadata     | KEEP w/ Phase 7 sweep        | Demographic proxy                            |
| account_verified_status      | YES               | low        | metadata     | KEEP                         | Low risk                                     |
| ResNet-50 penultimate vector | YES               | none       | embedding    | KEEP                         | Model representation                         |
| \_\_\_                       | \_\_\_            | \_\_\_     | \_\_\_       | \_\_\_                       | \_\_\_                                       |

## What I dropped and why (D3)

<Quantify what each drop costs in expected accuracy. "Dropping account_country costs ~0.5% F1 on the demographic-skew sweep, but eliminates the ethnicity-proxy audit risk.">

## Reversal condition (D5)

<When would I re-include a dropped feature? "If demographic-skew sweep in Phase 7 shows the model degrades >2% F1 on under-represented markets, revisit account_country with Phase 14 fairness audit (Week 7).">
