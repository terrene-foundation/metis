<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 11 — Constraint Classification

**Decision moment:** Which constraints are hard, which soft, with the dollar penalty named?
**Sprint:** 3 (Queue + RL + Agent)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_11_constraints.md`

## Five dimensions

- **D1 Harm framing** — misclassifying a hard constraint as soft = WSH breach + criminal liability.
- **D2 Metric → cost linkage** — hard constraint penalty = $1M+ (WSH); $50K (equipment); $4,200/board (FN).
- **D3 Trade-off honesty** — soft constraints (queue depth, throughput) trade off inside the LP.
- **D4 Constraint classification** — see specs/compliance-floors.md for the full hard table.
- **D5 Reversal condition** — regulator update → re-classify (this happens during Phase 11 post-WSH).

## What I decided

<List every constraint with hard/soft tag and dollar penalty. WSH+IPC=hard. $50K equipment=hard. Inspector head-count=soft. Tier SLA=soft.>

## Why

<Hard constraints have non-optimisable penalty; soft constraints trade off inside the optimiser.>

## What I rejected

<"Treat $50K equipment as a soft penalty" — would let the optimiser trade equipment damage against throughput, structurally unsafe.>

## Reversal condition

<MOM/WSH directive change → re-classify (see Phase 11 post-WSH).>

## Risks I am accepting

<Some soft constraints may need to harden as the line scales.>
