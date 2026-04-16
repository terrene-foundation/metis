# Scaffold Manifest — Week 4 Supply Chain Workshop

**Purpose**: canonical ground-truth list of every file students will see tomorrow. Resolves structural Issue 4. The opening prompt reads this file directly and asks Claude Code to verify each entry. This file is shipped to the workspace root tomorrow morning (likely as `workspaces/metis/week-04-supply-chain/SCAFFOLD_MANIFEST.md`) — the path in `01-analysis/` is the authored copy.

**Legend**:

- `[PRE-BUILT]` — scaffold ships a complete, working file. Students do not edit it.
- `[STUDENT-COMMISSIONED]` — scaffold ships a placeholder with a `# TODO-STUDENT:` banner. Students commission the real file by prompting Claude Code. Grader runs against the student's version.
- `[PRE-BUILT + STUDENT-EXTENDED]` — scaffold ships a skeleton with a named extension point; student adds content at the named slot.

Every `[STUDENT-COMMISSIONED]` and `[STUDENT-EXTENDED]` file begins with the banner:

```
# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace this file with the real
# implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.
# Do NOT edit manually — prompt Claude Code.
```

Python files use `#` comments; TypeScript/JSX use `//`; JSON uses a wrapping `{"_todo_student": "...", ...}` key.

---

## 1. Workspace root (`workspaces/metis/week-04-supply-chain/`)

| Path                   | State                    | What it contains                                                             | Why                                                                    |
| ---------------------- | ------------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `START_HERE.md`        | `[PRE-BUILT]`            | Student manual (this doc's parent produces the fixed version)                | Anchor doc — student reads before class                                |
| `SCAFFOLD_MANIFEST.md` | `[PRE-BUILT]`            | This file, copied to workspace root                                          | Opening prompt reads it for verification                               |
| `PLAYBOOK.md`          | `[PRE-BUILT]`            | 12-phase procedure, rubric examples, journal schemas, evaluation checklists  | Universal spine across Weeks 4-8                                       |
| `PRODUCT_BRIEF.md`     | `[PRE-BUILT]`            | Northwind business context, cost table, personas, 3:30 pm success definition | Grounds every phase's prompts in business numbers                      |
| `.env.example`         | `[PRE-BUILT]`            | Template env with `KAILASH_ML_AUTOML_QUICK=1`, DB paths, ports               | Preflight reads it; students copy to `.env`                            |
| `journal/` (directory) | `[STUDENT-COMMISSIONED]` | Student-written `phase_N.md` files; exported as `journal.pdf` at close       | Student creates entries via `metis journal add` or Claude Code prompts |
| `journal/_template.md` | `[PRE-BUILT]`            | Skeleton entry with rubric-dimension headings                                | Anchors students to the 5-dimension rubric                             |
| `journal/_examples.md` | `[PRE-BUILT]`            | 3 entries at 4/4 and 3 entries at 1/4, side-by-side per phase                | Makes the rubric gap visceral                                          |
| `journal.pdf`          | `[STUDENT-COMMISSIONED]` | Compiled output of journal/ at close                                         | `metis journal export` produces it                                     |
| `.session-notes`       | `[STUDENT-COMMISSIONED]` | `/wrapup` artifact, not a deliverable                                        | Optional, for instructor review                                        |

---

## 2. Backend source (`src/backend/`)

All backend code is kailash-nexus + kailash-ml. Students never touch this layer directly except by prompting Claude Code.

| Path                             | State                            | What it contains                                                                                                                                   | Why                                                                                   |
| -------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `src/backend/__init__.py`        | `[PRE-BUILT]`                    | Empty                                                                                                                                              | Module marker                                                                         |
| `src/backend/app.py`             | `[PRE-BUILT]`                    | Nexus app factory, CORS, logging, health endpoint                                                                                                  | Students must not touch framework plumbing                                            |
| `src/backend/config.py`          | `[PRE-BUILT]`                    | Reads `.env`, exposes `DB_URL`, `ARTIFACT_DIR`, `EXPERIMENT_DB`, `REGISTRY_DB`                                                                     | Single source of truth for configuration                                              |
| `src/backend/fs_preload.py`      | `[PRE-BUILT]`                    | Ingests `data/northwind_demand.csv` into FeatureStore on startup                                                                                   | Eliminates F10 (ingest-skipped)                                                       |
| `src/backend/drift_wiring.py`    | `[PRE-BUILT]`                    | Auto-calls `DriftMonitor.set_reference_data` on training completion event                                                                          | Eliminates F8 (reference-data-forgotten); satisfies orphan-detection (real call site) |
| `src/backend/routes/health.py`   | `[PRE-BUILT]`                    | `/health` endpoint — checks DB reachable, FeatureStore populated, drift wiring active                                                              | Preflight probes this                                                                 |
| `src/backend/routes/forecast.py` | `[STUDENT-COMMISSIONED]`         | `/forecast/train`, `/forecast/compare`, `/forecast/predict` stubs with banner                                                                      | Sprint 1 deliverable — student prompts Claude Code to implement                       |
| `src/backend/routes/optimize.py` | `[STUDENT-COMMISSIONED]`         | `/optimize/solve` stub with banner                                                                                                                 | Sprint 2 deliverable                                                                  |
| `src/backend/routes/drift.py`    | `[STUDENT-COMMISSIONED]`         | `/drift/check` stub with banner                                                                                                                    | Sprint 3 deliverable                                                                  |
| `src/backend/routes/__init__.py` | `[PRE-BUILT + STUDENT-EXTENDED]` | Mounts health; extension point for forecast / optimize / drift                                                                                     | Router registration slot; grader confirms mounts                                      |
| `src/backend/ml_context.py`      | `[PRE-BUILT]`                    | Single module that instantiates FeatureStore, ModelRegistry, ExperimentTracker, DriftMonitor against ConnectionManager; exposes `get_ml_context()` | Prevents parallel-framework construction (`facade-manager-detection.md`)              |

Orphan-detection check: every kailash-ml engine named in `START_HERE.md §3.5` has a real call site in the scaffold — FeatureStore in `fs_preload.py` and `ml_context.py`; ModelRegistry + ExperimentTracker in `ml_context.py` and `routes/forecast.py`; DriftMonitor in `drift_wiring.py` and `routes/drift.py`; InferenceServer via `routes/forecast.py` `/predict`; TrainingPipeline and AutoMLEngine via `routes/forecast.py` `/train`.

---

## 3. ML specs (`specs/`)

Specs are the domain-truth authority per `specs-authority.md`. All pre-built.

| Path                        | State         | What it contains                                                                       | Why                                               |
| --------------------------- | ------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `specs/_index.md`           | `[PRE-BUILT]` | Manifest listing every spec file with one-line description                             | Phases read this first                            |
| `specs/schemas/demand.py`   | `[PRE-BUILT]` | `FeatureSchema` for `user_demand` — 9 features, target `orders_next_day`               | TrainingPipeline / AutoMLEngine consume it        |
| `specs/schemas/routes.py`   | `[PRE-BUILT]` | Route-plan types: Vehicle, DeliveryWindow, RoutePlan, ConstraintSet                    | OR-Tools / PuLP consume it                        |
| `specs/business-costs.md`   | `[PRE-BUILT]` | $40 stockout / $12 overstock / $220 SLA / $45 overtime / $0.35 per km / $8 per kg CO₂  | Every prompt grounds against this                 |
| `specs/success-criteria.md` | `[PRE-BUILT]` | What "shipped" means per endpoint, mapped to rubric contracts                          | Grader script imports thresholds from here        |
| `specs/api-surface.md`      | `[PRE-BUILT]` | Endpoint signatures, request/response schemas, error taxonomy                          | Student + Claude Code prompt against it           |
| `specs/rubric.md`           | `[PRE-BUILT]` | 5-dimension scoring, 0/2/4 anchors, worked examples                                    | Journal rubric ground truth                       |
| `specs/ai-verify.md`        | `[PRE-BUILT]` | Transparency / Robustness / Safety dimensions for Phase 7 (Fairness -> Week 7 pointer) | AI Verify framework grounding (Issue 3, Option A) |

---

## 4. Data (`data/`)

Every student gets an identical `data/` directory so scenario injections land identically.

| Path                                | State                    | What it contains                                                                | Why                                 |
| ----------------------------------- | ------------------------ | ------------------------------------------------------------------------------- | ----------------------------------- |
| `data/northwind_demand.csv`         | `[PRE-BUILT]`            | 2 years of daily demand, 3 depots, 500 customers. Pre-cleaned                   | Training data                       |
| `data/northwind_demand_holdout.csv` | `[PRE-BUILT]`            | Final 30 days held out for Phase 7 red-team                                     | Unseen eval set                     |
| `data/leaderboard_prebaked.json`    | `[PRE-BUILT]`            | 30-trial / 5-family Bayesian AutoML leaderboard, real ExperimentTracker run IDs | Issue 1 pre-bake; students critique |
| `data/drift_baseline.json`          | `[PRE-BUILT]`            | DriftMonitor reference distribution for the training window                     | Phase 13 enablement                 |
| `data/scenarios/union_cap.json`     | `[PRE-BUILT]`            | Sprint 2 injection: overtime cap 5h/week + re-classification hint               | Scenario injection                  |
| `data/scenarios/week78_drift.json`  | `[PRE-BUILT]`            | Sprint 3 injection: post-drift 30-day window with shifted customer mix          | Scenario injection                  |
| `data/forecast_output.json`         | `[STUDENT-COMMISSIONED]` | Written by `/forecast/predict`                                                  | Optimizer consumes it               |
| `data/leaderboard.json`             | `[STUDENT-COMMISSIONED]` | Written by `/forecast/compare` — the student's live AutoML run                  | Viewer reads it                     |
| `data/route_plan.json`              | `[STUDENT-COMMISSIONED]` | Written by `/optimize/solve` — initial plan                                     | Sprint 2 deliverable                |
| `data/route_plan_preunion.json`     | `[STUDENT-COMMISSIONED]` | Snapshot before the union-cap injection                                         | F6 state-hygiene                    |
| `data/route_plan_postunion.json`    | `[STUDENT-COMMISSIONED]` | Re-solve after injection                                                        | F6 state-hygiene                    |
| `data/drift_report.json`            | `[STUDENT-COMMISSIONED]` | Written by `/drift/check`                                                       | Sprint 3 deliverable                |
| `data/README.md`                    | `[PRE-BUILT]`            | Enumerates every JSON the Viewer expects + who writes it                        | Debug aid                           |

---

## 5. Frontend Viewer (`apps/web/`)

Next.js read-only dashboard. Watches `data/` on disk; no HTTP cross-origin calls to Nexus.

| Path                                          | State         | What it contains                                                                                     | Why                                |
| --------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `apps/web/package.json`                       | `[PRE-BUILT]` | Next 14, React 18, Recharts, Tailwind                                                                | Standard Next.js app               |
| `apps/web/next.config.js`                     | `[PRE-BUILT]` | Filesystem-watch config pointing at `../../data/`                                                    | Eliminates CORS (F5)               |
| `apps/web/app/page.tsx`                       | `[PRE-BUILT]` | Top-level dashboard — 4 panels (Leaderboard, Forecast, Route, Drift)                                 | Students do not edit               |
| `apps/web/app/components/PreflightBanner.tsx` | `[PRE-BUILT]` | Red/green strip reading `.preflight.json`                                                            | F4 visibility                      |
| `apps/web/app/components/Leaderboard.tsx`     | `[PRE-BUILT]` | Reads `data/leaderboard.json` (student) AND `data/leaderboard_prebaked.json` (prebaked) side-by-side | Sprint 1 critique-the-prebake view |
| `apps/web/app/components/ForecastPanel.tsx`   | `[PRE-BUILT]` | Reads `data/forecast_output.json`, renders line chart                                                | Sprint 1                           |
| `apps/web/app/components/RoutePanel.tsx`      | `[PRE-BUILT]` | Reads `data/route_plan.json`; includes scenario toggle for `_preunion`/`_postunion`                  | Sprint 2 + F6                      |
| `apps/web/app/components/DriftPanel.tsx`      | `[PRE-BUILT]` | Reads `data/drift_report.json`; renders severity + per-feature test results                          | Sprint 3                           |
| `apps/web/app/components/JournalPanel.tsx`    | `[PRE-BUILT]` | Reads `journal/*.md`; renders rendered markdown with rubric dimension tags                           | Student sees their journal live    |
| `apps/web/app/api/state/route.ts`             | `[PRE-BUILT]` | Server-side filesystem watcher; returns current state snapshot                                       | Viewer backend                     |

Viewer has zero `[STUDENT-COMMISSIONED]` files. Students do not build the frontend — it is part of the scaffold. The Viewer is read-only by course contract.

---

## 6. Scripts (`scripts/`)

| Path                          | State         | What it contains                                                                             | Why                                    |
| ----------------------------- | ------------- | -------------------------------------------------------------------------------------------- | -------------------------------------- |
| `scripts/preflight.py`        | `[PRE-BUILT]` | Verifies `[xgb]`, `[explain]`, `ortools`, `pulp` installed; curls `:3000` and `:8000/health` | F4 mitigation                          |
| `scripts/grade_product.py`    | `[PRE-BUILT]` | Runs the 5 endpoint contracts from `specs/success-criteria.md` against live backend          | F2 mitigation; public run at 3:20 pm   |
| `scripts/seed_experiments.py` | `[PRE-BUILT]` | Populates `data/leaderboard_prebaked.json` into the ExperimentTracker DB                     | Run once during scaffolding            |
| `scripts/seed_drift.py`       | `[PRE-BUILT]` | Populates `data/drift_baseline.json` and `data/scenarios/week78_drift.json`                  | Run once during scaffolding            |
| `scripts/journal_export.py`   | `[PRE-BUILT]` | Compiles `journal/*.md` to `journal.pdf`                                                     | Invoked by `metis journal export`      |
| `scripts/scenario_inject.py`  | `[PRE-BUILT]` | Instructor CLI: `python scripts/scenario_inject.py union_cap` copies the payload into scope  | Scenario injection CLI (Issue context) |

---

## 7. CI (`.github/workflows/`)

| Path                              | State         | What it contains                                                       | Why                                           |
| --------------------------------- | ------------- | ---------------------------------------------------------------------- | --------------------------------------------- |
| `.github/workflows/preflight.yml` | `[PRE-BUILT]` | Nightly preflight run on a canonical machine                           | Catches SDK-version drift before workshop day |
| `.github/workflows/grade.yml`     | `[PRE-BUILT]` | Runs `grade_product.py` against a reference "gold standard" submission | Sanity check                                  |

---

## 8. Scenario CLI

Instructor-only tool, not on student machines.

| Path                          | State         | What it contains                                                        | Why                                    |
| ----------------------------- | ------------- | ----------------------------------------------------------------------- | -------------------------------------- |
| `scripts/scenario_inject.py`  | `[PRE-BUILT]` | (listed above) CLI to broadcast a scenario to the class                 | Instructor trigger for Sprints 2 and 3 |
| `scripts/instructor_brief.md` | `[PRE-BUILT]` | Minute-by-minute instructor runbook (00:15, 00:45, 03:20 announcements) | Instructor reads before class          |

---

## Orphan-detection audit

Per `orphan-detection.md`, every component that appears on the public surface (anything students can read or call) must have a production call site in the scaffold. Audit:

| Component         | Call site in scaffold                                                               |
| ----------------- | ----------------------------------------------------------------------------------- |
| FeatureStore      | `src/backend/fs_preload.py`, `src/backend/ml_context.py`                            |
| ModelRegistry     | `src/backend/ml_context.py`, `src/backend/routes/forecast.py` (after student fills) |
| ExperimentTracker | `src/backend/ml_context.py`, `src/backend/routes/forecast.py` (after student fills) |
| TrainingPipeline  | `src/backend/routes/forecast.py` `/train` (student fills in Sprint 1)               |
| AutoMLEngine      | `src/backend/routes/forecast.py` `/train` (Sprint 1, Phase 4)                       |
| InferenceServer   | `src/backend/routes/forecast.py` `/predict` (Sprint 1, Phase 8)                     |
| DriftMonitor      | `src/backend/drift_wiring.py`, `src/backend/routes/drift.py` (Sprint 3)             |
| ModelExplainer    | `src/backend/routes/forecast.py` Phase 7 call (Sprint 1 red-team)                   |
| OR-Tools VRP      | `src/backend/routes/optimize.py` (Sprint 2, student fills)                          |
| PuLP              | `src/backend/routes/optimize.py` alt path for LP decomposition                      |
| DataExplorer      | `src/backend/routes/forecast.py` Phase 2 call                                       |

Every component in `START_HERE.md §3` has at least one scaffold call site. No orphans.
