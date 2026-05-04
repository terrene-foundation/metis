<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 11 — Constraints (first pass · pre-WSH)

**Sprint:** Sprint 3 · Process Optimization + Inspector Queue + Agent autonomy · Decide
**Playbook phase:** Phase 11 — Constraints (first pass — pre-MOM/WSH injection)
**Trust-plane decision:** Classify all constraints across the queue allocator AND the agent autonomy ladder AND the RL simulate envelope as hard vs soft, with $ penalty for each soft. Inspector-minute budget = HARD (physics — 6 × 8 × 60 = 2,880). Per-tier SLA bounds (30 / 60 / 120 minutes) = SOFT. RL `safety_penalty` floor = HARD (route refuses below `RL_HARD_FLOOR_SAFETY_PENALTY`). Equipment-damage $50K and WSH $1M = HARD. MOM line-speed (≤60 boards/min) and zone-temp (≤250 °C) = SOFT in this first pass — they flip HARD in the post-WSH re-run. Agent autonomy ladder = first-pass freedom (set `recommend` or `act` on lower-stakes task classes).
**Paste prompt:** `playbook/phase-11-constraints.md` §1 (first-pass branch)
**Evaluation checklist:** `playbook/phase-11-constraints.md` §2
**Endpoints touched:** `POST /agent/policy` (sets autonomy ladder per task class); `POST /queue/solve` (first-pass with chosen queue_depth + inspector minutes); `GET /optimize/rl/reward_function` to read current hard-floor table.
**Skeleton to copy:** `journal/skeletons/phase_11_constraints.md` → `journal/phase_11_constraints.md`
**Acceptance criterion:** `journal/phase_11_constraints.md` exists ≥ 500 bytes, lists every constraint as hard or soft with rationale; soft constraints have a $ penalty per `business-costs.md`; inspector-minute cap (HARD — physics) named; RL safety_penalty floor (HARD) named; SLA windows (SOFT) named; agent autonomy first-pass values per task class declared with rationale; MOM line-speed/zone-temp ceilings explicitly noted as currently SOFT and reserved for the post-WSH re-run.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — constraints classified, agent autonomy POSTed
- [ ] WSH-affecting envelope flagged as currently soft, reserved for post-WSH
- [ ] Moved to `todos/completed/` on human approval
