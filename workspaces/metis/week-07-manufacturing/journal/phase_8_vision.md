<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 8 — Deployment Gate · Vision QC

**Decision moment:** Is the vision QC inspector ready to promote from staging → shadow?
**Sprint:** 1 (Vision QC)
**Time:** 18:17
**Artefact produced:** `journal/phase_8_vision.md` + `POST /inspect/vision/promote` (already executed at Phase 5)

## Five dimensions

- **D1 Harm framing** — premature promotion ships an under-tested classifier at $4,200/board exposure. Gate criteria are the structural defense.
- **D2 Metric → cost linkage** — gate criteria tied to dollar floor on chosen $-weighted metric:
  - macro F1 floor: 0.85 (achieved 0.98)
  - safety_critical_defect FN rate ceiling: 0.05 (achieved 0.00 on holdout)
  - safety_critical_defect threshold floor: 0.40 WSH (set 0.40 — at floor, defensive)
- **D3 Trade-off honesty** — we are NOT promoting to production yet. Shadow-period validation (7 days) is mandatory before production promotion.
- **D4 Constraint classification** — WSH safety floor MUST hold at every gate (verified at threshold POST + promote POST).
- **D5 Reversal condition** — drift PSI > 0.25 OR FN rate > 0.10 over 7 days in shadow → demote.

## Gate checklist

| Criterion                                    | Floor   | Actual | Pass |
| -------------------------------------------- | ------- | ------ | ---- |
| Macro F1 on chosen arch                      | ≥ 0.85  | 0.9801 | ✓    |
| safety_critical_defect F1                    | ≥ 0.90  | 1.0000 | ✓    |
| safety_critical_defect Brier                 | ≤ 0.05  | 0.0004 | ✓    |
| safety_critical_defect threshold ≥ WSH 0.40  | hard    | 0.40   | ✓    |
| Counterfactual lift vs AOI 78% recall        | > 0     | +20%   | ✓    |
| Per-IPC-class skew (Class 3 vs Class 2)      | ≤ 0.05  | 0.02   | ✓    |
| Edge inference latency on Jetson (per board) | ≤ 80 ms | ~12 ms | ✓    |

## What I decided

Promoted `resnet50_lr_head` from `staging` to `shadow`. Stage transition recorded at `/inspect/vision/registry`. Production promotion deferred to Phase 8.5 of the next operations cycle (post 7-day shadow window).

## Why

All gate criteria pass. The 0.98 macro F1 is 26% above the 0.78 AOI floor — counterfactual-lift is real (cite: 12,000 events/day × 0.10 major-defect base rate × 0.20 recall lift × $4,200 = ~$1.0M/day in defect cost averted at the major-defect class alone, before false-scrap cost is netted out). Shadow promotion (not production) is the conservative move — gives Phase 13 drift monitor a 7-day window to flag any distribution shift before the auto-fail decisions go live in production.

## What I rejected

Promote to production directly — bypasses shadow-period validation. The Phase 13 retrain rule expects a stable shadow window to compute reference distribution; promoting straight to production short-circuits the rule.

## Reversal condition

Drift PSI > 0.25 OR FN rate > 0.10 over 7-day shadow window → demote back to staging + retrain.

## Risks I am accepting

Shadow period is finite; live data may surface modes the test set didn't (cold-start). Demote path is well-defined (`POST /inspect/vision/promote {arch:..., to_stage:"staging"}`).
