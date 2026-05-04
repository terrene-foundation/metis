<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 4 — Candidate Models

**Decision moment:** Which 3 candidates are on the leaderboard for this sprint, and why those?
**Sprint:** 1 / 2 / 3
**Time:** <HH:MM>
**Artefact produced:** `journal/phase_4_candidates.md`

## Five dimensions

- **D1 Harm framing** — picking too few candidates risks under-exploration; too many risks dilution.
- **D2 Metric → cost linkage** — each candidate must be scored on the $-weighted metric.
- **D3 Trade-off honesty** — what didn't make the leaderboard (e.g., custom-trained CNN)?
- **D4 Constraint classification** — edge-deployment latency budget (80 ms/board) is hard.
- **D5 Reversal condition** — when does a 4th candidate enter (e.g., YOLOv8 once sample > 5,000 images)?

## What I decided

<Sprint 1: ResNet-50 / EfficientNet-B0 / ViT-Small. Sprint 2: LightGBM / LSTM / Survival Forest. Sprint 3: PPO / DQN / Random.>

## Why

<3 candidates per leaderboard span the inductive-bias spectrum + give a defendable story.>

## What I rejected

<YOLOv8 (object detection adds annotation cost we don't yet have); SAC (overkill for 5-zone discrete-ish action space).>

## Reversal condition

<If sample > 5,000 images → add ViT-Large; if RL action space goes continuous → add SAC.>

## Risks I am accepting

<3-candidate leaderboards may miss a better-suited 4th option.>
