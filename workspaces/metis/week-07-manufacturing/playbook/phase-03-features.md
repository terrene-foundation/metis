<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 3 — Feature Framing

## 1. What this phase decides

Decide which features each model uses, classified by availability-at-decision-time, leakage risk, and proxy-for-protected-cohort status — for vision (board pixels + augmentations + metadata), predmaint (sensor windows + cohort metadata), RL (state representation), and the agent (tool inputs).

## 2. The Week 7 lens

**Vision (Sprint 1):**
Pixel-level (raw RGB at the embedding scaffold's resolution); augmentations (random horizontal flip, color jitter for varied lighting; mixup is risky on rare safety_critical_defect class — flag for monitoring); metadata (line_id MEDIUM proxy, shift MEDIUM, supplier_lot_id MEDIUM, board_class LOW); embedding (frozen ResNet/EfficientNet/ViT penultimate-layer vector — IS the model).

**PredMaint (Sprint 2):**
Sensor channels (vibration RMS, motor_current_p95, head_temp rolling mean, cycle_count); window features (rolling 5-min / 15-min / 60-min mean + std + spectral peaks); per-machine metadata (machine_id LOW proxy, line_id MEDIUM, shift MEDIUM, last_calibration_age MEDIUM). LSTM uses raw sequence; LightGBM uses engineered windows.

**RL (Sprint 3):**
State representation (current 5-zone temperatures, line speed, board class on the line, minutes since last calibration). Reward components feed the four-term function. Action space discretised: ±5 °C per zone OR hold; ±10 boards/min OR hold.

**Agent (Sprint 4):**
Tool inputs are the upstream model outputs (`vision_classify` returns per-class scores; `predict_failure` returns per-day probabilities; `suggest_setpoint` returns RL action recommendation). The agent's "features" are these tool returns + the autonomy ladder + the audit context.

## 3. Your levers

- **In/out classification on 3 axes** — availability, proxy risk, source
- **Augmentation choices** — which augmentations preserve the defect signal vs corrupt it
- **Sensor window length** — short windows catch fast precursors, long windows are noise-robust
- **State / action space discretisation** — RL state granularity affects convergence
- **Proxy classification** — line_id and shift are the manufacturing analog to demographic proxy

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 3 — Feature Framing. For each feature each model
WILL use, classify on three axes:

A. Available-at-decision-time (yes/no — leaky if no)
B. Proxy-for-protected-cohort risk (low/medium/high; manufacturing
   cohorts are line/shift/operator/supplier-lot)
C. Engineering source (raw / augmentation / metadata / embedding /
   sensor-window / state-action)

Produce a table:
| feature | A | B | C | rationale |

Then propose drop / keep / monitor for each, but the decision is mine.

Tonight-specific (Sprint 1 vision):
Pixel-level (raw):
- raw RGB image (32×32 procedural in the scaffold; the embedding scaffold
  consumes per-class Gaussian centroids deterministically) — KEEP
- EXIF metadata — usually OFF (board capture timestamps could leak)
Augmentations (training-only):
- random horizontal flip — KEEP (PCB layouts are not orientation-bound)
- color jitter — KEEP if production handles varied LED lighting on the line
- mixup / cutmix — review against label noise; rare safety_critical_defect
  class breaks under mixup → MONITOR
Metadata (per-board):
- line_id — MEDIUM proxy (correlates with operator cohort + machine
  cohort). Phase 7 cohort sweep is the structural defense.
- shift — MEDIUM proxy. Same rationale.
- supplier_lot_id — MEDIUM (correlates with component vendor)
- board_class (Class 2 / Class 3) — LOW proxy, KEEP
Embedding:
- ResNet-50 / EfficientNet-B0 / ViT-Small penultimate-layer vector —
  KEEP (IS the model). Choice is Phase 5.

Tonight-specific (Sprint 2 predmaint):
Sensor channels (raw):
- vibration_rms — KEEP (primary failure precursor)
- motor_current_p95 — KEEP
- head_temp_rolling — KEEP
- cycle_count — KEEP (for time-to-event survival modelling)
Window features (engineered):
- rolling 5/15/60-min mean + std + spectral peaks — KEEP for LightGBM
- raw sequence — KEEP for LSTM (different family, different feature set)
Metadata:
- machine_id — LOW (the prediction is per-machine; this is the index)
- line_id — MEDIUM proxy
- shift — MEDIUM
- last_calibration_age — MEDIUM (correlates with operator schedule)

Tonight-specific (Sprint 3 RL):
State variables:
- 5 zone temperatures (continuous, 0–280 °C bounded)
- line_speed (continuous, 0–60 boards/min bounded under post-WSH ceiling)
- board_class on line (categorical: Class 2 / Class 3)
- minutes_since_calibration (continuous, 0–60 typically)
Action space:
- per-zone ±5 °C or hold (5 zones × 3 actions = 15)
- line_speed ±10 boards/min or hold (3 actions)
- combined: 45 discrete action atoms

Tonight-specific (Sprint 4 agent):
Tool-input features (the agent does NOT have raw access; it reads tool
outputs):
- vision_score (per-class probability vector, 4 classes) — from /inspect/vision/score
- failure_probability (per-day for next N days) — from /predict/maintenance/score
- setpoint_recommendation — from RL policy
- safety_event_log (recent) — from /agent/audit

Do NOT auto-drop features I might want for Phase 7 sweeps.
Do NOT use "blocker" without specifics.

Journal file: copy journal/skeletons/phase_3_features.md into
workspaces/metis/week-07-manufacturing/journal/phase_3_features.md.

When the table is drafted, stop.
```

## 5. Cost anchor

From `specs/business-costs.md`:

- An auto-dropped feature that should have stayed for Phase 7 cohort sweep means cohort skew goes undetected and propagates to deployment — blast radius bounded by $4,200 × per-cohort FN delta
- A leaky feature (e.g. predmaint window ending after `failure_event_time`) makes Phase 4 leaderboard look great while Phase 7 OOD finds catastrophic failure — wasted Phase 5 → Phase 8 cycle

## 6. Hard-floor table

Not directly applicable in Phase 3 — feature decisions are upstream of the floors. The floors live at Phase 6 / 11.

## 7. Reversal condition

A Phase 3 feature decision is reversed when:

- **Signal**: a Phase 7 cohort sweep reveals per-line / per-shift recall delta > 10 percentage points
- **Threshold**: 10 pp delta on any class
- **Duration**: any single sweep run

Then re-open Phase 3 for the offending modality and either drop the proxy feature or widen the Phase 7 sweep.

## 8. Transfer to next project

The 3-axis classification (availability / proxy / source) generalises to every supervised ML task. The augmentation question is specific to vision/audio. The window-length question is specific to time-series. The state-action discretisation question is specific to RL. In any new domain, the same hygiene applies: classify before training, flag proxies before they become a Phase 7 surprise, and never drop features the red-team needs for cohort sweeps.

---

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md)
