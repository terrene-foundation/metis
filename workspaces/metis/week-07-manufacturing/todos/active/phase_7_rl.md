<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 7 — RL Reward Function Weights ★

**Sprint:** Sprint 3 · Process Optimization · Reinforcement Learning · Optimize
**Playbook phase:** Phase 7 — Red-team (RL — reward function design)
**Trust-plane decision:** ★ Decision moment 4 of 5. Set the four reward function weights — `throughput`, `defect_cost`, `energy_cost`, `safety_penalty` — and prove with the leaderboard that the chosen weights do NOT reward-hack. `safety_penalty` MUST be ≥ `RL_HARD_FLOOR_SAFETY_PENALTY` (route refuses below with 422). Goodhart's Law check: the leaderboard MUST show your chosen weights produce defect rate below ceiling AND throughput at least 5% above the random baseline AND zero hard-floor violations — at full 10,000-episode simulate scale, NOT just the 500-episode promote bench (F3.2 trap).
**Paste prompt:** `playbook/phase-07-redteam.md` §1 (RL branch)
**Evaluation checklist:** `playbook/phase-07-redteam.md` §2
**Endpoints touched:** `POST /optimize/rl/reward_function` (sets the 4 weights — refuses safety_penalty below floor); `POST /optimize/rl/simulate` at `n_episodes=10000` with multiple seeds for full-bench reward-hack check; `GET /optimize/rl/leaderboard` for re-ranking under the new weights.
**Skeleton to copy:** `journal/skeletons/phase_7_red_team.md` → `journal/phase_7_rl.md`
**Acceptance criterion:** `journal/phase_7_rl.md` exists ≥ 500 bytes, names the four weights with arithmetic justifying each (throughput recovery in $, defect cost from $4,200 / $180, energy cost from $0.40/hr cloud or per-watt-hour line, safety_penalty floor cited from `RL_HARD_FLOOR_SAFETY_PENALTY` and `specs/compliance-floors.md`), Goodhart's Law check documented (the chosen weights produce zero hard-floor violations across at LEAST 10,000-episode simulate, not just the 500-episode promote bench), `POST /optimize/rl/reward_function` returned 200, `rl_reward_function.json` reflects the weights, equipment-damage $50K + WSH $1M ceilings explicitly named as hard floors NOT reward terms.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 4 weights POSTed
- [ ] Journal cites $4,200 / $180 / $50,000 / $1,000,000 / $0.40 from `PRODUCT_BRIEF.md §2`
- [ ] Full 10,000-episode simulate run (NOT just the 500-episode promote bench) — F3.2
- [ ] Hard floors explicitly named (NOT reward terms)
- [ ] Moved to `todos/completed/` on human approval
