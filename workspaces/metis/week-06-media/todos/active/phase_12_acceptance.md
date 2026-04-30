<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 12 — Solver Acceptance (first pass)

**Sprint:** Sprint 3 · Fusion + Queue · Decide
**Playbook phase:** Phase 12 — Acceptance (first pass — pre-IMDA)
**Trust-plane decision:** Run the LP, inspect feasibility + pathologies, pick disposition: ACCEPT / RE-TUNE objective weights / FALL BACK (demote a hard constraint) / REDESIGN (expand senior headcount, shift SLA). Verify `feasibility: true` on the response body directly — don't trust the viewer card alone (`failure-points.md` F3.3).
**Paste prompt:** `playbook/phase-12-acceptance.md` §1 (first-pass branch)
**Evaluation checklist:** `playbook/phase-12-acceptance.md` §2
**Endpoints touched:** `POST /queue/solve` (writes `queue_last_plan.json` on feasibility); `GET /queue/last_plan` for the persisted plan; `GET /queue/state` for headcount + capacity context.
**Skeleton to copy:** `journal/skeletons/phase_12_accept.md` → `journal/phase_12_acceptance.md`
**Acceptance criterion:** `journal/phase_12_acceptance.md` quotes `feasibility`, `total_sla_breach_minutes`, `reviewer_cost_total`, and the `pathologies` list directly from the solver's response body; disposition (ACCEPT/RE-TUNE/FALL BACK/REDESIGN) chosen with rationale.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — disposition recorded with rationale
- [ ] Plan body fields cited verbatim in journal
- [ ] Moved to `todos/completed/` on human approval
