# Phase 6 — Metric + Threshold

**Sprint:** 1 (Vision) / 2 (Text) · **Time:** **_:_** · **Artefact:** `journal/phase_6_metric_threshold_<vision|text>.md`

## Pre-registered floors (write BEFORE seeing the leaderboard)

> **CRITICAL:** these floors must be written into this file before opening Phase 4's leaderboard. Post-hoc floors score 0 on D5.

- Per-class precision floor: ≥ \_\_\_ (justify in $)
- Per-class recall floor on harm classes: ≥ \_\_\_ (justify in $)
- Per-class Brier ceiling: ≤ \_\_\_ (calibration matters because queue allocator consumes probabilities)
- csam_adjacent (Sprint 1): structural hard floor at threshold ≤ 0.40 per IMDA mandate (separate from cost-balanced)

## Per-class threshold table

| Class         | Cost-balanced threshold    | Justification ($)                    | Hard-floor override?       | Final threshold | Action       |
| ------------- | -------------------------- | ------------------------------------ | -------------------------- | --------------- | ------------ |
| nsfw          | \_\_\_                     | min ($320 × FN rate + $15 × FP rate) | none                       | \_\_\_          | auto_remove  |
| violence      | \_\_\_                     | \_\_\_                               | none                       | \_\_\_          | auto_remove  |
| weapons       | \_\_\_                     | \_\_\_                               | none                       | \_\_\_          | auto_remove  |
| csam_adjacent | (cost-bal would be \_\_\_) | $1M IMDA ceiling separate            | YES (≤ 0.40, IMDA mandate) | 0.40            | human_review |
| safe          | \_\_\_                     | \_\_\_                               | none                       | \_\_\_          | allow        |

(Sprint 2 / Text: hate_speech, harassment, threats, self_harm_encouragement, safe — note self_harm has clinical-safety dual-action: warn-and-queue at >0.5 even if auto-remove threshold is higher.)

## Calibration findings

<Brier per class. Any class > pre-registered ceiling: flag for tighter Phase 13 monitoring.>

## Reversal condition per class (D5)

<For each class: signal + threshold + duration. "If hate_speech recall drops below 0.78 for 5 consecutive daily checks, reduce threshold by 0.05.">

## Endpoint calls fired

- POST /moderate/<image|text>/threshold — one call per class (5 calls)
