# Canonical Values — Single Source of Truth

<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

This file is the single source of truth for every enumerated value, business number, endpoint contract, rubric anchor, and schema shape that the Week 4 specs reference. Every other spec cites from here rather than restating. When an upstream library value (e.g. a kailash-ml enum) changes, this file is updated first; every referencing spec follows.

Authored against the red-team cross-spec consistency matrix (04-validate/redteam-specs.md §3). All kailash-ml citations reference `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/` at the 2026-04-16 audit commit.

---

## 1. DriftMonitor severity enum — exactly 3 values

Source: `drift_monitor.py:48` — `_SEVERITY_ORDER = {"none": 0, "moderate": 1, "severe": 2}`.

There is **NO `"low"` level**. Any spec that listed `{none, low, moderate, severe}` is wrong; `"low"` does not exist in the library.

| Value      | Meaning                                | Produced when (`drift_monitor.py:594`) |
| ---------- | -------------------------------------- | -------------------------------------- |
| `none`     | No significant distribution shift      | `psi ≤ 0.1` for every feature          |
| `moderate` | Meaningful shift; investigate upstream | `0.1 < psi ≤ 0.25` for any feature     |
| `severe`   | Material shift; retraining is on table | `psi > 0.25` for any feature           |

The overall severity is the `max` across features by ordinal (`drift_monitor.py:608-613`).

Thresholds used by `DriftMonitor.__init__` (`drift_monitor.py:397-399`): `psi_threshold=0.2` (drift alert), `ks_threshold=0.05` (p-value cutoff), `performance_threshold=0.1` (absolute metric degradation). The severity label (`none/moderate/severe`) derives from PSI alone; the KS test governs `drift_detected: bool`, not the severity label.

## 2. AutoML search strategies

Source: `automl_engine.py:55` — `AutoMLConfig.search_strategy: str = "random"`.

Accepted string values passed through to `HyperparameterSearch` (`automl_engine.py:440`):

| Value                | Description                                    |
| -------------------- | ---------------------------------------------- |
| `grid`               | Exhaustive Cartesian over the search space     |
| `random`             | Uniform sampling (library default)             |
| `bayesian`           | Sequential model-based optimisation            |
| `successive_halving` | Multi-fidelity bandit; stops bad configs early |

Week 4 workshop explicitly sets `"random"` in `/forecast/train` so the 5-trial run completes inside the 90-second p95 budget. The library default is ALSO `"random"` — no Bayesian default, despite older spec wording.

## 3. EvalSpec split strategies

Source: `training_pipeline.py:93-95` — `EvalSpec.split_strategy: str = "holdout"`, options commented inline as `"holdout", "kfold", "stratified_kfold", "walk_forward"`.

| Value              | Description                                                | Suited for                |
| ------------------ | ---------------------------------------------------------- | ------------------------- |
| `holdout`          | Single train/test split by `test_size` (default 0.2)       | Quick sanity pass         |
| `kfold`            | K-fold cross-validation; `n_splits` controls folds         | Small tabular datasets    |
| `stratified_kfold` | K-fold preserving class balance per fold                   | Imbalanced classification |
| `walk_forward`     | Time-ordered expanding window; respects temporal causality | Time-series forecasting   |

Week 4 uses `"walk_forward"` (demand forecasting is time-series; `rolling_origin` from older drafts is NOT a valid value and must be replaced wherever it appears).

## 4. ModelRegistry lifecycle states + legal transitions

Source: `model_registry.py:42-49`.

Four states — no more, no less:

```
staging  →  shadow, production, archived
shadow   →  production, archived, staging
production → archived, shadow
archived → staging
```

| From         | Legal next states                   |
| ------------ | ----------------------------------- |
| `staging`    | `shadow`, `production`, `archived`  |
| `shadow`     | `production`, `archived`, `staging` |
| `production` | `archived`, `shadow`                |
| `archived`   | `staging` (reactivation only)       |

A newly registered model enters `staging` (`model_registry.py:508`).

## 5. ModelRegistry versioning shape — `(name, version)`

Source: `model_registry.py:138-145` — `ModelVersion.version: int`, primary key `(name, version)` (`model_registry.py:212`).

The canonical identity of a model version is the tuple `(name: str, version: int)`, NOT a single string `model_version_id`. Every API that currently emits `"model_version_id": "mv_007"` is using a **display alias**, not the registry primary key. When an endpoint needs to round-trip a model version, it MUST accept `name` + `version` OR accept the alias AND document that the alias resolves via a lookup table kept by the scaffold.

Recommended alias shape: `"{short_name}_{version:03d}"` (e.g. `"xgb_007"`) — human-readable, collision-free within one scaffold run.

## 6. Northwind business numbers — canonical forever

Source: `START_HERE.md` §2 (workspace root). These numbers are workshop invariants and MUST NOT drift across specs.

| Quantity           | Value        | Unit                        |
| ------------------ | ------------ | --------------------------- |
| Daily order volume | 12,000       | orders / day                |
| Depots             | 3            | count                       |
| Regular customers  | 500          | count                       |
| Vehicle fleet      | 20           | count                       |
| Historical data    | 2            | years                       |
| Drift event        | Week 78      | week index from 2024-01-01  |
| Stockout cost      | $40          | per unit short of demand    |
| Overstock cost     | $12          | per unit of excess capacity |
| Late-delivery SLA  | $220         | per violation               |
| Driver overtime    | $45          | per hour                    |
| Fuel cost          | $0.35        | per km                      |
| Carbon cost        | $8           | per kg CO₂                  |
| Peak season        | Q4 (Oct–Dec) | seasonal window             |

Stockout vs overstock ratio = $40 / $12 = **3.3 : 1**. Every journal entry scoring 4/4 on D1 (Harm framing) cites this ratio in dollar terms.

## 7. Port topology + service names

Local-only. Ports are not negotiable — Viewer filesystem-watch and preflight script hardcode them.

| Service                 | Port / URL                       | Process                          | Env var fallback           |
| ----------------------- | -------------------------------- | -------------------------------- | -------------------------- |
| Viewer Pane (Next.js)   | `http://localhost:3000`          | `apps/web/` — `next dev`         | `NEXT_PUBLIC_BACKEND_PORT` |
| Nexus API               | `http://localhost:8000`          | `src/backend/app.py` — `uvicorn` | `KAILASH_NEXUS_PORT`       |
| ExperimentTracker store | `sqlite:///data/.experiments.db` | Embedded in Nexus process        | `DATABASE_URL_EXPERIMENTS` |
| ModelRegistry store     | `sqlite:///data/.registry.db`    | Embedded in Nexus process        | `DATABASE_URL_REGISTRY`    |
| FeatureStore backing    | `sqlite:///data/.features.db`    | Embedded in Nexus process        | `DATABASE_URL_FEATURES`    |

If a port is already in use, `scripts/preflight.py` prints the offending PID (via `lsof -i :<port>`) and exits 2 with "stop that process or export `<env var>` to a free port and restart". It does NOT silently rebind.

## 8. Endpoint contracts — canonical

All endpoints are Nexus routes under `src/backend/routes/`. Auth: none (local workshop only). Every endpoint emits top-level telemetry `latency_ms: int` and `started_at: string (ISO-8601)` added by Nexus middleware — these exist on success AND error responses.

### 8.1 `POST /forecast/train`

- **Request** (all fields required unless marked optional):
  - `feature_schema: string` (e.g. `"user_demand"`)
  - `target: string` (e.g. `"orders_next_day"`)
  - `search_strategy: string` (one of §2 values; workshop uses `"random"`)
  - `search_n_trials: int` (workshop uses 5; capped at 20 when `KAILASH_ML_AUTOML_QUICK=1`)
  - `candidate_families: list[string]` (3 entries for workshop — see §8.7)
  - `split_strategy: string` (one of §3 values; workshop uses `"walk_forward"`)
  - `auto_approve: bool` (default `false`)
- **Response 200**: `{ experiment_run_id: string, leaderboard_path: string, n_runs_logged: int, best_metric: {mape: float, rmse: float}, training_duration_s: float }`
- **Errors**: `400` unknown schema · `409` FeatureStore empty · `422` `search_n_trials > 20` with QUICK env · `500` training failure (includes `error_category ∈ {xgb_missing, cv_split_failed, other}`)

### 8.2 `GET /forecast/compare`

- **Query**: `top_n: int = 5`, `scenario: string | null` (values `"preunion" | "postunion" | "postdrift"`)
- **Response 200**: `{ runs: list[{run_id, family, params_hash, metrics, training_duration_s}], compared_at: string }` — MUST return ≥ 3 runs with distinct `params_hash`.
- **Errors**: `409` fewer than 3 runs.

### 8.3 `POST /forecast/predict`

- **Request**: `{ model_version_id: string (alias per §5), inputs: list[{depot_id, date, features}] }`
- **Response 200**: `{ model_version_id, model_stage (§4 enum), predictions: list[{depot_id, date, predicted_orders: float, interval_80: [float, float]}], predicted_at: string }`
- **Errors**: `404` model not found · `409` model is `archived`.

### 8.4 `POST /optimize/solve`

- **Request**: `{ forecast_path, objective: {terms: [{name, weight, unit}]}, hard_constraints, soft_constraints, time_budget_s: int = 30, scenario_tag: string | null }`
- **Response 200**: `{ feasibility: bool, optimality_gap: float ≥ 0, objective_value: float, hard_constraints_satisfied: dict[str, bool], plan_path: string, solver: string, wallclock_s: float, experiment_tags: list[string] }`
- **Errors**: `422` missing forecast · `409` infeasible (body includes `violated_constraints` + `suggestion`).

### 8.5 `POST /drift/check`

- **Request**: `{ model_id: string (alias per §5), window_days: int = 30, reference_window: string = "training" }`
- **Response 200**: `{ model_id, severity: string (§1 enum; one of none/moderate/severe), tests: list[{name ∈ {ks, psi}, feature, statistic: float, p_value?: float, alert: bool}], recommendations: list[string], checked_at: string }` — tests are KS (continuous features) and PSI (population stability) only. No Chi² or JS-divergence; the library does not ship them.
- **Errors**: `404` model not found · `409` reference not set.

### 8.6 `GET /health`

- **Response 200** (field types locked): `{ ok: bool, db: bool, feature_store: bool, drift_wiring: bool, registry_runs: int }` — every status flag is boolean, not a string literal. Consumed by `scripts/preflight.py` and the Viewer preflight banner.

### 8.7 Candidate family list (workshop default)

`AutoMLConfig.candidate_families` takes **fully-qualified Python class paths** — the same dotted-path string a caller would pass to `importlib.import_module`. Short names (e.g. `"LinearRegression"`) are BLOCKED; every downstream spec (`product-northwind.md §8.1`, `data-fixtures.md §3.1`, `playbook-phases-sml.md`) cites this section as the pin.

Workshop trains three families in `/forecast/train` so the 5-trial run stays under 90s. The canonical Week 4 entries are:

```json
[
  "sklearn.linear_model.LinearRegression",
  "sklearn.linear_model.Ridge",
  "sklearn.ensemble.RandomForestRegressor",
  "sklearn.ensemble.GradientBoostingRegressor"
]
```

Plus `"xgboost.XGBRegressor"` when the `[xgb]` extra is available. When XGBoost is unavailable, `scripts/preflight.py` substitutes a second `"sklearn.ensemble.GradientBoostingRegressor"` instance with a different `random_state` so the family list length remains stable across machines; the substitution is announced visibly at preflight (never silent).

Grader and leaderboard comparisons match on the exact fully-qualified string; the regex `^[a-z_]+(\.[a-z_]+)+\.[A-Z][A-Za-z]+$` is the validation shape.

## 9. Rubric dimensions + score anchors (5 dims × 3 anchors)

Canonical for both `rubric-grader.md` and `decision-journal.md`. Scores are 0, 2, or 4 per dimension. Score 1 and 3 are not used (they were removed to force binary-plus-evidence anchors).

| Dim | Name                  | 0 anchor                     | 2 anchor                  | 4 anchor                                                   |
| --- | --------------------- | ---------------------------- | ------------------------- | ---------------------------------------------------------- |
| D1  | Harm framing          | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($40 vs $12 = 3.3:1) |
| D2  | Metric → cost linkage | Metric chosen without reason | Reason named              | Reason is a dollar figure or dollar-equivalent             |
| D3  | Trade-off honesty     | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice (e.g. "lost 0.8% MAPE")           |
| D4  | Constraint classify   | Unclear hard/soft            | Labelled correctly        | Penalty (in dollars) + reasoning included                  |
| D5  | Reversal condition    | "If data changed"            | Names a signal            | Names signal + threshold + duration window (no bare rules) |

Cohort-average target: ≥ 3.0 across all entries to pass. Not every dimension applies per phase — the applicability matrix lives in `rubric-grader.md` §1.3.

## 10. Journal entry schema

Filename: `journal/phase_<N>_<slug>.md` where `N ∈ 1..13` and `<slug>` is one of `{default, postunion, postdrift, retrain}`.

Required YAML frontmatter fields:

| Field                | Type                     | Required | Notes                                                     |
| -------------------- | ------------------------ | -------- | --------------------------------------------------------- |
| `phase`              | int (1..13)              | yes      | Must match filename                                       |
| `phase_name`         | string                   | yes      | From `playbook-universal.md` phase table                  |
| `sprint`             | int (1,2,3) \| `"close"` | yes      | —                                                         |
| `timestamp`          | string (ISO-8601 + tz)   | yes      | Auto-filled by `metis journal add`                        |
| `experiment_run_ids` | list[string]             | yes      | May be `[]`; graded 0 on D3 for phases that produce runs  |
| `model_version_ids`  | list[string]             | yes      | Registry aliases per §5                                   |
| `scenario_tag`       | string \| null           | yes      | One of `null`, `"preunion"`, `"postunion"`, `"postdrift"` |

Required body headings (one `##` per rubric dimension — graded by literal-match parsing): `## Harm framing`, `## Metric-cost linkage`, `## Trade-off honesty`, `## Constraint classification`, `## Reversal condition`.

## 11. Scenario event ID registry

Links to `scenario-catalog.md` where the full behaviour lives. Four live scenarios + one Week-7 rehearsal:

| ID                       | Sprint | Live in Week 4? | Full spec                                                                                  |
| ------------------------ | ------ | --------------- | ------------------------------------------------------------------------------------------ |
| `union-cap`              | 2      | yes             | scenario-catalog §2 (SG framing: MOM Employment Act tightening — legacy event ID retained) |
| `drift-week-78`          | 3      | yes             | scenario-catalog §3                                                                        |
| `lta-carbon-levy`        | 2 or 3 | yes             | scenario-catalog §4                                                                        |
| `hdb-loading-curfew`     | 2      | Week 5+ ready   | scenario-catalog §5                                                                        |
| `mas-climate-disclosure` | close  | Week 5+ ready   | scenario-catalog §6                                                                        |

## 12. ExperimentTracker run ID format

Source: `experiment_tracker.py:627` — `run_id = str(uuid.uuid4())`.

The internal identity is a canonical **UUID4** (36-char hyphenated hex, e.g. `"a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"`). The workshop additionally surfaces a **human-readable alias** (`"xgb_007_20260416_143012"`) in response bodies so students can reason about runs without squinting at UUIDs. The alias is a cosmetic index maintained by the scaffold in `data/.experiment_aliases.json`; the UUID is the canonical FK to `ExperimentTracker.get_run()`.

Grader assertion: the response `experiment_run_id` MUST resolve via `ExperimentTracker.get_run(id)` whether it was passed as UUID or alias — the scaffold's lookup handles both.

---

## Open TODOs (values not yet pinned to source)

- **ExperimentTracker alias generator** — the alias format `"{short_family}_{ordinal:03d}_{YYYYMMDD}_{HHMMSS}"` is workshop convention, not library contract. Flagged for scaffold implementation; no library citation possible.
- **XGBoost as 3rd family** — scaffold substitutes `GradientBoostingRegressor` when XGBoost is not installed. The substitution rule is workshop convention; preflight MUST announce the substitution visibly.
