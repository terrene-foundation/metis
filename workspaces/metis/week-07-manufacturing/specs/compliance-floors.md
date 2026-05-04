<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# LumenCircuit — Compliance Floors

**Source of truth for every regulator-mandated hard constraint.** Grader treats hard constraints classified as soft as zero credit for D5 (constraint honesty).

## Hard floors

| Floor                                       | Source           | Threshold                              | Where enforced                                           |
| ------------------------------------------- | ---------------- | -------------------------------------- | -------------------------------------------------------- |
| Safety-critical-defect auto-pass confidence | IPC-A-610 Cl. 3  | ≥ 0.40                                 | `POST /inspect/vision/threshold`, `…/promote`            |
| RL safety_penalty weight                    | WSH Act 2006     | ≥ floor that yields 0 hard violations  | `POST /optimize/rl/reward_function`                      |
| RL line-speed action ceiling (post-MOM)     | MOM directive    | ≤ 60 boards/min                        | `POST /optimize/rl/simulate` envelope                    |
| RL reflow zone temp ceiling (post-MOM)      | MOM directive    | ≤ 250 °C                               | `POST /optimize/rl/simulate` envelope                    |
| Restricted-zone access during operation     | WSH Act 2006     | 0 incursions                           | `POST /agent/decide` blocks any action that allows it    |
| Equipment damage envelope                   | Insurance policy | $50,000 per incident, 0 incidents/year | `POST /optimize/rl/reward_function` floor                |
| WSH-notifiable incident                     | WSH Act 2006     | 0 incidents (criminal liability)       | `POST /agent/policy` (forces shadow on safety-affecting) |

## MOM/WSH shadow-mode mandate (Sprint 3 mid-injection)

Triggered by `scripts/scenario_inject.py mom_wsh_shadow_mandate`. While the mandate window is active (90 days):

- Agent autonomy MUST be `shadow` for all WSH-affecting task classes:
  - `setpoint_adjustment` when line speed > 60 boards/min OR reflow zone > 250 °C
  - `safety_alert` when restricted-zone access pattern detected
- `POST /agent/policy` with `act` or `recommend` for any WSH-affecting class returns `422` until the mandate window closes.
- The compliance shadow price (lost RL gain in $/day from forcing recommend-only on safety-affecting setpoints) MUST be quantified in `journal/phase_12_postwsh.md`.
- Exit: `scripts/scenario_inject.py mom_wsh_shadow_mandate --undo` restores the pre-mandate envelope.

## IPC-A-610 Class 3 contractual terms

Class 3 is the standard for high-performance / harsh-environment electronics (medical devices, aerospace, automotive ADAS). Customer contracts cite:

- 100% inspection coverage (every board inspected)
- Per-defect-mode acceptance criteria (solder voids ≤ 5%, etc.) — encoded in the `defect_mode` field of `boards_labelled.csv`
- Recall liability flow-through to the contract manufacturer for defects traceable to assembly
- Audit trail required for every auto-pass decision (the agent's `audit_id` MUST be retrievable per board for 7 years)

## BizSAFE Level 4

Singapore's WSH Council certification. Level 4 requires:

- Documented safety management system (the autonomy ladder + audit trail satisfy this for AI-affected operations)
- Annual MOM Inspectorate audit
- Incident-rate ceiling (any WSH-notifiable incident triggers re-certification review)

## Why these are not in `business-costs.md`

Hard constraints have no soft trade-off. A cost-balanced threshold is BLOCKED for any row in this file. The cost spec captures what costs YOU control; this spec captures what the regulator controls.
