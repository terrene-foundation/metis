<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 8 — Deployment Gate

**Decision moment:** Is the chosen module ready to promote from staging → shadow?
**Sprint:** 1 / 2 / 3
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_8_gate.md` + `POST /<module>/promote`

## Five dimensions

- **D1 Harm framing** — premature promotion ships under-tested logic at $4,200/board.
- **D2 Metric → cost linkage** — gate criteria tied to dollar floor on chosen $-weighted metric.
- **D3 Trade-off honesty** — speed-to-shadow vs evidence-completeness.
- **D4 Constraint classification** — WSH safety floor MUST hold at every gate.
- **D5 Reversal condition** — shadow rollback signal (drift PSI > 0.25 OR FN rate > 0.10 for 7 days).

## What I decided

<Promote vision/predmaint/RL to shadow. Stage transition: staging → shadow.>

## Why

<Cite per-class metrics, hard-floor compliance, and rollout sample size.>

## What I rejected

<Promote to production directly — bypasses shadow-period validation.>

## Reversal condition

<Drift PSI > 0.25 OR FN rate > 0.10 over 7 days in shadow → demote.>

## Risks I am accepting

<Shadow period is finite; live data may surface modes the test set didn't.>
