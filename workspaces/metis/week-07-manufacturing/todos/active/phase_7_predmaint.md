<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 7 — Red-team (PredMaint)

**Sprint:** Sprint 2 · Predictive Maintenance · Time-Series ML · Predict
**Playbook phase:** Phase 7 — Red-team
**Trust-plane decision:** Run three Sprint-2-specific adversarial sweeps — sensor-noise robustness (vibration drift, current noise) / cross-machine generalisation (leakage between train and test machine splits — 4 of 10 machines have failures) / novel failure-mode (cold-start) — with pre-registered acceptance criteria. Decide which findings block Sprint 2's Phase 8 gate vs which become Phase 13 daily-cadence monitoring rules.
**Paste prompt:** `playbook/phase-07-redteam.md` §1 (PredMaint branch)
**Evaluation checklist:** `playbook/phase-07-redteam.md` §2
**Endpoints touched:** `POST /predict/maintenance/score` against held-out machine-windows (machine_id + window_days from the 432k-row sensor stream).
**Skeleton to copy:** `journal/skeletons/phase_7_red_team.md` → `journal/phase_7_predmaint.md`
**Acceptance criterion:** `journal/phase_7_predmaint.md` exists ≥ 500 bytes, lists three sweeps, each with: pre-registered acceptance threshold, observed result, severity (block / monitor / accept), and the Phase 13 daily-drift signal that catches it. Cross-machine generalisation case (a machine NOT seen in training) is one of the cases. Cold-start novel failure mode ($620/misclass per `business-costs.md`) is one of the cases.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 sweeps run, severity assigned
- [ ] Journal entry quotes pre-registered acceptance thresholds
- [ ] Cross-machine generalisation case explicitly run
- [ ] Moved to `todos/completed/` on human approval
