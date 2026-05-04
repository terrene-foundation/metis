<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 12 — Solver Acceptance (post-WSH re-run) ★

**Sprint:** Sprint 3 · Process Optimization + Inspector Queue + Agent autonomy · Decide (post-injection)
**Playbook phase:** Phase 12 — Acceptance (post-MOM/WSH re-solve)
**Trust-plane decision:** ★ Decision moment 5 of 5 (re-solve half). Re-run the agent decide loop AND the RL simulate under the post-MOM hard-shadow envelope. Quantify the optimization shadow price (compliance cost in $/day of lost RL throughput gains because `setpoint_adjustment` is now `shadow` — every recommended setpoint requires human-in-the-loop confirmation). Disposition: ACCEPT (compliance cost is bearable) / FALL BACK (request waiver from MOM with regulatory citation) / REDESIGN (operate the line at lower throughput targets that don't trigger the WSH-affecting envelope). Skipping this re-write is the most common D3 (trade-off honesty) zero on the rubric.
**Paste prompt:** `playbook/phase-12-acceptance.md` §1 (post-WSH branch)
**Evaluation checklist:** `playbook/phase-12-acceptance.md` §2
**Endpoints touched:** `POST /agent/decide` against test contexts under hard-shadow autonomy (returns the new `autonomy_mode = shadow` for WSH-affecting classes); `POST /optimize/rl/simulate` re-run under the line-speed and zone-temp ceilings (response includes `line_speed_violations` and `temp_violations` — both must be 0 for the post-MOM envelope to be honoured); `POST /queue/solve` re-run if the inspector backlog shifts under the new shadow-mode workflow.
**Skeleton to copy:** `journal/skeletons/phase_12_postwsh.md` → `journal/phase_12_postwsh.md`
**Acceptance criterion:** `journal/phase_12_postwsh.md` exists ≥ 500 bytes, quotes `mean_return`, `safety_violations`, `line_speed_violations`, `temp_violations` directly from the post-mandate `simulate` response body; quantifies the compliance shadow price in $/day (lost RL throughput-recovery gains × workdays during the 90-day mandate window); disposition chosen with $-quantified rationale; first-pass `phase_12_acceptance.md` AND post-WSH `phase_12_postwsh.md` BOTH exist (auto-detected by `routes/state.py`).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — re-solve disposition recorded
- [ ] Compliance shadow price quantified in $/day
- [ ] Both `phase_12_acceptance.md` and `phase_12_postwsh.md` present in `journal/`
- [ ] Moved to `todos/completed/` on human approval
