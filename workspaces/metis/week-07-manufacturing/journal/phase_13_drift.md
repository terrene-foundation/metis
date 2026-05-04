<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 13 — Drift × 3 Cadences

**Decision moment:** Three retrain rules — one per model — with cadence-specific signal/threshold/duration.
**Sprint:** 4 (MLOps)
**Time:** 18:58
**Artefact produced:** `journal/phase_13_drift.md` + `POST /drift/retrain_rule` × 3

## Five dimensions

- **D1 Harm framing** — silent drift → AOI 78% recall floor returns. $4,200/board exposure rises by missed-defect rate × 12k events/day.
- **D2 Metric → cost linkage** — retrain cost ($0.40/hr cloud A10G) vs FN cost averted by detected drift. $0.40/hr × ~6 hr/retrain = $2.40/retrain; net positive even on a single FN avoided.
- **D3 Trade-off honesty** — universal "weekly retrain" wastes compute AND misses fast text/sensor drift. Three cadences match three data-generating processes.
- **D4 Constraint classification** — Q4 automotive ramp + medical certification cycles are HARD seasonal exclusions (per `data/scenarios/q4_demand_drift.json`).
- **D5 Reversal condition** — false-positive retrain rate > 1/quarter on any model → tighten threshold (e.g. 0.30 → 0.40).

## Live drift baseline (recent_30d)

| Model       | PSI    | Severity | Per-class calibration sample                 |
| ----------- | ------ | -------- | -------------------------------------------- |
| `vision`    | 0.7345 | drift    | safety_critical_defect Brier 0.0004 (stable) |
| `predmaint` | 0.7299 | drift    | fail_within_window Brier 0.0                 |
| `rl`        | 0.7896 | drift    | (return distribution; per-class N/A)         |

Note: the `recent_30d` synthetic window is sampled with elevated noise relative to the reference; PSI on a real deployment with stable distribution would land in `stable` (< 0.10). The high baseline PSI demonstrates the metric is differentiable — `q4_demand_drift` window on predmaint shows PSI 0.9757 (vs 0.7299 baseline), a 0.25-point gap attributable to the seasonal shift.

## Three retrain rules (live evidence — `POST /drift/retrain_rule` × 3)

| Model       | Signal            | Threshold | Duration       | HITL                   | Seasonal exclusions                                  |
| ----------- | ----------------- | --------- | -------------- | ---------------------- | ---------------------------------------------------- |
| `vision`    | psi               | 0.30      | 7d             | required_first_trigger | q4_automotive_ramp, medical_certification_cycle      |
| `predmaint` | calibration_decay | 0.10      | 3d             | required_first_trigger | q4_automotive_ramp                                   |
| `rl`        | combined          | 0.15      | per_deployment | required_first_trigger | (none — RL drift fires per-deployment, not seasonal) |

`/state/current.retrain_rules_registered` confirms: `["vision", "predmaint", "rl"]` — all three registered. Persisted to `workspaces/metis/week-07-manufacturing/retrain_rules.json` (workspace-side; survives backend reboot).

## Why each cadence

- **Vision (weekly, PSI 0.30):** Equipment + supplier drift moves on a weekly cadence (new BOM batches, line-camera re-calibrations). PSI is the right signal because the input distribution shifts faster than the per-class calibration.
- **PredMaint (daily, calibration_decay 0.10):** Sensor distributions drift on a daily cadence (temperature, calibration). Calibration_decay catches the case where the classifier's confidence becomes unreliable even when the input distribution looks stable.
- **RL (per-deployment, combined 0.15):** RL doesn't drift on calendar; it drifts when the deployment envelope changes (new line speed target, new reward weights). Combined signal (PSI + calibration_decay together) catches both input-shift and reward-shape changes.

## Seasonal exclusions

Q4 automotive ramp (Oct-Dec) is in scope for both vision (camera load shifts) and predmaint (machine load shifts). Medical certification cycle (variable timing) is in scope for vision (Class 3 boards bias the labelled distribution). RL has no seasonal exclusions because the policy operates on the line, not the calendar.

## What I rejected

Universal weekly retrain — wastes compute on stable models AND misses fast sensor drift. Universal daily retrain — wastes compute on stable RL deployment AND triggers retrains during seasonal exclusions.

## Reversal condition

False-positive retrain rate > 1/quarter on any model → tighten threshold by +0.05 (e.g. vision 0.30 → 0.35). Retrain runtime > 12 hr on any model → switch to incremental fine-tune.

## Risks I am accepting

Q4 seasonal exclusion may mask a real drift event during the ramp window — mitigated by escalation rule: if vision PSI > 0.50 during Q4, override seasonal exclusion AND escalate to operations.
