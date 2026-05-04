<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 6 — Metric + Threshold ★ (Vision QC)

**Decision moment:** Per-class auto-pass threshold for vision QC, with WSH floor on safety_critical.
**Sprint:** 1 (Vision QC)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_6_metric_threshold.md` + `POST /inspect/vision/threshold` (× 4 classes)

## Five dimensions

- **D1 Harm framing** — $4,200 per major-defect shipped vs $85 per false scrap = 49:1 asymmetry.
- **D2 Metric → cost linkage** — chosen threshold minimises (FN × $4,200) + (FP × $85) on the test set.
- **D3 Trade-off honesty** — recall-heavy thresholds inflate the inspector queue (tradeoff in $/min).
- **D4 Constraint classification** — safety_critical_defect threshold ≥ 0.40 is HARD (WSH + IPC-A-610 Class 3).
- **D5 Reversal condition** — per-class FN rate trend up by > 0.05 for 7 days → re-tune threshold.

## What I decided

<Per-class thresholds: good=<X>, minor=<Y>, major=<Z>, safety_critical=<W ≥ 0.40>. Action mapping per class.>

## Why

<Cost-balanced thresholds for non-safety classes; WSH floor 0.40 for safety_critical (cite specs/compliance-floors.md).>

## What I rejected

<A single global threshold — under-prices the safety_critical class and over-prices minor.>

## Reversal condition

<Per-class FN rate > 0.05 for 7 consecutive days → retrain trigger AND threshold review.>

## Risks I am accepting

<Per-class threshold inflation on minor adds queue load (~$X/day); accepted to keep safety_critical tight.>
