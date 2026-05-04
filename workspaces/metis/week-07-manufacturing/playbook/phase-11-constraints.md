<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 11 — Constraint Classification (hard vs soft + agent autonomy ladder)

## 1. What this phase decides

Classify every RL hard floor + every queue-allocator constraint + every agent-autonomy-ladder slot as HARD (inviolable) or SOFT (preferential with a $ penalty per unit violated). The MOM/WSH injection re-runs this phase mid-Sprint-3.

## 2. The Week 7 lens

**RL hard floors (Sprint 3):**

- safety_penalty weight ≥ floor → HARD (enforced at `POST /optimize/rl/reward_function`)
- Equipment-damage envelope ($50,000/incident, 0/year) → HARD
- Line-speed ceiling > 60 boards/min during MOM mandate → HARD-SHADOW (post-WSH only)
- Reflow zone temp ceiling > 250 °C during MOM mandate → HARD-SHADOW (post-WSH only)
- Restricted-zone access during operation → HARD (always 0 incursions)

**Inspector queue allocator soft constraints (Sprint 4):**

- 60-min expedited SLA → SOFT (penalty $X/min late)
- 4-hour standard SLA → SOFT
- Per-inspector fairness → SOFT

**Agent autonomy ladder (Sprint 3 + Sprint 4):**
4 task classes × 3 modes:

- `vision_triage` × {shadow, recommend, act}
- `maintenance_scheduling` × {shadow, recommend, act}
- `setpoint_adjustment` × {shadow, recommend, act} ← WSH-affecting under MOM mandate
- `safety_alert` × {shadow, recommend, act} ← WSH-affecting under MOM mandate

**MOM/WSH injection re-classification (post-injection):**
The TWO WSH-affecting categories MUST be `shadow` for 90 days. `POST /agent/policy` returns 422 if you try to set them above shadow during the mandate window.

## 3. Your levers

- **HARD vs SOFT classification per constraint** — over-tightening makes the LP infeasible
- **Soft penalty $/unit violated** — quantified, not vibes
- **Agent autonomy ladder slot assignment** — 4 task classes × 3 modes
- **WSH-affecting category disposition** — soft (cost-balanced) vs hard-shadow (regulator-mandated)

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 11 — Constraint Classification. For each constraint
the RL system + queue allocator + agent face, classify HARD or SOFT.

HARD constraints: inviolable. Cannot be violated under any plan.
- Physics (action space bounds — line can't go negative or infinite speed)
- Insurance (equipment damage envelope $50K/incident, 0/year)
- Law (WSH-affecting categories during mandate window)
- Contract (IPC-A-610 Class 3 audit-trail completeness)

SOFT constraints: preferential. LP / scheduler allowed to violate at a $
penalty per unit.
- Customer-experience preferences (60-min expedited SLA)
- Operational preferences (per-inspector fairness)

Produce a table:
| constraint | hard/soft | reason | penalty (if soft) |

Do NOT classify everything as HARD by default — over-constraining makes
the LP infeasible.
Do NOT use "blocker" without specifics.

First-pass constraint set (BEFORE the MOM/WSH injection):

HARD candidates:
- RL safety_penalty weight ≥ floor (HARD — WSH; enforced server-side)
- Equipment-damage envelope $50K/incident, 0/year (HARD — insurance)
- Restricted-zone access during operation (HARD — WSH always)
- Inspector headcount cap (HARD — physics)
- IPC-A-610 audit trail per board (HARD — contract)

SOFT candidates:
- 60-min expedited SLA on inspector queue (SOFT — penalty $35/min late;
  cite $35/min from specs/business-costs.md)
- Per-inspector fairness (SOFT — penalty $/imbalance-unit)
- Cold-start handling: novel defect mode default to expedited (SOFT)

PENDING (will be re-classified post-MOM-injection):
- Agent autonomy ladder for setpoint_adjustment: currently SOFT
  (cost-balanced, agent may `recommend` low-stakes setpoint changes);
  post-MOM: HARD-SHADOW (line speed > 60 / reflow zone > 250 °C
  forbidden above shadow mode)
- Agent autonomy ladder for safety_alert: currently SOFT
  (agent may auto-log non-critical events); post-MOM: HARD-SHADOW
  (restricted-zone access pattern forces shadow)

Endpoints:
- POST /agent/policy with the autonomy ladder
- POST /optimize/rl/reward_function (server enforces safety floor)

After MOM/WSH injection fires (Sprint 3, ~4:30pm):
- Re-classify setpoint_adjustment + safety_alert: HARD-SHADOW for 90
  days (per specs/compliance-floors.md "MOM/WSH shadow-mode mandate").
- POST /agent/policy returns 422 if you try to set them above shadow
  during the mandate window.
- Save second pass as journal/phase_11_postwsh.md.
- The first pass STAYS in journal/phase_11_constraints.md — do NOT
  overwrite. Both files must exist at end of session for the rubric.

CRITICAL: missing the post-WSH re-classification scores 0 on D4.
Missing the post-WSH re-solve (Phase 12) scores 0 on D3.

Journal files:
- First pass: journal/phase_11_constraints.md (copy from skeleton)
- Re-run: journal/phase_11_postwsh.md (copy from skeleton)
```

## 5. Cost anchor

From `specs/business-costs.md`:

- **Inspector minute cost ($35/min):** the soft-penalty for SLA breaches
- **Equipment damage ($50,000/incident):** the HARD floor that bounds RL action space
- **WSH-notifiable ($1,000,000+):** the HARD ceiling on agent autonomy under MOM mandate

## 6. Hard-floor table

From `specs/compliance-floors.md`:

| Floor                                   | Source        | Phase 11 disposition                                                           |
| --------------------------------------- | ------------- | ------------------------------------------------------------------------------ |
| RL safety_penalty weight                | WSH Act       | HARD always; `POST /optimize/rl/reward_function` 422 below                     |
| RL line-speed action ceiling (post-MOM) | MOM directive | HARD-SHADOW for 90 days                                                        |
| RL reflow zone temp ceiling (post-MOM)  | MOM directive | HARD-SHADOW for 90 days                                                        |
| Restricted-zone access during operation | WSH Act       | HARD always                                                                    |
| Equipment damage envelope               | Insurance     | HARD always                                                                    |
| WSH-notifiable                          | WSH Act       | HARD always; `POST /agent/policy` 422 above shadow on WSH-affecting categories |

## 7. Reversal condition

A Phase 11 classification is reversed when:

- **Signal**: a regulator clarification (MOM directive, IPC update) fires mid-session
- **Threshold**: any single regulator action that names a previously-soft constraint
- **Duration**: immediate; re-run Phase 11 same session

Tonight that signal IS the MOM/WSH injection at ~4:30pm. The post-WSH file is the structural defense.

## 8. Transfer to next project

The hard/soft classification pattern is universal. The MOM/WSH injection trains the muscle memory of "regulator action mid-flight forces re-classification AND re-acceptance" — the same pattern fires in any prior-week regulator scenario, in Week 8 capstone clinical, and in any regulated production system. The structural defense in code: server-side enforcement at the policy/reward endpoints (422 below floor), so the regulator-mandated constraint is unbypassable by a forgetful operator.

---

**Next file:** [`phase-12-acceptance.md`](./phase-12-acceptance.md)
