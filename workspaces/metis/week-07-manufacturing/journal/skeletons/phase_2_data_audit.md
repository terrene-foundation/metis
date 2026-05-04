<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 2 — Data Audit

**Decision moment:** Is the labelled dataset trustworthy enough to ship a decision against?
**Sprint:** 1 (Vision QC) / 2 (PredMaint)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_2_data_audit.md`

## Five dimensions

- **D1 Harm framing** — labelling errors on the safety_critical class translate to what $ exposure?
- **D2 Metric → cost linkage** — what's the per-class base rate; how does it shape Phase 6 metric choice?
- **D3 Trade-off honesty** — what data wasn't collected (e.g., night-shift signal)? What's the bias?
- **D4 Constraint classification** — IPC-A-610 Class 3 traceability is hard (audit retention 7 years).
- **D5 Reversal condition** — what data-quality threshold flips this decision (e.g., labelling drift > 5%)?

## What I decided

<Per-class label counts; AOI false-positive rate floor; sensor-stream gaps; noting the 4-of-10 failing-machine sample size.>

## Why (in business terms)

<Cite `boards_labelled.csv` row counts and per-class base rates. Cite sensor stream coverage.>

## What I rejected

<"Pull more labels from the existing operator queue" — bias risk, queue triage already filters.>

## Reversal condition

<E.g.: per-class label noise > 5% triggers a re-labelling cycle.>

## Risks I am accepting

<E.g.: the 4 failing machines may not span all 7 defect modes.>
