<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 3 — Feature Framing

**Decision moment:** What features are inputs to each module, and how do you frame them honestly?
**Sprint:** 1+2+3+4 — shared
**Time:** 18:03
**Artefact produced:** `journal/phase_3_features.md`

## Five dimensions

- **D1 Harm framing** — features that exclude minority customer segments (e.g. Class-2 boards under-sampled at 40%) → bias-shipped cost. Features keyed to specific machine ids encode line-2-bias.
- **D2 Metric → cost linkage** — feature engineering on sensor trend → predmaint precision lift in $. Hand-engineered features (mean/std/max/min/trend per channel) deliver the LightGBM win.
- **D3 Trade-off honesty** — rejected as too leaky: post-failure sensor reading (the fact of failure leaks into pre-failure features); RL features that include the agent's own previous action; vision features keyed to image filename (encodes labelling order).
- **D4 Constraint classification** — features that touch PII (operator names, badge IDs in safety images) are HARD-prohibited; restricted-zone footage is HARD-prohibited from leaving the local Jetson.
- **D5 Reversal condition** — feature drift > 0.25 PSI on any feature → re-engineer; per-feature quartile shift > 30% over 7 days → re-engineer.

## What I decided

**Vision**: frozen backbone (ResNet-50 / EfficientNet-B0 / ViT-Small) + task-specific classifier head (LR / RF / GBM). Embedding dimension differs per architecture (32 / 24 / 40) to mimic real backbone differences. **PredMaint**: hand-engineered statistical features per channel (vibration / motor current / head temperature / cycle count) — mean, std, max, min, linear trend (5 features × 4 channels = 20 features). **RL**: state = (5 zone temps, line speed, board class on line, minutes since last calibration). Action = ±5 °C per zone or hold + ±10 boards/min line speed. **Agent**: tools schema = `vision_classify`, `predict_failure`, `suggest_setpoint`, `log_safety_incident` — 4 tools, no chained reasoning at the agent layer.

## Why

Hand-engineered features beat raw sequence at 10-machine scale (LightGBM > LSTM pedagogy). Frozen-backbone transfer is the practical default at 800-image scale (ResNet wins; ViT data-hungry). Reflow-oven RL state is bounded enough that PPO converges on cached rollouts; agent tools schema is deterministic to keep audit-trail coherent.

## What I rejected

Raw spectrogram features for predmaint — too rich for 10-machine sample size (would over-fit); raw image bytes for vision — would drop from 0.98 macro_f1 (transfer) to ~0.65 (training from scratch on 800 imgs). Adding "operator who labelled" as a feature — IPC-A-610 Class 3 prohibits.

## Reversal condition

Drift PSI > 0.25 on any feature for 7 consecutive days → re-feature. Brier > 0.20 on chosen vision arch over 7 days → re-engineer (signal: backbone no longer matches data distribution).

## Risks I am accepting

Hand-engineered features will need refactor when the line adds a new sensor channel or the cycle-count granularity changes. Per-machine features encode the 10-machine sample's idiosyncrasy.
