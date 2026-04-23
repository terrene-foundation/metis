<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Arcadia Retail — Business Costs

**Source of truth for every dollar figure cited in a journal entry.** Grader treats figures not in this table as zero credit for D2 (metric → cost linkage).

## Direct costs

| Term                            | Value | Unit                                    | Phase |
| ------------------------------- | ----- | --------------------------------------- | ----- |
| Converted recommendation        | +$18  | per converted click                     | 6, 10 |
| Wasted impression               | $14   | per session shown irrelevant recs       | 6, 7  |
| Wrong-segment campaign          | $45   | per customer sent to the wrong offer    | 6, 7  |
| Per-customer touch (email/push) | $3    | per marketing contact                   | 11    |
| PDPA breach (under-18 history)  | $220  | per record exposure                     | 7, 11 |
| Cold-start fallback             | $8    | per new-user session with no rec signal | 11    |

## Volumes (for Phase 1 framing)

- 50 000 customers on record; ~18 000 active in last 90 days
- 2 000 SKUs; ~1 200 in stock at any time; 40 SKUs rotate weekly
- 500 000 transactions / year; 60% e-com, 40% in-store
- 8 000 product-page views / day on e-com; 12% CTR on the existing rule-based system (the baseline to beat)

## Seasonality

Peak: **Nov–Dec** (Black Friday / Year-End). Drift anomalies in this window are expected — do not auto-retrain during peak.

## Decision anchors

- **Recommender economics**: $18 basket lift vs $14 wasted impression → ratio 1.3 : 1 favour conversion. A recommender that converts below the 12% rule-based baseline is net-negative after touch cost.
- **Segment economics**: $45 wrong-segment campaign vs $3 per-touch cost → asymmetry 15 : 1. Better to under-segment than to mis-segment.
- **PDPA**: $220 per under-18 record exposure is a **hard** line. Never classify as soft.
