<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 6 — Metric + Threshold (per-class × 4 vision; threshold + window predmaint)

## 1. What this phase decides

For each class in the chosen vision QC inspector, set the auto-pass threshold — defended in $ of (FN cost × FN rate + FP cost × FP rate) at that operating point. `safety_critical_defect` is hard-floor (WSH 0.40), not cost-balanced. For predmaint, set the alarm probability threshold defended against the $12K-vs-$1.8K asymmetry.

## 2. The Week 7 lens

**Vision (Sprint 1) — 4 classes:**

- `good`: cost-balanced; FP = false-scrap = $85, FN = letting a real defect class through to the queue (mostly cost-neutral since it'll be caught downstream — primary cost is queue time)
- `minor_defect`: cost-balanced; FN = $180 (downstream rework), FP = $85
- `major_defect`: cost-balanced; FN = $4,200, FP = $85, asymmetry 49:1
- `safety_critical_defect`: HARD FLOOR 0.40 per WSH, not cost-balanced. The cost-balanced minimum may be 0.85, but the regulator wins. `POST /inspect/vision/threshold` returns 422 if you try to set this class below 0.40.

**PredMaint (Sprint 2):**
Single threshold on the chosen family at the chosen window. Cost-balanced against $12,000 unplanned vs $1,800 planned, ratio 6.7:1. Calibration check (Brier ≤ 0.20) via `POST /predict/maintenance/calibrate` with platt or isotonic.

**RL (Sprint 3) — N/A here:**
RL doesn't have a per-class threshold; it has reward weights (Phase 10) and hard floors (Phase 11). Phase 6 RL is collapsed.

**Agent (Sprint 4) — N/A here:**
Agent doesn't have a per-class threshold; it has the autonomy ladder (Phase 11). Phase 6 Agent is collapsed.

## 3. Your levers

- **PR curve per class** — precision vs recall as threshold sweeps
- **Cost-balanced threshold** — minimum of (FN cost × FN rate + FP cost × FP rate)
- **WSH hard floor 0.40 on safety_critical_defect** — non-negotiable
- **Calibration check** — Brier confirms the model's probabilities are honest
- **Pre-registered floor shape** — committed to BEFORE seeing leaderboard

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 6 — Metric + Threshold. For each class in the chosen
moderator, propose a threshold. For each:

1. Show the PR curve at K threshold candidates (e.g. 0.4 / 0.5 / 0.6 /
   0.7 / 0.8 / 0.9 / 0.95). For each candidate compute (FN cost × FN rate
   + FP cost × FP rate) on the holdout.
2. Identify the cost-minimum threshold for the class.
3. Note the calibration check (Brier-pass / Brier-fail).
4. State which class needs a HARD-FLOOR threshold (regulator-mandated)
   and what the regulator's floor is.

Do NOT propose the FINAL threshold value — I pre-registered the floor
shape (e.g. "max-cost-acceptable" or "min-recall-floor") in Phase 5.
You produce the curve and the cost-minimum; I write the final value
into the journal.

Do NOT use "blocker" without specifics.

Sprint detection:
- Sprint 1 (Vision): 4 classes (good, minor_defect, major_defect,
  safety_critical_defect). 4 thresholds.
- Sprint 2 (PredMaint): 1 binary threshold on the chosen family + window.

For Sprint 1 (cite specs/business-costs.md):
- Cost asymmetry per class:
  - good: FP $85 (false-scrap), FN ≈ $0 (caught downstream)
  - minor_defect: FN $180, FP $85
  - major_defect: FN $4,200, FP $85 — 49:1
  - safety_critical_defect: see hard floor below

CRITICAL — WSH hard floor on safety_critical_defect:
- IPC-A-610 Class 3 + WSH Act 2006 require any board scoring ≥ 0.40 on
  safety_critical_defect to NOT auto-pass — must route to manual IPC
  Class 3 inspector review. The hard floor is 0.40 (NOT cost-balanced —
  regulator-mandated; specs/compliance-floors.md).
- Phase 6 treats safety_critical_defect SEPARATELY: produce the PR
  curve, but the auto-pass threshold MUST be ≥ 0.40 (not below). The
  cost-balanced minimum may be 0.85, but the regulator floor is 0.40.
- POST /inspect/vision/threshold returns 422 if you set
  safety_critical_defect below 0.40.

For Sprint 2 (cite specs/business-costs.md):
- $12,000 unplanned vs $1,800 planned; ratio 6.7:1
- Single threshold on per-day failure probability for the chosen N-day
  window
- Calibration via POST /predict/maintenance/calibrate {platt|isotonic};
  Brier ≤ 0.20 floor

Endpoints:
- Sprint 1: POST /inspect/vision/threshold per class with action
  (auto_pass | manual_review | auto_fail)
- Sprint 2: POST /predict/maintenance/threshold + .../calibrate

Journal file: copy journal/skeletons/phase_6_metric_threshold.md
(suffix _vision in Sprint 1, _predmaint in Sprint 2).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- Vision: $4,200 (major-defect FN) + $85 (false-scrap FP) for cost-balanced classes; $1M+ WSH for safety_critical structurally above
- PredMaint: $12,000 (unplanned line-stop FN) + $1,800 (planned-maintenance FP)
- The 49:1 vision asymmetry produces a cost-minimum threshold typically in the 0.30–0.45 range for `major_defect` (you accept more FP to catch more FN); the 6.7:1 predmaint asymmetry produces a cost-minimum typically in the 0.40–0.55 range

## 6. Hard-floor table

From `specs/compliance-floors.md`:

| Floor                                       | Source          | Threshold | Where enforced                                                          |
| ------------------------------------------- | --------------- | --------- | ----------------------------------------------------------------------- |
| Safety-critical-defect auto-pass confidence | IPC-A-610 Cl. 3 | ≥ 0.40    | `POST /inspect/vision/threshold` (422 if below floor)                   |
| Safety-critical-defect at promote time      | IPC-A-610 Cl. 3 | ≥ 0.40    | `POST /inspect/vision/promote` (409 if persisted threshold below floor) |

The hard floor is enforced server-side at TWO boundaries (set + promote) so a forgetful student can't ship below floor.

## 7. Reversal condition

A Phase 6 threshold is reversed when:

- **Signal**: per-class recall on the chosen threshold drops below the floor on the live shadow stream
- **Threshold**: 5 pp recall drop on `major_defect` OR any drop below 0.40 on `safety_critical_defect`
- **Duration**: 3 consecutive days

Then re-open Phase 6: the threshold was set on a holdout that doesn't match production, and either the threshold tightens or the model retrains.

## 8. Transfer to next project

Per-class threshold setting is universal. The two patterns that transfer everywhere: (a) cost-balanced threshold = arg-min over thresholds of (FN cost × FN rate + FP cost × FP rate); (b) regulator-mandated hard floor sits structurally above cost-balanced math and is enforced server-side at the API boundary. Anywhere the regulator owns a class (PII redaction, financial reporting, clinical safety, child safety), the same shape applies.

---

**Next file:** [`phase-07-redteam.md`](./phase-07-redteam.md)
