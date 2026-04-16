<!--
GENERATED — do not edit directly.
Source spec: specs/scaffold-contract.md §1–8.
Regenerate with: scripts/build_manifest.py
-->

<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Scaffold Manifest — Week 4 Supply Chain

**Version:** 2026-04-16 · **Generated:** 2026-04-16 from `specs/scaffold-contract.md` · **License:** CC BY 4.0

## What this file is for

This manifest enumerates every file the Week 4 scaffold ships, and labels each with its state. The opening prompt (see `START_HERE.md` §9) reads this file so Claude Code verifies the scaffold against a fixed list rather than fabricating one. If a file appears in this manifest with state `[STUDENT-COMMISSIONED]`, your prompts must replace it. If a file is `[PRE-BUILT]`, do not edit it. If a file is `[PRE-BUILT + STUDENT-EXTENDED]`, you add content at the named extension point only.

## State legend

- `[PRE-BUILT]` — ships complete; do not edit.
- `[STUDENT-COMMISSIONED]` — ships with a `# TODO-STUDENT` banner; your prompt to Claude Code replaces it.
- `[PRE-BUILT + STUDENT-EXTENDED]` — ships a skeleton with a named extension point; you add content at that slot only.

A `[STUDENT-COMMISSIONED]` or `[STUDENT-EXTENDED]` file without the banner is a scaffolding error. The grader treats `"placeholder": true` in JSON files as a zero-score signal.

## File table

| §   | Path                                          | State                            | Role                                                                                        |
| --- | --------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| 1   | `START_HERE.md`                               | `[PRE-BUILT]`                    | Student manual — read before class                                                          |
| 1   | `SCAFFOLD_MANIFEST.md`                        | `[PRE-BUILT]`                    | This file — workspace-root copy of the scaffold contract                                    |
| 1   | `PLAYBOOK.md`                                 | `[PRE-BUILT]`                    | 14-phase procedure, prompts, checklists, journal schemas                                    |
| 1   | `PRODUCT_BRIEF.md`                            | `[PRE-BUILT]`                    | Business context; cost table; personas; 3:30 pm success definition                          |
| 1   | `.env.example`                                | `[PRE-BUILT]`                    | Template env with `KAILASH_ML_AUTOML_QUICK=1`, DB paths, ports                              |
| 1   | `journal/`                                    | `[STUDENT-COMMISSIONED]`         | Directory of `phase_N.md` entries                                                           |
| 1   | `journal/_template.md`                        | `[PRE-BUILT]`                    | Skeleton entry with 5 rubric-dimension headings                                             |
| 1   | `journal/_examples.md`                        | `[PRE-BUILT]`                    | 3 entries at 4/4 and 3 at 1/4, side-by-side per phase                                       |
| 1   | `journal.pdf`                                 | `[STUDENT-COMMISSIONED]`         | Compiled output of `journal/` at close                                                      |
| 1   | `.session-notes`                              | `[STUDENT-COMMISSIONED]`         | `/wrapup` artifact; optional                                                                |
| 2   | `src/backend/__init__.py`                     | `[PRE-BUILT]`                    | Module marker                                                                               |
| 2   | `src/backend/app.py`                          | `[PRE-BUILT]`                    | Nexus app factory, CORS, logging, health endpoint                                           |
| 2   | `src/backend/config.py`                       | `[PRE-BUILT]`                    | Reads `.env`; exposes `DB_URL`, `ARTIFACT_DIR`, `EXPERIMENT_DB`, `REGISTRY_DB`              |
| 2   | `src/backend/fs_preload.py`                   | `[PRE-BUILT]`                    | Loads `data/northwind_demand.csv`; `register_features` + `store`; idempotent                |
| 2   | `src/backend/drift_wiring.py`                 | `[PRE-BUILT]`                    | `wire(model_name, reference_df, feature_columns)`; calls `set_reference_data` synchronously |
| 2   | `src/backend/ml_context.py`                   | `[PRE-BUILT]`                    | Shared `FeatureStore`/`ModelRegistry`/`ExperimentTracker`/`DriftMonitor`                    |
| 2   | `src/backend/routes/__init__.py`              | `[PRE-BUILT + STUDENT-EXTENDED]` | Mounts `health` + `drift_status`; 501-stubs for `forecast`/`optimize`/`drift`               |
| 2   | `src/backend/routes/health.py`                | `[PRE-BUILT]`                    | `GET /health` — typed boolean status payload                                                |
| 2   | `src/backend/routes/drift_status.py`          | `[PRE-BUILT]`                    | `GET /drift/status/<model_id>` — debug probe                                                |
| 2   | `src/backend/routes/forecast.py`              | `[STUDENT-COMMISSIONED]`         | `/forecast/train` + `/compare` + `/predict` stubs with banner                               |
| 2   | `src/backend/routes/optimize.py`              | `[STUDENT-COMMISSIONED]`         | `/optimize/solve` stub with banner                                                          |
| 2   | `src/backend/routes/drift.py`                 | `[STUDENT-COMMISSIONED]`         | `/drift/check` stub with banner                                                             |
| 3   | `specs/_index.md`                             | `[PRE-BUILT]`                    | Manifest of every spec file                                                                 |
| 3   | `specs/schemas/demand.py`                     | `[PRE-BUILT]`                    | `FeatureSchema` for `user_demand` — 9 features, target `orders_next_day`                    |
| 3   | `specs/schemas/routes.py`                     | `[PRE-BUILT]`                    | Route-plan types: `Vehicle`, `DeliveryWindow`, `RoutePlan`, `ConstraintSet`                 |
| 3   | `specs/business-costs.md`                     | `[PRE-BUILT]`                    | Dollar values for every cost term — read by every prompt template                           |
| 3   | `specs/success-criteria.md`                   | `[PRE-BUILT]`                    | Endpoint contract assertions imported by `grade_product.py`                                 |
| 3   | `specs/api-surface.md`                        | `[PRE-BUILT]`                    | Endpoint signatures, request/response schemas, error taxonomy                               |
| 3   | `specs/rubric.md`                             | `[PRE-BUILT]`                    | 5-dimension scoring, 0/2/4 anchors, worked examples                                         |
| 3   | `specs/ai-verify.md`                          | `[PRE-BUILT]`                    | Transparency / Robustness / Safety dimensions (Fairness → Week 7)                           |
| 4   | `data/northwind_demand.csv`                   | `[PRE-BUILT]`                    | 2 years daily demand, 3 depots, 500 customers, pre-cleaned                                  |
| 4   | `data/northwind_demand_holdout.csv`           | `[PRE-BUILT]`                    | Final 30 days held out for Phase 7 red-team                                                 |
| 4   | `data/leaderboard_prebaked.json`              | `[PRE-BUILT]`                    | 30-trial / 5-family Bayesian AutoML leaderboard with real run IDs                           |
| 4   | `data/drift_baseline.json`                    | `[PRE-BUILT]`                    | DriftMonitor reference distribution for the training window                                 |
| 4   | `data/scenarios/union_cap.json`               | `[PRE-BUILT]`                    | Sprint 2 injection: overtime cap 5 h/week + re-classification hint                          |
| 4   | `data/scenarios/week78_drift.json`            | `[PRE-BUILT]`                    | Sprint 3 injection: 30-day post-drift window with shifted customer mix                      |
| 4   | `data/forecast_output.json`                   | `[STUDENT-COMMISSIONED]`         | Written by `/forecast/predict`                                                              |
| 4   | `data/leaderboard.json`                       | `[STUDENT-COMMISSIONED]`         | Written by `/forecast/compare` — the live AutoML run                                        |
| 4   | `data/route_plan.json`                        | `[STUDENT-COMMISSIONED]`         | Written by `/optimize/solve` — initial plan                                                 |
| 4   | `data/route_plan_preunion.json`               | `[STUDENT-COMMISSIONED]`         | Snapshot before the union-cap injection                                                     |
| 4   | `data/route_plan_postunion.json`              | `[STUDENT-COMMISSIONED]`         | Re-solve after injection                                                                    |
| 4   | `data/drift_report.json`                      | `[STUDENT-COMMISSIONED]`         | Written by `/drift/check`                                                                   |
| 4   | `data/README.md`                              | `[PRE-BUILT]`                    | Enumerates every JSON the Viewer expects + who writes it                                    |
| 5   | `apps/web/package.json`                       | `[PRE-BUILT]`                    | Next 14, React 18, Recharts, Tailwind                                                       |
| 5   | `apps/web/next.config.js`                     | `[PRE-BUILT]`                    | Filesystem-watch config pointing at `../../data/`                                           |
| 5   | `apps/web/app/page.tsx`                       | `[PRE-BUILT]`                    | Top-level dashboard — 5 panels                                                              |
| 5   | `apps/web/app/components/PreflightBanner.tsx` | `[PRE-BUILT]`                    | Red/green strip reading `.preflight.json`                                                   |
| 5   | `apps/web/app/components/Leaderboard.tsx`     | `[PRE-BUILT]`                    | Reads `leaderboard.json` AND `leaderboard_prebaked.json` side-by-side                       |
| 5   | `apps/web/app/components/ForecastPanel.tsx`   | `[PRE-BUILT]`                    | Reads `data/forecast_output.json`; renders line chart + interval band                       |
| 5   | `apps/web/app/components/RoutePanel.tsx`      | `[PRE-BUILT]`                    | Reads `data/route_plan.json` with `_preunion` / `_postunion` scenario toggle                |
| 5   | `apps/web/app/components/DriftPanel.tsx`      | `[PRE-BUILT]`                    | Reads `data/drift_report.json`; renders severity + per-feature tests                        |
| 5   | `apps/web/app/components/JournalPanel.tsx`    | `[PRE-BUILT]`                    | Reads `journal/*.md`; renders markdown with rubric-dimension tags                           |
| 5   | `apps/web/app/api/state/route.ts`             | `[PRE-BUILT]`                    | Server-side filesystem watcher; returns current state snapshot                              |
| 6   | `scripts/preflight.py`                        | `[PRE-BUILT]`                    | Verifies extras, ports, `/health`; writes `.preflight.json`                                 |
| 6   | `scripts/run_backend.sh`                      | `[PRE-BUILT]`                    | Canonical uvicorn entrypoint for `src/backend/app.py`                                       |
| 6   | `scripts/grade_product.py`                    | `[PRE-BUILT]`                    | Runs 5 endpoint contracts at 03:20 public grading                                           |
| 6   | `scripts/seed_experiments.py`                 | `[PRE-BUILT]`                    | Populates `leaderboard_prebaked.json` into `ExperimentTracker`                              |
| 6   | `scripts/seed_drift.py`                       | `[PRE-BUILT]`                    | Populates `drift_baseline.json` + `week78_drift.json`                                       |
| 6   | `scripts/seed_route_plan.py`                  | `[PRE-BUILT]`                    | Writes baseline `route_plan.json`; used by `scenario_inject.py --undo`                      |
| 6   | `scripts/journal_export.py`                   | `[PRE-BUILT]`                    | Compiles `journal/*.md` → `journal.pdf` with fallback banner on failure                     |
| 6   | `scripts/scenario_inject.py`                  | `[PRE-BUILT]`                    | Instructor CLI; see `specs/scenario-injection.md` for the full contract                     |
| 6   | `scripts/instructor_brief.md`                 | `[PRE-BUILT]`                    | Minute-by-minute runbook; 00:15 + 00:45 + 03:20 announcements                               |
| 7   | `.github/workflows/preflight.yml`             | `[PRE-BUILT]`                    | Nightly preflight on a canonical machine — catches SDK-version drift                        |
| 7   | `.github/workflows/grade.yml`                 | `[PRE-BUILT]`                    | Runs `grade_product.py` against a reference "gold standard" submission                      |
| 8   | `scripts/scenario_inject.py`                  | `[PRE-BUILT]`                    | (instructor-only view) CLI to broadcast scenarios                                           |
| 8   | `scripts/instructor_brief.md`                 | `[PRE-BUILT]`                    | (instructor-only view) Runbook for the three announcements                                  |

## Workshop run-of-show cross-reference

For the minute-by-minute script, see `specs/workshop-runofshow.md`. Minute-zero deliverables and their producing shards:

| Checkpoint | Expectation                                   | Producer                                     |
| ---------- | --------------------------------------------- | -------------------------------------------- |
| 00:00      | `.preflight.json` all-green                   | Shard 01 (scaffold) + 06 (scripts) + 09 (ci) |
| 00:27      | AutoML run completes ≤ 90 s                   | Shard 02 (ExperimentTracker wiring)          |
| 02:05      | Union-cap fires; `/optimize/solve` tag-aware  | Shards 03a (optimize) + 06 (scenario inject) |
| 03:20      | `grade_product.py` runs publicly on projector | Shard 06 (scripts)                           |
| pre-class  | `instructor_brief.md` available               | Shard 09 (instructor ops)                    |

## Orphan-detection audit

Per `orphan-detection.md` Rule 1 + `facade-manager-detection.md` Rule 2, every public component MUST have BOTH a production call site AND a named Tier 2 wiring test. The full table is in `specs/scaffold-contract.md` §9; it covers `FeatureStore`, `ModelRegistry`, `ExperimentTracker`, `TrainingPipeline`, `AutoMLEngine`, `InferenceServer`, `DriftMonitor`, `ModelExplainer`, OR-Tools VRP, PuLP, `DataExplorer`, and `get_ml_context()`.

Since the scaffold ships with 501-stub registrations (not missing routes), every component has a production call site from commit 1 — orphan-detection Rule 1 is satisfied the moment the scaffold lands. The student replaces the 501-stub handler body; the route registration and wiring test survive.
