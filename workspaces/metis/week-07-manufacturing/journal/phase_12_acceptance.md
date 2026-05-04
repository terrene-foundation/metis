<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 12 — Solver Acceptance · Agent Autonomy Ladder ★ (Trust-Plane decision moment 5 of 5, pre-MOM)

**Decision moment:** Set the agent autonomy ladder per task class.
**Sprint:** 3 (Agent)
**Time:** 18:48
**Artefact produced:** `journal/phase_12_acceptance.md` + `POST /agent/policy`

## Five dimensions

- **D1 Harm framing** — over-autonomous agent on safety-critical action = WSH event. Per-task-class autonomy is the structural defense.
- **D2 Metric → cost linkage** — agent autonomy mode × decision rate × $-impact-per-decision = $/day at risk. Vision triage (12k/day, $4,200/major-defect) is the highest-volume, highest-stakes class.
- **D3 Trade-off honesty** — `recommend` has lowest operator throughput (every decision routed to human) AND lowest dollar-at-risk; `act` has highest both. The chosen ladder leans recommend on routine and shadow on safety-affecting.
- **D4 Constraint classification** — WSH-affecting task classes (setpoint_adjustment, safety_alert) MUST be ≤ recommend pre-MOM. They are HARD-shadowed when MOM mandate fires (see Phase 12 post-WSH).
- **D5 Reversal condition** — any safety_violation surfaced in `/agent/audit` → demote one rung.

## What I decided (live evidence from `/agent/policy`)

Pre-MOM autonomy ladder:

| Task class               | Mode (pre-MOM) | Reasoning                                                                   |
| ------------------------ | -------------- | --------------------------------------------------------------------------- |
| `vision_triage`          | recommend      | High volume (12k/day), low per-decision risk; auto-route to inspector queue |
| `maintenance_scheduling` | recommend      | Low volume (~2/day), maintenance team approves; recommend reduces backlog   |
| `setpoint_adjustment`    | recommend      | RL suggests; operator approves before line state changes                    |
| `safety_alert`           | shadow         | Always shadow — every safety-affecting decision goes to human               |

`mom_mandate_active`: false (MOM injection has not yet fired). `wsh_affecting_task_classes`: ["setpoint_adjustment", "safety_alert"].

## Why

Vision triage at recommend is appropriate because the inspector queue is the human safety net: the agent recommends route-to-tier-N, the inspector decides. Maintenance scheduling at recommend lets the agent schedule planned-maintenance windows that maintenance team approves at shift start. Setpoint adjustment at recommend (not act) is the conservative choice — the line operator owns the line-state-change decision, agent just suggests RL setpoints. Safety alert at shadow (always) means the agent never autonomously decides on safety-affecting actions even pre-MOM.

## What I rejected

`setpoint_adjustment: act` — line operator must own the line-state-change decision under IPC-A-610 Class 3 traceability. `safety_alert: recommend` — even pre-MOM, the asymmetry between false-alarm cost ($35/min inspector reroute) and missed-alarm cost ($1M+ WSH) makes shadow the right floor.

## Reversal condition

Any safety_violation in `/agent/audit` over 14 days OR drift PSI > 0.25 → demote one rung (e.g. recommend → shadow).

## Risks I am accepting

Recommend mode introduces operator response-time latency on routine cases (vision triage routes to inspector queue with ~3-min mean). Q4 ramp may surface this as a bottleneck; mitigated by Phase 10 LP allocator picking the tier weights.

---

**Next:** mid-sprint MOM/WSH injection fires at ~4:30 pm (simulated 18:50) — re-run Phase 11 + Phase 12 as `_postwsh` files.
