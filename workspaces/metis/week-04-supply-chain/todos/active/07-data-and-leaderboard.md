---
shard_id: 07
slug: data-and-leaderboard
title: >
  Generate the synthetic Northwind dataset and all pre-baked fixtures:
  northwind_demand.csv (2 years, 3 depots, ~2190 rows), northwind_demand_holdout.csv
  (final 30 days), week78_drift.json (30-day post-CNY drift window),
  drift_baseline.json (DriftMonitor reference distribution),
  leaderboard_prebaked.json (30-trial Bayesian AutoML run), union_cap.json,
  and specs/schemas/demand.py (FeatureSchema). All generated with deterministic
  seeds; no randomness without seed.
loc_estimate: 350
invariants:
  - deterministic-seeds: RANDOM_SEED=42 for training CSV, AUTOML_SEED=2026 for pre-bake, DRIFT_SEED=78 for drift window; same seed + same kailash_ml version = identical bytes per data-fixtures.md §7
  - week78-date: week 78 day 1 = 2024-01-01 + 77 weeks × 7 days = 2025-06-23 (1-based week indexing, NOT ISO-week convention); any code that computes this date must use 1-based arithmetic and document the conversion per data-fixtures.md §1.1
  - no-todo-student-in-prebaked: PRE-BUILT fixture files MUST NOT contain "_todo_student" marker (not as null, not as string); the banner is STUDENT-COMMISSIONED-only per scaffold-contract.md §4 + data-fixtures.md §2.3
  - leaderboard-field-name: leaderboard_prebaked.json uses candidate_families field name (NOT families) per data-fixtures.md §3.1; search_strategy is "bayesian" (explicit, not the AutoMLConfig default of "random")
  - feature-schema-9-columns: specs/schemas/demand.py FeatureSchema declares exactly 9 features matching data-fixtures.md §1.2 column table; target is orders_next_day; no extra or missing columns
call_graph_hops: 2
depends_on: [01]
blocks: [02, 03, 04, 06]
dependency_note: >
  C3 fix: leaderboard_prebaked.json generation in seed_experiments.py requires a live
  ExperimentTracker + AutoMLEngine via get_ml_context() to produce real UUID4 run IDs
  per data-fixtures.md §3.2 and canonical-values.md §12. Shard 01 must land first.
  The "07 blocks 01" edge in the original DAG was wrong — 01 does not require the
  leaderboard; it requires specs/schemas/demand.py and the CSV (both still produced
  here), but those can only be READ by 01 after 07 runs. Corrected: 07 depends_on=[01],
  blocks=[02,03,04,06]. 07 no longer lists itself as blocking 01.
multi_writer_note: >
  READS .env.example and .preflight.json. Does NOT write .env.example; shard 09 is
  sole writer. The seed scripts READ RANDOM_SEED/AUTOML_SEED/DRIFT_SEED from .env
  (via python-dotenv); they do not write .env.example.
specs_consulted:
  - specs/data-fixtures.md §1 (northwind_demand.csv shape: ~2190 rows, 13 columns, date range 2024-01-01 to 2025-12-31, distribution anchors D01≈4500/D02≈4000/D03≈3500)
  - specs/data-fixtures.md §1.3 (distribution anchors: Q4 +18%, Saturday +12%, Sunday -15%, Monday -5%, holiday -22%, customer_mix_hash 3 stable segments pre-drift)
  - specs/data-fixtures.md §1.4 (holdout: final 30 days 2025-12-02 through 2025-12-31)
  - specs/data-fixtures.md §2 (drift window: week 78 = 2025-06-23; 4 changes: customer_mix shift, avg_order_value +18%, day-of-week flattening, 4-mode customer_mix_hash)
  - specs/data-fixtures.md §2.3 (week78_drift.json payload schema)
  - specs/data-fixtures.md §3 (leaderboard_prebaked.json: 30 trials, Bayesian, 5 families, EvalSpec split_strategy="walk_forward" n_splits=6 test_size=0.2, MAPE-optimised)
  - specs/data-fixtures.md §3.2 (leaderboard content schema: run_id, family, params_hash, params, metrics{mape/rmse/mae/fold_variance}, training_duration_s, tracker_run_id, best_by_family dict)
  - specs/data-fixtures.md §4 (drift_baseline.json schema: model_id, reference_window, feature_summaries with quantiles, target_summary)
  - specs/data-fixtures.md §5 (union_cap.json payload: constraint, new_cap:5, unit, classification_hint, reason with dollar figure)
  - specs/data-fixtures.md §6 (FeatureStore loading flow — confirms register_features + store two-call API; no ingest())
  - specs/data-fixtures.md §7 (determinism: RANDOM_SEED=42, AUTOML_SEED=2026, DRIFT_SEED=78)
  - specs/scaffold-contract.md §4 (data/ file list, PRE-BUILT roles, no _todo_student in pre-built fixtures)
acceptance_criteria:
  - specs/schemas/demand.py exists and defines FeatureSchema with exactly 9 feature columns matching data-fixtures.md §1.2 (orders_last_day, orders_7d_rolling_avg, orders_28d_rolling_avg, day_of_week, is_holiday, active_customers, customer_mix_hash, avg_order_value, is_peak_season) and target orders_next_day; used by fs_preload.py (shard 01)
  - scripts/seed_experiments.py generates data/northwind_demand.csv: ~2190 rows (3 depots × 730 days), 13 columns per data-fixtures.md §1.2, date range 2024-01-01 through 2025-12-31, RANDOM_SEED=42, distribution anchors within ±5% of spec means
  - scripts/seed_experiments.py generates data/northwind_demand_holdout.csv: final 30 days (2025-12-02 through 2025-12-31), same 13 columns
  - scripts/seed_experiments.py generates data/leaderboard_prebaked.json: 30 real ExperimentTracker runs, Bayesian search (search_strategy="bayesian" — explicit, not library default), 5 families (Ridge/RF/GBM/LR/XGB when [xgb] available; 4 families otherwise), EvalSpec(split_strategy="walk_forward", n_splits=6, test_size=0.2), sorted by MAPE ascending, best_by_family dict, schema per data-fixtures.md §3.2
  - Pre-baked leaderboard entries use fully-qualified model_class values matching canonical-values.md §8.7 (e.g. "sklearn.linear_model.Ridge", "xgboost.XGBRegressor"); best_by_family keys use the same fully-qualified strings; short-name entries are BLOCKED
  - scripts/seed_drift.py generates data/scenarios/week78_drift.json: 90 rows (30 days × 3 depots), window_start "2025-06-23" (1-based week 78 day 1), 4 changes per data-fixtures.md §2.1 (customer_mix shift retail 55%→35% + government 5% new segment, avg_order_value +18%, Saturday lift +4% not +12%, 4-mode customer_mix_hash), DRIFT_SEED=78; no _todo_student marker
  - scripts/seed_drift.py generates data/drift_baseline.json: feature_summaries for all 9 features with mean/std/quantiles (p05/p25/p50/p75/p95), target_summary, model_id field left as placeholder (filled by drift_wiring.py at first training), per data-fixtures.md §4
  - data/scenarios/union_cap.json exists with constraint="driver_overtime_hours_max", new_cap=5, unit="hours_per_week", classification_hint="hard", reason string with dollar figure per data-fixtures.md §5; no _todo_student marker
  - data/README.md enumerates every JSON file the Viewer expects + who writes it per scaffold-contract.md §4
  - .env.example is NOT authored by this shard; shard 09 is sole .env.example writer; seed scripts read RANDOM_SEED/AUTOML_SEED/DRIFT_SEED from .env via python-dotenv
  - tests/unit/test_data_fixtures_determinism.py passes: runs seed_experiments.py twice with same seed and asserts byte-identical northwind_demand.csv output; asserts week78 window_start == "2025-06-23"
  - tests/unit/test_demand_schema_columns.py passes: imports FeatureSchema from specs/schemas/demand.py; asserts exactly 9 feature names + 1 target; asserts no "ingest" method exists on FeatureStore (guards F3 from risk-assessment)
wiring_tests:
  - tests/unit/test_data_fixtures_determinism.py (data-fixtures.md §7 seed contract)
  - tests/unit/test_demand_schema_columns.py (data-fixtures.md §1.2 column count + no-ingest guard)
---

# Shard 07 — Data and Leaderboard

## What

Generate all pre-built data fixtures that every other shard depends on: the synthetic Northwind demand CSV, holdout CSV, pre-baked AutoML leaderboard, drift baseline, week-78 drift payload, union-cap scenario fixture, and the `FeatureSchema` Python dataclass. Two generator scripts (`seed_experiments.py`, `seed_drift.py`) run once during scaffolding and are checked into the repo as one-shot generators; students never re-run them.

## Why

This shard blocks 01/02/03/04/06 because all of them import from `specs/schemas/demand.py` or read the CSV at startup. If the week-78 date is wrong (the off-by-one between 1-based and ISO-week conventions documented in `data-fixtures.md §1.1`), every Sprint 3 drift scenario lands on the wrong data window and produces no KS/PSI signal. The determinism tests catch seed regression — a generator that passes with one `numpy` version but produces different bytes on another will fail the CI preflight.

## Implementation sketch

- `specs/schemas/demand.py` — `FeatureSchema` dataclass with 9 named fields matching the column table; `target = "orders_next_day"`; validates column presence at import time (raises on mismatch)
- `scripts/seed_experiments.py` — `numpy.random.default_rng(42)` for the CSV; 3-depot × 730-day loop computing each column per the distribution anchors; writes `data/northwind_demand.csv` + `data/northwind_demand_holdout.csv`; then constructs real `AutoMLEngine` with `search_strategy="bayesian"`, `AutoMLConfig(candidate_families=[...])`, `EvalSpec(split_strategy="walk_forward", n_splits=6, test_size=0.2)`, runs 30 trials, writes real ExperimentTracker run IDs to `data/leaderboard_prebaked.json`
- `scripts/seed_drift.py` — `numpy.random.default_rng(78)` for the drift window; computes week 78 day 1 as `date(2024, 1, 1) + timedelta(weeks=77)` = 2025-06-23 (1-based); generates 90 rows with the 4 distribution changes from `data-fixtures.md §2.1`; writes `data/scenarios/week78_drift.json` + `data/drift_baseline.json`
- `data/scenarios/union_cap.json` — hand-authored static JSON (no generator needed); matches `data-fixtures.md §5` exactly
- `data/README.md` — enumerates all data/ files per `scaffold-contract.md §4`

## Out of scope

- FeatureStore ingest (that is shard 01's `fs_preload.py`)
- DriftMonitor wiring (shard 01's `drift_wiring.py`)
- scenario_inject.py (shard 06)

## Acceptance

- [ ] specs/schemas/demand.py defines FeatureSchema with exactly 9 features + target orders_next_day
- [ ] scripts/seed_experiments.py generates northwind_demand.csv ~2190 rows with RANDOM_SEED=42, distribution anchors within ±5% of spec means
- [ ] scripts/seed_experiments.py generates northwind_demand_holdout.csv (final 30 days)
- [ ] scripts/seed_experiments.py generates leaderboard_prebaked.json: 30 runs, Bayesian, 5 families (4 if no [xgb]), walk_forward EvalSpec, sorted by MAPE, best_by_family dict
- [ ] scripts/seed_drift.py generates week78_drift.json: 90 rows, window_start "2025-06-23", 4 distribution changes, DRIFT_SEED=78; no \_todo_student marker
- [ ] scripts/seed_drift.py generates drift_baseline.json: all 9 features with quantiles, target_summary, model_id placeholder
- [ ] data/scenarios/union_cap.json matches data-fixtures.md §5 exactly; no \_todo_student marker
- [ ] data/README.md enumerates all data/ files
- [ ] .env.example is NOT authored by this shard; shard 09 is sole writer; seed scripts read seeds from .env via python-dotenv
- [ ] tests/unit/test_data_fixtures_determinism.py passes (byte-identical output + week78 date check)
- [ ] tests/unit/test_demand_schema_columns.py passes (9 features + no ingest guard)
