# Phase 4 — Candidates

**Sprint:** 1 (Vision) / 2 (Text) · **Time:** **_:_** · **Artefact:** `journal/phase_4_candidates_<vision|text>.md` · **Output file:** `data/leaderboard.json`

## Candidate space

**Sprint 1 (Vision):** unfreeze depth ∈ {frozen, partial-unfreeze (last 2 conv blocks), full-unfreeze}
**Sprint 2 (Text):** family ∈ {bert_base, roberta, zero_shot_llm}

## Sweep configuration

- Trials: 3 per candidate (3 seeds: RANDOM_SEED, +1, +2)
- Epochs: 2 (Sprint 1) / 3 (Sprint 2)
- Holdout: 10% stratified, time-respected, demographic-balanced

## Leaderboard summary

| Candidate | Per-class F1 (mean) | csam_adjacent recall | Brier (mean) | Train time (s) | Inference (ms/sample) |
| --------- | ------------------- | -------------------- | ------------ | -------------- | --------------------- |
| \_\_\_    | \_\_\_              | \_\_\_               | \_\_\_       | \_\_\_         | \_\_\_                |

## Baseline-to-beat check (cite PRODUCT_BRIEF.md §1)

- Rule-keyword baseline: 31% recall on harmful, 4% FP rate
- Candidates beating baseline on harm-recall: \_\_\_

## Notes

<Any candidate that failed (e.g. zero-shot LLM mis-formatted output)? Stop and flag.>
