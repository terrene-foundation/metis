---
shard_id: 02
slug: forecast-endpoints
title: >
  Implement the three STUDENT-COMMISSIONED forecast route handlers
  (POST /forecast/train, GET /forecast/compare, POST /forecast/predict)
  with correct kailash-ml constructor shapes, walk_forward eval, synchronous
  drift_wiring call after train, and the four Tier-2 wiring tests that guard
  TrainingPipeline, AutoMLEngine, ExperimentTracker, ModelRegistry, and
  InferenceServer.
loc_estimate: 390
invariants:
  - automl-constructor: AutoMLEngine(pipeline, search, registry=registry) positional + keyword; never AutoMLEngine(feature_store=, model_registry=, config=)
  - automlconfig-field: AutoMLConfig uses candidate_families=[...]; no families= alias
  - evalspec-strategy: EvalSpec uses split_strategy="walk_forward"; never cv_strategy="rolling_origin"
  - drift-wire-before-return: drift_wiring.wire() called synchronously after pipeline.train() completes, before HTTP response is sent
  - model-version-id-derived: /forecast/predict accepts model_version_id string of form {name}_v{version}; resolves via ml_context.parse_model_version_id
call_graph_hops: 4
depends_on: [01]
blocks: [04]
specs_consulted:
  - specs/canonical-values.md §2 (AutoML search strategies)
  - specs/canonical-values.md §3 (EvalSpec split strategies)
  - specs/canonical-values.md §4 (ModelRegistry lifecycle states)
  - specs/canonical-values.md §5 (model versioning shape)
  - specs/canonical-values.md §8.1-8.3 (endpoint contracts)
  - specs/canonical-values.md §12 (ExperimentTracker run ID format)
  - specs/product-northwind.md §8.1-8.3 (full request/response schemas + error taxonomy)
  - specs/scaffold-contract.md §2 (banner text for routes/forecast.py, verbatim)
  - specs/wiring-contracts.md §1-5 (TrainingPipeline, AutoMLEngine, ExperimentTracker, ModelRegistry, InferenceServer)
acceptance_criteria:
  - src/backend/routes/forecast.py ships with the TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub handler bodies remain intact for student replacement
  - POST /forecast/train: constructs TrainingPipeline(feature_store=fs, registry=registry), HyperparameterSearch, AutoMLEngine(pipeline, search, registry=registry); calls engine.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name="forecast_sprint1", tracker=tracker); calls drift_wiring.wire() synchronously before return; returns schema from canonical-values.md §8.1
  - GET /forecast/compare: calls ctx.experiment_tracker.list_runs or compare_runs; returns >=3 runs with distinct params_hash; returns 409 when fewer than 3 runs; schema per canonical-values.md §8.2
  - POST /forecast/predict: accepts model_version_id of form {name}_v{version}; resolves via ml_context.parse_model_version_id; calls ctx.inference_server.predict; writes data/forecast_output.json; returns 404/409/422 error cases per canonical-values.md §8.3
  - AutoMLConfig uses candidate_families=[...] with KAILASH_ML_AUTOML_QUICK cap of 20 trials enforced; returns 422 on violation
  - AutoMLConfig.candidate_families receives fully-qualified Python class names per canonical-values.md §8.7 (e.g. "sklearn.linear_model.LinearRegression", "xgboost.XGBRegressor"); short names are BLOCKED; preflight substitution for missing [xgb] extra documented (GradientBoostingRegressor with different random_state, announced visibly)
  - EvalSpec uses split_strategy="walk_forward"; returns 400 on unrecognised value
  - tests/integration/test_training_pipeline_wiring.py passes per wiring-contracts.md §1 external assertions (model artifact on disk + ExperimentTracker row with status=COMPLETED)
  - tests/integration/test_automl_engine_wiring.py passes per wiring-contracts.md §2 (>=2 tracker rows, leaderboard.json written)
  - tests/integration/test_experiment_tracker_wiring.py passes per wiring-contracts.md §3 (run_id visible to /compare via shared ConnectionManager)
  - tests/integration/test_model_registry_wiring.py passes per wiring-contracts.md §4 (last_accessed_at updated after /predict)
  - tests/integration/test_inference_server_wiring.py passes per wiring-contracts.md §5 (data/forecast_output.json written, model_version_id + predictions present)
  - tests/integration/test_model_explainer_wiring.py passes per wiring-contracts.md §7: imports ModelExplainer through get_ml_context() facade; calls explain() on a trained model; asserts non-empty explanation dict returned (orphan-detection Rule 2 — real infrastructure, no mocks)
  - tests/integration/test_data_explorer_wiring.py passes per wiring-contracts.md §8: imports DataExplorer through get_ml_context() facade; calls describe(df) on northwind_demand.csv sample; asserts non-empty summary dict with at least one feature key (orphan-detection Rule 2)
  - tests/integration/test_model_visualizer_wiring.py passes per wiring-contracts.md §9: imports ModelVisualizer through get_ml_context() facade; calls plot() on a trained model; asserts returned artifact path string is non-empty (orphan-detection Rule 2)
  - After each AutoMLEngine.run() completes in /forecast/train, the handler appends a {alias: uuid4} entry to data/.experiment_aliases.json atomically (read-modify-write with .tmp+rename) for each run produced, using alias format "{short_family}_{ordinal:03d}_{YYYYMMDD}_{HHMMSS}" per canonical-values.md §12
orphan_resolution:
  ModelExplainer: "WIRED — test_model_explainer_wiring.py added to this shard; call site is the Phase 7 red-team path in routes/forecast.py (student-commissioned) but the wiring test proves the facade accessor resolves to a live object; per orphan-detection Rule 1 + facade-manager-detection Rule 1"
  DataExplorer: "WIRED — test_data_explorer_wiring.py added to this shard; call site is the Phase 2 data audit path (student-commissioned); wiring test asserts DataExplorer.describe() returns a non-empty dict"
  ModelVisualizer: "WIRED — test_model_visualizer_wiring.py added to this shard; call site is the Phase 5 fold-variance plot path (student-commissioned); wiring test asserts ModelVisualizer.plot() produces an artifact path string"
wiring_tests:
  - tests/integration/test_training_pipeline_wiring.py (wiring-contracts.md §1)
  - tests/integration/test_automl_engine_wiring.py (wiring-contracts.md §2)
  - tests/integration/test_experiment_tracker_wiring.py (wiring-contracts.md §3)
  - tests/integration/test_model_registry_wiring.py (wiring-contracts.md §4)
  - tests/integration/test_inference_server_wiring.py (wiring-contracts.md §5)
  - tests/integration/test_model_explainer_wiring.py (wiring-contracts.md §7)
  - tests/integration/test_data_explorer_wiring.py (wiring-contracts.md §8)
  - tests/integration/test_model_visualizer_wiring.py (wiring-contracts.md §9)
  - tests/unit/test_experiment_alias_write.py (canonical-values.md §12 alias-write contract: asserts /forecast/train appends {alias: uuid4} entry to data/.experiment_aliases.json for each run)
---

# Shard 02 — Forecast Endpoints

## What

Implement the three forecast route handlers that students will eventually replace with their own commissioned versions, but ship first as 501-stubs with the correct banner text and the wiring tests that prove the production call sites are real from commit 1. The route file itself is STUDENT-COMMISSIONED; this shard builds the surrounding test harness and the 501-registration layer so orphan-detection Rule 1 is satisfied before any student touches the code.

## Why

The five wiring tests in this shard are the primary guard against the Phase 5.11 orphan pattern: a TrainingPipeline or AutoMLEngine that is instantiated in ml_context but never actually called on the hot path. Without these tests passing, the scaffold can ship a leaderboard UI that is populated by a path that bypasses the ml_context facade entirely.

## Implementation sketch

- `routes/forecast.py` — TODO-STUDENT banner (verbatim from scaffold-contract.md §2); three 501-stub handler bodies; route registrations stay put; inline comment documenting forbidden constructor shapes (redteam C1, C9) and required call sites
- Wiring test structure follows wiring-contracts.md §1-5 exactly: each test (a) imports through get_ml_context(), (b) constructs against real SQLite tmp_path via ml_context_real fixture, (c) POSTs via Nexus TestClient (no mocks), (d) asserts an externally-observable side effect (file on disk, DB row, timestamp updated)
- `tests/integration/conftest.py` — add `seed_feature_store(ctx, sample_df)` helper; add `sample_eval_spec` fixture with split_strategy="walk_forward"; add minimal LinearRegression artifact fixture for InferenceServer test
- Each test must NOT use assert_called — wiring-contracts.md §1 rule; only real state assertions

## Out of scope

- ModelExplainer / DataExplorer / ModelVisualizer ROUTE BODIES — these are student-commissioned; however wiring tests §7/8/9 ARE in scope for this shard per orphan-detection Rule 1 + facade-manager-detection Rule 1 (call sites must exist in the same PR as the facade)
- /optimize/solve (shard 03)
- /drift/check (shard 04)

## Acceptance

- [ ] src/backend/routes/forecast.py ships with the TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub handler bodies remain intact for student replacement
- [ ] POST /forecast/train: constructs TrainingPipeline(feature_store=fs, registry=registry), HyperparameterSearch, AutoMLEngine(pipeline, search, registry=registry); calls engine.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name="forecast_sprint1", tracker=tracker); calls drift_wiring.wire() synchronously before return; returns schema from canonical-values.md §8.1
- [ ] GET /forecast/compare: calls ctx.experiment_tracker.list_runs or compare_runs; returns >=3 runs with distinct params_hash; returns 409 when fewer than 3 runs; schema per canonical-values.md §8.2
- [ ] POST /forecast/predict: accepts model_version_id of form {name}\_v{version}; resolves via ml_context.parse_model_version_id; calls ctx.inference_server.predict; writes data/forecast_output.json; returns 404/409/422 error cases per canonical-values.md §8.3
- [ ] AutoMLConfig uses candidate_families=[...] with KAILASH_ML_AUTOML_QUICK cap of 20 trials enforced; returns 422 on violation
- [ ] EvalSpec uses split_strategy="walk_forward"; returns 400 on unrecognised value
- [ ] tests/integration/test_training_pipeline_wiring.py passes per wiring-contracts.md §1 external assertions (model artifact on disk + ExperimentTracker row with status=COMPLETED)
- [ ] tests/integration/test_automl_engine_wiring.py passes per wiring-contracts.md §2 (>=2 tracker rows, leaderboard.json written)
- [ ] tests/integration/test_experiment_tracker_wiring.py passes per wiring-contracts.md §3 (run_id visible to /compare via shared ConnectionManager)
- [ ] tests/integration/test_model_registry_wiring.py passes per wiring-contracts.md §4 (last_accessed_at updated after /predict)
- [ ] tests/integration/test_inference_server_wiring.py passes per wiring-contracts.md §5 (data/forecast_output.json written, model_version_id + predictions present)
- [ ] tests/integration/test_model_explainer_wiring.py passes: imports through facade, calls explain(), asserts non-empty dict (wiring-contracts.md §7; no mocks)
- [ ] tests/integration/test_data_explorer_wiring.py passes: imports through facade, calls describe(), asserts non-empty summary dict (wiring-contracts.md §8; no mocks)
- [ ] tests/integration/test_model_visualizer_wiring.py passes: imports through facade, calls plot(), asserts non-empty artifact path string (wiring-contracts.md §9; no mocks)
