<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Scaffold Manifest — Week 7 Manufacturing (LumenCircuit)

**Version:** 2026-05-04 · **License:** CC BY 4.0

The industrial AI product is pre-built at the repo root (`src/manufacturing/` + `apps/web/manufacturing/`). Workspace artefacts are student-produced during `/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`.

## State legend

- `[PRE-BUILT]` — ships complete; students do not edit.
- `[STUDENT-PRODUCED]` — written during `/analyze` / `/todos` / `/implement` / `/redteam` / `/codify`.
- `[PRE-BUILT + STUDENT-EXTENDED]` — skeleton ships; students extend at a named point.

## Repo-root (pre-built product)

| Path                                                           | State         | Role                                                                                              |
| -------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------- |
| `pyproject.toml`                                               | `[PRE-BUILT]` | Shared deps (kailash 2.12.0, kailash-ml 1.6.0, fastapi, uvicorn, scikit-learn, lightgbm, scipy)   |
| `MONOREPO.md`                                                  | `[PRE-BUILT]` | Monorepo doctrine (src/<domain> + apps/<platform>/<domain>)                                       |
| `src/manufacturing/backend/app.py`                             | `[PRE-BUILT]` | FastAPI app factory + CORS + lifespan                                                             |
| `src/manufacturing/backend/config.py`                          | `[PRE-BUILT]` | Env reader; resolves `manufacturing_root` and `workspace_root`                                    |
| `src/manufacturing/backend/startup.py`                         | `[PRE-BUILT]` | Loads data, fits 3 vision heads, fits 3 predmaint families, loads RL caches, registers drift refs |
| `src/manufacturing/backend/ml_context.py`                      | `[PRE-BUILT]` | Shared state: boards + sensor stream + rl episodes + per-modality baselines + drift refs          |
| `src/manufacturing/backend/routes/health.py`                   | `[PRE-BUILT]` | `GET /health`                                                                                     |
| `src/manufacturing/backend/routes/inspect_vision.py`           | `[PRE-BUILT]` | per-class scores + 3-arch leaderboard + threshold + promote + registry                            |
| `src/manufacturing/backend/routes/predict_maintenance.py`      | `[PRE-BUILT]` | LightGBM + LSTM + Survival Forest 3-family leaderboard + window + threshold + calibration         |
| `src/manufacturing/backend/routes/optimize_rl.py`              | `[PRE-BUILT]` | PPO + DQN + Random 3-policy leaderboard + reward function persistence + simulate                  |
| `src/manufacturing/backend/routes/agent.py`                    | `[PRE-BUILT]` | LLM-style agent harness: tools + autonomy ladder + decide + audit-trail                           |
| `src/manufacturing/backend/routes/drift.py`                    | `[PRE-BUILT]` | per-modality drift signals + per-class calibration decay + retrain-rule persistence × 3           |
| `src/manufacturing/backend/routes/queue.py`                    | `[PRE-BUILT]` | inspector queue allocator (LP) + queue depth + SLA timer                                          |
| `src/manufacturing/backend/routes/state.py`                    | `[PRE-BUILT]` | `GET /state/current` aggregator: pipeline phases + ★ decision moments from journal evidence       |
| `src/manufacturing/data/boards_labelled.csv`                   | `[PRE-BUILT]` | 800 labelled PCB inspection events (image_id + AOI flag + manual decision + class + defect mode)  |
| `src/manufacturing/data/images_pcb/`                           | `[PRE-BUILT]` | 800 procedural 32×32 RGB PNGs referenced by boards_labelled.csv                                   |
| `src/manufacturing/data/images_safety/`                        | `[PRE-BUILT]` | 200 procedural 32×32 RGB PNGs (PPE/no-PPE × restricted-zone/clear)                                |
| `src/manufacturing/data/sensor_stream.csv`                     | `[PRE-BUILT]` | 30 days × 10 SMT machines × 1-min cadence ≈ 432k rows; 4 machines have a labelled failure         |
| `src/manufacturing/data/rl_episodes.json`                      | `[PRE-BUILT]` | Cached PPO + DQN + Random transition tables (10k episodes per policy)                             |
| `src/manufacturing/data/baseline_vision_metrics.json`          | `[PRE-BUILT]` | Per-class P/R/F1 for the 3 vision heads (ResNet > EfficientNet > ViT pedagogy)                    |
| `src/manufacturing/data/baseline_predmaint_metrics.json`       | `[PRE-BUILT]` | 3-family leaderboard (LightGBM > LSTM > Survival Forest pedagogy) per-window                      |
| `src/manufacturing/data/baseline_rl_metrics.json`              | `[PRE-BUILT]` | 3-policy leaderboard with throughput / defect-rate / energy / safety per policy                   |
| `src/manufacturing/data/drift_baseline.json`                   | `[PRE-BUILT]` | Reference distributions for vision / predmaint / rl (3 separate baselines)                        |
| `src/manufacturing/data/scenarios/mom_wsh_shadow_mandate.json` | `[PRE-BUILT]` | Sprint 3 mid-injection — re-classify agent autonomy ladder for safety-affecting actions           |
| `src/manufacturing/data/scenarios/q4_demand_drift.json`        | `[PRE-BUILT]` | Sprint 4 mid-injection — adversarial drift on predictive-maintenance signal                       |
| `src/manufacturing/scripts/generate_data.py`                   | `[PRE-BUILT]` | Data generator (seed 20260504) — deterministic re-run                                             |
| `src/manufacturing/scripts/preflight.py`                       | `[PRE-BUILT]` | Green-light check; exit 0 = all green                                                             |
| `src/manufacturing/scripts/run_backend.sh`                     | `[PRE-BUILT]` | `uvicorn backend.app:app` with `METIS_API_HOST`/`METIS_API_PORT`                                  |
| `src/manufacturing/scripts/scenario_inject.py`                 | `[PRE-BUILT]` | Fire mom_wsh_shadow_mandate or q4_demand_drift; writes marker in workspace                        |
| `apps/web/manufacturing/index.html`                            | `[PRE-BUILT]` | Viewer Pane — 6 cards polling backend every 5 s (vision / predmaint / rl / agent / drift / queue) |
| `apps/web/manufacturing/serve.sh`                              | `[PRE-BUILT]` | `python3 -m http.server 3000`                                                                     |

## Endpoint inventory (34 routes)

| Endpoint                           | Method | Purpose                                                                                                                                              |
| ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/health`                          | GET    | Liveness check                                                                                                                                       |
| `/inspect/vision/leaderboard`      | GET    | 3-arch leaderboard with per-class P/R/F1                                                                                                             |
| `/inspect/vision/score`            | POST   | Score a single board image (returns per-class probabilities + chosen class)                                                                          |
| `/inspect/vision/threshold`        | POST   | Set per-class threshold (422 if safety-critical below WSH floor 0.40); current state available via `/inspect/vision/leaderboard.promoted_thresholds` |
| `/inspect/vision/promote`          | POST   | Promote a chosen architecture from staging to shadow                                                                                                 |
| `/inspect/vision/registry`         | GET    | Current registry state                                                                                                                               |
| `/inspect/vision/train`            | POST   | Re-fit the leaderboard (deterministic with seed)                                                                                                     |
| `/predict/maintenance/leaderboard` | GET    | 3-family leaderboard per prediction window (3 / 7 / 14 days)                                                                                         |
| `/predict/maintenance/score`       | POST   | Score a machine sensor window                                                                                                                        |
| `/predict/maintenance/window`      | POST   | Set chosen prediction window                                                                                                                         |
| `/predict/maintenance/family`      | POST   | Set chosen family                                                                                                                                    |
| `/predict/maintenance/threshold`   | POST   | Set chosen probability threshold                                                                                                                     |
| `/predict/maintenance/calibrate`   | POST   | Post-hoc calibration (platt/isotonic) — returns Brier pre/post + reliability                                                                         |
| `/predict/maintenance/train`       | POST   | Re-fit the leaderboard (deterministic with seed)                                                                                                     |
| `/predict/maintenance/promote`     | POST   | Promote a chosen family + window                                                                                                                     |
| `/predict/maintenance/registry`    | GET    | Current registry state                                                                                                                               |
| `/optimize/rl/leaderboard`         | GET    | 3-policy leaderboard (PPO + DQN + Random) with throughput/defect/energy/safety                                                                       |
| `/optimize/rl/reward_function`     | GET    | Read current reward weights + hard-floor table                                                                                                       |
| `/optimize/rl/reward_function`     | POST   | Set reward weights (422 if safety_penalty < hard floor)                                                                                              |
| `/optimize/rl/simulate`            | POST   | Roll a policy on the cached environment for N episodes                                                                                               |
| `/optimize/rl/promote`             | POST   | Promote a chosen policy                                                                                                                              |
| `/optimize/rl/registry`            | GET    | Current registry state                                                                                                                               |
| `/agent/policy`                    | GET    | Read current autonomy ladder (per-task-class autonomy mode)                                                                                          |
| `/agent/policy`                    | POST   | Set autonomy ladder (422 if WSH-affecting category not shadow during MOM mandate)                                                                    |
| `/agent/decide`                    | POST   | Agent decision on a board+machine context; returns action + autonomy mode + audit                                                                    |
| `/agent/audit`                     | GET    | Recent audit-trail entries                                                                                                                           |
| `/drift/check`                     | POST   | Per-modality drift signal + per-class calibration decay (model_id ∈ vision/predmaint/rl)                                                             |
| `/drift/retrain_rule/{model_id}`   | GET    | Read current retrain rule for one model_id                                                                                                           |
| `/drift/retrain_rule`              | POST   | Persist retrain rule per model_id                                                                                                                    |
| `/drift/status/{model_id}`         | GET    | Is the drift reference registered? Returns modality + cadence + window_size                                                                          |
| `/queue/state`                     | GET    | Inspector queue depth + SLA + per-class breakdown                                                                                                    |
| `/queue/solve`                     | POST   | Run LP allocator with current constraints                                                                                                            |
| `/queue/last_plan`                 | GET    | Most-recent allocator plan + dual prices                                                                                                             |
| `/state/current`                   | GET    | Aggregator for the viewer: pipeline phases + ★ decision moments from journal evidence                                                                |

## Workspace (student-produced)

| Path                                 | State                | When produced                              |
| ------------------------------------ | -------------------- | ------------------------------------------ |
| `PRODUCT_BRIEF.md`                   | `[PRE-BUILT]`        | Ships with scaffold                        |
| `PLAYBOOK.md`                        | `[PRE-BUILT]`        | Ships with scaffold                        |
| `START_HERE.md`                      | `[PRE-BUILT]`        | Ships with scaffold                        |
| `SCAFFOLD_MANIFEST.md`               | `[PRE-BUILT]`        | Ships with scaffold                        |
| `playbook/`                          | `[PRE-BUILT]`        | 14 phase docs + 8 workflows + 2 appendices |
| `specs/_index.md` + supporting specs | `[PRE-BUILT]`        | Ships with scaffold                        |
| `journal/_template.md`               | `[PRE-BUILT]`        | Schema for entries                         |
| `journal/skeletons/`                 | `[PRE-BUILT]`        | Fill-in-the-blank per-phase templates      |
| `briefs/`                            | `[STUDENT-PRODUCED]` | Student-writable                           |
| `01-analysis/failure-points.md`      | `[PRE-BUILT]`        | Pre-run `/analyze`                         |
| `01-analysis/assumptions.md`         | `[PRE-BUILT]`        | Pre-run `/analyze`                         |
| `01-analysis/decisions-open.md`      | `[PRE-BUILT]`        | Pre-run `/analyze`                         |
| `todos/active/phase_N_*.md` (×~21)   | `[PRE-BUILT]`        | Pre-run `/todos`                           |
| `todos/completed/phase_N_*.md`       | `[STUDENT-PRODUCED]` | `/implement`                               |
| `journal/phase_{1..13}_*.md`         | `[STUDENT-PRODUCED]` | `/implement`                               |
| `journal/phase_11_postwsh.md`        | `[STUDENT-PRODUCED]` | Sprint 3 injection                         |
| `journal/phase_12_postwsh.md`        | `[STUDENT-PRODUCED]` | Sprint 3 injection                         |
| `04-validate/redteam.md`             | `[STUDENT-PRODUCED]` | `/redteam`                                 |
| `.session-notes`                     | `[STUDENT-PRODUCED]` | `/wrapup`                                  |

## Contract violations

- A `[PRE-BUILT]` file with a `TODO-STUDENT` marker is a scaffolding error — instructor fixes.
- A `[STUDENT-PRODUCED]` file with `"placeholder": true` or a `# TODO` marker in the body scores zero on the rubric.
- Missing `journal/phase_N_*.md` for a phase the student claimed to run is a D3 (trade-off honesty) zero.

## Implementation deviations (2026-05-04)

The scaffold ships per the table above. Three implementation choices deviate from the brief's literal phrasing — all pedagogically conservative.

1. **"Frozen ResNet head" / "fine-tuned LightGBM" / "PPO trained" use sklearn / scipy / cached-rollout surrogates.**
   The backend trains real classifiers on per-class Gaussian-centroid embeddings synthesised deterministically per `image_id` (vision) and per-machine sliding windows (predmaint), and rolls the cached transitions deterministically (RL). The classifiers themselves are real sklearn fits (LogisticRegression, RandomForestClassifier, HistGradientBoostingClassifier for vision; LightGBM, an LSTM-shaped numpy approximation, RandomSurvivalForest-shaped scipy approximation for predmaint) producing real per-class precision / recall / F1 / Brier. RL "policies" are cached deterministic rollouts producing real per-policy throughput / defect / energy / safety signal. Reason: a literal ResNet-50 + EfficientNet + ViT fine-tune at startup AND a literal PPO training run would take >60 minutes on a laptop CPU and break the student iteration loop. The pedagogical contract — "students see the leaderboard differ across architectures and defend a reward function under the hard-floor table" — is intact. Live `/inspect/vision/train` re-runs the sweep so students can observe the leaderboard move with seed; live `/optimize/rl/simulate` re-runs the rollout.

2. **`src/manufacturing/data/images_pcb/` ships 32×32 procedural PNGs.** The manifest specifies "800 image files referenced by boards_labelled.csv". The scaffold writes 800 32×32 RGB PNGs whose pixel content is deterministic per-class noise (each defect class has a distinct base color + Gaussian noise). Total disk = ~1.5 MB. The backend does NOT read pixels at inference time — it uses synthesised embeddings — so the images are a teaching artefact only (students who curl `data/images_pcb/board_000123.png` see a real PNG, which is what the manifest's intent requires).

3. **The RL "environment" is a cached transition table, not a live simulator.** A literal Gym-style reflow-oven simulator with multi-zone thermodynamics would itself take a session to write and would not change the pedagogical content (students still defend reward weights against a leaderboard). The scaffold writes 10,000 episode transitions per policy as JSON, deterministic per seed, and `/optimize/rl/simulate` looks them up. Students who ask "can I retrain PPO with my own weights" get a soft re-weighting via the cached transitions (re-score with new reward, re-rank policies on the new objective) — same pedagogy, fraction of the compute.

Endpoint-name mapping (backend-actual ↔ brief-spec):

- `/inspect/vision/*` ✓ (replaces Week 6's `/moderate/image/*`)
- `/predict/maintenance/*` ✓
- `/optimize/rl/*` ✓
- `/agent/*` ✓ (replaces Week 6's `/moderate/fusion/*`)
- `/drift/check` ✓ (accepts model_id ∈ {vision, predmaint, rl} + window)
- `/drift/retrain_rule` ✓ (one rule per model_id)
- `/queue/*` ✓ (Phase 11+12 — inspector queue allocator)
- `/state/current` ✓ (viewer aggregator)

Family / architecture names diverge from "ResNet / EfficientNet / ViT" plain to make the pedagogy explicit:

- Vision: `resnet50_lr_head` / `efficientnet_b0_rf_head` / `vit_small_gbm_head` (all share the same frozen-embedding scaffold; different head classifiers AND different embedding dimensionalities to mimic the real-architecture differences).
- PredMaint: `lightgbm_features` / `lstm_sequence` / `survival_forest_tte` (the 3-family pattern matches the brief's "LightGBM + LSTM + Survival Forest" leaderboard).
- RL: `ppo_continuous` / `dqn_discrete` / `random_baseline` (the 3-policy pattern matches the brief's reward-function story).

The WSH safety floor (0.40) on the safety-critical defect class is enforced at the `POST /inspect/vision/threshold` boundary (422 below floor) AND at the `POST /inspect/vision/promote` boundary (422 if the persisted threshold is below floor at promote time). Both gates are defensive; either one catches a student who forgets that this class is structurally hard.

The WSH shadow-mode mandate (after MOM injection) is enforced at the `POST /agent/policy` boundary (422 if any WSH-affecting task class is set above shadow during the mandate window). The mandate window is read from `data/scenarios/mom_wsh_shadow_mandate.json` after `scripts/scenario_inject.py mom_wsh_shadow_mandate` is run.

The RL hard floors (equipment-damage $50K + WSH $1M) are enforced at the `POST /optimize/rl/reward_function` boundary (422 if safety_penalty weight is below the floor that yields zero hard-floor violations on the cached rollouts).
