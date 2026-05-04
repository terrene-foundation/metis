<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 3 — Feature Framing

**Decision moment:** What features are inputs to each module, and how do you frame them honestly?
**Sprint:** all 4
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_3_features.md`

## Five dimensions

- **D1 Harm framing** — features that exclude minority customer segments → bias-shipped cost.
- **D2 Metric → cost linkage** — feature engineering on sensor trend → predmaint precision lift in $.
- **D3 Trade-off honesty** — what features were rejected as too leaky (e.g., post-failure sensor reading)?
- **D4 Constraint classification** — features that touch PII or restricted-zone footage are hard.
- **D5 Reversal condition** — feature drift > 0.25 PSI → re-engineer.

## What I decided

<Vision: frozen backbone + LR/RF/GBM head. PredMaint: hand-engineered statistical features. RL: state = (5 zone temps, line speed, board class). Agent: tools schema.>

## Why

<Hand-engineered features beat raw sequence at 10-machine scale (LightGBM > LSTM pedagogy).>

## What I rejected

<Raw spectrogram features for predmaint — too rich for 10-machine sample size.>

## Reversal condition

<Drift PSI > 0.25 on any feature for 7 days → re-feature.>

## Risks I am accepting

<Hand-engineered features will need refactor when the line adds a new sensor channel.>
