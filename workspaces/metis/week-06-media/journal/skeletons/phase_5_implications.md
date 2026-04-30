# Phase 5 — Implications

**Sprint:** 1 (Vision) / 2 (Text) / 3 (Fusion arch) · **Time:** **_:_** · **Artefact:** `journal/phase_5_implications_<vision|text|fusion>.md`

## Picked

<Architecture / family / fusion mode chosen, with run_id from leaderboard.>

## Why (cite PRODUCT_BRIEF.md §2 cost asymmetry)

- **Cost-asymmetry-weighted score:** ($320 × FN rate + $15 × FP rate) summed over classes = $\_\_\_
- **Calibration:** Brier per class within pre-registered ceiling? \_\_\_
- **Inference cost feasibility:** $\_\_\_/day at 600k images (or 2M text) — within team budget of $\_\_\_/day
- **Sprint 3 (multi-modal only):** cross-modal coverage gain $\_\_\_/year vs compute delta $\_\_\_/year

## What I rejected (D3 — quantify the sacrifice)

<For each non-picked candidate: what it scored higher on, what it scored lower on, what the $ delta is.>
<Example: "Rejected RoBERTa: scored 0.02 F1 higher on hate_speech but Brier was 0.18 (failed pre-registered ceiling of 0.12). Calibration matters because the queue allocator consumes probabilities directly.">

## csam_adjacent defended separately (Sprint 1 only)

<The picked architecture's csam_adjacent recall must be high enough to make IMDA hard-floor (0.40) viable. Show recall at 0.40 threshold.>

## Reversal condition (D5)

<What signal would flip this pick? "If text moderator's per-class Brier exceeds 0.18 for 5 consecutive daily checks, re-evaluate against RoBERTa.">

## Risks accepted

<1–3 lines.>
