# Scaffold Contract — Pre-Built vs Student-Commissioned

This spec is the authority on which files the scaffold ships, which files the student commissions by prompting Claude Code, and which files are pre-built with named extension points. The workspace-root `SCAFFOLD_MANIFEST.md` is a generated view over this spec and is read by the opening prompt so Claude Code verifies the scaffold against a fixed list rather than fabricating one.

## Legend

- `[PRE-BUILT]` — scaffold ships a complete, working file. Students do not edit it.
- `[STUDENT-COMMISSIONED]` — scaffold ships a placeholder with the `# TODO-STUDENT:` banner. Students commission the real file by prompting Claude Code. The grader runs against the student's version.
- `[PRE-BUILT + STUDENT-EXTENDED]` — scaffold ships a skeleton with a named extension point; student adds content at the named slot.

## TODO-STUDENT banner (verbatim, zero-tolerance Rule 2 compliance)

Every `[STUDENT-COMMISSIONED]` and `[STUDENT-EXTENDED]` file MUST begin with the banner below. The comment character varies by language but the text is identical.

```
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace this file with the real
# implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.
# Do NOT edit manually — prompt Claude Code.
```

- Python files: `#` prefix.
- TypeScript / TSX / JSX files: `//` prefix.
- JSON files: wrap as `{"_todo_student": "...banner text...", ...}` — the grader ignores the `_todo_student` key.

The banner is what prevents the scaffold from violating `zero-tolerance.md` Rule 2 ("no stubs"). A file without the banner is either fully implemented (`[PRE-BUILT]`) or a zero-tolerance violation.

## 1. Workspace root (`workspaces/metis/week-04-supply-chain/`)

| Path                   | State                    | Role                                                                       | Orphan-check                 |
| ---------------------- | ------------------------ | -------------------------------------------------------------------------- | ---------------------------- |
| `START_HERE.md`        | `[PRE-BUILT]`            | Student manual — read before class                                         | n/a (doc)                    |
| `SCAFFOLD_MANIFEST.md` | `[PRE-BUILT]`            | Workspace-root copy of this spec; read by opening prompt                   | n/a (doc)                    |
| `PLAYBOOK.md`          | `[PRE-BUILT]`            | 12-phase-in-Week-4 procedure, prompts, checklists, journal schemas, rubric | n/a (doc)                    |
| `PRODUCT_BRIEF.md`     | `[PRE-BUILT]`            | Business context; cost table; personas; 3:30 pm success definition         | n/a (doc)                    |
| `.env.example`         | `[PRE-BUILT]`            | Template env with `KAILASH_ML_AUTOML_QUICK=1`, DB paths, ports             | Read by preflight            |
| `journal/`             | `[STUDENT-COMMISSIONED]` | Directory of `phase_N.md` entries; students write or prompt                | n/a (output)                 |
| `journal/_template.md` | `[PRE-BUILT]`            | Skeleton entry with 5 rubric-dimension headings                            | Read by `metis journal add`  |
| `journal/_examples.md` | `[PRE-BUILT]`            | 3 entries at 4/4 and 3 at 1/4, side-by-side per phase                      | n/a (doc)                    |
| `journal.pdf`          | `[STUDENT-COMMISSIONED]` | Compiled output of `journal/` at close                                     | Produced by `journal_export` |
| `.session-notes`       | `[STUDENT-COMMISSIONED]` | `/wrapup` artifact; not a deliverable                                      | Optional                     |

## 2. Backend source (`src/backend/`)

All backend code is kailash-nexus + kailash-ml. Students never touch this layer except via prompting Claude Code to fill the `[STUDENT-COMMISSIONED]` routes.

| Path                                 | State                            | Role                                                                                                                                                                                                                                                                                                                                                               | Orphan-check                                                                                                                                                                                                                                      |
| ------------------------------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `src/backend/__init__.py`            | `[PRE-BUILT]`                    | Module marker                                                                                                                                                                                                                                                                                                                                                      | n/a                                                                                                                                                                                                                                               |
| `src/backend/app.py`                 | `[PRE-BUILT]`                    | Nexus app factory, CORS, logging, health endpoint                                                                                                                                                                                                                                                                                                                  | Used by `uvicorn` entrypoint                                                                                                                                                                                                                      |
| `src/backend/config.py`              | `[PRE-BUILT]`                    | Reads `.env`; exposes `DB_URL`, `ARTIFACT_DIR`, `EXPERIMENT_DB`, `REGISTRY_DB`                                                                                                                                                                                                                                                                                     | Imported by `app.py`, `ml_context.py`                                                                                                                                                                                                             |
| `src/backend/fs_preload.py`          | `[PRE-BUILT]`                    | On Nexus startup: loads `data/northwind_demand.csv` into a Polars DataFrame, calls `await fs.register_features(schema)` then `await fs.store(schema, df)` — NOT `fs.ingest()` (no such method). Idempotent.                                                                                                                                                        | Called from `app.py` startup; eliminates F10. Writes `.preflight.json.feature_store_populated: true` after completion.                                                                                                                            |
| `src/backend/drift_wiring.py`        | `[PRE-BUILT]`                    | Exposes `wire(model_name: str, reference_df: pl.DataFrame, feature_columns: list[str])` which calls `await DriftMonitor.set_reference_data(model_name, reference_df, feature_columns)` and writes `.preflight.json.drift_wiring: true` as a side effect. `TrainingPipeline` has NO `on_complete` event hook in kailash-ml; wiring is synchronous-call not pub/sub. | Called by `routes/forecast.py` after each `pipeline.train(...)` call completes. Eliminates F8; satisfies `orphan-detection` Rule 1 (production call site) and Rule 2 (Tier 2 wiring test — see `tests/integration/test_drift_monitor_wiring.py`). |
| `src/backend/ml_context.py`          | `[PRE-BUILT]`                    | Constructs `FeatureStore`, `ModelRegistry`, `ExperimentTracker`, `DriftMonitor` against a shared `ConnectionManager`; exposes `get_ml_context()`. Also owns the `model_version_id` derivation: `derive_model_version_id(name, version) -> f"{name}_v{version}"` and `parse_model_version_id(mvid) -> (name, version)`.                                             | Imported by every route; prevents parallel-framework construction (`facade-manager-detection.md`). Wiring test: `tests/integration/test_ml_context_wiring.py` asserts all 4 engines share a single `ConnectionManager.id`.                        |
| `src/backend/routes/__init__.py`     | `[PRE-BUILT + STUDENT-EXTENDED]` | Mounts `health` + `drift_status`; ships 501-stub registrations for `forecast`, `optimize`, `drift` that return `{"error": "not implemented — prompt Claude Code to commission this endpoint", "hint": "see PLAYBOOK.md Phase 4 for /forecast/train"}`. Student replaces each handler body; the route registrations stay put.                                       | Satisfies `orphan-detection` Rule 1 from the moment the scaffold ships — every route is registered; only the body is student-commissioned. Grader confirms the bodies have been replaced (501 → 200 with contract-valid payload).                 |
| `src/backend/routes/health.py`       | `[PRE-BUILT]`                    | `GET /health` — returns typed booleans: `{"ok": bool, "db": bool, "feature_store": bool, "drift_wiring": bool, "registry_runs": int, "nexus_port": int}` (see `product-northwind.md` §8.6).                                                                                                                                                                        | Probed by `scripts/preflight.py`, which asserts `ok: true` AND `feature_store: true` AND `drift_wiring: true`.                                                                                                                                    |
| `src/backend/routes/drift_status.py` | `[PRE-BUILT]`                    | `GET /drift/status/<model_id>` — debug probe returning `{"model_id", "reference_set": bool, "reference_set_at": iso8601                                                                                                                                                                                                                                            | null, "window_size": int}`. Exists so Phase 13 students can verify `drift_wiring.wire`fired without reading`.preflight.json`.                                                                                                                     | Called by Viewer's DriftPanel debug row. |
| `src/backend/routes/forecast.py`     | `[STUDENT-COMMISSIONED]`         | `/forecast/train`, `/forecast/compare`, `/forecast/predict` stubs with banner                                                                                                                                                                                                                                                                                      | Fills the call sites for `TrainingPipeline`, `AutoMLEngine`, `ExperimentTracker`, `InferenceServer`, `ModelExplainer`. Also calls `drift_wiring.wire(...)` synchronously at the end of `/forecast/train` before returning.                        |
| `src/backend/routes/optimize.py`     | `[STUDENT-COMMISSIONED]`         | `/optimize/solve` stub with banner                                                                                                                                                                                                                                                                                                                                 | Fills the call sites for OR-Tools VRP + PuLP                                                                                                                                                                                                      |
| `src/backend/routes/drift.py`        | `[STUDENT-COMMISSIONED]`         | `/drift/check` stub with banner                                                                                                                                                                                                                                                                                                                                    | Fills the call site for `DriftMonitor.check_drift`                                                                                                                                                                                                |

### Banner text for `routes/forecast.py` (verbatim)

```python
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace each handler body (the 501 stubs
# below) with the real implementation described in SCAFFOLD_MANIFEST.md and
# PLAYBOOK.md. The route registrations are PRE-BUILT and stay put.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoints:
#   POST /forecast/train   — AutoMLEngine run, returns experiment_run_id.
#                            Construct: TrainingPipeline(feature_store=fs, registry=registry);
#                                       HyperparameterSearch(pipeline, registry);
#                                       AutoMLEngine(pipeline, search, registry=registry).
#                            Call:      await engine.run(data=df, schema=schema,
#                                                         config=AutoMLConfig(candidate_families=[...]),
#                                                         eval_spec=EvalSpec(split_strategy='walk_forward'),
#                                                         experiment_name='forecast_sprint1',
#                                                         tracker=tracker).
#                            After pipeline.train() completes, call
#                            drift_wiring.wire(model_name, reference_df, feature_columns)
#                            synchronously before returning the response (writes
#                            .preflight.json.drift_wiring: true as a side effect).
#   GET  /forecast/compare — ExperimentTracker list+compare, returns >=3 runs
#   POST /forecast/predict — InferenceServer.predict. Accept model_version_id as
#                            a derived string `{name}_v{version}`; resolve to
#                            (name, version) via ml_context.parse_model_version_id.
#
# Forbidden constructor shapes (red-team findings):
#   - AutoMLEngine(feature_store=, model_registry=, config=)    # does not exist
#   - AutoMLConfig(families=[...])                              # use candidate_families
#   - EvalSpec(cv_strategy='rolling_origin')                    # use split_strategy='walk_forward'
#   - FeatureStore.ingest(path=, schema=)                       # use register_features + store
#
# Required call sites (for orphan-detection):
#   - TrainingPipeline, AutoMLEngine (from ml_context.get_ml_context())
#   - ExperimentTracker (list runs, compare runs)
#   - ModelRegistry.get_model / .promote_model
#   - InferenceServer.predict / .predict_batch
#   - ModelExplainer (surfaced in Phase 7 red-team; fall back to
#                      kailash_ml.engines.model_visualizer.permutation_importance
#                      on ImportError)
#   - drift_wiring.wire (called at end of /forecast/train)
```

### Banner text for `routes/optimize.py` (verbatim)

```python
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace this file with the real
# implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoint:
#   POST /optimize/solve — OR-Tools VRP (primary) or PuLP LP decomposition
#
# Required call sites:
#   - ortools.constraint_solver.pywrapcp (VRP)
#   - pulp (alt LP path)
#   - ExperimentTracker.log_run(tag="phase=optimize", scenario=<preunion|postunion>)
```

### Banner text for `routes/drift.py` (verbatim)

```python
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace the 501-stub handler body with
# the real /drift/check implementation described in PLAYBOOK.md Phase 13.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoint:
#   POST /drift/check — DriftMonitor.check_drift(model_name, current_data)
#                        returns DriftReport with overall_severity in
#                        {"none", "moderate", "severe"} (3 values, not 4 —
#                        the library never emits "low"). Per-feature results
#                        carry psi, ks_statistic, ks_pvalue (KS + PSI only;
#                        no chi2, no JS-divergence in kailash-ml).
#                        set_reference_data is called by routes/forecast.py
#                        via drift_wiring.wire() after each train completes;
#                        /drift/check does NOT re-seed reference data.
#
# Required call sites:
#   - DriftMonitor.check_drift (from ml_context)
#
# Status probe: /drift/status/<model_id> is pre-built in routes/drift_status.py
# so students can verify reference_set state without reading .preflight.json.
```

## 3. Specs (`specs/`)

All spec files are `[PRE-BUILT]`. They are the domain-truth authority for every prompt template. See `_index.md` for the full set.

| Path                        | State         | Role                                                                        |
| --------------------------- | ------------- | --------------------------------------------------------------------------- |
| `specs/_index.md`           | `[PRE-BUILT]` | Manifest of every spec file                                                 |
| `specs/schemas/demand.py`   | `[PRE-BUILT]` | `FeatureSchema` for `user_demand` — 9 features, target `orders_next_day`    |
| `specs/schemas/routes.py`   | `[PRE-BUILT]` | Route-plan types: `Vehicle`, `DeliveryWindow`, `RoutePlan`, `ConstraintSet` |
| `specs/business-costs.md`   | `[PRE-BUILT]` | Dollar values for every cost term — read by every prompt template           |
| `specs/success-criteria.md` | `[PRE-BUILT]` | Endpoint contract assertions; imported by `grade_product.py`                |
| `specs/api-surface.md`      | `[PRE-BUILT]` | Endpoint signatures, request/response schemas, error taxonomy               |
| `specs/rubric.md`           | `[PRE-BUILT]` | 5-dimension scoring, 0/2/4 anchors, worked examples                         |
| `specs/ai-verify.md`        | `[PRE-BUILT]` | Transparency / Robustness / Safety dimensions (Fairness → Week 7)           |

## 4. Data (`data/`)

Every student gets an identical `data/` directory so scenario injections land identically across machines.

| Path                                | State                    | Role                                                                                  |
| ----------------------------------- | ------------------------ | ------------------------------------------------------------------------------------- |
| `data/northwind_demand.csv`         | `[PRE-BUILT]`            | 2 years daily demand, 3 depots, 500 customers, pre-cleaned                            |
| `data/northwind_demand_holdout.csv` | `[PRE-BUILT]`            | Final 30 days held out for Phase 7 red-team                                           |
| `data/leaderboard_prebaked.json`    | `[PRE-BUILT]`            | 30-trial / 5-family Bayesian AutoML leaderboard with real `ExperimentTracker` run IDs |
| `data/drift_baseline.json`          | `[PRE-BUILT]`            | DriftMonitor reference distribution for the training window                           |
| `data/scenarios/union_cap.json`     | `[PRE-BUILT]`            | Sprint 2 injection: overtime cap 5 h/week + re-classification hint                    |
| `data/scenarios/week78_drift.json`  | `[PRE-BUILT]`            | Sprint 3 injection: post-drift 30-day window with shifted customer mix                |
| `data/forecast_output.json`         | `[STUDENT-COMMISSIONED]` | Written by `/forecast/predict`                                                        |
| `data/leaderboard.json`             | `[STUDENT-COMMISSIONED]` | Written by `/forecast/compare` — the student's live AutoML run                        |
| `data/route_plan.json`              | `[STUDENT-COMMISSIONED]` | Written by `/optimize/solve` — initial plan                                           |
| `data/route_plan_preunion.json`     | `[STUDENT-COMMISSIONED]` | Snapshot before the union-cap injection                                               |
| `data/route_plan_postunion.json`    | `[STUDENT-COMMISSIONED]` | Re-solve after injection                                                              |
| `data/drift_report.json`            | `[STUDENT-COMMISSIONED]` | Written by `/drift/check`                                                             |
| `data/README.md`                    | `[PRE-BUILT]`            | Enumerates every JSON the Viewer expects + who writes it                              |

JSON banners: a `[STUDENT-COMMISSIONED]` JSON file ships with `{"_todo_student": "scaffold placeholder — written by endpoint X", "placeholder": true}`. The grader treats `placeholder: true` as a zero-score signal.

**`[PRE-BUILT]` JSON fixtures MUST NOT contain the `_todo_student` marker — not as a null value, not as a placeholder string, not at all.** The banner is a `[STUDENT-COMMISSIONED]` signal only; shipping it (even as `null`) in a pre-built fixture teaches the wrong lesson about banner hygiene and is a `zero-tolerance.md` Rule 2 violation. See `data-fixtures.md` for the cleaned fixture bodies.

## 5. Frontend Viewer (`apps/web/`)

Next.js 14 + React 18 + Tailwind + Recharts. Watches `data/` on disk via a server-side filesystem watcher — no cross-origin HTTP to Nexus. Entire Viewer is `[PRE-BUILT]`; students do not edit the frontend.

| Path                                          | State         | Role                                                                             |
| --------------------------------------------- | ------------- | -------------------------------------------------------------------------------- |
| `apps/web/package.json`                       | `[PRE-BUILT]` | Next 14, React 18, Recharts, Tailwind                                            |
| `apps/web/next.config.js`                     | `[PRE-BUILT]` | Filesystem-watch config pointing at `../../data/`                                |
| `apps/web/app/page.tsx`                       | `[PRE-BUILT]` | Top-level dashboard — 5 panels                                                   |
| `apps/web/app/components/PreflightBanner.tsx` | `[PRE-BUILT]` | Red/green strip reading `.preflight.json`                                        |
| `apps/web/app/components/Leaderboard.tsx`     | `[PRE-BUILT]` | Reads `data/leaderboard.json` AND `data/leaderboard_prebaked.json` side-by-side  |
| `apps/web/app/components/ForecastPanel.tsx`   | `[PRE-BUILT]` | Reads `data/forecast_output.json`; renders line chart + interval band            |
| `apps/web/app/components/RoutePanel.tsx`      | `[PRE-BUILT]` | Reads `data/route_plan.json` with scenario toggle for `_preunion` / `_postunion` |
| `apps/web/app/components/DriftPanel.tsx`      | `[PRE-BUILT]` | Reads `data/drift_report.json`; renders severity + per-feature tests             |
| `apps/web/app/components/JournalPanel.tsx`    | `[PRE-BUILT]` | Reads `journal/*.md`; renders markdown with rubric-dimension tags                |
| `apps/web/app/api/state/route.ts`             | `[PRE-BUILT]` | Server-side filesystem watcher; returns current state snapshot                   |

## 6. Scripts (`scripts/`)

All scripts are `[PRE-BUILT]` and shipped with the scaffold.

| Path                          | State         | Role                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ----------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/preflight.py`        | `[PRE-BUILT]` | Verifies `[xgb]`, `[explain]`, `ortools`, `pulp` installed (hard-fail on missing — no silent fallback for `[explain]`; the Phase 7 fallback is a recovery path, not a workaround). Detects if `:8000` / `:3000` already bound by another process and prints `"port 8000 taken — export KAILASH_NEXUS_PORT=8001 and retry"`. Probes `:8000/health` asserting `ok: true`, `db: true`, `feature_store: true`, `drift_wiring: true`; fails red with `kill <pid>` instruction (via psutil) if any false. Writes `.preflight.json`. |
| `scripts/run_backend.sh`      | `[PRE-BUILT]` | Canonical backend entrypoint: `uvicorn src.backend.app:app --host 127.0.0.1 --port ${KAILASH_NEXUS_PORT:-8000} --reload`. Documented so students have one place to debug startup failures.                                                                                                                                                                                                                                                                                                                                    |
| `scripts/grade_product.py`    | `[PRE-BUILT]` | Runs the 5 endpoint contracts from `specs/success-criteria.md` against live backend. Uses `httpx.Client(timeout=120)` so the 90-s `/forecast/train` contract has headroom. Does NOT retry on 5xx — this is a live grade at 03:20.                                                                                                                                                                                                                                                                                             |
| `scripts/seed_experiments.py` | `[PRE-BUILT]` | Populates `data/leaderboard_prebaked.json` into the `ExperimentTracker` DB (run during scaffolding). Uses `search_strategy='bayesian'` explicitly; AutoMLConfig's own default is `'random'`.                                                                                                                                                                                                                                                                                                                                  |
| `scripts/seed_drift.py`       | `[PRE-BUILT]` | Populates `data/drift_baseline.json` + `data/scenarios/week78_drift.json`                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `scripts/seed_route_plan.py`  | `[PRE-BUILT]` | Writes a baseline `data/route_plan.json` from the pre-baked leaderboard + a minimal solver seed. Used by `scenario_inject.py --undo` when both `route_plan.json` and `route_plan_preunion.json` are missing.                                                                                                                                                                                                                                                                                                                  |
| `scripts/journal_export.py`   | `[PRE-BUILT]` | Compiles `journal/*.md` → `journal.pdf`; invoked by `metis journal export`. On `pandoc` / LaTeX missing, emits `journal_markdown_fallback.md` with a `PDF export failed because <reason>; lost features: cited-sources appendix, rubric-dimension badges` banner at the top (not silent — instructor assesses impact).                                                                                                                                                                                                        |
| `scripts/scenario_inject.py`  | `[PRE-BUILT]` | Instructor CLI; see `scenario-injection.md` for the full contract                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `scripts/instructor_brief.md` | `[PRE-BUILT]` | Minute-by-minute runbook; 00:15 + 00:45 + 03:20 announcements                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

## 7. CI (`.github/workflows/`)

| Path                              | State         | Role                                                                   |
| --------------------------------- | ------------- | ---------------------------------------------------------------------- |
| `.github/workflows/preflight.yml` | `[PRE-BUILT]` | Nightly preflight on a canonical machine — catches SDK-version drift   |
| `.github/workflows/grade.yml`     | `[PRE-BUILT]` | Runs `grade_product.py` against a reference "gold standard" submission |

## 8. Instructor-only

Not installed on student machines.

| Path                          | State         | Role                                               |
| ----------------------------- | ------------- | -------------------------------------------------- |
| `scripts/scenario_inject.py`  | `[PRE-BUILT]` | (listed above) CLI to broadcast scenarios          |
| `scripts/instructor_brief.md` | `[PRE-BUILT]` | (listed above) Runbook for the three announcements |

## 9. Orphan-detection audit

Per `orphan-detection.md` Rule 1 (production call site) and `facade-manager-detection.md` Rule 2 (named Tier 2 wiring test), every public component MUST have BOTH a production call site AND a named wiring test. Audit:

| Component           | Production call site                                                                            | Tier 2 wiring test                                                                                          |
| ------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `FeatureStore`      | `src/backend/fs_preload.py`, `src/backend/ml_context.py`                                        | `tests/integration/test_feature_store_wiring.py`                                                            |
| `ModelRegistry`     | `src/backend/ml_context.py`, `src/backend/routes/forecast.py` (501-stub → student-filled)       | `tests/integration/test_model_registry_wiring.py`                                                           |
| `ExperimentTracker` | `src/backend/ml_context.py`, `src/backend/routes/forecast.py` (501-stub → student-filled)       | `tests/integration/test_experiment_tracker_wiring.py`                                                       |
| `TrainingPipeline`  | `src/backend/routes/forecast.py` `/train`                                                       | `tests/integration/test_training_pipeline_wiring.py`                                                        |
| `AutoMLEngine`      | `src/backend/routes/forecast.py` `/train`                                                       | `tests/integration/test_automl_engine_wiring.py`                                                            |
| `InferenceServer`   | `src/backend/routes/forecast.py` `/predict`                                                     | `tests/integration/test_inference_server_wiring.py`                                                         |
| `DriftMonitor`      | `src/backend/drift_wiring.py` (via `wire()`), `src/backend/routes/drift.py`                     | `tests/integration/test_drift_monitor_wiring.py`                                                            |
| `ModelExplainer`    | `src/backend/routes/forecast.py` Phase 7 red-team call (with `permutation_importance` fallback) | `tests/integration/test_model_explainer_wiring.py`                                                          |
| OR-Tools VRP        | `src/backend/routes/optimize.py`                                                                | `tests/integration/test_ortools_vrp_wiring.py`                                                              |
| PuLP                | `src/backend/routes/optimize.py` (alt LP path)                                                  | `tests/integration/test_pulp_wiring.py`                                                                     |
| `DataExplorer`      | `src/backend/routes/forecast.py` Phase 2 call                                                   | `tests/integration/test_data_explorer_wiring.py`                                                            |
| `get_ml_context()`  | `src/backend/routes/__init__.py` + every route                                                  | `tests/integration/test_ml_context_wiring.py` (asserts all 4 engines share a single `ConnectionManager.id`) |

Each wiring test imports through the framework facade (`db.X` / `get_ml_context().X`), constructs against real SQLite, calls at least one method on the component, and asserts the externally-observable effect (row persisted, redaction applied, metric counted). Tier 1 mock-based tests do NOT satisfy this contract.

Since the scaffold ships with 501-stub registrations (not missing routes), every component has a production call site from commit 1 — orphan-detection Rule 1 is satisfied the moment the scaffold lands. The student replaces the 501-stub handler body; the route registration and wiring test survive.

## 10. `.env.example` enumeration

All keys referenced by any backend, CLI, or Viewer component MUST appear in `.env.example`. Current set:

```
# Backend
KAILASH_NEXUS_PORT=8000
KAILASH_ML_AUTOML_QUICK=1
DATABASE_URL_EXPERIMENTS=sqlite:///data/.experiments.db
DATABASE_URL_REGISTRY=sqlite:///data/.registry.db
DATABASE_URL_FEATURES=sqlite:///data/.features.db
ARTIFACT_DIR=data/

# Seeds (determinism)
RANDOM_SEED=42
AUTOML_SEED=2026
DRIFT_SEED=78

# Viewer
NEXT_PUBLIC_POLL_MS=1000
NEXT_PUBLIC_BACKEND_PORT=8000
METIS_WORKSPACE_ROOT=../../

# LLM (only when kailash-ml[agents] is active — Week 4 does NOT exercise agents)
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=
```

Per `env-models.md`, model names MUST come from `.env` — no hard-coded `"gpt-4"` / `"claude-3-opus"` string in any prompt template.

## Open questions

None — red-team cycle closed API-fabrication, orphan-detection, and env-enumeration gaps. Open questions that survived are tracked in `scenario-injection.md` (shared-classroom topology) and `data-fixtures.md` (holiday-calendar parametrization).
