<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · RL Process Optimization ★

**Decision moment:** Which policy do we promote (PPO / DQN / Random baseline)?
**Sprint:** 3 (RL)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_5_rl.md` + `POST /optimize/rl/promote`

## Five dimensions

- **D1 Harm framing** — wrong policy at the reflow oven = defect rate × throughput × $4,200.
- **D2 Metric → cost linkage** — expected return under chosen reward weights = $/day estimate.
- **D3 Trade-off honesty** — PPO needs continuous action space; DQN simpler but discretised.
- **D4 Constraint classification** — equipment damage envelope ($50K) and WSH ($1M) are hard floors.
- **D5 Reversal condition** — safety violation count > 0 in 1,000 simulated rollouts → de-promote.

## What I decided

<Policy: ppo_continuous. Avg return: <X>. Safety violations: <Y>.>

## Why

<PPO produces 0 hard-floor violations across 10,000 cached episodes; DQN ~10; Random ~419.>

## What I rejected

<DQN — same reward but ~10 safety violations, unacceptable above WSH ceiling.>

## Reversal condition

<Any safety_violation in /optimize/rl/simulate over 1,000 episodes → demote.>

## Risks I am accepting

<Cached transitions assume reflow-oven dynamics stay within the envelope the policy was trained on.>
