<!--
SPDX-License-Identifier: CC-BY-4.0
Copyright (c) 2026 Terrene Foundation. Licensed under CC BY 4.0.
-->

# Wiring Contracts — Tier-2 Integration Tests for Every Facade Manager

**Authority**: `.claude/rules/facade-manager-detection.md` MUST Rules 1-3 and `.claude/rules/orphan-detection.md` MUST Rules 1-2. The red-team audit (`04-validate/redteam-specs.md §4`) found 11/11 components exposed through the Week 4 scaffold fail the wiring test requirement — `scaffold-contract.md §9` lists intended call sites but names no test file. This spec closes that gap by defining one Tier-2 wiring test per component.

**Rule restated**: every `*Manager` / `*Executor` / `*Store` / `*Registry` / `*Engine` / `*Service` exposed via a framework facade (`get_ml_context().X`, `nexus.register_endpoints`) MUST have `tests/integration/test_<lowercase_name>_wiring.py` that (a) imports the class through the facade, (b) constructs a real instance against real infrastructure, (c) triggers a production code path, (d) asserts an externally-observable effect. Mocks of the component-under-test or its dependencies are BLOCKED in these tests (`.claude/rules/testing.md` § Tier 2).

**Scope**: the 11 kailash-ml engines named in the scaffold. The three [STUDENT-COMMISSIONED] route files (`forecast.py`, `optimize.py`, `drift.py`) assume the 501-stub registration fix from the red team (C11) so the production call site exists at commit time, before the student fills the body. Shared fixture: `tests/integration/conftest.py::ml_context_real` constructs `get_ml_context()` against a temp SQLite DB and yields it; every test below consumes that fixture. (AnomalyDetectionEngine was previously listed as component §12; removed per `orphan-detection.md` MUST Rule 3 — no natural call site existed; decision recorded in `todos/active/04-drift-endpoints.md`.)

---

## 1. TrainingPipeline

**Defined in spec**: `scaffold-contract.md §9`, `product-northwind.md §8.1`, `playbook-universal.md` Phase 4.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_train` — the `POST /forecast/train` handler constructs `TrainingPipeline(feature_store=ctx.feature_store, registry=ctx.model_registry)` and calls `.train(data=df, schema=schema, config=config, eval_spec=eval_spec)`. The 501-stub registration from redteam fix C11 is the pre-student call site; the filled body is the post-student call site.
**Test file**: `tests/integration/test_training_pipeline_wiring.py`
**Test name**: `test_training_pipeline_persists_model_artifact`
**Import path**: `from src.backend.ml_context import get_ml_context` then `ctx.training_pipeline` (NOT `from kailash_ml.engines.training_pipeline import TrainingPipeline`).
**Real infrastructure required**: real SQLite FeatureStore + ModelRegistry DBs under `tmp_path`, real `northwind_demand.csv` slice (100 rows), real `FeatureSchema` from `specs/schemas/demand.py`.
**Setup**: `ml_context_real` fixture, `seed_feature_store(ctx, sample_df)` helper to pre-populate the schema, `sample_eval_spec` with `split_strategy="walk_forward"` (per redteam C5).
**Action**: POST `/forecast/train` with `{"candidate_families": ["sklearn.linear_model.LinearRegression"], "search_n_trials": 1, "split_strategy": "walk_forward"}` — fully-qualified class paths per `canonical-values.md §8.7`.
**External assertion**: (1) HTTP 200 with `experiment_run_id` in the body; (2) `ctx.model_registry.get_model("forecast", version=1)` returns a `ModelVersion` whose `artifact_path` is a file that exists on disk and is non-empty; (3) `ctx.experiment_tracker.get_run(experiment_run_id)` returns a row with `status="COMPLETED"` and at least one metric. No `assert_called` calls permitted.
**Failure mode this test prevents**: Phase 5.11-style orphan — `TrainingPipeline` instantiated in `ml_context.py` but never invoked because the route handler skipped the facade and constructed its own pipeline. Also catches the C1 constructor-kwarg regression.
**Cross-ref**: `scaffold-contract.md §9`; `product-northwind.md §8.1`.

## 2. AutoMLEngine

**Defined in spec**: `product-northwind.md §8.1`, `playbook-universal.md` Phase 4, `scaffold-contract.md` `routes/forecast.py` banner.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_train` — the same handler constructs `AutoMLEngine(pipeline, search, registry=ctx.model_registry)` (positional per redteam C1) and calls `.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name="forecast_sprint1", tracker=ctx.experiment_tracker)`.
**Test file**: `tests/integration/test_automl_engine_wiring.py`
**Test name**: `test_automl_engine_populates_leaderboard_via_tracker`
**Import path**: via `ctx.automl_engine` if exposed on `ml_context`, else constructed in the test exactly as the route handler does; never bypass `ml_context`.
**Real infrastructure required**: real SQLite (ExperimentTracker + ModelRegistry + FeatureStore), real polars DataFrame slice.
**Setup**: `ml_context_real`; `AutoMLConfig(candidate_families=["sklearn.linear_model.LinearRegression", "sklearn.ensemble.RandomForestRegressor"], max_trials=2)` — per redteam C9 the field is `candidate_families`, not `families`; values are fully-qualified Python class paths per `canonical-values.md §8.7`.
**Action**: POST `/forecast/train` with 2 candidate families and 2 trials; then GET `/forecast/compare`.
**External assertion**: (1) `ctx.experiment_tracker.list_runs(experiment_name="forecast_sprint1")` returns ≥2 rows; (2) at least one has a non-null `metrics["rmse"]`; (3) a leaderboard JSON is written to `data/leaderboard.json` with ≥2 entries sorted by rmse ascending.
**Failure mode this test prevents**: the C1 regression (wrong kwargs crash the first Phase 4 run, silently producing an empty leaderboard if the route handler swallows the TypeError) and the orphan pattern where AutoMLEngine runs but never writes to the tracker the ml_context constructed.
**Cross-ref**: `product-northwind.md §8.1`; `playbook-universal.md` Phase 4.

## 3. ExperimentTracker

**Defined in spec**: `scaffold-contract.md §9`, `product-northwind.md §7`, `decision-journal.md §3`.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_compare` (GET `/forecast/compare` calls `ctx.experiment_tracker.compare_runs`) and `:forecast_train` (logs run via tracker passed to AutoMLEngine).
**Test file**: `tests/integration/test_experiment_tracker_wiring.py`
**Test name**: `test_experiment_tracker_persists_run_id_across_compare`
**Import path**: `ctx.experiment_tracker`.
**Real infrastructure required**: real SQLite experiment DB under `tmp_path`.
**Setup**: `ml_context_real`; seed three runs via `scripts/seed_experiments.py` helper to populate `data/leaderboard_prebaked.json` ExperimentTracker rows.
**Action**: POST `/forecast/train` once, then GET `/forecast/compare` with the seeded run_ids + the new run_id.
**External assertion**: (1) response body contains ≥3 rows with distinct `run_id`s; (2) `ctx.experiment_tracker.get_run(new_run_id)` returns a row with non-null `created_at`; (3) the same connection used by `ml_context` can read the run immediately (single-DB coherence check) — proves the shared `ConnectionManager` invariant from redteam C6.
**Failure mode this test prevents**: parallel-framework orphan — if each engine constructed its own ExperimentTracker, the run_id written during `/train` would not be visible to the ExperimentTracker queried by `/compare`, and journal entries would cite run_ids that vanish between phases.
**Cross-ref**: `decision-journal.md §3`; `product-northwind.md §8.2`.

## 4. ModelRegistry

**Defined in spec**: `product-northwind.md §8.3`, `scaffold-contract.md §9`, `playbook-universal.md` Phase 9.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_predict` calls `ctx.model_registry.get_model(name, version)` to resolve the served version; `:forecast_train` transitions stage after successful run.
**Test file**: `tests/integration/test_model_registry_wiring.py`
**Test name**: `test_model_registry_round_trips_via_predict`
**Import path**: `ctx.model_registry`.
**Real infrastructure required**: real SQLite registry DB + real on-disk artifact dir.
**Setup**: `ml_context_real`; pre-register one model via `ctx.model_registry.register_model(name="forecast", version=1, artifact_path=..., stage="staging")`.
**Action**: POST `/forecast/predict` with `{"model_name": "forecast", "model_version": 1, "features": {...}}`.
**External assertion**: (1) response includes the resolved `model_version_id` (per redteam C8 derivation); (2) the ModelVersion row read back from `ctx.model_registry.get_model("forecast", 1)` has a `last_accessed_at` timestamp strictly greater than before the predict call, proving the route actually hit the registry the facade exposes.
**Failure mode this test prevents**: the "ModelRegistry was built but never consulted" orphan — the route could hard-code a model path and bypass the registry entirely, which would pass a happy-path smoke test but leave `stage` transitions never called.
**Cross-ref**: `product-northwind.md §8.3`.

## 5. InferenceServer

**Defined in spec**: `product-northwind.md §8.3`, `scaffold-contract.md §9`.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_predict` — the handler calls `await ctx.inference_server.predict(model_name, version, features)`; the Nexus `register_endpoints` wiring is called from `src/backend/app.py` startup (if used as a Nexus plugin).
**Test file**: `tests/integration/test_inference_server_wiring.py`
**Test name**: `test_inference_server_writes_forecast_output_file`
**Import path**: `ctx.inference_server`.
**Real infrastructure required**: real on-disk artifact, real kailash-nexus app in-process (TestClient, NO mocks).
**Setup**: `ml_context_real`, pre-registered model with a minimal sklearn LinearRegression artifact persisted by a helper fixture.
**Action**: POST `/forecast/predict` with valid features via the Nexus TestClient.
**External assertion**: (1) response contains numeric `predictions` array of expected length; (2) a file at `data/forecast_output.json` is written (the Viewer filesystem-watch contract from `viewer-pane.md`) and contains `model_version_id`, `predictions`, `generated_at`; (3) `ctx.inference_server.get_model_info(...)` reports the model is loaded (proves cache coherence between predict and info paths).
**Failure mode this test prevents**: the "InferenceServer exposed but predictions bypass it" orphan — the route could call `sklearn.predict` directly, skipping the server's caching, batching, and model-version tracking.
**Cross-ref**: `product-northwind.md §8.3`; `viewer-pane.md` (forecast-output contract).

## 6. DriftMonitor

**Defined in spec**: `product-northwind.md §6, §8.5`, `scaffold-contract.md` drift_wiring.py, `playbook-universal.md` Phase 13.
**Production call site(s)**: `src/backend/drift_wiring.py:wire` (called synchronously from `routes/forecast.py` after `.train()` completes, per redteam C3 fix — not via event hook) calls `ctx.drift_monitor.set_reference_data(...)`; `src/backend/routes/drift.py:drift_check` calls `ctx.drift_monitor.check_drift(...)`.
**Test file**: `tests/integration/test_drift_monitor_wiring.py`
**Test name**: `test_drift_monitor_overall_severity_after_train_then_check`
**Import path**: `ctx.drift_monitor`.
**Real infrastructure required**: real SQLite drift-state DB (shared ConnectionManager with other engines), real pre- and post-drift polars frames.
**Setup**: `ml_context_real`; two frames — a reference slice and `data/scenarios/week78_drift.json` applied to the holdout.
**Action**: POST `/forecast/train` (triggers `drift_wiring.wire` as a side effect), then POST `/drift/check` with `model_id` and `current_data_ref`.
**External assertion**: (1) response JSON contains `overall_severity` (NOT `severity` per redteam C2) with value ∈ `{"none", "moderate", "severe"}` (3-value enum); (2) `data/drift_report.json` written to disk with same field name; (3) `.preflight.json.drift_wiring === true` after the train call, proving `drift_wiring.wire` fired (side-effect marker per redteam C3).
**Failure mode this test prevents**: the original C3 failure — `drift_wiring.py` subscribes to a non-existent event hook, so `set_reference_data` is never called, so every `/drift/check` returns 409 "reference data not set." The test asserts the synchronous-wire fix actually runs.
**Cross-ref**: `product-northwind.md §8.5`; `scaffold-contract.md` drift_wiring.py row.

## 7. ModelExplainer

**Defined in spec**: `playbook-universal.md` Phase 7, `scaffold-contract.md §9`.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_explain` (Phase 7 red-team path) — student fills but the 501-stub registration ships from scaffold; calls `ModelExplainer(model=..., background_data=..., feature_names=...).explain_global()`.
**Test file**: `tests/integration/test_model_explainer_wiring.py`
**Test name**: `test_model_explainer_returns_feature_importance_or_falls_back`
**Import path**: constructed inline via `kailash_ml.engines.model_explainer.ModelExplainer` (not a facade manager; it's a per-call object). The wiring test nonetheless asserts the route file imports it.
**Real infrastructure required**: real trained model artifact from a real TrainingPipeline run (chained fixture on `test_training_pipeline_wiring`).
**Setup**: `ml_context_real`, pre-trained model via the training-pipeline helper, `kailash-ml[explain]` present (preflight hard-fail per redteam C10 if missing).
**Action**: call the explainer path (direct or via a Phase 7 helper endpoint) with the trained model.
**External assertion**: (1) returned dict has non-empty `feature_importance` with values summing to a finite number; (2) if SHAP ImportError fires, the `model_visualizer.permutation_importance` fallback runs AND the journal-entry side effect records the fallback reason (per redteam C10); (3) no silent-pass path — either SHAP works or the documented fallback fires with a logged reason. TODO: the route for Phase 7 explanation is not pinned in `product-northwind.md §8` endpoint list; flag to pin before `/implement`.
**Failure mode this test prevents**: SHAP import works in CI but fails on 15-30% of Apple-Silicon student machines (redteam C10). The fallback is documented but untested, meaning the fallback path could itself be broken.
**Cross-ref**: `playbook-universal.md` Phase 7.

## 8. DataExplorer

**Defined in spec**: `playbook-universal.md` Phase 2, `scaffold-contract.md §9`.
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_explore` (Phase 2 path) — student fills; 501-stub ships from scaffold; calls `DataExplorer(...).profile(df)` and `.visualize(df)`.
**Test file**: `tests/integration/test_data_explorer_wiring.py`
**Test name**: `test_data_explorer_profile_emits_schema_and_visualize_writes_file`
**Import path**: `kailash_ml.engines.data_explorer.DataExplorer` constructed in the route; the wiring test asserts the route imports and calls it.
**Real infrastructure required**: real `data/northwind_demand.csv` (100-row slice).
**Setup**: `ml_context_real`, pre-loaded sample frame.
**Action**: call the Phase 2 explore endpoint with the sample frame.
**External assertion**: (1) `.profile()` returns a dict containing `schema`, `row_count` equal to input length, per-column `null_count`; (2) `.visualize()` writes an HTML/PNG artifact under `data/artifacts/` that exists on disk and is non-empty; (3) no mocked DataFrame — real polars frame produces real numeric stats.
**Failure mode this test prevents**: Phase 2 could be "skipped" by the student's prompt (the playbook prompt describes it but doesn't hard-require the call), producing journal entries that cite insights DataExplorer never actually computed.
**Cross-ref**: `playbook-universal.md` Phase 2.

## 9. ModelVisualizer

**Defined in spec**: `playbook-universal.md` Phase 5 (fold-variance plot), red-team fallback for `ModelExplainer` (redteam C10 — `permutation_importance` path).
**Production call site(s)**: `src/backend/routes/forecast.py:forecast_train` writes `training_history` plot via `ModelVisualizer(...).training_history(...)` after training; the SHAP-fallback path in Phase 7 uses `model_visualizer.permutation_importance`.
**Test file**: `tests/integration/test_model_visualizer_wiring.py`
**Test name**: `test_model_visualizer_training_history_writes_png`
**Import path**: `kailash_ml.engines.model_visualizer.ModelVisualizer`.
**Real infrastructure required**: real trained-model artifact + real CV history from a TrainingPipeline fold-log (chained on `test_training_pipeline_wiring`).
**Setup**: `ml_context_real`, real TrainingResult with ≥2 folds.
**Action**: POST `/forecast/train` with `split_strategy="walk_forward"` and 3 folds.
**External assertion**: (1) a PNG file lands at `data/artifacts/training_history_<run_id>.png` and decodes as a valid image (PIL `Image.open` loads without error); (2) the run's metrics include per-fold entries. TODO: the scaffold does not currently pin the visualizer's output path — flag to add to `product-northwind.md §8.1`.
**Failure mode this test prevents**: Phase 5's fold-variance journal claim is backed by a real plot; without the test, the student's journal could cite fold variance using numbers the visualizer never computed.
**Cross-ref**: `playbook-universal.md` Phase 5.

## 10. FeatureEngineer

**Defined in spec**: `playbook-universal.md` Phase 3 (optional feature engineering), `scaffold-contract.md §9` (implied — not explicitly listed, flagged as TODO in redteam audit).
**Production call site(s)**: `src/backend/fs_preload.py` — after CSV ingestion via `ctx.feature_store.register_features` + `.store` (redteam C4 fix), `FeatureEngineer(...).generate(df)` runs lag/rolling feature derivation before the store call. TODO: the scaffold today does NOT name this call site; if FeatureEngineer is not invoked by `fs_preload.py` it is a pure orphan and should be removed from the public surface (per `orphan-detection.md` MUST Rule 3). Decision required at `/implement` gate.
**Test file**: `tests/integration/test_feature_engineer_wiring.py`
**Test name**: `test_feature_engineer_adds_lag_columns_before_store`
**Import path**: `kailash_ml.engines.feature_engineer.FeatureEngineer`.
**Real infrastructure required**: real polars frame, real FeatureStore.
**Setup**: `ml_context_real`, baseline frame without lag columns.
**Action**: run `fs_preload` against the real CSV slice.
**External assertion**: after preload, `ctx.feature_store.get_features(schema, entity_ids)` returns rows where the engineered columns (e.g. `orders_lag_7`, `orders_rolling_28d`) are populated with non-null numeric values; row count equals input row count minus the lag window.
**Failure mode this test prevents**: FeatureEngineer is wired in `fs_preload.py` but the output is not persisted (orphan by side-effect) — training sees un-engineered features, Phase 4 models silently underperform, and the leaderboard story is false.
**Cross-ref**: `playbook-universal.md` Phase 3. **TODO**: confirm the call site before `/implement` lands.

## 11. FeatureStore

**Defined in spec**: `product-northwind.md §8.1`, `scaffold-contract.md fs_preload.py`, `data-fixtures.md §6.2`.
**Production call site(s)**: `src/backend/fs_preload.py` (startup — calls `ctx.feature_store.register_features(schema)` then `.store(schema, df)` per redteam C4 — NOT `.ingest()`); `src/backend/routes/forecast.py:forecast_train` calls `ctx.feature_store.get_features(...)` to pull training data.
**Test file**: `tests/integration/test_feature_store_wiring.py`
**Test name**: `test_feature_store_preload_populates_and_get_features_reads`
**Import path**: `ctx.feature_store`.
**Real infrastructure required**: real SQLite FeatureStore DB under `tmp_path`, real CSV slice.
**Setup**: `ml_context_real`, fresh DB.
**Action**: invoke `fs_preload.main(ctx)` (startup hook) then call `ctx.feature_store.get_features(schema, entity_ids=[...])`.
**External assertion**: (1) `ctx.feature_store.list_schemas()` contains `"user_demand"` after preload; (2) `get_features` returns ≥1 row with every feature column populated per `specs/schemas/demand.py`; (3) `/health` returns `feature_store: true` (boolean per redteam H2).
**Failure mode this test prevents**: the C4 regression — `fs_preload.py` called the non-existent `ingest()` method, crashing startup silently; the test forces the real `register_features`+`store` path.
**Cross-ref**: `product-northwind.md §8.1`; `scaffold-contract.md` fs_preload.py row.

---

## Audit hook

`/redteam` and `/codify` MUST, per `orphan-detection.md` § Detection Protocol, grep `tests/integration/` for the 11 filenames listed above; any missing file is a HIGH finding. `grade_product.py` SHOULD run these 11 tests as part of preflight on every student machine — if any fail, `.preflight.json.wiring_tests = false` and the red strip surfaces a specific component name.
