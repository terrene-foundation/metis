---
shard_id: 01
slug: backend-core
title: >
  Build the Nexus app factory plus the ml_context facade that wires all
  five kailash-ml engines under a shared ConnectionManager; ship the
  health endpoint, fs_preload startup hook, drift_wiring module, and the
  integration test that proves all four engines share one ConnectionManager.id.
loc_estimate: 280
invariants:
  - shared-connection: all four SQLite stores (.experiments.db, .registry.db, .features.db, implicit drift state) are owned by one ConnectionManager instance
  - fs-preload-idempotent: register_features + store are safe no-ops on second call; never calls non-existent ingest()
  - drift-wiring-synchronous: drift_wiring.wire() is a plain function call, NOT a pub/sub subscriber on a non-existent on_complete event
  - health-booleans: /health fields db/feature_store/drift_wiring are typed bool, not string literals
  - env-only-config: all ports, DB paths, artifact dirs come from .env; no hard-coded values
  - alias-resolver-bijective: resolve_experiment_run_id works for both UUID4 and alias inputs per canonical-values.md §12 — returns UUID unchanged when input already a UUID; resolves alias via data/.experiment_aliases.json; raises KeyError when neither resolves in ExperimentTracker.get_run
call_graph_hops: 3
depends_on: []
blocks: [02, 03, 04]
multi_writer_note: >
  READS .env.example and .preflight.json. Does NOT write .env.example; shard 09 is
  sole writer. fs_preload.py and drift_wiring.py UPDATE specific keys in .preflight.json
  using read-modify-write (json.load → merge dict → atomic .tmp+rename); they do NOT
  perform a full rewrite.
specs_consulted:
  - specs/canonical-values.md §7 (port topology + service names)
  - specs/product-northwind.md §8.6 (health endpoint schema)
  - specs/scaffold-contract.md §2 (backend source file list, PRE-BUILT roles)
  - specs/wiring-contracts.md §11 (FeatureStore wiring test contract)
  - specs/data-fixtures.md §6 (FeatureStore loading flow)
acceptance_criteria:
  - src/backend/app.py creates a Nexus app, registers CORS (localhost-only), calls fs_preload on startup, and mounts routes/__init__.py
  - src/backend/config.py reads all keys enumerated in scaffold-contract.md §10 from .env; no hard-coded strings
  - src/backend/ml_context.py exposes get_ml_context() returning an object with .feature_store, .model_registry, .experiment_tracker, .drift_monitor all sharing one ConnectionManager.id
  - ml_context.py implements derive_model_version_id(name, version) -> "{name}_v{version}" and parse_model_version_id(mvid) -> (name, version) per canonical-values.md §5
  - ml_context.resolve_experiment_run_id(id: str) -> str helper returns the UUID4 for an alias OR the UUID4 unchanged; raises if neither resolves in ExperimentTracker.get_run; reads alias mapping from data/.experiment_aliases.json per canonical-values.md §12
  - At startup, initializes data/.experiment_aliases.json if absent (empty JSON object "{}"); this is the bootstrap step for the alias registry so shard 02 can append atomically on the first train call
  - src/backend/fs_preload.py calls register_features(schema) then store(schema, df) on startup; writes .preflight.json feature_store_populated:true; never calls ingest()
  - src/backend/drift_wiring.py exposes wire(model_name, reference_df, feature_columns) as a plain synchronous function; writes .preflight.json drift_wiring:true as side effect
  - src/backend/routes/health.py returns GET /health with schema from canonical-values.md §8.6 (ok/db/feature_store/drift_wiring as bool, registry_runs as int)
  - src/backend/routes/__init__.py mounts health + drift_status; ships 501-stub registrations for forecast/optimize/drift per scaffold-contract.md §2 banner text (verbatim)
  - src/backend/routes/drift_status.py returns GET /drift/status/<model_id> per product-northwind.md §8.5.1
  - tests/integration/test_ml_context_wiring.py passes: imports via get_ml_context(), constructs against real SQLite tmp_path, calls one method per engine, asserts all four share a single ConnectionManager.id
  - tests/integration/test_feature_store_wiring.py passes per wiring-contracts.md §11 external assertions
  - .preflight.json is updated by fs_preload.py and drift_wiring.py using read-modify-write (json.load → merge dict → atomic .tmp+rename); never a full overwrite
  - .env.example is NOT authored by this shard; shard 09 is sole .env.example writer
wiring_tests:
  - tests/integration/test_ml_context_wiring.py (shared ConnectionManager.id)
  - tests/integration/test_feature_store_wiring.py (wiring-contracts.md §11)
---

# Shard 01 — Backend Core

## What

Implement all PRE-BUILT backend infrastructure files that every other shard depends on. This is the single foundation shard: Nexus app factory, config, ml_context facade, fs_preload, drift_wiring, health route, drift_status route, routes **init** with 501-stubs, conftest for integration tests, and the two wiring tests that guard this shard's external-observable contracts.

## Why

Every other backend shard (02, 03, 04) imports from `src/backend/ml_context` and calls `get_ml_context()`. If the ConnectionManager is not shared, run IDs written during /forecast/train vanish from /forecast/compare. If drift_wiring subscribes to a non-existent event hook, every /drift/check returns 409. This shard must land before any route shard can be built.

## Implementation sketch

- `config.py` — pydantic Settings class reading all keys from scaffold-contract.md §10; no defaults for secrets
- `ml_context.py` — constructs ConnectionManager once; passes it to FeatureStore, ModelRegistry, ExperimentTracker, DriftMonitor constructors; caches the result in module-level `_ctx`; adds `derive_model_version_id` + `parse_model_version_id` helpers per canonical-values.md §5
- `fs_preload.py` — imports FeatureSchema from specs/schemas/demand.py; loads northwind_demand.csv with polars; calls `await fs.register_features(schema)` then `await fs.store(schema, df)`; writes `.preflight.json` key atomically
- `drift_wiring.py` — `wire(model_name, reference_df, feature_columns)`: calls `await ctx.drift_monitor.set_reference_data(model_name, reference_df, feature_columns)` (positional); writes `.preflight.json.drift_wiring: true`
- `app.py` — Nexus factory with CORS bound to 127.0.0.1; startup lifespan hook calls `fs_preload.run()`; mounts `routes.router`
- `routes/__init__.py` — mounts health + drift_status; 501-stub registrations for forecast/optimize/drift with banner text from scaffold-contract.md §2 (verbatim copy)
- `routes/health.py` — probes each engine connection; returns typed booleans; reads `.preflight.json` for feature_store + drift_wiring flags
- `routes/drift_status.py` — calls `ctx.drift_monitor.get_reference_status(model_name)`; 200 for both set+unset states, 404 for unknown model
- `tests/integration/conftest.py` — `ml_context_real` fixture: constructs get_ml_context() against tmp_path SQLite dirs; yields; cleans up
- Both wiring tests per wiring-contracts.md §11 contracts

## Out of scope

- Route handler bodies for /forecast, /optimize, /drift (shards 02, 03, 04)
- OR-Tools / PuLP integration (shard 03)
- Next.js viewer (shard 05)
- Data generation (shard 07)
- All scripts except as called by app.py startup (shard 06)

## Acceptance

- [ ] src/backend/app.py creates a Nexus app, registers CORS (localhost-only), calls fs_preload on startup, and mounts routes/**init**.py
- [ ] src/backend/config.py reads all keys enumerated in scaffold-contract.md §10 from .env; no hard-coded strings
- [ ] src/backend/ml_context.py exposes get_ml_context() returning an object with .feature_store, .model_registry, .experiment_tracker, .drift_monitor all sharing one ConnectionManager.id
- [ ] ml_context.py implements derive_model_version_id(name, version) -> "{name}\_v{version}" and parse_model_version_id(mvid) -> (name, version) per canonical-values.md §5
- [ ] ml_context.py implements resolve_experiment_run_id(id: str) -> str that returns the UUID4 for an alias OR the UUID4 unchanged; raises if neither resolves via ExperimentTracker.get_run; reads data/.experiment_aliases.json per canonical-values.md §12
- [ ] At startup, data/.experiment_aliases.json is initialized if absent (empty JSON object "{}")
- [ ] src/backend/fs_preload.py calls register_features(schema) then store(schema, df) on startup; writes .preflight.json feature_store_populated:true; never calls ingest()
- [ ] src/backend/drift_wiring.py exposes wire(model_name, reference_df, feature_columns) as a plain synchronous function; writes .preflight.json drift_wiring:true as side effect
- [ ] src/backend/routes/health.py returns GET /health with schema from canonical-values.md §8.6 (ok/db/feature_store/drift_wiring as bool, registry_runs as int)
- [ ] src/backend/routes/**init**.py mounts health + drift_status; ships 501-stub registrations for forecast/optimize/drift per scaffold-contract.md §2 banner text (verbatim)
- [ ] src/backend/routes/drift_status.py returns GET /drift/status/<model_id> per product-northwind.md §8.5.1
- [ ] tests/integration/test_ml_context_wiring.py passes: imports via get_ml_context(), constructs against real SQLite tmp_path, calls one method per engine, asserts all four share a single ConnectionManager.id
- [ ] tests/integration/test_feature_store_wiring.py passes per wiring-contracts.md §11 external assertions
- [ ] .preflight.json updated by fs_preload.py + drift_wiring.py using read-modify-write (json.load → merge dict → atomic .tmp+rename); never a full rewrite
- [ ] .env.example is NOT authored by this shard; shard 09 is sole .env.example writer
