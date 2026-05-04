<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (PredMaint) ★

**Sprint:** Sprint 2 · Predictive Maintenance · Time-Series ML · Predict (replay)
**Playbook phase:** Phase 5 — Implications
**Trust-plane decision:** ★ Decision moment 3 of 5. Pick the predictive-maintenance prediction window (3 / 7 / 14 days) AND family (LightGBM / LSTM / Survival Forest) — defended jointly, NOT independently (`failure-points.md` F2.1 is the trap). Defended in $ of unplanned-stop ($12,000) avoidance vs planned-maintenance ($1,800) overhead — 6.7:1 ratio per `business-costs.md §"Decision anchors"`. Held-out calibration check on the chosen pair (NOT in-sample — F2.2 is the trap).
**Paste prompt:** `playbook/phase-05-implications.md` §1 (PredMaint branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** `GET /predict/maintenance/leaderboard`; `POST /predict/maintenance/window` to set chosen window; `POST /predict/maintenance/family` to set chosen family.
**Skeleton to copy:** `journal/skeletons/phase_5_predmaint.md` → `journal/phase_5_predmaint.md`
**Acceptance criterion:** `journal/phase_5_predmaint.md` exists ≥ 500 bytes, names the chosen (family, window) PAIR jointly, dollar defense via $12,000 / $1,800 unplanned-vs-planned asymmetry (6.7:1), in-sample-calibration caveat documented (F2.2), retrain-cadence implication for Phase 13 named (predmaint is daily — A9), `POST /predict/maintenance/window` and `POST /predict/maintenance/family` both returned 200.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — (family, window) pair POSTed via both endpoints
- [ ] Journal cites $12,000 and $1,800 from `PRODUCT_BRIEF.md §2`
- [ ] In-sample-calibration caveat called out
- [ ] Moved to `todos/completed/` on human approval
