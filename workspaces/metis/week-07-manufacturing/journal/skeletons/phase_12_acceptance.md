<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 12 — Solver Acceptance ★ (Agent Autonomy Ladder)

**Decision moment:** Set the agent autonomy ladder per task class.
**Sprint:** 3 (Agent)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_12_acceptance.md` + `POST /agent/policy`

## Five dimensions

- **D1 Harm framing** — over-autonomous agent on safety-critical action = WSH event.
- **D2 Metric → cost linkage** — agent autonomy mode × decision rate × $-impact-per-decision.
- **D3 Trade-off honesty** — shadow has lowest autonomy AND lowest dollar value; act has highest both.
- **D4 Constraint classification** — WSH-affecting task classes are hard-shadowed when MOM active.
- **D5 Reversal condition** — any safety_violation surfaced in /agent/audit → demote one rung.

## What I decided

<Per-task-class autonomy mode: vision_triage=recommend, maintenance_scheduling=recommend, setpoint_adjustment=recommend (or shadow if MOM), safety_alert=shadow.>

## Why

<Vision/maintenance are low-stakes; setpoint/safety are high-stakes per WSH.>

## What I rejected

<setpoint_adjustment=act — violates the WSH-affecting category rule.>

## Reversal condition

<Any safety_violation in /agent/audit OR drift PSI > 0.25 → demote.>

## Risks I am accepting

<Recommend mode introduces operator response-time latency on routine cases.>
