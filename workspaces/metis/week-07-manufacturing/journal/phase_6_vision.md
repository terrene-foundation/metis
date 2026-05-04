<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 6 — Metric + Threshold · Vision QC ★ (Trust-Plane decision moment 2 of 5)

**Decision moment:** Per-class auto-pass threshold for vision QC, with WSH 0.40 hard floor on safety_critical.
**Sprint:** 1 (Vision QC)
**Time:** 18:11
**Artefact produced:** `journal/phase_6_vision.md` + `POST /inspect/vision/threshold` × 4

## Five dimensions

- **D1 Harm framing** — $4,200 per major-defect shipped vs $85 per false-scrap = 49:1 asymmetry on major + safety classes; $180 vs $85 = ~2:1 on minor_defect.
- **D2 Metric → cost linkage** — chosen threshold per class minimises (FN × FN-cost) + (FP × FP-cost) on the held-out set, EXCEPT safety_critical_defect which is HARD-floored at 0.40 (not cost-balanced — see decision moment 5).
- **D3 Trade-off honesty** — major_defect threshold 0.30 (lower than 0.50 default) moves the decision boundary toward catching FN at the cost of more FP. Quantified: at base rate 10%, threshold 0.30 vs 0.50 doubles FP rate to ~2× but cuts FN rate by ~3× — net cost decrease of ~$3,300/day at 12k events.
- **D4 Constraint classification** — safety_critical_defect threshold ≥ 0.40 is HARD (WSH + IPC-A-610 Class 3). Route refuses any POST below 0.40 with HTTP 409. Promote refuses with 409 if persisted threshold drops below floor at promote time. Both gates verified by /redteam (R2.23a returned 409).
- **D5 Reversal condition** — per-class FN rate trend up by > 0.05 for 7 days → re-tune threshold. Brier on safety_critical_defect drifts > 0.05 in 14 days → re-fit chosen arch.

## What I decided (live evidence from `/inspect/vision/leaderboard.promoted_thresholds`)

| Class                  | Threshold | Action        | Reasoning                                                                    |
| ---------------------- | --------- | ------------- | ---------------------------------------------------------------------------- |
| good                   | 0.50      | auto_pass     | Default release threshold; passing this routes the board to the line egress  |
| minor_defect           | 0.50      | manual_review | 2:1 cost ratio is balanced; route to inspector queue for human disposition   |
| major_defect           | 0.30      | auto_fail     | 49:1 asymmetry pulls threshold low; auto-scrap is cheaper than missed recall |
| safety_critical_defect | 0.40      | auto_fail     | HARD WSH floor; below this threshold the route refuses POST with 409         |

## Why

The asymmetry is per-class, not global. Safety-critical lives in regulator-mandated structural-hard land — the 0.40 floor is not a number we computed, it's a number IPC-A-610 Class 3 + WSH Act mandates and the API enforces. Major-defect is cost-balanced under 49:1 and the math drops the threshold to 0.30. Minor-defect at 2:1 sits at the default 0.50. The "good" class threshold is symmetric — passing the auto-pass line releases the board to egress.

## What I rejected

A single global threshold (0.50 for all classes) — silently averages the 49:1 asymmetry on major/safety with the 2:1 on minor, mis-prices safety. Tested via threshold POST below floor on safety_critical (0.20) — route returned 409 with WSH-cited error: "safety_critical_defect threshold 0.20 below WSH hard floor 0.40 (IPC-A-610 Class 3 + WSH Act). This class is structurally hard, not cost-balanced." Validated.

## Reversal condition

Per-class FN rate > 0.05 for 7 consecutive days on any class → retrain trigger AND threshold review. Per-class FP rate > 0.15 for 7 days → relax threshold one notch (0.30 → 0.35 on major_defect, etc.).

## Risks I am accepting

Major-defect threshold at 0.30 inflates the inspector manual-review queue by approximately 8% (more boards above 0.30 than above 0.50); accepted to keep safety_critical tight. Per-class FP rate elevated on minor_defect (2:1 ratio means we're slightly over-paying for FP); revisit at 14-day shadow checkpoint.
