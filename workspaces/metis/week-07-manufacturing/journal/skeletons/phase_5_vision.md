<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · Vision QC ★

**Decision moment:** Which vision QC architecture do we promote (ResNet / EfficientNet / ViT)?
**Sprint:** 1 (Vision QC)
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_5_vision.md` + `POST /inspect/vision/promote`

## Five dimensions

- **D1 Harm framing** — picking a data-hungry architecture at 800 imgs ships under-trained recall.
- **D2 Metric → cost linkage** — macro_f1 differential × volume × $4,200 = $/day at stake.
- **D3 Trade-off honesty** — edge inference latency 80 ms/board vs accuracy gain.
- **D4 Constraint classification** — IPC-A-610 Class 3 100% inspection coverage is hard.
- **D5 Reversal condition** — labelled image count > 5,000 → re-evaluate ViT.

## What I decided

<Architecture chosen, macro_f1, per-class P/R/F1 from `/inspect/vision/leaderboard`.>

## Why

<ResNet expected to win at 800-img scale because ViT data-hungry. EfficientNet for edge-deployable second pick.>

## What I rejected

<ViT — under-trained at 800 imgs (cite macro_f1 gap).>

## Reversal condition

<Labelled image count > 5,000 AND ViT macro_f1 > ResNet by ≥ 0.05 → re-promote.>

## Risks I am accepting

<Frozen-backbone transfer may miss a defect mode the backbone never saw on ImageNet.>
