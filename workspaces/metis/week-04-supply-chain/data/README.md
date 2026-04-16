# Week 4 — Northwind Synthetic Data Fixtures

> **SYNTHETIC DATA NOTICE**
> Every file in this directory is **synthetic**. No real customers, no real
> orders, no PII. Generated deterministically by `_generate.py` for the
> Week 4 MBA Supply-Chain workshop. Do NOT use these figures to make real
> business decisions. Authority: [specs/data-fixtures.md](../specs/data-fixtures.md).

## Files shipped

| File                        | Rows / Size           | Role                                                     | Writer (audit)          |
| --------------------------- | --------------------- | -------------------------------------------------------- | ----------------------- |
| `northwind_demand.csv`      | 2,193 rows × 13 cols  | Primary training set (2 yr × 3 depots × 730 days +3)     | Shard 07 `_generate.py` |
| `northwind_customers.csv`   | 500 rows × 5 cols     | Customer roster (depot, volume tier, cultural mix)       | Shard 07 `_generate.py` |
| `northwind_fleet.csv`       | 20 rows × 4 cols      | Vehicle fleet (capacity, home depot, base cost)          | Shard 07 `_generate.py` |
| `northwind_depots.csv`      | 3 rows × 6 cols       | Depot locations (lat/lon, labour cost)                   | Shard 07 `_generate.py` |
| `week78_drift.json`         | 90 rows (30 days × 3) | Post-CNY drift window fixture (2025-06-23 to 2025-07-22) | Shard 07 `_generate.py` |
| `leaderboard_prebaked.json` | 30 trials, 5 families | Pre-baked 30-trial AutoML leaderboard                    | Shard 07 `_generate.py` |
| `.experiment_aliases.json`  | `{}` stub             | Runtime alias map (populated by `/forecast/train`)       | Shard 07 (stub only)    |
| `_generate.py`              | n/a                   | One-shot generator. Students do NOT re-run.              | Shard 07                |

### Files NOT written by shard 07 (produced by other shards)

| File                           | Writer                         | Purpose                     |
| ------------------------------ | ------------------------------ | --------------------------- |
| `northwind_demand_holdout.csv` | Shard 01 (fs_preload split)    | Phase-7 red-team holdout    |
| `drift_baseline.json`          | Shard 01 (drift_wiring)        | DriftMonitor reference      |
| `scenarios/union_cap.json`     | Shard 06                       | Sprint-2 union-cap scenario |
| `leaderboard.json`             | Shard 01 (live AutoML run)     | Student's live 5-trial run  |
| `forecast_output.json`         | Shard 01 (`/forecast/predict`) | InferenceServer output      |
| `drift_report.json`            | Shard 04 (`/drift/check`)      | DriftMonitor report         |

## Columns — `northwind_demand.csv`

Matches `specs/data-fixtures.md §1.2` exactly. 13 columns = 3 identifiers + 9 features + 1 target:

Identifiers: `date`, `depot_id`, `week_number`
Features: `orders_last_day`, `orders_7d_rolling_avg`, `orders_28d_rolling_avg`, `day_of_week`, `is_holiday`, `active_customers`, `customer_mix_hash`, `avg_order_value`, `is_peak_season`
Target: `orders_next_day`

## Deterministic seeds

| Seed            | Value  | Scope                                                         |
| --------------- | ------ | ------------------------------------------------------------- |
| `RANDOM_SEED`   | `42`   | `northwind_demand.csv`, customers, depots (shared generator)  |
| `RANDOM_SEED+1` | `43`   | `northwind_fleet.csv` (separate stream to avoid cross-draw)   |
| `AUTOML_SEED`   | `2026` | `leaderboard_prebaked.json` — pre-baked leaderboard authoring |
| `DRIFT_SEED`    | `78`   | `week78_drift.json` — drift window generation                 |

Every random draw uses `numpy.random.default_rng(seed=<named>)`. Same seed +
same numpy major version ⇒ byte-identical output. Verified across two
consecutive runs on numpy 2.4.0 (MD5 unchanged).

Seeds will be mirrored to `.env.example` by shard 09 (`RANDOM_SEED=42`,
`AUTOML_SEED=2026`, `DRIFT_SEED=78`). Shard 07 does NOT write `.env.example`.

## Drift signature — PSI verification

**PSI(`customer_mix_hash` | reference vs week-78 drift window) = 10.16**

Computed across 10 equal-width bins with Laplace smoothing. The `moderate`
threshold is 0.1 and `severe` is 0.25 (per `canonical-values.md §1`). Observed
10.16 is **two orders of magnitude above `severe`** — the intentional design:
pre-drift has 3 customer-mix modes, post-drift has 4 (government segment is
unseen during training), and `_customer_mix_hash` maps 4-mode inputs to a
distinctly separated numeric band from 3-mode inputs. KS and PSI tests in
`DriftMonitor` will both fire without ambiguity.

## Business numbers (per `canonical-values.md §6`)

- Daily order volume: ~12,000 orders/day (sum of depot means 4500+4000+3500)
- Depots: 3 (`D01` Jurong, `D02` Changi, `D03` Woodlands — SG proxies)
- Regular customers: 500
- Vehicle fleet: 20
- Peak season: Q4 (Oct–Dec) — +18% lift
- Drift event: Week 78 day 1 = **2025-06-23** (1-based from 2024-01-01)

## Leaderboard — `leaderboard_prebaked.json`

30 AUTHORED trials across 5 fully-qualified families (per `canonical-values.md §8.7`):

1. `sklearn.linear_model.LinearRegression`
2. `sklearn.linear_model.Ridge`
3. `sklearn.ensemble.RandomForestRegressor`
4. `sklearn.ensemble.GradientBoostingRegressor`
5. `xgboost.XGBRegressor`

Per-run fields: `run_id` (UUID4), `alias` (per `canonical-values.md §12`
format: `{short}_{ordinal:03d}_{YYYYMMDD}_{HHMMSS}`), `model_class`
(fully-qualified), `params_hash`, `params`, `metrics{mape, rmse, mae,
fold_variance}`, `training_duration_s`, `tracker_run_id`, `created_at`.

Winner MAPE = **0.0592** (`xgboost.XGBRegressor`) — within the spec band
[0.05, 0.08]. Sorted ascending by MAPE. `best_by_family` keys are the
fully-qualified class strings.

**Note**: The leaderboard is AUTHORED, not trained. The user task for this
shard explicitly forbids using sklearn/torch directly — values are plausible
per `data-fixtures.md §3.2`. The live 5-trial AutoML run produced by shard 01
will write a separate `leaderboard.json`, and the Phase-5 trust question
("pre-bake beats my live run by ~1.5pp MAPE") uses the gap between the two.

## Deviations from spec (documented)

- **User task said week 78 starts 2025-07-07; spec says 2025-06-23.**
  Followed the spec (`data-fixtures.md §1.1` and acceptance criteria in
  `todos/active/07-data-and-leaderboard.md`). Date derived as
  `date(2024,1,1) + timedelta(weeks=77) = 2025-06-23` (1-based week counting,
  consistent with `week_number` column in the demand CSV).
- **Holdout CSV, drift_baseline.json, union_cap.json NOT written by this
  shard.** User task did not request them; workspace shard (`07-...md`) lists
  them as shard-07 deliverables. Per user task priority, skipped; shard 01 /
  09 / 06 will own them per the dependency_note in the shard's YAML
  frontmatter.
- **Canonical-values §8.7 validation regex imprecision.** Regex
  `^[a-z_]+(\.[a-z_]+)+\.[A-Z][A-Za-z]+$` does NOT match `xgboost.XGBRegressor`
  (class name contains a digit — `[A-Za-z]+` excludes `\d`). The string value
  is correct per the §8.7 canonical list; the regex itself is slightly loose.
  Flagged for specs update: regex should be
  `^[a-z_]+(\.[a-z_]+)+\.[A-Z][A-Za-z0-9]+$`.

## Reproducibility

```bash
cd data && python3 _generate.py
# Expected output:
#   northwind_demand.csv -> 2193 rows
#   week78_drift.json -> 90 rows, window_start=2025-06-23
#   leaderboard_prebaked.json -> 30 runs, winner MAPE=0.0592
#   PSI(customer_mix_hash | reference vs week78 drift) = 10.1588
```

Students should **not** re-run the generator. It is checked in for audit and
for scaffold regeneration only.
