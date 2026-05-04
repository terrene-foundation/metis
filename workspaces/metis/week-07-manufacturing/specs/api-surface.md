<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# LumenCircuit — API Surface

Base URL: `http://127.0.0.1:8000` (override with `METIS_API_PORT`).

All endpoints are wired in `src/manufacturing/backend/routes/`. Students call them indirectly through Claude Code; they do not implement them.

## Health

- `GET /health` — `{ status, boards, sensor_rows, rl_episodes, vision_baseline_arch, vision_baseline_f1, predmaint_baseline_family, predmaint_baseline_brier, rl_baseline_policy, drift_refs_active }`

## Vision QC Inspector (Sprint 1 · Transfer Learning)

- `GET  /inspect/vision/leaderboard` — per-class P/R/F1 (4 classes: good, minor_defect, major_defect, safety_critical_defect) on the 3-architecture leaderboard (resnet50_lr_head / efficientnet_b0_rf_head / vit_small_gbm_head)
- `POST /inspect/vision/train` — `{ arch?, seed }` — re-fit the leaderboard with a new seed (Phase 4 lever; arch optional, currently unused)
- `POST /inspect/vision/threshold` — `{ class_name, threshold, action: "auto_pass"|"manual_review"|"auto_fail" }` — Phase 6 deliverable; safety-critical threshold validated against WSH hard floor 0.40
- `POST /inspect/vision/promote` — `{ version, to_stage }` — staging → shadow → production → archived
- `GET  /inspect/vision/registry` — all versions + current production + shadow
- `POST /inspect/vision/score` — `{ image_id }` — per-class scores for one image (Phase 7 robustness probe)

## Predictive Maintenance Classifier (Sprint 2 · Time-series ML)

- `GET  /predict/maintenance/leaderboard` — 3-family leaderboard (lightgbm_features / lstm_sequence / survival_forest_tte) × 3 prediction windows (3 / 7 / 14 days)
- `POST /predict/maintenance/train` — `{ family?, seed }` — re-fit the leaderboard with a new seed
- `POST /predict/maintenance/window` — `{ window_days: 3|7|14 }` — sets chosen prediction window (Phase 5 SML deliverable)
- `POST /predict/maintenance/family` — `{ family }` — sets chosen family (Phase 5 SML deliverable; alternative to setting via promote)
- `POST /predict/maintenance/threshold` — `{ threshold, action: "auto_schedule"|"manual_review"|"none" }` — Phase 6 deliverable
- `POST /predict/maintenance/calibrate` — `{ method: "platt"|"isotonic" }` — post-hoc calibration; returns Brier pre/post + reliability diagram
- `POST /predict/maintenance/promote` — `{ family, window_days, to_stage }`
- `GET  /predict/maintenance/registry`
- `POST /predict/maintenance/score` — `{ machine_id, window_days? }` — per-day failure probability for the next N days

## Process-Optimization Controller (Sprint 3 · RL)

- `GET  /optimize/rl/leaderboard` — 3-policy leaderboard (ppo_continuous / dqn_discrete / random_baseline) with throughput / defect_rate / energy_kwh / safety_violations per policy
- `GET  /optimize/rl/reward_function` — current reward weights `{ throughput, defect_cost, energy_cost, safety_penalty }` + hard-floor table
- `POST /optimize/rl/reward_function` — Phase 7 deliverable; sets weights with dollar justification (422 if safety_penalty below the floor that yields zero hard-floor violations on cached rollouts)
- `POST /optimize/rl/simulate` — `{ policy_id, n_episodes, seed }` — re-roll a policy on the cached environment for N episodes
- `POST /optimize/rl/promote` — `{ policy_id, to_stage }`
- `GET  /optimize/rl/registry`

## Coordination Agent (Sprint 4 · LLM Agent)

- `GET  /agent/policy` — current autonomy ladder per task class (vision_triage / maintenance_scheduling / setpoint_adjustment / safety_alert) × autonomy mode (shadow / recommend / act)
- `POST /agent/policy` — Phase 11 + 12 deliverable; sets ladder (422 if any WSH-affecting category set above shadow during MOM mandate window)
- `POST /agent/decide` — `{ board_id, machine_id, line_state }` — agent decision on a board+machine context; returns `{ action, autonomy_mode, tools_called, audit_id }`
- `GET  /agent/audit` — `{ since: ISO8601 }` — recent audit-trail entries

## Drift (Sprint 4 · MLOps)

- `GET  /drift/status/{model_id}` — is reference registered? `model_id` ∈ `{vision, predmaint, rl}`
- `POST /drift/check` — `{ model_id, window: "recent_30d"|"q4_demand_drift"|"custom" }` — per-feature PSI + per-class calibration decay + overall severity
- `GET  /drift/retrain_rule/{model_id}` — current rule for that model
- `POST /drift/retrain_rule` — Phase 13 deliverable; `{ model_id, signals, thresholds, duration_window, hitl, seasonal_exclusions }`

## Inspector Queue Allocator (Sprint 4 · LP)

- `GET  /queue/state` — current queue depth + SLA timer + per-class breakdown
- `POST /queue/solve` — solves the LP; returns plan + queue depth + expected SLA + shadow prices
- `GET  /queue/last_plan` — most recent solve result

## State (viewer aggregator)

- `GET /state/current` — `{ phases: {...}, decisions: {...}, sprints: {...}, mom_mandate_active: bool }` — used by the value-chain banner

## Error taxonomy

- `404` — unknown version / unknown image_id / unknown machine_id / unknown model_id
- `409` — illegal stage transition (names the legal set) / WSH-hard threshold below regulator floor 0.40
- `422` — unknown family / unknown policy / unknown calibration method / two classes got the same action / hard constraint set is infeasible / safety_penalty weight below RL hard floor / WSH-affecting agent category set above shadow during mandate
