<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (RL · policy choice)

**Sprint:** Sprint 3 · Process Optimization · Reinforcement Learning · Optimize
**Playbook phase:** Phase 5 — Implications (RL pass)
**Trust-plane decision:** Read the 3-policy RL leaderboard (`ppo_continuous` / `dqn_discrete` / `random_baseline`) and pick the policy. Defended on per-policy throughput / defect_rate / energy / safety_violation under the CURRENT reward weights. Recognise that "training" is re-scoring of cached transitions (F3.1 trap) — picking a policy here precedes setting reward weights at Phase 7 (★ decision moment 4).
**Paste prompt:** `playbook/phase-05-implications.md` §1 (RL branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** `GET /optimize/rl/leaderboard` (3 policies × current reward weights); `GET /optimize/rl/reward_function` to read the current weights + hard-floor table.
**Skeleton to copy:** `journal/skeletons/phase_5_rl.md` → `journal/phase_5_rl.md`
**Acceptance criterion:** `journal/phase_5_rl.md` exists ≥ 500 bytes, names the chosen policy, dollar defense via 2-3% throughput recovery on 40,000 boards/day × ~$60 contribution margin = $48,000-$72,000/day per `business-costs.md §"Decision anchors"`, F3.1 caveat documented (cached transitions, not re-trained policy), reward-function pre-registration cited (Phase 7 owns the weights — this phase picks the policy under the existing weights).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — chosen policy named
- [ ] Journal cites the 2-3% throughput-recovery dollar framing
- [ ] F3.1 (cached transitions, not re-trained) caveat called out
- [ ] Moved to `todos/completed/` on human approval
