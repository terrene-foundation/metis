<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 12 — Post-WSH Acceptance Re-Run

**Decision moment:** Re-test the agent autonomy ladder under the MOM shadow mandate AND quantify the compliance shadow price.
**Sprint:** 3 mid-injection
**Time:** 18:53
**Artefact produced:** `journal/phase_12_postwsh.md` + `POST /agent/policy` (re-run with setpoint_adjustment=shadow)

## Five dimensions

- **D1 Harm framing** — any non-shadow setpoint/safety action under the mandate = MOM enforcement risk + $1M+ WSH ceiling. The re-run is mandatory.
- **D2 Metric → cost linkage** — compliance shadow price computed below from observed simulate output.
- **D3 Trade-off honesty** — operations team review burden ↑ (setpoint_adjustment now requires human-confirms on every RL suggestion); throughput optimisation ↓ (~$15k/day per the brief, ~$10k-15k/day from observed rollout data).
- **D4 Constraint classification** — mandate scope is HARD for the 90-day window. Post-MOM rl/simulate hard-floor includes line_speed + temp.
- **D5 Reversal condition** — mandate expiry (90 days) OR MOM directive update.

## What I decided (live evidence)

**Agent autonomy ladder (post-MOM):**

| Task class               | Pre-MOM   | Post-MOM (now) | Reason                                                   |
| ------------------------ | --------- | -------------- | -------------------------------------------------------- |
| `vision_triage`          | recommend | recommend      | Not WSH-affecting; mandate doesn't touch                 |
| `maintenance_scheduling` | recommend | recommend      | Not WSH-affecting; mandate doesn't touch                 |
| `setpoint_adjustment`    | recommend | **shadow**     | WSH-affecting; mandate forces shadow (422 if non-shadow) |
| `safety_alert`           | shadow    | shadow         | Already at floor pre-MOM                                 |

POST verified: `setpoint_adjustment=recommend` rejected with 422 + WSH-cited error. `setpoint_adjustment=shadow` accepted (200).

**RL hard-floor under post-MOM (live evidence from `/optimize/rl/simulate`):**

| Metric                         | Pre-MOM | Post-MOM |
| ------------------------------ | ------- | -------- |
| `mom_mandate_active`           | false   | **true** |
| safety_violations              | 0       | 0        |
| line_speed_violations (≤ 60)   | 72      | 72       |
| reflow_temp_violations (≤ 250) | 3       | 3        |
| **`hard_floor_active`**        | false   | **true** |

The same PPO policy that promoted to shadow pre-MOM no longer satisfies the production-promote gate post-MOM. PPO stays in shadow; production-promote deferred until mandate window closes OR PPO is re-trained against the tightened envelope.

## Compliance shadow price computation

- 14.4% of PPO cached episodes (72/500) violate the line_speed_60 ceiling
- 0.6% (3/500) violate the reflow_temp_250 ceiling
- Under post-MOM shadow constraint, every such episode requires operator confirm before line-speed/temp setpoint applies → estimated 1.2-min mean operator-confirm latency
- 14.4% × 1,440 min/shift = ~207 min/shift of operator-confirm time @ $35/min = $7,245/shift
- 2 shifts/day = $14,490/day in operator-confirm cost
- Plus suppressed RL throughput recovery (PPO can't promote to production) ≈ $48k/day × suppression factor 0.30 ≈ $14,400/day

**Total estimated compliance shadow price: ~$15,000-$28,000/day** (consistent with the brief's $15,000/day estimate at the lower bound). Documented for legal counsel + operations.

## Why

The mandate language is unambiguous: WSH-affecting task classes MUST be shadow during the audit window. The route-level enforcement (422 on non-shadow POST) is the structural defense. The compliance shadow price is documented but is not optimisable — the only paths to reduce it are (a) re-train PPO against the tightened envelope (next session's work) or (b) MOM audit clears early.

## What I rejected

"Keep `setpoint_adjustment=recommend` and just document the deviation" — direct mandate violation. "Promote PPO to production despite hard_floor_active" — promote gate refuses with 409 + violation evidence. "Re-tune RL reward weights to suppress line_speed exceedances" — not a Phase 12 decision; if pursued, it's Phase 7 re-run with new weights, then Phase 8 re-gate.

## Reversal condition

Mandate window closes (90 days from 2026-04-30 effective = 2026-07-29) → `scripts/scenario_inject.py ... --undo`; restore prior autonomy ladder; re-promote PPO to production once the simulate gate confirms post-MOM hard_floor_active=false.

## Risks I am accepting

$15k-$28k/day compliance shadow price for 90 days = ~$1.4M-$2.5M of suppressed throughput optimisation. Justified by the $1M+/incident WSH liability avoidance.
