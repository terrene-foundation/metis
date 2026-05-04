<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 6 — Metric + Threshold (PredMaint)

**Sprint:** Sprint 2 · Predictive Maintenance · Time-Series ML · Predict
**Playbook phase:** Phase 6 — Metric + Threshold
**Trust-plane decision:** Set the cost-balanced probability threshold for the chosen (family, window) pair against the $12,000 unplanned-stop vs $1,800 planned-stop asymmetry (6.7:1). Declare the action mapping — above threshold → `schedule_planned_maintenance`; below → `monitor`. Held-out calibration confirmation on the chosen pair, NOT in-sample (F2.2 trap).
**Paste prompt:** `playbook/phase-06-metric-threshold.md` §1 (Sprint 2 / PredMaint branch)
**Evaluation checklist:** `playbook/phase-06-metric-threshold.md` §2
**Endpoints touched:** `POST /predict/maintenance/threshold` (sets chosen probability threshold + action); `POST /predict/maintenance/calibrate` with `{method:"platt"|"isotonic"}` for post-hoc reliability evidence (NB: scaffold-side calibration is in-sample — call this out and treat the held-out check as a Phase 7 sweep input).
**Skeleton to copy:** `journal/skeletons/phase_6_metric_threshold.md` → `journal/phase_6_predmaint.md`
**Acceptance criterion:** `journal/phase_6_predmaint.md` exists ≥ 500 bytes, cost-balanced minimum threshold computed with arithmetic shown using $12,000 / $1,800, action mapping declared (above-threshold → `schedule_planned_maintenance`; below → `monitor`), `POST /predict/maintenance/threshold` returned 200, in-sample-calibration caveat documented per F2.2.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — threshold + action POSTed
- [ ] Journal entry quotes $12,000 / $1,800 from `PRODUCT_BRIEF.md §2`
- [ ] In-sample-calibration caveat named
- [ ] Moved to `todos/completed/` on human approval
