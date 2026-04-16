# Data Fixtures — Synthetic Northwind Dataset

This spec is the authority on the data that ships with the Week 4 scaffold. The dataset is synthetic (no real customer data), designed to produce a meaningful model comparison in a 5-trial AutoML run AND to exhibit a clean drift signal at week 78.

Every file listed is `[PRE-BUILT]` per `scaffold-contract.md` §4. Data generation is done once during scaffolding via `scripts/seed_experiments.py` + `scripts/seed_drift.py`; students never regenerate.

## 1. Primary training dataset — `data/northwind_demand.csv`

### 1.1 Shape

- **Rows**: ~2,190 (= 3 depots × 730 days × 1 row per depot-day).
- **Columns**: 13 (9 features + 1 target + 3 identifiers).
- **Temporal range**: 2 full years, from `2024-01-01` through `2025-12-31` inclusive. Week indexing is 1-based from `2024-01-01` (day 1 = week 1). Under this convention, week 78 day 1 = 2024-01-01 + 77 weeks × 7 days = `2025-06-23`. (An older draft used `2025-07-01`; the off-by-one came from 1-based week indexing vs ISO-week convention. The generator uses 1-based; the date is `2025-06-23`. If an ISO-week reading is ever needed for cross-reference, document the conversion at that call site.)
- **File size**: ~280 KB uncompressed; < 1 s to ingest into `FeatureStore`.

### 1.2 Columns

| Column                   | Type   | Role       | Description                                                                         |
| ------------------------ | ------ | ---------- | ----------------------------------------------------------------------------------- |
| `date`                   | date   | identifier | Daily granularity; format `YYYY-MM-DD`                                              |
| `depot_id`               | string | identifier | One of `D01`, `D02`, `D03`                                                          |
| `week_number`            | int    | identifier | 1-based week counter from 2024-01-01                                                |
| `orders_last_day`        | int    | feature    | Previous day's order count for the depot (autoregressive feature)                   |
| `orders_7d_rolling_avg`  | float  | feature    | 7-day trailing average of orders                                                    |
| `orders_28d_rolling_avg` | float  | feature    | 28-day trailing average of orders                                                   |
| `day_of_week`            | int    | feature    | 0–6                                                                                 |
| `is_holiday`             | bool   | feature    | Singapore public holidays (workshop is aimed at SG MBA cohort)                      |
| `active_customers`       | int    | feature    | Customers with ≥ 1 order in the last 28 days, scoped to depot                       |
| `customer_mix_hash`      | float  | feature    | Categorical hash of the active customer segment distribution (drift signal carrier) |
| `avg_order_value`        | float  | feature    | Rolling 7-day average order value in dollars                                        |
| `is_peak_season`         | bool   | feature    | True for Q4 dates (Oct–Dec)                                                         |
| `orders_next_day`        | int    | **target** | Next day's order count — what the model predicts                                    |

The 9 features match `specs/schemas/demand.py` exactly. The target is `orders_next_day`, computed as a 1-day lookahead during data generation so training is leak-free when rolling-origin CV is used.

### 1.3 Distribution anchors

- Daily order mean by depot: D01 ≈ 4,500; D02 ≈ 4,000; D03 ≈ 3,500 (sums to ~12,000, matching `product-northwind.md` §5).
- Q4 seasonality: +18% mean lift across all depots.
- Weekday pattern: Saturday +12%, Sunday −15%, Monday −5% vs mid-week baseline.
- Holiday dip: −22% on `is_holiday` dates.
- Customer mix (`customer_mix_hash`): three stable segments pre-drift — `retail` (55%), `hospitality` (30%), `industrial` (15%).

### 1.4 Holdout file — `data/northwind_demand_holdout.csv`

Final 30 days of the training range (`2025-12-02` through `2025-12-31`) held out for Phase 7 red-team. Same columns; same distribution. Students do NOT see this during AutoML — it only comes in at Phase 7 for adversarial evaluation.

## 2. Injected drift at week 78

Week 78 corresponds to `2025-06-23` (day 1 of week 78 with 2024-01-01 as week 1 day 1, 1-based indexing). The drift is injected NOT into the primary training CSV (which must stay stable across sessions) but into a separate post-drift window — see `data/scenarios/week78_drift.json` below. The training CSV ends at 2025-12-31 and remains unchanged; the drift window is a "what if week 78's pattern persisted for 30 days" alternate future that the instructor activates during Sprint 3.

### 2.1 Exactly what changes in the drift window

All changes are relative to the pre-drift training distribution, NOT relative to the prior day:

1. **Customer mix shift** — `retail` drops from 55% → 35%, `hospitality` stays at 30%, `industrial` rises from 15% → 35%. A new segment `government` appears at 5% (unseen in training — this is the drift signal).
2. **Order value shift** — `avg_order_value` mean rises by 18% (industrial customers place larger orders).
3. **Day-of-week flattening** — Saturday lift drops from +12% → +4% (industrial + government customers don't weekend-buy).
4. **Customer mix hash distribution** — `customer_mix_hash` has 4 modes instead of 3 (the new `government` segment); the PSI and KS tests against the training reference will fire on this column.

### 2.2 What stays the same

- `depot_id` distribution (still 3 depots in D01/D02/D03 proportions).
- `is_holiday` schedule.
- `is_peak_season` flag (drift window is July — not peak-season).
- The target variable `orders_next_day` is generated under the shifted distribution, so a model trained on pre-drift data will systematically under-predict for the new mix.

### 2.3 Payload file — `data/scenarios/week78_drift.json`

Per `scaffold-contract.md` §4, pre-built JSON fixtures MUST NOT carry the `_todo_student` marker (even as `null`) — the banner is a `[STUDENT-COMMISSIONED]` signal only; shipping it in a pre-built fixture teaches the wrong hygiene.

```json
{
  "scenario": "week78_drift",
  "window_start": "2025-06-23",
  "window_days": 30,
  "rows": [
    {
      "date": "2025-06-23",
      "depot_id": "D01",
      "week_number": 78,
      "orders_last_day": 4521,
      "orders_7d_rolling_avg": 4480.2,
      "orders_28d_rolling_avg": 4405.7,
      "day_of_week": 0,
      "is_holiday": false,
      "active_customers": 512,
      "customer_mix_hash": 0.87,
      "avg_order_value": 47.2,
      "is_peak_season": false,
      "orders_next_day": 4398
    }
    // ... 89 more rows (30 days × 3 depots)
  ]
}
```

## 3. Pre-baked AutoML leaderboard — `data/leaderboard_prebaked.json`

Produced once by `scripts/seed_experiments.py` during scaffolding. Real `ExperimentTracker` run IDs, real metrics, real parameter hashes — not synthetic. Students compare their live 5-trial run against this pre-baked 30-trial run.

### 3.1 Generation parameters

- **Search strategy**: `"bayesian"` (explicitly set in `seed_experiments.py` — AutoMLConfig's own default is `"random"`; Bayesian is the deliberate choice for the pre-bake, NOT a library default).
- **Total trials**: 30 (vs the live run's 5).
- **Candidate families**: 5 — `sklearn.linear_model.Ridge`, `sklearn.ensemble.RandomForestRegressor`, `sklearn.ensemble.GradientBoostingRegressor`, `sklearn.linear_model.LinearRegression`, `xgboost.XGBRegressor` (when `[xgb]` extra available on the scaffolding machine; otherwise omitted and the pre-bake has 4 families). Field name on `AutoMLConfig` is `candidate_families`, NOT `families`. Entries are **fully-qualified Python class paths** per `canonical-values.md §8.7` — the `model_class` field in the leaderboard schema (§3.2) uses these exact strings so grader comparisons match without lowercase-shortname ambiguity.
- **Eval split**: `EvalSpec(split_strategy='walk_forward', n_splits=6, test_size=0.2)` — the library's supported value for time-series rolling-origin-style evaluation; `cv_strategy='rolling_origin'` is NOT a valid EvalSpec value.
- **Metric optimised**: MAPE.
- **Auto-approve**: true (the seed script runs unattended).

### 3.2 Content schema

The `model_class` field MUST carry the fully-qualified Python class path that matches `AutoMLConfig.candidate_families` (`canonical-values.md §8.7`). Grader comparisons (shard 06 `grade_product.py`) key on exact-string match against this field; short names are rejected with a guidance message.

```json
{
  "generated_at": "2026-04-15T22:30:00Z",
  "kailash_ml_version": "<pinned version>",
  "runs": [
    {
      "run_id": "prebake_xgb_011",
      "model_class": "xgboost.XGBRegressor",
      "params_hash": "f7a2c9b1",
      "params": {"n_estimators": 240, "max_depth": 6, "learning_rate": 0.07, ...},
      "metrics": {
        "mape": 0.0589,
        "rmse": 39.8,
        "mae": 28.4,
        "fold_variance": 0.0032
      },
      "training_duration_s": 18.4,
      "tracker_run_id": "<uuid>"
    },
    {
      "run_id": "prebake_gbm_013",
      "model_class": "sklearn.ensemble.GradientBoostingRegressor",
      "params_hash": "a4d8e2f0",
      "params": {"n_estimators": 180, "max_depth": 4, "learning_rate": 0.05},
      "metrics": {
        "mape": 0.0612,
        "rmse": 41.2,
        "mae": 29.1,
        "fold_variance": 0.0038
      },
      "training_duration_s": 14.9,
      "tracker_run_id": "<uuid>"
    }
    // ... 28 more runs, sorted by MAPE ascending
  ],
  "best_by_family": {
    "sklearn.linear_model.LinearRegression": "prebake_lr_003",
    "sklearn.linear_model.Ridge": "prebake_ridge_002",
    "sklearn.ensemble.RandomForestRegressor": "prebake_rf_007",
    "sklearn.ensemble.GradientBoostingRegressor": "prebake_gbm_013",
    "xgboost.XGBRegressor": "prebake_xgb_011"
  }
}
```

### 3.3 Expected jump

A 5-trial / 3-family live run on a student laptop produces headline MAPE of ~0.074 in ~80 s. The pre-baked 30-trial / 5-family run's best is ~0.059. The ~1.5-percentage-point gap is the Trust Plane question for Phase 5: "the pre-bake beats my live run by 1.8% MAPE — is the lift worth 6× the compute AND the risk of over-fit to this specific fold layout?"

## 4. Drift baseline — `data/drift_baseline.json`

Produced by `scripts/seed_drift.py`. Captures the `DriftMonitor` reference distribution for the training window. Structure:

```json
{
  "model_id": "<reserved>", // filled in by drift_wiring.py at first training completion
  "reference_window": "2024-01-01 to 2025-12-01",
  "feature_summaries": {
    "customer_mix_hash": {
      "type": "numeric",
      "mean": 0.52,
      "std": 0.18,
      "quantiles": {
        "p05": 0.22,
        "p25": 0.38,
        "p50": 0.51,
        "p75": 0.66,
        "p95": 0.79
      }
    },
    "avg_order_value": {
      "type": "numeric",
      "mean": 40.1,
      "std": 5.2,
      "quantiles": {
        "p05": 32.1,
        "p25": 36.4,
        "p50": 40.0,
        "p75": 43.8,
        "p95": 48.9
      }
    }
    // ... 7 more features
  },
  "target_summary": {
    "type": "numeric",
    "mean": 4013.5,
    "std": 620.4
  }
}
```

`drift_wiring.wire(model_name, reference_df, feature_columns)` reads this file (and the training rows) and calls `await DriftMonitor.set_reference_data(model_name, reference_data, feature_columns)` — positional `model_name` + `reference_data` + `feature_columns`. `TrainingPipeline` has NO `on_complete` event hook in kailash-ml; `drift_wiring.wire` is called synchronously by `/forecast/train` after `pipeline.train(...)` returns. Students do not touch this file.

## 5. Union-cap scenario — `data/scenarios/union_cap.json`

```json
{
  "scenario": "union_cap",
  "constraint": "driver_overtime_hours_max",
  "new_cap": 5,
  "unit": "hours_per_week",
  "classification_hint": "hard",
  "reason": "driver union collective bargaining agreement; violation exposes the company to arbitration penalties estimated at $18,000 per driver-incident"
}
```

No `_todo_student` marker (pre-built fixture — per `scaffold-contract.md` §4, the banner is `[STUDENT-COMMISSIONED]`-only).

The reason string is deliberately grounded in a dollar figure so the student's Phase 11 journal entry has a number to cite when explaining the hard/soft re-classification.

## 6. FeatureStore loading flow

1. **Nexus startup** — `src/backend/app.py` imports `fs_preload` and calls `fs_preload.run()` in the startup hook.
2. **`fs_preload.run()`** — loads `data/northwind_demand.csv` into a Polars DataFrame, imports the `FeatureSchema` from `specs/schemas/demand.py`, then awaits `fs.register_features(schema)` followed by `fs.store(schema, df)` — the two-call API kailash-ml actually exposes. There is NO `fs.ingest()` method on `FeatureStore`; attempting it raises `AttributeError`. On completion, writes `.preflight.json` key `feature_store_populated: true`. Idempotent — if the schema is already registered and rows are already stored, `register_features` + `store` are safe no-ops.
3. **First `/forecast/train` call** — the route hander calls `fs.register_features(schema)` + `fs.store(schema, df)` itself (defence-in-depth for the startup hook) before constructing `TrainingPipeline`. `TrainingPipeline.train` queries the FeatureStore via `fs.get_features`/`get_training_set` as needed; returns rows as a Polars DataFrame.
4. **After `/forecast/train` returns** — route handler calls `drift_wiring.wire(model_name, reference_df, feature_columns)` synchronously BEFORE returning the HTTP response. `wire()` reads `data/drift_baseline.json` if the reference isn't already set for this model, then awaits `DriftMonitor.set_reference_data(model_name, reference_data, feature_columns)` (positional signature per source) and writes `.preflight.json.drift_wiring: true`. There is NO `TrainingPipeline.on_complete` event hook in kailash-ml; wiring is synchronous-call, not pub/sub.
5. **Scenario activation** — when `scenario_inject.py` fires, the endpoint paths (`/optimize/solve`, `/drift/check`) read `data/scenarios/active_*.json` markers and adjust their behaviour.

## 7. Determinism

- Training CSV seed: `RANDOM_SEED=42` in `seed_experiments.py`. Same seed + same `kailash_ml` version produces identical bytes.
- AutoML pre-bake seed: `AUTOML_SEED=2026` in `seed_experiments.py`. Same seed + same Bayesian backend produces identical leaderboard.
- Drift window seed: `DRIFT_SEED=78` in `seed_drift.py`.

Seeds live in `.env.example`. Students inherit via `.env` copy. A student who re-runs a seed script (not expected — it's one-shot) reproduces the exact shipped data.

## 8. Data hygiene

- No real customer identifiers. Every `depot_id` / `customer_mix_hash` is synthetic.
- No PII. `active_customers` is an integer count; no names, no IDs.
- No secrets in the data files.
- CSV + JSON only; no parquet (keeps the scaffold dependency-light).

## Open questions

- **Holiday calendar** — the data generator uses Singapore public holidays (instructor's current teaching context). If the course runs in another jurisdiction, the holiday column will be miscalibrated but won't break the workshop; `is_holiday` is one of 9 features. Flag for Week 5+: parameterise in the seed script.
- **~~Drift-week numbering~~** — closed in red-team. The training CSV contains NO historical week-40 drift; the week-78 injection is the ONLY drift the workshop tests. `product-northwind.md` and `START_HERE.md` references to "historical drift week 40" have been removed. If a future week needs a historical-variance grounding, inject a mild seasonal wobble in the generator AND document it here.
