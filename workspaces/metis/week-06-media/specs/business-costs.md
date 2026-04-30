<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# MosaicHub — Business Costs

**Source of truth for every dollar figure cited in a journal entry.** Grader treats figures not in this table as zero credit for D2 (metric → cost linkage).

## Direct costs

| Term                                                | Value      | Unit                                              | Phase    |
| --------------------------------------------------- | ---------- | ------------------------------------------------- | -------- |
| False negative (harmful left up, then reported)     | $320       | per piece (regulator + lawsuit)                   | 6, 7, 10 |
| False positive (legitimate auto-removed)            | $15        | per piece (creator trust + appeal handling)       | 6, 7, 10 |
| Human reviewer-minute                               | $22        | per minute on the queue                           | 10, 11   |
| SG Online Safety Code violation (CSAM non-takedown) | $1,000,000 | per incident — IMDA fine + CEO-level reputational | 7, 11    |
| Cold-start misclassification (novel content type)   | $8         | per piece                                         | 11, 13   |
| GPU inference                                       | $0.03      | per 1,000 image classifications served            | 6, 10    |

## Volumes (for Phase 1 framing)

- 5,000,000 MAU across SG / MY / ID / PH / TH; 80% Gen-Z
- 2,000,000 text+image posts / day; 100,000 video uploads / day
- 30,000,000 daily reactions+comments
- Reviewer queue: 8,000-item average start-of-day; 90-min SLA target
- Current rule+keyword system: 31% recall on harmful, 4% FP rate (the floor to beat)
- Scaffold sample: 80,000 labelled posts (24k image / 56k text / 8k multi-modal memes)

## Seasonality

Peak adversarial windows: **election cycles** + **major news events**. Drift anomalies in these windows are expected — do not auto-retrain during them.

## Decision anchors

- **Per-class threshold economics**: $320 FN vs $15 FP → ratio **21 : 1** in favour of catching harm. A symmetric metric (raw accuracy) systematically under-prices missing harmful content.
- **CSAM-adjacent class**: $1M IMDA ceiling sits structurally above any cost-balanced threshold. The CSAM threshold is **HARD** (regulator-mandated minimum), not cost-balanced. Never classify as soft.
- **Queue allocator economics**: $22/min reviewer vs $320/$15 mis-classification → reviewer-time is the second-order cost; the queue allocator trades reviewer-minutes against expected mis-classification cost at each tier.
- **Compute economics**: $0.03 / 1,000 image classifications × 600,000 daily image classifications = $18 / day for image alone. Fusion is 3× compute → $54 / day for fusion. Multi-modal pays for itself only if cross-modal coverage gain > $36 / day in (FN cost × catches).
