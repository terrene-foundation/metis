<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 4 — Candidates (Vision in Sprint 1, PredMaint in Sprint 2)

## 1. What this phase decides

Sweep a small candidate space to produce a leaderboard the next phase reads. Sprint 1 sweeps three vision architectures on the frozen-embedding scaffold. Sprint 2 sweeps three predmaint families × three prediction windows.

## 2. The Week 7 lens

**Vision sweep (Sprint 1):**
The scaffold ships the 3-architecture leaderboard at `/inspect/vision/leaderboard`: `resnet50_lr_head`, `efficientnet_b0_rf_head`, `vit_small_gbm_head`. All three share the same frozen-embedding scaffold (per `SCAFFOLD_MANIFEST.md` "Implementation deviations") with different head classifiers and embedding dimensionalities mimicking real-architecture differences. `POST /inspect/vision/train` re-runs the sweep with new hyperparameters.

**PredMaint sweep (Sprint 2):**
3 families × 3 windows = 9 cells on `/predict/maintenance/leaderboard`. Families: `lightgbm_features`, `lstm_sequence`, `survival_forest_tte`. Windows: 3 / 7 / 14 days. `POST /predict/maintenance/train` re-fits one family.

**RL sweep (Sprint 3 — separate Phase 4 run NOT in tonight's main flow):**
3 cached policies (`ppo_continuous`, `dqn_discrete`, `random_baseline`) at `/optimize/rl/leaderboard`. The "sweep" tonight is read-only — the cached transitions are deterministic. `POST /optimize/rl/simulate` re-rolls a policy. Phase 4 RL is collapsed into Phase 5 RL pick + Phase 7 RL Goodhart defense; no separate Phase 4 RL todo.

## 3. Your levers

- **Sprint detection** — am I in Sprint 1 (Vision) or Sprint 2 (PredMaint)?
- **Sweep configuration** — seeds, epoch budget, holdout split
- **Baseline-to-beat** — Sprint 1: AOI 78% recall / 12% FP rate. Sprint 2: zero baseline (AOI doesn't predict failures)
- **Per-class P/R/F1** — multi-class is the default
- **Brier score per class** — calibration matters for downstream consumers

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 4 — Candidates. The scaffold ships ONE pre-trained
baseline per family; my job is to sweep variations on the baselines
(NOT new architectures) so Phase 5 has a leaderboard to read.

Run the sweep. For each candidate, log:
- Per-class P/R/F1 on the holdout
- Brier score per class (calibration)
- Wall-clock training time
- Wall-clock inference time per sample (for Phase 10 cost reasoning)

Compare against the baseline.

Do NOT propose which candidate wins — that's Phase 5.
Do NOT introduce architectures not in scope (no AutoML, no random search).
Do NOT use "blocker" without specifics.

When the leaderboard is written, stop.

Sprint detection (which sprint am I in?):

Sprint 1 (Vision):
- Sweep: 3 architectures × 3 seeds = 9 rows
  - resnet50_lr_head
  - efficientnet_b0_rf_head
  - vit_small_gbm_head
- Endpoint: POST /inspect/vision/train with { unfreeze_layers, lr,
  epochs, seed }
- Baseline-to-beat (cite PRODUCT_BRIEF.md §1): AOI 78% recall on true
  defects, 12% FP rate. Any candidate not beating this on
  major_defect + safety_critical_defect recall is BLOCKED from Phase 5
  promotion.
- Edge-latency budget: 80 ms/board on Jetson-class hardware
  (PRODUCT_BRIEF.md §4.1 + §7). Inference time per sample MUST be
  recorded for the Phase 5 trade-off.

Sprint 2 (PredMaint):
- Sweep: 3 families × 3 windows × 3 seeds = 27 rows
  - lightgbm_features × {3, 7, 14}
  - lstm_sequence × {3, 7, 14}
  - survival_forest_tte × {3, 7, 14}
- Endpoint: POST /predict/maintenance/train with { family, lr, epochs,
  seed }
- Baseline-to-beat: zero (AOI doesn't predict failures). The bar is
  beat random chance on the 4-of-10 failing-machine cohort, AND have a
  Brier ≤ 0.20 for downstream scheduler consumption.

Configuration:
- 3 trials per candidate, seed in {RANDOM_SEED, RANDOM_SEED+1, +2}
- Holdout: time-respected 20% (later boards/machines than training)

Result file: data/leaderboard.json (overwritten per sprint, with
sprint_tag in JSON to distinguish vision vs predmaint).

Journal file: copy journal/skeletons/phase_4_candidates.md (apply
_vision suffix in Sprint 1, _predmaint suffix in Sprint 2).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- A vision candidate that beats AOI on major_defect recall by 5 pp at our 12,000 inspection events/day saves 12,000 × 0.05 × $4,200 = **$2.5M/day in expected FN avoidance** — even a small leaderboard delta is worth millions
- A predmaint family with Brier 0.05 better than the alternative produces noticeably better scheduler decisions, where each correct planned-maintenance avoids one $12,000 unplanned stop (at our 4-of-10 base rate, even one extra correct call per month is $144K/year)

## 6. Hard-floor table

Not directly applicable in Phase 4 — sweep is read-only against the leaderboard. Floors apply at Phase 6 (per-class threshold).

## 7. Reversal condition

A Phase 4 leaderboard is reversed when:

- **Signal**: re-running the sweep with the same seed produces visibly different metrics
- **Threshold**: any per-class metric delta > 2 pp on the same seed
- **Duration**: any single re-run

Non-determinism is a scaffold bug, not a Phase 4 finding — raise a hand. The cached results MUST be deterministic per seed (`SCAFFOLD_MANIFEST.md` "Implementation deviations" #1).

## 8. Transfer to next project

The 3-candidate sweep pattern is universal. In any new domain: pick a small candidate space, hold seed and holdout fixed, log per-class metrics + calibration + wall-clock, never name a winner here. The "baseline-to-beat" anchor (Sprint 1 AOI here, the rule-based system or the human or the previous-quarter model elsewhere) is the structural defense against shipping a fancy model that's worse than the simple alternative.

---

**Next file:** [`phase-05-implications.md`](./phase-05-implications.md)
