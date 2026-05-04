<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 8 — Deployment Gate (PredMaint)

**Sprint:** Sprint 2 · Predictive Maintenance · Time-Series ML · Predict
**Playbook phase:** Phase 8 — Deployment Gate
**Trust-plane decision:** Sign the PASS/FAIL gate for the predictive-maintenance classifier: chosen (family, window) pair + threshold defense + Phase 7 findings + held-out calibration check. On PASS, promote the chosen family to `shadow` stage; on FAIL, name the deficit and next action. No WSH hard-floor gate on this endpoint — calibration confirmation + degenerate-flag check are the substitutes.
**Paste prompt:** `playbook/phase-08-gate.md` §1 (PredMaint branch)
**Evaluation checklist:** `playbook/phase-08-gate.md` §2
**Endpoints touched:** `POST /predict/maintenance/promote`; `GET /predict/maintenance/leaderboard` for chosen-pair confirmation.
**Skeleton to copy:** `journal/skeletons/phase_8_gate.md` → `journal/phase_8_predmaint.md`
**Acceptance criterion:** `journal/phase_8_predmaint.md` exists ≥ 500 bytes, records PASS or FAIL with named criteria; if PASS, `predmaint_state.json` reflects the promoted family and the chosen window; degenerate-flag check explicitly cited.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — gate signed
- [ ] If PASS, `POST /predict/maintenance/promote` returned 200
- [ ] Moved to `todos/completed/` on human approval
