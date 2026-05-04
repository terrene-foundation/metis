<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 2 — Data Audit

**Decision moment:** Is the labelled dataset trustworthy enough to ship a decision against?
**Sprint:** 1 (Vision QC) — shared with Sprint 2 (PredMaint)
**Time:** 18:01
**Artefact produced:** `journal/phase_2_data_audit.md`

## Five dimensions

- **D1 Harm framing** — labelling errors on the safety_critical class translate to $1M+ exposure per shipped defect under WSH; on minor_defect to $180 rework per board.
- **D2 Metric → cost linkage** — per-class base rates from `boards_labelled.csv`: good 63.5% / minor_defect 23.0% / major_defect 10.0% / safety_critical_defect 3.5%. Imbalance forces per-class P/R/F1 at Phase 6, NOT macro accuracy.
- **D3 Trade-off honesty** — what wasn't collected: night-shift AOI signal (Lines 2/3 only labelled day shifts), supplier-batch metadata (no traceability to BOM batch), inspector-confidence scores (binary fail/pass only). Bias: shift-time selection means the night-shift defect distribution is an extrapolation.
- **D4 Constraint classification** — IPC-A-610 Class 3 traceability is HARD: every inspection event MUST have an audit-trail entry retrievable for 7 years (the agent's `audit_id`).
- **D5 Reversal condition** — per-class label noise > 5% triggers a re-labelling cycle. Per-machine sensor data gap > 1 day triggers a stream audit.

## What I decided

Per-class label counts from the live `/health` boot — total 800 boards, 507 good / 185 minor / 78 major / 30 safety-critical. AOI baseline floor: 78% recall on true defects, 12% FP rate. Sensor stream: 30 days × 10 SMT machines × 1-min cadence = 432,000 rows; 4 of 10 machines have a labelled failure event in the window. RL: 10,000 cached episodes per policy.

## Why

The 30-board safety-critical sample is small for stratified train/test (375%+ FP rate hides easily on a 30-board class), and the per-class P/R/F1 leaderboard is the structural defense against a 96%-accurate-but-wrong-on-safety-critical model. Every threshold defended in Phase 6 must cite the per-class base rate explicitly.

## What I rejected

"Pull more labels from the existing operator queue" — bias risk, queue triage already filters; "Synthesise more safety-critical examples via augmentation" — risks training on the augmentations rather than the underlying defect modes.

## Reversal condition

Per-class label noise above 5% on any class → halt promote-to-shadow until re-labelling completes. Per-machine sensor gap > 1 day in 30-day window → drift trigger.

## Risks I am accepting

The 4 failing machines may not span all 7 defect modes (solder_bridge / missing_component / tombstone / cold_joint / scratch / contamination / none). The 10-machine sample for predmaint cannot discriminate cleanly between LSTM-shaped and Survival-Forest-shaped surrogates — see `journal/0002-RISK-predmaint-strict-ordering-overstated.md`.
