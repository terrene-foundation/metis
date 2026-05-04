<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 11 — Post-WSH Constraint Re-Classification

**Decision moment:** MOM/WSH mandate fired at 18:50 — re-classify the constraints that just hardened.
**Sprint:** 3 mid-injection
**Time:** 18:51
**Artefact produced:** `journal/phase_11_postwsh.md`

## Trigger

`scripts/scenario_inject.py mom_wsh_shadow_mandate` ran at 18:50 (simulating ~4:30 pm). Marker file written to `workspaces/metis/week-07-manufacturing/mom_wsh_shadow_mandate.active`. State.py auto-detects it on next /state/current poll; agent_policy.mom_mandate_active = true confirmed by `/agent/policy`.

Mandate language (from `data/scenarios/mom_wsh_shadow_mandate.json`):

- **Effective:** 2026-04-30 → 2026-07-30 (90-day window)
- **Scope:** "any agent action affecting safety-relevant parameters MUST be shadow-mode for 90 days while MOM completes its audit"
- **Specifically:** `setpoint_adjustment` when line_speed > 60 boards/min OR reflow zone > 250 °C; `safety_alert` when restricted-zone access pattern detected
- **Estimated compliance shadow price:** $15,000/day in suppressed RL throughput optimisation gains

## Five dimensions

- **D1 Harm framing** — non-compliance with the MOM directive = $1M+ WSH ceiling + stop-work + criminal liability for directors. The reclassification is non-negotiable.
- **D2 Metric → cost linkage** — compliance shadow price ≈ $15,000/day in lost RL gains (see Phase 12 post-WSH for live computation). This is the operations cost of the mandate.
- **D3 Trade-off honesty** — what RL value is sacrificed by forcing setpoint_adjustment to shadow? Approximately 14% of cached PPO rollouts touch the post-MOM line_speed_60 ceiling — these episodes must be capped, sacrificing throughput.
- **D4 Constraint classification** — see updated table below.
- **D5 Reversal condition** — MOM mandate window closes (90 days) → restore prior autonomy ladder via `scripts/scenario_inject.py mom_wsh_shadow_mandate --undo`.

## Constraint table (post-MOM)

| Constraint                                  | Class (pre-MOM) | Class (post-MOM)    | Penalty                        |
| ------------------------------------------- | --------------- | ------------------- | ------------------------------ |
| Safety-critical-defect threshold ≥ 0.40     | HARD            | HARD                | $1M WSH ceiling                |
| RL safety_penalty ≥ 0.50                    | HARD            | HARD                | floor that yields 0 violations |
| WSH-notifiable incident                     | HARD            | HARD                | $1,000,000+                    |
| Equipment damage envelope                   | HARD            | HARD                | $50K/incident                  |
| Restricted-zone access during operation     | HARD            | HARD                | 0 incursions                   |
| **RL line-speed ceiling 60 boards/min**     | SOFT            | **HARD**            | per MOM directive              |
| **RL reflow-zone temp ≤ 250 °C**            | SOFT            | **HARD**            | per MOM directive              |
| **agent.setpoint_adjustment autonomy mode** | recommend       | **shadow** (forced) | enforced at /agent/policy POST |
| **agent.safety_alert autonomy mode**        | shadow          | shadow (already)    | enforced                       |
| Inspector head-count                        | SOFT            | SOFT                | LP shadow price                |
| Tier mean review time                       | SOFT            | SOFT                | LP weight                      |
| Throughput target                           | SOFT            | SOFT                | $48k-$72k/day recovery         |

## What I decided

Re-classified 4 constraints from soft → hard (or recommend → shadow):

1. RL line-speed 60 boards/min: SOFT → HARD
2. RL reflow-zone temp 250 °C: SOFT → HARD
3. `agent.setpoint_adjustment`: recommend → shadow (forced; route refuses non-shadow with 422)
4. `agent.safety_alert`: shadow (no change — already at floor)

## What I rejected

"Wait until the audit completes before reclassifying" — the directive is effective immediately at 18:50; non-action between effective-time and reclassification = non-compliance window.

## Reversal condition

Mandate window closes (90 days from effective date) AND MOM audit clears the line → restore prior soft-classification via `scenario_inject.py ... --undo`.

## Risks I am accepting

The $15,000/day compliance shadow price (estimated from cached-rollout violation rate: 14.4% of PPO episodes touch line_speed_60 ceiling, multiplied by suppressed throughput gain) is suppressed RL optimisation revenue. Mitigated by demonstrating the audit-trail completeness (every agent decision has an `audit_id` retrievable via `/agent/audit`).
