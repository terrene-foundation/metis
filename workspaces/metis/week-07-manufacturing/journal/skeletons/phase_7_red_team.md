<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 7 — Red-Team · RL Reward Function ★

**Decision moment:** Set the four RL reward weights (throughput, defect_cost, energy_cost, safety_penalty).
**Sprint:** 3 (RL)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_7_red_team.md` + `POST /optimize/rl/reward_function`

## Five dimensions

- **D1 Harm framing** — Goodhart: max-throughput-only → agent skips quality, $4,200/board recall storm.
- **D2 Metric → cost linkage** — each reward weight maps to a $-equivalent cost term.
- **D3 Trade-off honesty** — safety_penalty very high → throughput drops; pin the dollar value of the trade.
- **D4 Constraint classification** — safety_penalty ≥ 0.50 is HARD (cached rollouts at lower → ≥ 1 violation).
- **D5 Reversal condition** — any safety_violation in 1,000 simulated rollouts under chosen weights → re-tune.

## What I decided

<Weights: throughput=<X>, defect_cost=<Y>, energy_cost=<Z>, safety_penalty=<W ≥ 0.50>. Avg return per policy under chosen weights.>

## Why

<Defends throughput recovery (~$48-72k/day target) without breaching the WSH or $50K equipment-damage floor.>

## What I rejected

<safety_penalty=0 — verified Random policy hits 419 violations across 10,000 episodes. Unacceptable.>

## Reversal condition

<Any safety_violation in /optimize/rl/simulate over 1,000 fresh episodes → freeze policy + escalate.>

## Risks I am accepting

<Reward function tuned offline; live distribution may shift relative weights.>
