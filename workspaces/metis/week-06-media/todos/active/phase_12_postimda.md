<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 12 — Solver Acceptance (post-IMDA re-run)

**Sprint:** Sprint 3 · Fusion + Queue · Decide (post-injection)
**Playbook phase:** Phase 12 — Acceptance (post-IMDA re-solve)
**Trust-plane decision:** Re-run the LP under the new HARD CSAM-adjacent constraint, quantify the compliance cost from the plan body's `compliance_cost_imda` field — that is the shadow price of the IMDA mandate in dollars of senior-reviewer time. Disposition: ACCEPT (compliance cost is bearable) / FALL BACK (demote the hard constraint with regulatory waiver) / REDESIGN (expand senior pool to make the LP feasible). Skipping this re-write is the most common D3 zero on the rubric. (Decision moment 4 of 5, re-solve half.)
**Paste prompt:** `playbook/phase-12-acceptance.md` §1 (post-IMDA branch)
**Evaluation checklist:** `playbook/phase-12-acceptance.md` §2
**Endpoints touched:** `POST /queue/solve` (re-solve under the IMDA-active constraint set); `GET /queue/last_plan` for the persisted plan. If the LP returns `feasibility: false`, the response includes a `hint` string — copy it verbatim into the journal as the framing for FALL BACK / REDESIGN.
**Skeleton to copy:** `journal/skeletons/phase_12_postimda.md` → `journal/phase_12_postimda.md`
**Acceptance criterion:** `journal/phase_12_postimda.md` quotes `compliance_cost_imda` (or the infeasibility hint, if applicable) directly from the response body; disposition chosen with $-quantified rationale; first-pass `phase_12_acceptance.md` and post-IMDA `phase_12_postimda.md` both exist (auto-detected by `routes/state.py::_decision_moments_completed` to flip decision moment 4 green).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — re-solve disposition recorded
- [ ] `compliance_cost_imda` (or infeasibility `hint`) quoted verbatim in journal
- [ ] Both `phase_12_acceptance.md` and `phase_12_postimda.md` present in `journal/`
- [ ] Moved to `todos/completed/` on human approval
