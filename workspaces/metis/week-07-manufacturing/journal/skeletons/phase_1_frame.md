<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 1 — Frame

**Decision moment:** What is THIS workshop's product trying to do, and for whom?
**Sprint:** 1 (Vision QC)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_1_frame.md`

## Five dimensions (rubric)

- **D1 Harm framing** — who bears what cost in named dollars from PRODUCT_BRIEF.md §2?
- **D2 Metric → cost linkage** — what's the headline metric and why does $4,200 vs $85 force its shape?
- **D3 Trade-off honesty** — what does the platform sacrifice if it ships AOI 78% recall as good enough?
- **D4 Constraint classification** — what's hard (WSH/IPC/$50K) vs soft (throughput, queue depth)?
- **D5 Reversal condition** — what would force you to re-frame? Customer mix shift? New defect mode?

## What I decided

<Name the four modules in scope (vision QC / predmaint / RL / agent), the WSH safety floor, and the 49:1 asymmetry as the framing constraint.>

## Why (in business terms)

<$4,200 FN vs $85 FP. $1M WSH ceiling. $50K equipment damage. Reviewer queue at $35/min × 1,400 boards × 3 min mean = $147K/day.>

## What I rejected

<"Just tune AOI thresholds" — would not address the $4,200/board recall risk on novel defect modes.>

## Reversal condition

<E.g.: customer mix shifts away from IPC-A-610 Class 3 → re-evaluate WSH floor; or a new defect mode appears with >0.05 base rate → retrain trigger.>

## Risks I am accepting

<E.g.: 800 labelled images is small for transfer learning; novel defect modes cold-start cost is $620/incident.>
