<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 4 — Candidate Models · Vision QC

**Decision moment:** Which 3 vision-arch candidates are on the leaderboard for Sprint 1, and why those?
**Sprint:** 1 (Vision QC)
**Time:** 18:05
**Artefact produced:** `journal/phase_4_vision.md`

## Five dimensions

- **D1 Harm framing** — picking too few candidates (e.g. ResNet-only) risks under-exploration AND misses the edge-deployment trade-off (Jetson-class vs cloud).
- **D2 Metric → cost linkage** — each candidate must be scored on per-class P/R/F1 + Brier under the 49:1 asymmetry, NOT macro accuracy.
- **D3 Trade-off honesty** — what didn't make the leaderboard: YOLOv8 (object-detection, would need bounding-box labels we don't have); custom-trained CNN (no compute budget at 800-image scale).
- **D4 Constraint classification** — edge inference latency 80 ms/board is HARD on the line cameras (Jetson Nano class). Cloud inference would push the workshop's $0.001/board edge cost up by 30× and hit the 12,000-event/day at $360/day.
- **D5 Reversal condition** — sample > 5,000 images AND ViT macro_f1 > ResNet by ≥ 0.05 → add ViT-Large to the leaderboard. New defect mode → trigger feature re-engineering before adding a 4th arch.

## What I decided (live evidence from `/inspect/vision/leaderboard`)

Three architectures on the leaderboard, all transfer-learned from ImageNet-pretrained backbones with task-specific heads:

| Architecture                | Embed dim | Macro F1 | Why                                                                                       |
| --------------------------- | --------- | -------- | ----------------------------------------------------------------------------------------- |
| `resnet50_lr_head`          | 32d       | 0.9801   | Frozen ResNet-50 + linear head — robust, edge-deployable, fast inference                  |
| `efficientnet_b0_rf_head`   | 24d       | 0.5180   | Frozen EfficientNet-B0 + RF head — best accuracy/efficiency on Jetson, mid-tier macro F1 |
| `vit_small_gbm_head`        | 40d       | 0.3249   | Frozen ViT-Small + GBM head — data-hungry; under-trains at 800 images                    |

## Why these three

ResNet-50 is the practical default at 800-image transfer-learning scale (the inductive bias of conv layers handles small-image-count better than attention). EfficientNet-B0 is on the leaderboard because the deployment target is edge-Jetson, where the accuracy/MFLOPS ratio matters more than absolute accuracy. ViT-Small is on the leaderboard as the over-parameterised candidate — students see explicitly how attention under-performs at 800-image scale (the canonical "data-hungry" lesson).

## What I rejected

YOLOv8 — needs bounding-box annotations that the dataset does not have. Adding a 4th candidate (e.g. ConvNeXt) — confirmation bias risk: with 3 candidates spanning the inductive-bias spectrum the choice is defendable; a 4th adds noise without information.

## Reversal condition

If labelled image count grows > 5,000 AND ViT macro_f1 closes the gap to within 0.05 of ResNet → re-evaluate.

## Risks I am accepting

3-candidate leaderboards may miss a better-suited 4th option. Frozen-backbone transfer cannot adapt to defect modes ImageNet's pre-training did not see (electronics-specific texture).
