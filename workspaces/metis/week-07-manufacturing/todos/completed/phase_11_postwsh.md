<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 11 — Constraints (post-WSH re-run) ★

**Sprint:** Sprint 3 · Process Optimization + Inspector Queue + Agent autonomy · Decide (post-injection at ~4:30 pm)
**Playbook phase:** Phase 11 — Constraints (post-MOM/WSH re-classification)
**Trust-plane decision:** ★ Decision moment 5 of 5 (re-class half). Re-classify the agent autonomy ladder: WSH-affecting task classes (`setpoint_adjustment`, `safety_alert`) are STRUCTURALLY hard-shadowed during the MOM mandate window. Flip RL line-speed ceiling (≤60 boards/min) and zone-temp ceiling (≤250 °C) from SOFT to HARD. Enumerate ALL endpoints the MOM mandate touches — agent autonomy, RL simulate envelope, RL reward function (already had safety_penalty floor) — so nothing slips (`failure-points.md` F3.3). Trigger fires via `src/manufacturing/scripts/scenario_inject.py mom_wsh_shadow_mandate` (instructor-launched OR student-launched per workshop staging).
**Paste prompt:** `playbook/phase-11-constraints.md` §1 (post-WSH branch)
**Evaluation checklist:** `playbook/phase-11-constraints.md` §2
**Endpoints touched:** `POST /agent/policy` (refused 422 if WSH-affecting class is non-shadow during mandate — defensive gate per `routes/agent.py::set_policy`); re-confirm `POST /optimize/rl/reward_function` weights still respect `RL_HARD_FLOOR_SAFETY_PENALTY`; `POST /optimize/rl/simulate` re-run under the post-MOM line-speed and zone-temp ceilings.
**Skeleton to copy:** `journal/skeletons/phase_11_postwsh.md` → `journal/phase_11_postwsh.md`
**Acceptance criterion:** `journal/phase_11_postwsh.md` exists ≥ 500 bytes, enumerates the THREE endpoints touched by the mandate (agent policy, RL simulate envelope, RL reward function), each with the new constraint state and rationale citing `PRODUCT_BRIEF.md §2` $1,000,000+ WSH ceiling and $50,000 equipment-damage; `agent_policy.json` shows `mom_mandate_active=True` and `setpoint_adjustment + safety_alert` both forced to `shadow`; F3.3 trap explicitly flagged in the journal (the MOM mandate touches three endpoints, not one).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — three endpoints touched
- [ ] `agent_policy.json` shows MOM mandate active and WSH-affecting classes hard-shadowed
- [ ] Journal quotes $1,000,000+ and $50,000 from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
