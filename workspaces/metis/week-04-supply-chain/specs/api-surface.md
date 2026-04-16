<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# API Surface — Student Reference

Prose view of the six Nexus endpoints the workshop ships, mirroring `canonical-values.md` §8.1-§8.6. Keep them in sync: a change to an endpoint contract must land in both specs.

All endpoints are unauthenticated (local workshop only) and emit top-level telemetry fields `latency_ms: int` and `started_at: string (ISO-8601)` added by Nexus middleware — these appear on both success and error responses.

---

## 1. `POST /forecast/train`

Train a model using AutoML + the FeatureStore. Canonical: `canonical-values.md` §8.1.

Request:

- `feature_schema: string` — e.g. `"user_demand"`; must be registered by `fs_preload.py`.
- `target: string` — e.g. `"orders_next_day"`.
- `search_strategy: string` — one of `"grid"`, `"random"`, `"bayesian"`, `"successive_halving"` (see `canonical-values.md` §2). Workshop default: `"random"`.
- `search_n_trials: int` — workshop uses 5; the `KAILASH_ML_AUTOML_QUICK=1` env caps this at 20.
- `candidate_families: list[string]` — fully-qualified Python class paths; see `canonical-values.md` §8.7.
- `split_strategy: string` — one of `"holdout"`, `"kfold"`, `"stratified_kfold"`, `"walk_forward"` (see `canonical-values.md` §3). Workshop default: `"walk_forward"`.
- `auto_approve: bool` — default `false`.

Response 200: `{ experiment_run_id, leaderboard_path, n_runs_logged, best_metric: {mape, rmse}, training_duration_s }`.

Errors:

- `400` unknown schema — "schema X not registered; check `fs_preload.py` ran".
- `409` FeatureStore empty — "restart Nexus so `fs_preload.py` runs `register_features` + `store` on startup".
- `422` trial cap — "reduce `search_n_trials` to <=20, or unset `KAILASH_ML_AUTOML_QUICK`".
- `500` training failure — body carries `error_category ∈ {xgb_missing, cv_split_failed, other}`.

---

## 2. `GET /forecast/compare`

List and compare prior training runs for the Leaderboard panel. Canonical: §8.2.

Query: `top_n: int = 5`, `scenario: string | null` (one of `"preunion"`, `"postunion"`, `"postdrift"`).

Response 200: `{ runs: [{run_id, family, params_hash, metrics, training_duration_s}], compared_at }` — at least 3 runs, each with distinct `params_hash`.

Errors:

- `409` — fewer than 3 runs available. Fix: fall back to `data/leaderboard_prebaked.json`.

---

## 3. `POST /forecast/predict`

Predict from a trained model version. Canonical: §8.3.

Request: `{ model_version_id, inputs: [{depot_id, date, features}] }`. The `model_version_id` is the derived string `{name}_v{version}` per `canonical-values.md` §5.

Response 200: `{ model_version_id, model_stage, predictions: [{depot_id, date, predicted_orders, interval_80: [lo, hi]}], predicted_at }`. `model_stage` is one of the four lifecycle states in `canonical-values.md` §4.

Errors:

- `404` model not found — "run Phase 4 AutoML + Phase 8 to register and promote a model".
- `409` archived — "promote archived → staging first".
- `422` feature validation — "all features in the schema must be present and numeric".

---

## 4. `POST /optimize/solve`

Solve a VRP (OR-Tools primary; PuLP LP alt). Canonical: §8.4.

Request: `{ forecast_path, objective: {terms: [{name, weight, unit}]}, hard_constraints, soft_constraints, time_budget_s = 30, scenario_tag }`.

Response 200: `{ feasibility, optimality_gap, objective_value, hard_constraints_satisfied, plan_path, solver, wallclock_s, experiment_tags }`. `hard_constraints_satisfied` is a dict keyed by constraint name with boolean values; grader requires at minimum `vehicle_capacity` and `driver_hours_max` keys.

Errors:

- `422` — forecast missing; "run `/forecast/predict` first".
- `409` — infeasible with no soft constraint to relax; body carries `violated_constraints` + `suggestion`.
- `500` — solver crashed or exceeded `time_budget_s`; body carries `error_category ∈ {timeout, internal}`.

---

## 5. `POST /drift/check`

Run `DriftMonitor.check_drift`. Canonical: §8.5.

Request: `{ model_id, window_days = 30, reference_window = "training" }`. `model_id` is the alias per `canonical-values.md` §5.

Response 200: `{ model_id, severity, tests: [{name, feature, statistic, p_value?, alert}], recommendations, checked_at }`. `severity` is one of `"none"`, `"moderate"`, `"severe"` — there is no `"low"` value (the kailash-ml library never emits it; `canonical-values.md` §1). `tests[*].name` is one of `"ks"`, `"psi"` — no chi² or JS-divergence (library does not ship them).

Errors:

- `404` model not found.
- `409` reference not set — "GET /drift/status/<model_id> to confirm; if `reference_set: false`, re-run `/forecast/train` (which calls `drift_wiring.wire` synchronously)".

---

## 6. `GET /health`

Canonical: §8.6.

Response 200: `{ ok: bool, db: bool, feature_store: bool, drift_wiring: bool, registry_runs: int, nexus_port: int }`. Every flag is a boolean (not a string). Consumed by `scripts/preflight.py` and the Viewer's Preflight Banner.

---

## Error taxonomy (summary)

- `4xx` — caller error. Body carries a short `error` string plus, where the endpoint supports it, a specific hint (e.g. `suggestion`, `violated_constraints`, `error_category`).
- `5xx` — server error. Body carries `error_category` (string, bounded vocabulary per endpoint) so the grader can map to an actionable fix message.
- Every error response carries `latency_ms` and `started_at`.

## Related specs

- `canonical-values.md` §8 — request/response shapes, single source of truth.
- `success-criteria.md` — the `ENDPOINT_CONTRACTS` dict the grader imports.
- `rubric-grader.md` §3.4 — actionable-message mapping for every documented error.
- `product-northwind.md` §8 — example request/response bodies.
