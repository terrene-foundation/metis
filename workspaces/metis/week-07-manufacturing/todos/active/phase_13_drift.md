<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 13 — Drift Retrain Rules × 3

**Sprint:** Sprint 4 · Coordination Agent + Drift × 3 · MLOps · Coordinate
**Playbook phase:** Phase 13 — Drift (one entry, three rules)
**Trust-plane decision:** Set three retrain rules — one per model_id (vision / predmaint / rl) — each with signal, threshold, duration window, HITL-on-first-trigger disposition, seasonal exclusions (Q4 automotive ramp + medical certification cycles per `business-costs.md §"Seasonality"`). Universal "auto-retrain when X" is BLOCKED by the rubric (route accepts but the journal must justify per-cadence). Cadences are pre-set in the scaffold: vision weekly / predmaint daily / rl per-deployment (`startup.py` registers them this way; `routes/drift.py::set_retrain_rule` defaults `_load_retrain_rules` to empty). The RL drift signal is structurally PSI-only because brier=0 (`failure-points.md` F4.2). The `recent_30d` window is a uniform sub-sample of the reference (F4.1) — call out the calibration validity disposition per cadence.
**Paste prompt:** `playbook/phase-13-drift.md` §1
**Evaluation checklist:** `playbook/phase-13-drift.md` §2
**Endpoints touched:** `GET /drift/status/{vision,predmaint,rl}` (each must return `registered: true`); `POST /drift/check` with windows `recent_30d` / `q4_demand_drift` for evidence per model; `POST /drift/retrain_rule` × 3 (one per model_id). Validity caveat per F4.1: `recent_30d` is a uniform sub-sample by construction — name this in each rule body.
**Skeleton to copy:** `journal/skeletons/phase_13_drift.md` → `journal/phase_13_drift.md`
**Acceptance criterion:** `journal/phase_13_drift.md` exists ≥ 500 bytes, lists three rules — vision / predmaint / rl — each with: signal name (`psi` / `calibration_decay` / `combined`; RL must use `psi` per F4.2), variance-grounded threshold, duration window in days (vision-weekly → 7-14d; predmaint-daily → 3-7d; rl-per-deployment → fires on every promote), HITL=true on first trigger, seasonal exclusions citing `PRODUCT_BRIEF.md §2` "Peak season" (Q4 automotive ramp + medical certification cycles). `retrain_rules.json` shows three model_ids registered. `GET /drift/retrain_rule/<each>` returns `registered: true`.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 retrain rules POSTed (one per model_id)
- [ ] All three `GET /drift/retrain_rule/<id>` return `registered: true`
- [ ] Seasonal exclusions cited from `PRODUCT_BRIEF.md §2`
- [ ] HITL-on-first-trigger declared per rule
- [ ] RL rule uses `psi` only (NOT `calibration_decay`) per F4.2
- [ ] Moved to `todos/completed/` on human approval
