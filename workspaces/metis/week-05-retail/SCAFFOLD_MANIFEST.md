<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Scaffold Manifest — Week 5 Retail (Arcadia)

**Version:** 2026-04-23 · **License:** CC BY 4.0

The retail product is pre-built at the repo root (`src/retail/` + `apps/web/retail/`). Workspace artefacts are student-produced during `/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`.

## State legend

- `[PRE-BUILT]` — ships complete; students do not edit.
- `[STUDENT-PRODUCED]` — written during `/analyze` / `/todos` / `/implement` / `/redteam` / `/codify`.
- `[PRE-BUILT + STUDENT-EXTENDED]` — skeleton ships; students extend at a named point.

## Repo-root (pre-built product)

| Path                                           | State         | Role                                                                               |
| ---------------------------------------------- | ------------- | ---------------------------------------------------------------------------------- |
| `pyproject.toml`                               | `[PRE-BUILT]` | Shared deps (kailash 2.8.12, kailash-ml 0.17.0, sklearn, polars, fastapi, uvicorn) |
| `MONOREPO.md`                                  | `[PRE-BUILT]` | Monorepo doctrine (src/<domain> + apps/<platform>/<domain>)                        |
| `src/retail/backend/app.py`                    | `[PRE-BUILT]` | FastAPI app factory + CORS + lifespan                                              |
| `src/retail/backend/config.py`                 | `[PRE-BUILT]` | Env reader; resolves `retail_root` and `workspace_root`                            |
| `src/retail/backend/startup.py`                | `[PRE-BUILT]` | Loads data, trains K=3 baseline, builds content recommender, registers drift ref   |
| `src/retail/backend/ml_context.py`             | `[PRE-BUILT]` | Shared state: customers/products/txns + baseline + recommender + sweep + drift ref |
| `src/retail/backend/routes/health.py`          | `[PRE-BUILT]` | `GET /health`                                                                      |
| `src/retail/backend/routes/segment.py`         | `[PRE-BUILT]` | K=3 baseline + K-sweep + live fit + name + promote + registry + stability probe    |
| `src/retail/backend/routes/recommend.py`       | `[PRE-BUILT]` | content + collaborative (NMF) + hybrid + cold-start strategies + offline compare   |
| `src/retail/backend/routes/drift.py`           | `[PRE-BUILT]` | PSI per feature + segment-membership churn + retrain-rule persistence              |
| `src/retail/data/arcadia_customers.csv`        | `[PRE-BUILT]` | 5 000 customers × 14 features (latent segments + income_tier are grader-only)      |
| `src/retail/data/arcadia_products.csv`         | `[PRE-BUILT]` | 400 SKUs × 9 features                                                              |
| `src/retail/data/arcadia_transactions.csv`     | `[PRE-BUILT]` | 120 000 transactions                                                               |
| `src/retail/data/segment_baseline.json`        | `[PRE-BUILT]` | K=3 baseline (silhouette ≈ 0.34)                                                   |
| `src/retail/data/segment_candidates.json`      | `[PRE-BUILT]` | K-sweep K=2..10 (pre-baked reference)                                              |
| `src/retail/data/drift_baseline.json`          | `[PRE-BUILT]` | Reference distribution for each clustering feature                                 |
| `src/retail/data/scenarios/pdpa_redline.json`  | `[PRE-BUILT]` | Sprint 2 mid-injection — re-classify under-18 browse as hard constraint            |
| `src/retail/data/scenarios/catalog_drift.json` | `[PRE-BUILT]` | Sprint 3 mid-injection — wellness launch shifts category mix                       |
| `src/retail/scripts/generate_data.py`          | `[PRE-BUILT]` | Data generator (seed 20260423) — deterministic re-run                              |
| `src/retail/scripts/preflight.py`              | `[PRE-BUILT]` | Green-light check; exit 0 = all green                                              |
| `src/retail/scripts/run_backend.sh`            | `[PRE-BUILT]` | `uvicorn backend.app:app` with `METIS_API_HOST`/`METIS_API_PORT`                   |
| `src/retail/scripts/scenario_inject.py`        | `[PRE-BUILT]` | Fire pdpa_redline or catalog_drift; writes marker in workspace                     |
| `apps/web/retail/index.html`                   | `[PRE-BUILT]` | Viewer Pane — 6 cards polling backend every 5 s                                    |
| `apps/web/retail/serve.sh`                     | `[PRE-BUILT]` | `python3 -m http.server 3000`                                                      |

## Workspace (student-produced)

| Path                                 | State                | When produced       |
| ------------------------------------ | -------------------- | ------------------- |
| `PRODUCT_BRIEF.md`                   | `[PRE-BUILT]`        | Ships with scaffold |
| `PLAYBOOK.md`                        | `[PRE-BUILT]`        | Ships with scaffold |
| `START_HERE.md`                      | `[PRE-BUILT]`        | Ships with scaffold |
| `specs/_index.md` + supporting specs | `[PRE-BUILT]`        | Ships with scaffold |
| `journal/_template.md`               | `[PRE-BUILT]`        | Schema for entries  |
| `briefs/`                            | `[STUDENT-PRODUCED]` | Student-writable    |
| `01-analysis/failure-points.md`      | `[STUDENT-PRODUCED]` | `/analyze`          |
| `01-analysis/assumptions.md`         | `[STUDENT-PRODUCED]` | `/analyze`          |
| `01-analysis/decisions-open.md`      | `[STUDENT-PRODUCED]` | `/analyze`          |
| `todos/active/phase_N_*.md` (×13)    | `[STUDENT-PRODUCED]` | `/todos`            |
| `todos/completed/phase_N_*.md`       | `[STUDENT-PRODUCED]` | `/implement`        |
| `journal/phase_{1..13}_*.md`         | `[STUDENT-PRODUCED]` | `/implement`        |
| `journal/phase_11_postpdpa.md`       | `[STUDENT-PRODUCED]` | Sprint 2 injection  |
| `journal/phase_12_postpdpa.md`       | `[STUDENT-PRODUCED]` | Sprint 2 injection  |
| `04-validate/redteam.md`             | `[STUDENT-PRODUCED]` | `/redteam`          |
| `.session-notes`                     | `[STUDENT-PRODUCED]` | `/wrapup`           |

## Contract violations

- A `[PRE-BUILT]` file with a `TODO-STUDENT` marker is a scaffolding error — instructor fixes.
- A `[STUDENT-PRODUCED]` file with `"placeholder": true` or a `# TODO` marker in the body scores zero on the rubric.
- Missing `journal/phase_N_*.md` for a phase the student claimed to run is a D3 (trade-off honesty) zero.
