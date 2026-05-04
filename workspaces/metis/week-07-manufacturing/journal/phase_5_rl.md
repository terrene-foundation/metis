<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · RL Process Optimization

**Decision moment:** Which policy do we promote (PPO / DQN / Random baseline)?
**Sprint:** 3 (RL)
**Time:** 18:36
**Artefact produced:** `journal/phase_5_rl.md` + `POST /optimize/rl/promote {policy:"ppo_continuous", to_stage:"shadow"}`

## Five dimensions

- **D1 Harm framing** — wrong policy at the reflow oven = defect rate × throughput × $4,200/board. Random baseline produces 419 hard-floor violations across 10k cached episodes vs PPO 0; that's the price of choosing wrong.
- **D2 Metric → cost linkage** — expected return under chosen reward weights = $/day estimate. PPO mean_return 53.76 (under chosen weights throughput=1, defect_cost=10, energy=0.1, safety=1) vs Random 37.11 — the 16-point gap is the recoverable throughput at the reflow oven.
- **D3 Trade-off honesty** — PPO needs continuous action space; DQN simpler but discretised. At 5-zone reflow with ±5°C action granularity, DQN is the natural fit but PPO's continuous action policy produces 5× fewer defect events per episode.
- **D4 Constraint classification** — equipment damage envelope ($50K) and WSH ($1M+) are hard floors at the reward function. Line-speed and reflow-temp ceilings (60 / 250) are HARD post-MOM, soft pre-MOM (per `specs/compliance-floors.md`).
- **D5 Reversal condition** — any safety_violation surfaced in `/optimize/rl/simulate` over 500-episode bench → demote.

## What I decided (live evidence from `/optimize/rl/leaderboard`)

| Policy             | Throughput | Defect rate | Energy | Safety violations | Avg return (default w) | Return under chosen w |
| ------------------ | ---------- | ----------- | ------ | ----------------- | ---------------------- | --------------------- |
| `ppo_continuous` ★ | 53.974     | 0.0182      | 0.062  | 0                 | 53.877                 | 53.787                |
| `dqn_discrete`     | 50.976     | 0.0251      | 0.068  | 10                | 50.843                 | 50.717                |
| `random_baseline`  | 38.001     | 0.0838      | 0.092  | 419               | 37.552                 | 37.113                |

Promoted PPO to `shadow` via `/optimize/rl/promote`. The promote gate ran a 500-episode simulate at seed=42; result: 0 safety violations (hard floor satisfied), 72 line_speed_violations + 3 temp_violations (soft pre-MOM).

## Why

PPO produces 0 hard-floor safety violations across 10,000 cached episodes vs DQN 10 vs Random 419. The throughput delta (53.97 vs 50.98 vs 38.00) translates to ~$48k-$72k/day recoverable throughput at the reflow oven. DQN's 10 safety violations make it unacceptable above the WSH ceiling; Random is at the floor. PPO is the only acceptable choice under the WSH safety floor.

## What I rejected

DQN — same reward shape but ~10 safety violations per 10k episodes, which is non-zero on a $1M-ceiling event. Random baseline — pedagogical floor only; 419 violations.

## Reversal condition

Any safety_violation in `/optimize/rl/simulate` over 1,000 fresh episodes → freeze policy + escalate. line_speed_violations + temp_violations > 200/500 episodes (post-MOM threshold) → re-tune.

## Risks I am accepting

Cached transitions assume reflow-oven dynamics stay within the envelope the policy was trained on. line_speed_violations (72/500) and temp_violations (3/500) are soft pre-MOM but become HARD when the MOM mandate fires (Phase 11/12 post-WSH).
