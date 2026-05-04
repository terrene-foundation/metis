<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 7 — Red-Team · RL Reward Function ★ (Trust-Plane decision moment 4 of 5)

**Decision moment:** Set the four RL reward weights (throughput, defect_cost, energy_cost, safety_penalty).
**Sprint:** 3 (RL)
**Time:** 18:39
**Artefact produced:** `journal/phase_7_rl.md` + `POST /optimize/rl/reward_function`

## Five dimensions

- **D1 Harm framing** — Goodhart: max-throughput-only → agent skips quality, $4,200/board recall storm. defect_cost too low → defect rate triples; safety_penalty too low → equipment crash.
- **D2 Metric → cost linkage** — each reward weight maps to a $-equivalent cost term:
  - throughput=1.0 anchors the optimisation
  - defect_cost=10.0 reflects the 10:1 defect-cost-per-throughput-unit ratio (each defect is ~10× more expensive than the marginal throughput it costs to avoid)
  - energy_cost=0.10 reflects edge inference + reflow energy (small relative to defect/safety)
  - safety_penalty=1.0 sits 2× above the hard floor of 0.50, ensuring zero hard-floor violations under the chosen leaderboard
- **D3 Trade-off honesty** — chose safety_penalty=1.0 not 0.50 (the floor). Reason: at 0.50 PPO's leaderboard return is 53.79; at 1.0 it's 53.76 — 0.03 cost. The defense-in-depth is worth 0.03 throughput points.
- **D4 Constraint classification** — safety_penalty ≥ 0.50 is HARD (cached rollouts at lower → ≥ 1 safety violation across 10k episodes). Verified: route refuses POST safety_penalty=0 with 422 + WSH-cited error.
- **D5 Reversal condition** — any safety_violation in 1,000 simulated rollouts under chosen weights → re-tune. defect_rate > 0.05 in 500-episode simulate → reduce defect_cost (currently 10) further.

## What I decided (live evidence from `/optimize/rl/reward_function`)

| Weight           | Value | Floor    | Defense                                                               |
| ---------------- | ----- | -------- | --------------------------------------------------------------------- |
| `throughput`     | 1.0   | 0        | anchor                                                                |
| `defect_cost`    | 10.0  | 0        | 10:1 defect-cost ratio (per business-costs.md $4,200 vs ~$420/min throughput contrib) |
| `energy_cost`    | 0.10  | 0        | small relative; energy is not the binding constraint                  |
| `safety_penalty` | 1.0   | **0.50** | 2× above the hard floor; 0 violations across 10k episodes             |

Hard-floor table (from `/optimize/rl/reward_function`):

```
safety_penalty_min: 0.50
line_speed_ceiling_boards_per_min: 60.0
reflow_temp_ceiling_celsius: 250.0
equipment_damage_dollars_per_incident: $50,000
wsh_notifiable_incident_dollars: $1,000,000
```

## Why

Set `safety_penalty=1.0` (2× hard floor) to defend against Goodhart-style optimisation pressure. The 10:1 `defect_cost`-to-`throughput` ratio reflects that each defective board costs ~$4,200 (recall) while each marginal throughput unit contributes ~$420 in revenue per minute — defect cost dominates. Energy is small (~$0.10/board variable cost) so weight=0.10 is right-sized.

## What I rejected

`safety_penalty=0` — verified Random policy hits 419 violations across 10k episodes; PPO drops to 0 violations only when safety_penalty ≥ 0.50. Hard floor is real, route returns 422 with the cached-rollout-evidence error message.

`defect_cost=5.0` (default) — too low; under that weight DQN's 2.5% defect rate looks acceptable. Bumping to 10.0 makes DQN's 10 safety_violations the dominant differentiator vs PPO's 0.

`safety_penalty=0.50` (at floor) — defendable but no defense-in-depth. Picked 1.0 to add 0.03-point return cost in exchange for 2× safety-margin.

## Reversal condition

Any safety_violation in `/optimize/rl/simulate` over 1,000 fresh episodes under chosen weights → freeze policy + escalate. defect_rate > 0.05 in 500-episode simulate → adjust defect_cost upward.

## Risks I am accepting

Reward function tuned offline against cached rollouts; live distribution may shift relative weights. The chosen `safety_penalty=1.0` adds defense-in-depth at the cost of 0.03 throughput points; if Q4 demand pressures push throughput target up, this becomes the constraint to revisit (defendable on safety grounds).
