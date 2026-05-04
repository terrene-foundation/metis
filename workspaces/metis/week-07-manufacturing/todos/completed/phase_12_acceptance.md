<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 12 — Solver Acceptance (first pass · pre-WSH)

**Sprint:** Sprint 3 · Process Optimization + Inspector Queue + Agent autonomy · Decide
**Playbook phase:** Phase 12 — Acceptance (first pass — pre-MOM/WSH injection)
**Trust-plane decision:** Run the queue LP, the RL simulate, and the agent decide loop end-to-end under the first-pass constraints. Inspect feasibility + pathologies + per-tier coverage; pick disposition: ACCEPT / RE-TUNE objective / FALL BACK (demote a hard constraint with documented exception) / REDESIGN (expand inspector pool, shift SLA, change RL reward weights). Verify `feasibility: true` on the queue solve response body directly — don't trust the viewer alone.
**Paste prompt:** `playbook/phase-12-acceptance.md` §1 (first-pass branch)
**Evaluation checklist:** `playbook/phase-12-acceptance.md` §2
**Endpoints touched:** `POST /queue/solve` (writes `queue_last_plan.json` on feasibility); `GET /queue/last_plan`; `POST /optimize/rl/simulate` at chosen reward weights for full-bench check; `POST /agent/decide` against test contexts to confirm the autonomy ladder dispatches correctly.
**Skeleton to copy:** `journal/skeletons/phase_12_acceptance.md` → `journal/phase_12_acceptance.md`
**Acceptance criterion:** `journal/phase_12_acceptance.md` exists ≥ 500 bytes, quotes `feasibility`, queue-plan body fields, RL simulate `mean_return` + `safety_violations`, agent decide `audit_id` + `autonomy_mode` directly from response bodies; disposition (ACCEPT/RE-TUNE/FALL BACK/REDESIGN) chosen with rationale.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — disposition recorded with rationale
- [ ] Plan body fields cited verbatim
- [ ] Moved to `todos/completed/` on human approval
