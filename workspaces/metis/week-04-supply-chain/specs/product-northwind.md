# Northwind Logistics Control Tower — Product Spec

This spec is the authority on the product students ship in Week 4. It covers the three modules (Forecast / Optimize / Monitor), the user personas, the business numbers that ground every decision, the endpoint contracts with request/response schemas, the SLOs, and the deployment topology.

`START_HERE.md` §2 and §3 are generated views over this spec. When product truth changes, this file is updated first.

## 1. What the product is

A last-mile delivery operator's control dashboard for a fictional company, **Northwind Logistics**. The product surfaces three modules on a single read-only dashboard (the Viewer Pane) backed by a Nexus API and a kailash-ml stack. A Trust Plane user (the Ops Manager) reads the dashboard, approves tomorrow's plan, and owns the retrain decision. The Execution Plane (Claude Code + kailash-ml + OR-Tools / PuLP + Nexus) produces the forecasts, plans, and drift reports.

The product is real enough to defend: every endpoint returns artefacts a real operator could act on, every number is grounded in the business-cost table below, every decision is journalled.

## 2. Modules

### 2.1 Demand Forecaster

Predicts next-day order volume per depot. Feeds the Route Optimizer. Target: how many orders each depot will receive tomorrow (one prediction per depot per day). Underlying column: `orders_next_day`, keyed on the `(depot_id, date)` pair. Horizon: 1 day rolling (Week 4 scope; Week 5-8 may extend to 7 days). Training surface: `TrainingPipeline` + `AutoMLEngine` over `FeatureStore` schema `user_demand` (9 features, defined in `specs/schemas/demand.py`).

### 2.2 Route Optimizer

Consumes forecast output + vehicle/driver/constraint specs; produces tomorrow's route plan. Solver stack: OR-Tools VRP as primary, PuLP as LP-decomposition alternative. Objective function and constraint hard/soft classification are the student's decisions (Phases 10 and 11).

### 2.3 Drift Monitor

Watches whether the forecast model's input distribution has drifted from its training window. Uses `kailash_ml.DriftMonitor`, which ships two per-feature statistical tests: **KS** (Kolmogorov-Smirnov, for continuous features) and **PSI** (Population Stability Index). The library does NOT emit `chi2` or `js-divergence` per-feature results — do not reference them in prompts, schemas, or graders. Produces an `overall_severity` rating in `{"none", "moderate", "severe"}` (3 values, not 4 — the library never emits `"low"`) plus human-readable recommendations. The retrain rule itself lives in the Trust Plane — the student journals it in Phase 13.

## 3. Users and personas

| Persona            | Plane     | What they do                                                                     | What they read                         |
| ------------------ | --------- | -------------------------------------------------------------------------------- | -------------------------------------- |
| **Ops Manager**    | Trust     | Approves tomorrow's plan; decides go/no-go on deploy                             | Dashboard, journal, daily digest       |
| **Demand Planner** | Trust     | Tracks forecast accuracy, owns model health                                      | Leaderboard, drift chart               |
| **Dispatcher**     | Trust     | Reads routes, adjusts for real-world events                                      | Route map, time-window violations      |
| **ML Engineer**    | Execution | Ships training pipeline, registry, drift monitor (= Claude Code during workshop) | Logs, ExperimentTracker, ModelRegistry |
| **Student**        | Trust     | Commissions every piece; scored on journal + contract grader                     | Viewer Pane + terminal + PLAYBOOK.md   |

The workshop's framing is that the student plays the role of a one-person founder who owns the Ops Manager + Demand Planner decisions and commissions the Execution Plane (Claude Code) to do the engineering.

## 4. User flows

### 4.1 Opening (00:00 – 00:10)

Student lands in workspace, reads `SCAFFOLD_MANIFEST.md`, runs `scripts/preflight.py`, opens terminal + Viewer Pane + `PLAYBOOK.md`, types the opening prompt. Claude Code verifies the scaffold manifest. Instructor projects manifest on main screen.

### 4.2 Sprint 1 — Forecast (00:10 – 01:25)

Phases 1, 2, 4, 5, 6, 7, 8 (Phase 3 folded into 2). Student commissions `/forecast/train`, runs live AutoML (5 trials, 3 families, random search, ~90s wall-clock), compares against pre-baked 30-trial leaderboard, picks a model + threshold, red-teams on AI Verify dimensions (Transparency / Robustness / Safety; Fairness deferred to Week 7), promotes to `staging` → `shadow` via ModelRegistry. Journal: entries for phases 1, 2, 5, 6, 7, 8.

### 4.3 Break (01:25 – 01:35)

### 4.4 Sprint 2 — Optimize (01:35 – 02:35)

Phases 10, 11, 12. At ~02:05 the instructor fires the **union-cap injection**: driver overtime capped at 5h/week. Student saves prior plan as `route_plan_preunion.json`, re-classifies the constraint (soft → hard), re-solves, saves as `route_plan_postunion.json`, re-runs Phase 8 (deployment gate) to sign off on the new plan. Journal: entries for 10, 11, 11-postunion, 12, 12-postunion.

### 4.5 Sprint 3 — Monitor (02:35 – 03:15)

Phase 13. Instructor fires the **week-78 drift injection**: post-drift 30-day window loaded. Student runs `DriftMonitor.check_drift`, surfaces per-feature statistical tests + severity, re-runs Phases 5 and 6 on post-drift data. Journal: entry for Phase 13.

### 4.6 Close (03:15 – 03:30)

Phase 9 (codify) runs against the day's journal. Instructor runs `scripts/grade_product.py` publicly on the projector — students see their score live. Student runs `metis journal export` → `journal.pdf`.

## 5. Business numbers (ground truth for all phases)

From `START_HERE.md` §2. These numbers MUST be referenced in Phase 6 (metric+threshold), Phase 10 (objective function), and Phase 13 (drift triggers). Journal entries that name asymmetry in these units score 4/4 on the "Harm framing" dimension.

| Quantity           | Value                                    | Used in                                |
| ------------------ | ---------------------------------------- | -------------------------------------- |
| Daily order volume | ~12,000 orders/day                       | Scale framing; capacity reasoning      |
| Depots             | 3                                        | Population scope (Phase 1)             |
| Regular customers  | 500                                      | Subgroup audit (Phase 7 Robustness)    |
| Vehicle fleet      | 20                                       | Optimizer capacity                     |
| Stockout cost      | $40 per unit short of demand             | Cost asymmetry, MAPE weighting         |
| Overstock cost     | $12 per unit of excess capacity deployed | Cost asymmetry (ratio 3.3:1)           |
| Late-delivery SLA  | $220 per violation                       | Phase 10 objective; Phase 7 Safety     |
| Driver overtime    | $45 per hour                             | Phase 10 objective; union-cap scenario |
| Fuel cost          | $0.35 per km                             | Phase 10 objective                     |
| Carbon cost        | $8 per kg CO₂                            | Phase 10 objective (optional ESG term) |
| Peak season        | Q4 (Oct–Dec)                             | Sensitivity in Phase 6                 |
| Drift event        | Week 78                                  | Sprint 3 injection                     |

These numbers live as a table in `specs/business-costs.md` (scaffold file, read by every prompt template).

## 6. SLOs

The contract grader asserts these SLOs. See `rubric-grader.md` for the full assertion list.

- `/forecast/train` — p95 latency ≤ 90 s on 5-trial / 3-family AutoML; MUST return an `experiment_run_id` that resolves in `ExperimentTracker`.
- `/forecast/compare` — p95 latency ≤ 2 s; MUST return ≥ 3 runs with distinct `params_hash`.
- `/forecast/predict` — p95 latency ≤ 500 ms; MUST return a `model_version_id` resolvable in `ModelRegistry` at stage in `{staging, shadow, production}`. (The `model_version_id` is a derived string ID of form `{model_name}_v{version}`, produced by `ml_context` — see §8.3 and `scaffold-contract.md` §2.)
- `/optimize/solve` — time budget 30 s for VRP solve; MUST return `feasibility: true` OR `feasibility: false` with violated constraint names; optimality gap as float ≥ 0.
- `/drift/check` — p95 latency ≤ 3 s; MUST return ≥ 1 named statistical test (`ks` or `psi` — those are the two kailash-ml emits) with a numeric statistic AND `overall_severity ∈ {"none", "moderate", "severe"}` (3-value enum; see §8.5).

The workshop does NOT test load — these are single-user local targets. Production deployment (not in Week 4 scope) would tighten.

## 7. Deployment topology

Local-only for the workshop. Everything runs on the student's laptop.

| Component                   | Port / Path                      | Process                          | Owner      |
| --------------------------- | -------------------------------- | -------------------------------- | ---------- |
| Viewer Pane (Next.js)       | `http://localhost:3000`          | `apps/web/` — `next dev`         | Scaffolded |
| Nexus API                   | `http://localhost:8000`          | `src/backend/app.py` — `uvicorn` | Scaffolded |
| ExperimentTracker store     | `sqlite:///data/.experiments.db` | Embedded in Nexus process        | Scaffolded |
| ModelRegistry store         | `sqlite:///data/.registry.db`    | Embedded in Nexus process        | Scaffolded |
| FeatureStore backing        | `sqlite:///data/.features.db`    | Embedded in Nexus process        | Scaffolded |
| DriftMonitor reference data | `data/drift_baseline.json`       | Written by `fs_preload.py`       | Scaffolded |
| Artifact dir                | `data/`                          | JSON files watched by Viewer     | Mixed      |

Ports are the default but not hard-coded. The preflight script detects `:8000` or `:3000` already bound and prints a remediation hint pointing at the `KAILASH_NEXUS_PORT` env var (and `NEXT_PUBLIC_BACKEND_PORT` for the Viewer). The Viewer Pane's filesystem-watch config resolves `data/` through `METIS_WORKSPACE_ROOT` (or `path.resolve(__dirname, '../../data')`); the resolution is tested in preflight. ExperimentTracker uses its own SQLite store. kailash-ml also ships an MLflow-format writer (`MlflowFormatWriter` → `mlruns/`) as an interoperability helper for teams migrating from MLflow; Kailash does not depend on MLflow, and the "mlflow on :5000" server is not part of the scaffold.

## 8. Endpoint contracts

All endpoints are authored as Nexus routes in `src/backend/routes/`. The three student-commissioned route files (`forecast.py`, `optimize.py`, `drift.py`) ship as `[STUDENT-COMMISSIONED]` stubs with the `# TODO-STUDENT:` banner. Students prompt Claude Code to fill them.

### 8.1 `POST /forecast/train`

The route handler follows the kailash-ml source API exactly. On each call it (1) ensures the `FeatureStore` schema exists via `feature_store.register_features(schema)` and loads rows via `feature_store.store(schema, df)` (idempotent no-op if `fs_preload.py` already ran); (2) constructs `TrainingPipeline(feature_store=fs, registry=registry)` and `HyperparameterSearch(pipeline=pipeline, registry=registry)`; (3) constructs `AutoMLEngine(pipeline, search, registry=registry)` — positional `pipeline` + `search`, keyword-only `registry`; (4) calls `await engine.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name='forecast_sprint1', tracker=tracker)` and returns the `AutoMLResult`'s best run ID.

`AutoMLConfig` uses `candidate_families=[...]` (the library field name — there is no `families` alias). `EvalSpec` uses `split_strategy` (NOT `cv_strategy`) with one of `{"holdout", "kfold", "stratified_kfold", "walk_forward"}`. For time-series demand forecasting, use `split_strategy="walk_forward"` — the library's supported name for rolling-origin-style evaluation. Do NOT pass `cv_strategy="rolling_origin"`; the library has no such value and will fall back silently or raise, depending on dispatch.

- **Auth:** none (local-only workshop).
- **Request body (application/json):**

  ```json
  {
    "feature_schema": "user_demand",
    "target": "orders_next_day",
    "search_strategy": "random",
    "search_n_trials": 5,
    "candidate_families": [
      "sklearn.linear_model.Ridge",
      "sklearn.ensemble.RandomForestRegressor",
      "sklearn.ensemble.GradientBoostingRegressor"
    ],
    "split_strategy": "walk_forward",
    "auto_approve": false
  }
  ```

  Field names match the library: `candidate_families` → `AutoMLConfig.candidate_families`, `split_strategy` → `EvalSpec.split_strategy`. The route handler is responsible for mapping this request body onto `AutoMLConfig(task_type='regression', metric_to_optimize='mape', candidate_families=[...], search_strategy='random', search_n_trials=5, auto_approve=False)` and `EvalSpec(metrics=['mape','rmse'], split_strategy='walk_forward', test_size=0.2)`.

- **Response 200 (application/json):**

  ```json
  {
    "experiment_run_id": "<uuid>",
    "leaderboard_path": "data/leaderboard.json",
    "n_runs_logged": 5,
    "best_metric": { "mape": 0.062, "rmse": 41.3 },
    "training_duration_s": 87.4,
    "started_at": "2026-04-16T14:32:18Z",
    "latency_ms": 87412
  }
  ```

  `experiment_run_id` is the `ExperimentTracker` run UUID; the human-readable run_name stored on the run (e.g. `forecast_sprint1_GradientBoostingRegressor`) is cosmetic and not used as a grader key.

- **Error cases:** every error response shares the top-level telemetry fields `latency_ms` and `started_at`.
  - `400` — unknown `feature_schema` → `{"error": "feature schema 'X' not registered in FeatureStore", "latency_ms": 12, "started_at": "..."}`
  - `400` — unsupported `split_strategy` (not in `{"holdout","kfold","stratified_kfold","walk_forward"}`) → `{"error": "split_strategy 'X' not in library vocabulary; use walk_forward for time-series"}`
  - `409` — FeatureStore not yet populated (no rows for the schema) → `{"error": "FeatureStore has no rows for schema 'user_demand'; fs_preload should have called register_features + store on startup"}` (should not occur; `fs_preload.py` runs on Nexus startup)
  - `422` — `search_n_trials > 20` AND `KAILASH_ML_AUTOML_QUICK=1` → `{"error": "AUTOML_QUICK env caps trials at 20", "warning": "quick-mode cap in effect; restart Nexus without KAILASH_ML_AUTOML_QUICK to raise"}`. The cap is defence-in-depth for accidental `search_n_trials=30`; the Sprint 1 default is `search_n_trials=5` so the cap is rarely reached.
  - `500` — training failure → stack trace logged to server; response includes `error_category` in `{"xgb_missing", "cv_split_failed", "candidate_all_failed", "other"}` plus `training_duration_s` (partial).
- **Grader assertion:** response contains `experiment_run_id`; `ExperimentTracker.get_run(id)` returns params AND ≥ 2 metrics AND a non-null training timestamp.

### 8.2 `GET /forecast/compare`

- **Auth:** none.
- **Query params:** `top_n` (default 5), `scenario` (optional; values `preunion` / `postunion`).
- **Response 200 (application/json):**
  ```json
  {
    "runs": [
      {
        "run_id": "xgb_007_20260416_143012",
        "family": "xgboost.XGBRegressor",
        "params_hash": "a1b2c3d4",
        "metrics": { "mape": 0.062, "rmse": 41.3, "fold_variance": 0.004 },
        "training_duration_s": 14.2
      }
      // ... ≥ 3 runs
    ],
    "compared_at": "2026-04-16T14:32:18Z"
  }
  ```
- **Error cases:**
  - `409` — fewer than 3 runs in tracker → `{"error": "need >=3 runs to compare; got N"}`
- **Grader assertion:** response is a list of ≥ 3 runs; each run has distinct `params_hash`; `metrics` column present and numeric.

### 8.3 `POST /forecast/predict`

kailash-ml's `ModelRegistry` uses `(name: str, version: int)` as the primary key — there is NO opaque string `model_version_id` in the library. This endpoint exposes a derived string ID of the form `{model_name}_v{version}` (e.g. `forecast_sprint1_v3`) that is produced and resolved by `ml_context` helpers. The derivation is one-way: the route handler splits on the last `_v` to recover `(name, version)` before calling `registry.get_model(name, version=version)` or `registry.get_model(name, stage="shadow")`.

- **Auth:** none.
- **Request body:**
  ```json
  {
    "model_version_id": "forecast_sprint1_v3",
    "inputs": [{"depot_id": "D01", "date": "2026-04-17", "features": {...}}, ...]
  }
  ```
  Alternative shape also accepted: `{"model_name": "forecast_sprint1", "model_version": 3, "inputs": [...]}`. When both are present, `model_version_id` wins.
- **Response 200:**
  ```json
  {
    "model_version_id": "forecast_sprint1_v3",
    "model_name": "forecast_sprint1",
    "model_version": 3,
    "model_stage": "shadow",
    "predictions": [
      {
        "depot_id": "D01",
        "date": "2026-04-17",
        "predicted_orders": 478.2,
        "interval_80": [412.0, 544.4]
      }
    ],
    "predicted_at": "2026-04-16T14:40:02Z",
    "started_at": "2026-04-16T14:40:02Z",
    "latency_ms": 212
  }
  ```
- **Error cases:** every error response shares the top-level `latency_ms` + `started_at` telemetry fields.
  - `400` — `model_version_id` malformed (no `_v<int>` suffix) → `{"error": "model_version_id 'X' invalid; expected format <name>_v<int>"}`
  - `404` — resolved `(name, version)` not in ModelRegistry (`ModelNotFoundError` from the library) → `{"error": "model version 'X' not found"}`
  - `409` — model is `archived` → `{"error": "cannot predict with archived model; promote from archived → staging first"}`
  - `422` — feature validation failed (InferenceServer strict mode) → `{"error": "required feature 'X' missing or non-numeric in inputs[3]"}`
- **Grader assertion:** response contains `model_version_id`; handler resolves to `(name, version)` and calls `ModelRegistry.get_model(name, version)`, confirming `.stage ∈ {"staging", "shadow", "production"}`; `predictions` is a non-empty list of objects where each `predicted_orders` is numeric.

### 8.4 `POST /optimize/solve`

- **Auth:** none.
- **Request body:**
  ```json
  {
    "forecast_path": "data/forecast_output.json",
    "objective": {
      "terms": [
        { "name": "fuel", "weight": 0.35, "unit": "per_km" },
        { "name": "sla", "weight": 220, "unit": "per_violation" },
        { "name": "overtime", "weight": 45, "unit": "per_hour" }
      ]
    },
    "hard_constraints": { "vehicle_capacity": 40, "driver_hours_max": 9 },
    "soft_constraints": {
      "delivery_before_5pm": { "penalty": 15, "unit": "per_hour_late" }
    },
    "time_budget_s": 30,
    "scenario_tag": "preunion"
  }
  ```
- **Response 200:**
  ```json
  {
    "feasibility": true,
    "optimality_gap": 0.031,
    "objective_value": 12450.8,
    "hard_constraints_satisfied": {
      "vehicle_capacity": true,
      "driver_hours_max": true
    },
    "plan_path": "data/route_plan.json",
    "solver": "or_tools_vrp",
    "wallclock_s": 22.1,
    "experiment_tags": ["phase=optimize", "scenario=preunion"]
  }
  ```
- **Error cases:** every error response shares the top-level `latency_ms` + `started_at` telemetry fields.
  - `422` — forecast_path missing → `{"error": "forecast_output.json not found; run /forecast/predict first"}`
  - `409` — infeasible + no soft constraint to relax → `{"feasibility": false, "violated_constraints": ["driver_hours_max"], "suggestion": "re-classify driver_hours_max as soft"}`
  - `500` — solver crashed or exceeded `time_budget_s` without returning → `{"error": "solver failed", "error_category": "timeout|internal", "wallclock_s": 30.0}`
- **Grader assertion:** response contains `feasibility: true`, `optimality_gap` as float ≥ 0, `hard_constraints_satisfied` as dict containing AT LEAST keys `vehicle_capacity` and `driver_hours_max` (additional hard-constraint keys are welcome) where every value is `true`.

### 8.5 `POST /drift/check`

Calls `DriftMonitor.check_drift(model_name, current_data)` which returns a `DriftReport`. `overall_severity` is a 3-value string enum: `"none" | "moderate" | "severe"` — the library never emits `"low"`. Per-feature results carry `psi: float`, `ks_statistic: float`, `ks_pvalue: float` — the library computes only PSI and KS, not chi² or JS-divergence.

- **Auth:** none.
- **Request body:**
  ```json
  {
    "model_id": "forecast_sprint1_v3",
    "window_days": 30,
    "reference_window": "training"
  }
  ```
- **Response 200:**
  ```json
  {
    "model_id": "forecast_sprint1_v3",
    "overall_severity": "moderate",
    "tests": [
      {
        "name": "ks",
        "feature": "customer_mix_hash",
        "statistic": 0.34,
        "p_value": 0.002,
        "alert": true
      },
      {
        "name": "psi",
        "feature": "customer_mix_hash",
        "statistic": 0.21,
        "alert": true
      },
      {
        "name": "ks",
        "feature": "avg_order_value",
        "statistic": 0.11,
        "p_value": 0.06,
        "alert": false
      }
    ],
    "recommendations": [
      "customer_mix_hash has shifted — investigate upstream data source",
      "7-day rolling MAPE exceeds training-window p95 on 4 of 7 days"
    ],
    "checked_at": "2026-04-16T15:10:44Z",
    "started_at": "2026-04-16T15:10:43Z",
    "latency_ms": 1840
  }
  ```
  `overall_severity` (not `severity`) matches the library's JSON field name. Each `tests[].name` is one of `{"ks", "psi"}` — those are the two tests kailash-ml emits per feature.
- **Error cases:** every error response shares the top-level `latency_ms` + `started_at` telemetry fields.
  - `409` — `set_reference_data` not yet called → `{"error": "reference data not set for model 'X'; drift_wiring should have fired on train completion — check GET /drift/status/<model_id>"}`. Should not occur because the `/forecast/train` route calls `drift_wiring.wire()` synchronously before returning.
  - `404` — model_id not in registry → `{"error": "model 'X' not found"}`
- **Grader assertion:** response contains ≥ 1 test whose `name ∈ {"ks", "psi"}` with a numeric `statistic`; top-level `overall_severity ∈ {"none", "moderate", "severe"}`.

### 8.5.1 `GET /drift/status/<model_id>`

Debug endpoint so the student can confirm `drift_wiring` fired without having to read `.preflight.json` manually.

- **Response 200:**
  ```json
  {
    "model_id": "forecast_sprint1_v3",
    "reference_set": true,
    "reference_set_at": "2026-04-16T14:32:45Z",
    "window_size": 720
  }
  ```
- **Error cases:**
  - `404` — model_id not in registry → `{"error": "model 'X' not found"}`
  - When `reference_set` is `false`, returns 200 with `{"model_id": "...", "reference_set": false, "reference_set_at": null, "window_size": 0}` — the endpoint's purpose is to surface this state without error.

### 8.6 Health + metadata

- `GET /health` — returns typed booleans throughout. Example:
  ```json
  {
    "ok": true,
    "db": true,
    "feature_store": true,
    "drift_wiring": true,
    "registry_runs": 3,
    "nexus_port": 8000,
    "version": "<kailash-ml pinned version>"
  }
  ```
  All status fields (`db`, `feature_store`, `drift_wiring`) are booleans. `registry_runs` is an integer count. Read by `scripts/preflight.py` and by the Viewer Pane's preflight banner; both parse the fields as booleans.
- **Error cases:** `/health` does NOT return 4xx for partial readiness — it returns 200 with individual booleans set to `false` so the banner can surface the specific failing component. Only a 5xx is returned when the Nexus process itself cannot serve (process-level failure).

## 9. Out-of-scope for Week 4

- Fairness audit (Phase 14) — deferred to Week 7.
- Multi-horizon forecasting (7-day + 30-day) — Weeks 5+.
- **Multi-tenant isolation** — deferred because every process runs as a single user. When this product is re-scoped in Week 5+ to a shared backend, `ExperimentTracker.list_runs` MUST take `tenant_id`, every CLI (`metis journal add/list`) MUST pass `tenant_id`, and cache keys / audit rows / metric labels MUST carry a tenant dimension (see `tenant-isolation.md` MUST Rule 1). Week 4's auto-linkage query `ExperimentTracker.list_runs(created_after=<last_entry_timestamp>)` is safe because there is exactly one tenant per process; it would cross-leak in a shared Nexus deployment and is the first call to update.
- Production auth, rate limiting, CORS — disabled; `src/backend/app.py` listens only on `localhost`.
- **Singapore reimbursement-shock scenario** (the SG-equivalent of Week 7's US Medicare scenario; Week 4 ships only the `--dry-run` path for instructor rehearsal — no actual workspace mutation). See `scenario-injection.md` for the renamed event.

## Open questions

None — red-team cycle closed all fabricated APIs and cross-spec inconsistencies. Open questions that survived (e.g. shared-classroom topology, holiday-calendar parametrization) are tracked in the owning specs (`scenario-injection.md`, `data-fixtures.md`).
