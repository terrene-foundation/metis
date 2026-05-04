<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# LumenCircuit — Business Costs

**Source of truth for every dollar figure cited in a journal entry.** Grader treats figures not in this table as zero credit for D2 (metric → cost linkage).

## Direct costs

| Term                                                    | Value           | Unit                                                       | Phase    |
| ------------------------------------------------------- | --------------- | ---------------------------------------------------------- | -------- |
| Major defect shipped (recall / field return)            | $4,200          | per board (warranty + replacement + customer-confidence)   | 6, 7, 10 |
| Minor defect shipped (downstream rework)                | $180            | per board (in-line rework + repackage)                     | 6        |
| Good board scrapped (false-positive auto-fail)          | $85             | per board (component + labour cost of scrapped BOM)        | 6, 7, 10 |
| Unplanned line-stop (missed maintenance signal)         | $12,000         | per stop (4-hour mean recovery × $3,000/hour line revenue) | 11, 12   |
| Planned-maintenance window                              | $1,800          | per stop (off-shift; component + labour only)              | 11, 12   |
| Equipment damage from RL action outside safe envelope   | $50,000         | per incident (oven re-line + downtime)                     | 7, 11    |
| **WSH-notifiable incident (worker injury or fatality)** | **$1,000,000+** | per incident — MOM fine + criminal liability + reputation  | 7, 11, ★ |
| Qualified inspector time (IPC-A-610 Class 3 certified)  | $35             | per minute on the manual-review queue                      | 10, 11   |
| Cold-start misclassification (novel defect mode)        | $620            | per misclassified novel mode (recall escalation)           | 11, 13   |
| Edge inference (on-line camera, Jetson-class)           | $0.001          | per board classification served at the edge                | 6, 10    |
| Cloud RL training (A10G class)                          | $0.40           | per training hour                                          | 10, 13   |

## Volumes (for Phase 1 framing)

- ~40,000 boards / day across 3 SMT lines; 24/6 operating model
- ~12,000 inspection events / day (post-AOI gray-zone routing)
- Manual-review queue: ~1,400 boards average start-of-shift; 60-min SLA target
- Current AOI: 78% recall on true defects, 12% FP rate (the floor to beat)
- Predictive-maintenance scaffold: 30 days × 10 SMT machines × 1-min cadence ≈ 432,000 sensor rows; 4 of 10 machines have a labelled failure event in the window
- RL scaffold: 10,000 reflow-oven episodes per policy (PPO / DQN / Random)
- Vision scaffold: 800 labelled PCB images (60% IPC-A-610 Class 3 / 40% Class 2)
- Safety scaffold: 200 procedural images (PPE/no-PPE × restricted-zone/clear)

## Seasonality

Peak throughput windows: **Q4 automotive ramp** + **medical device certification cycles**. Drift anomalies in these windows are expected — do not auto-retrain during them.

## Decision anchors

- **Per-class threshold economics**: $4,200 FN vs $85 FP → ratio **49 : 1** in favour of catching defects. A symmetric metric (raw accuracy) systematically under-prices missing real defects.
- **Safety-critical-defect class**: $1M WSH ceiling sits structurally above any cost-balanced threshold. The safety-critical threshold is **HARD** (regulator-mandated minimum 0.40 confidence to auto-pass), not cost-balanced. Never classify as soft.
- **Predictive-maintenance economics**: $12,000 unplanned vs $1,800 planned → ratio **6.7 : 1** in favour of early prediction. The chosen prediction window (3/7/14 days) is the trade-off between FP rate (false alarms cost planned-maintenance dollars) and FN rate (missed signal costs an unplanned stop).
- **RL economics**: throughput recovery target = 2-3% × 40,000 boards/day × ~$60 average board contribution margin = $48,000-$72,000/day. The reward function MUST surface this gain WITHOUT triggering the $50K equipment-damage hard floor or the WSH ceiling.
- **Queue allocator economics**: $35/min inspector × ~1,400 queue start × ~3-min mean review time = $147,000/day in inspector cost — second-order to the FN cost on safety-critical, but binding on the throughput side.
- **Compute economics**: Edge $0.001 × 12,000/day = $12/day for vision inspection. Cloud RL $0.40/hr × ~6 hr/week retrain = $2.40/week. Both negligible compared to the $4,200 FN cost or the $50K equipment penalty — compute is NOT the binding constraint.
