<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 13 — Drift Retrain Rules × 3

**Sprint:** Sprint 4 · MLOps · Monitor
**Playbook phase:** Phase 13 — Drift (one entry, three rules)
**Trust-plane decision:** Set three retrain rules — one per model_id (image / text / fusion) — each with signal, threshold, duration window, HITL-on-first-trigger disposition, seasonal exclusions (election cycles + major news events). Universal "auto-retrain when X" is BLOCKED by the rubric (and the route accepts but the journal must justify per-cadence). Cadences are pre-set in the scaffold: image weekly / text daily / fusion per-incident (`startup.py` registers them this way; `routes/drift.py::_load_retrain_rules` defaults them all to null). (Decision moment 5 of 5.)
**Paste prompt:** `playbook/phase-13-drift.md` §1
**Evaluation checklist:** `playbook/phase-13-drift.md` §2
**Endpoints touched:** `GET /drift/status/image_moderator`, `GET /drift/status/text_moderator`, `GET /drift/status/fusion_moderator` (must each return `reference_set: true`); `POST /drift/check` with windows `recent_30d` / `imda_csam_mandate` / `election_cycle_drift` for evidence; `POST /drift/retrain_rule` × 3 (one per model_id). Validity caveat: `recent_30d` is a calm-state sub-sample (`_simulate_recent_30d`) — `failure-points.md` F4.2 — call this out in the rule body.
**Skeleton to copy:** `journal/skeletons/phase_13_retrain.md` → `journal/phase_13_retrain.md`
**Acceptance criterion:** `journal/phase_13_retrain.md` lists three rules — image / text / fusion — each with: signal name, variance-grounded threshold, duration window in days, HITL=true on first trigger, seasonal exclusions citing `PRODUCT_BRIEF.md §2` "Peak season". `drift_retrain_rules.json` shows `set_count == 3`. `GET /drift/retrain_rule` returns `complete: true`. (`routes/state.py::_decision_moments_completed` flips decision moment 5 green only when phase_13_retrain.md is journaled AND the JSON shows 3 set rules.)

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 retrain rules POSTed
- [ ] `GET /drift/retrain_rule` returns `complete: true`
- [ ] Seasonal exclusions cited from `PRODUCT_BRIEF.md §2`
- [ ] HITL-on-first-trigger declared per rule
- [ ] Moved to `todos/completed/` on human approval
