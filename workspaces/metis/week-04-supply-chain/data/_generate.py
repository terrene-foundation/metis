"""
Deterministic fixture generator for Week 4 Northwind synthetic dataset.

Run once during scaffolding; fixtures are checked in. Students do NOT re-run
this script; it exists for reproducibility and audit.

Seeds (see data/README.md):
    RANDOM_SEED    = 42    # demand CSV + customers + depots + fleet
    AUTOML_SEED    = 2026  # pre-baked leaderboard
    DRIFT_SEED     = 78    # week-78 drift payload

This script is self-contained; it does NOT import kailash-ml or sklearn.
The leaderboard JSON is AUTHORED (plausible metric values per
data-fixtures.md §3.2), NOT trained.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# --- Seeds (canonical, documented in README) ----------------------------------
RANDOM_SEED = 42
AUTOML_SEED = 2026
DRIFT_SEED = 78

# --- Output paths -------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent

# --- Workshop business constants (canonical-values.md §6) --------------------
DEPOTS = [
    {
        "depot_id": "D01",
        "city": "Jurong",
        "lat": 1.3329,
        "lon": 103.7436,
        "mean_orders": 4500,
        "labour_cost_usd_per_hour": 22.50,
    },
    {
        "depot_id": "D02",
        "city": "Changi",
        "lat": 1.3644,
        "lon": 103.9915,
        "mean_orders": 4000,
        "labour_cost_usd_per_hour": 23.00,
    },
    {
        "depot_id": "D03",
        "city": "Woodlands",
        "lat": 1.4382,
        "lon": 103.7890,
        "mean_orders": 3500,
        "labour_cost_usd_per_hour": 21.75,
    },
]

N_CUSTOMERS = 500
N_VEHICLES = 20

# Cultural-mix labels (SG proxy segments). Pre-drift weights per data-fixtures.md §1.3
# re-mapped to cultural labels for the customer roster.
CULTURAL_MIX_PRE_DRIFT = {
    "Chinese": 0.55,  # retail-heavy segment (proxy)
    "Malay": 0.20,  # hospitality-heavy (proxy)
    "Indian": 0.15,  # industrial-heavy (proxy)
    "Other_SG": 0.10,  # mixed
}

VOLUME_TIERS = ["small", "medium", "large", "enterprise"]
VOLUME_WEIGHTS = [0.50, 0.30, 0.15, 0.05]

# --- Singapore public holidays 2024-2025 (static list; no external deps) -----
SG_HOLIDAYS_2024_2025 = {
    "2024-01-01",
    "2024-02-10",
    "2024-02-11",
    "2024-02-12",
    "2024-03-29",
    "2024-04-10",
    "2024-05-01",
    "2024-05-22",
    "2024-06-17",
    "2024-08-09",
    "2024-10-31",
    "2024-12-25",
    "2025-01-01",
    "2025-01-29",
    "2025-01-30",
    "2025-03-31",
    "2025-04-18",
    "2025-05-01",
    "2025-05-12",
    "2025-06-07",
    "2025-08-09",
    "2025-10-20",
    "2025-12-25",
}


def _seeded_rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


# =============================================================================
# 1. Depots CSV
# =============================================================================


def generate_depots_csv() -> pd.DataFrame:
    df = pd.DataFrame(DEPOTS)
    df.to_csv(DATA_DIR / "northwind_depots.csv", index=False)
    return df


# =============================================================================
# 2. Customers CSV
# =============================================================================


def generate_customers_csv() -> pd.DataFrame:
    rng = _seeded_rng(RANDOM_SEED)
    depot_ids = [d["depot_id"] for d in DEPOTS]
    # Assign roughly in proportion to depot mean_orders
    mean_orders = np.array([d["mean_orders"] for d in DEPOTS], dtype=float)
    depot_weights = mean_orders / mean_orders.sum()

    customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, N_CUSTOMERS + 1)]
    depots = rng.choice(depot_ids, size=N_CUSTOMERS, p=depot_weights)
    tiers = rng.choice(VOLUME_TIERS, size=N_CUSTOMERS, p=VOLUME_WEIGHTS)
    cultural_labels = list(CULTURAL_MIX_PRE_DRIFT.keys())
    cultural_weights = list(CULTURAL_MIX_PRE_DRIFT.values())
    cultural_mix = rng.choice(cultural_labels, size=N_CUSTOMERS, p=cultural_weights)

    # Approx monthly order volume by tier
    tier_volume = {"small": 8, "medium": 25, "large": 80, "enterprise": 250}
    monthly_orders = np.array([tier_volume[t] for t in tiers], dtype=int)
    # Perturb ±15% deterministically
    monthly_orders = (
        (monthly_orders * (1 + rng.uniform(-0.15, 0.15, N_CUSTOMERS))).round().astype(int)
    )

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "depot_id": depots,
            "volume_tier": tiers,
            "cultural_mix": cultural_mix,
            "monthly_order_volume": monthly_orders,
        }
    )
    df.to_csv(DATA_DIR / "northwind_customers.csv", index=False)
    return df


# =============================================================================
# 3. Fleet CSV
# =============================================================================


def generate_fleet_csv() -> pd.DataFrame:
    rng = _seeded_rng(RANDOM_SEED + 1)  # separate stream
    vehicle_ids = [f"V{str(i).zfill(3)}" for i in range(1, N_VEHICLES + 1)]
    depot_ids = [d["depot_id"] for d in DEPOTS]

    # Distribute fleet roughly proportional to depot volume
    mean_orders = np.array([d["mean_orders"] for d in DEPOTS], dtype=float)
    depot_weights = mean_orders / mean_orders.sum()
    home_depots = rng.choice(depot_ids, size=N_VEHICLES, p=depot_weights)

    # Capacity in units (not weight) — Northwind-scale
    capacities = rng.choice([180, 240, 320, 450], size=N_VEHICLES, p=[0.25, 0.35, 0.25, 0.15])
    # Base cost per day in USD (fixed lease + driver baseline, pre-overtime)
    base_costs = rng.uniform(180.0, 280.0, N_VEHICLES).round(2)

    df = pd.DataFrame(
        {
            "vehicle_id": vehicle_ids,
            "home_depot_id": home_depots,
            "capacity_units": capacities,
            "base_cost_usd_per_day": base_costs,
        }
    )
    df.to_csv(DATA_DIR / "northwind_fleet.csv", index=False)
    return df


# =============================================================================
# 4. Demand CSV (the core training dataset) — 13 columns per data-fixtures.md §1.2
# =============================================================================


def _customer_mix_hash(
    retail: float, hospitality: float, industrial: float, government: float = 0.0
) -> float:
    """Stable hash of the customer-mix distribution in [0, 1]."""
    # Deterministic: weighted combination; pre-drift has 3 modes, drift has 4.
    vec = np.array([retail, hospitality, industrial, government])
    vec = vec / max(vec.sum(), 1e-9)
    # Produce a number in [0,1]; uses a fixed basis so pre-drift lands ~0.45-0.60,
    # drift lands ~0.75-0.95 (separates the distributions for PSI/KS).
    basis = np.array([0.12, 0.34, 0.56, 0.91])
    return float(np.clip(np.dot(vec, basis), 0.0, 1.0))


def generate_demand_csv() -> pd.DataFrame:
    rng = _seeded_rng(RANDOM_SEED)
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    n_days = (end - start).days + 1
    dates = [start + timedelta(days=i) for i in range(n_days)]

    rows = []
    # Pre-compute per-depot order time-series for autoregressive features
    for depot in DEPOTS:
        mean_demand = depot["mean_orders"]
        orders_history: list[int] = []
        avg_order_value_history: list[float] = []
        active_customers_history: list[int] = []

        for i, day in enumerate(dates):
            # Trend: +5% across 2 years (gentle upward drift to make RF/GBM beat LR)
            trend_factor = 1.0 + 0.05 * (i / n_days)
            # Seasonality Q4 (Oct-Dec) +18%
            is_peak_season = day.month in (10, 11, 12)
            seasonal_factor = 1.18 if is_peak_season else 1.0
            # Weekly pattern (per §1.3): Sat +12%, Sun -15%, Mon -5%
            dow = day.weekday()  # Mon=0, Sun=6
            weekday_factors = {0: 0.95, 1: 1.00, 2: 1.00, 3: 1.00, 4: 1.00, 5: 1.12, 6: 0.85}
            weekday_factor = weekday_factors[dow]
            # Holiday dip -22%
            is_holiday = day.isoformat() in SG_HOLIDAYS_2024_2025
            holiday_factor = 0.78 if is_holiday else 1.0
            # Stochastic component ~N(1, 0.05)
            noise = rng.normal(1.0, 0.05)
            # Compute today's orders
            orders_today = (
                mean_demand
                * trend_factor
                * seasonal_factor
                * weekday_factor
                * holiday_factor
                * noise
            )
            orders_today_int = max(0, int(round(orders_today)))
            orders_history.append(orders_today_int)

            # avg_order_value ~ N(40.1, 5.2) pre-drift (matches drift_baseline summary)
            aov = rng.normal(40.1, 5.2)
            avg_order_value_history.append(float(aov))

            # active_customers: scale by depot mean, with noise
            ac_mean = 500 * (mean_demand / 4000.0)
            ac = int(max(50, rng.normal(ac_mean, ac_mean * 0.06)))
            active_customers_history.append(ac)

        # Second pass: compute derived features + target (orders_next_day)
        for i, day in enumerate(dates):
            orders_today = orders_history[i]
            orders_last = orders_history[i - 1] if i > 0 else orders_today
            window_7 = orders_history[max(0, i - 7) : i]
            window_28 = orders_history[max(0, i - 28) : i]
            roll_7 = float(np.mean(window_7)) if window_7 else float(orders_today)
            roll_28 = float(np.mean(window_28)) if window_28 else float(orders_today)

            # orders_next_day target: 1-day lookahead (for walk-forward CV)
            if i + 1 < n_days:
                target = orders_history[i + 1]
            else:
                target = orders_today  # last day: fall back to self

            # customer_mix_hash: stable pre-drift (retail 55 / hosp 30 / industrial 15)
            # with tiny jitter so it's not constant (needed for PSI baseline distribution)
            retail_w = 0.55 + rng.normal(0, 0.02)
            hosp_w = 0.30 + rng.normal(0, 0.02)
            ind_w = 0.15 + rng.normal(0, 0.02)
            mix_hash = _customer_mix_hash(retail_w, hosp_w, ind_w)

            # week_number: 1-based from 2024-01-01
            week_number = ((day - start).days // 7) + 1
            is_holiday = day.isoformat() in SG_HOLIDAYS_2024_2025
            is_peak_season = day.month in (10, 11, 12)

            rows.append(
                {
                    "date": day.isoformat(),
                    "depot_id": depot["depot_id"],
                    "week_number": week_number,
                    "orders_last_day": orders_last,
                    "orders_7d_rolling_avg": round(roll_7, 2),
                    "orders_28d_rolling_avg": round(roll_28, 2),
                    "day_of_week": day.weekday(),
                    "is_holiday": is_holiday,
                    "active_customers": active_customers_history[i],
                    "customer_mix_hash": round(mix_hash, 4),
                    "avg_order_value": round(avg_order_value_history[i], 2),
                    "is_peak_season": is_peak_season,
                    "orders_next_day": target,
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "northwind_demand.csv", index=False)
    return df


# =============================================================================
# 5. Week-78 drift payload (2025-06-23 + 30 days, 3 depots)
# =============================================================================


def generate_week78_drift_json() -> dict:
    rng = _seeded_rng(DRIFT_SEED)
    window_start = date(2024, 1, 1) + timedelta(weeks=77)  # 2025-06-23
    assert window_start.isoformat() == "2025-06-23", f"week78 date wrong: {window_start}"
    rows: list[dict] = []

    for offset in range(30):
        day = window_start + timedelta(days=offset)
        for depot in DEPOTS:
            mean_demand = depot["mean_orders"]
            # Drift: retail 35, hospitality 30, industrial 30, government 5
            retail_w = 0.35 + rng.normal(0, 0.02)
            hosp_w = 0.30 + rng.normal(0, 0.02)
            ind_w = 0.30 + rng.normal(0, 0.02)
            gov_w = 0.05 + rng.normal(0, 0.01)
            mix_hash = _customer_mix_hash(retail_w, hosp_w, ind_w, gov_w)

            # Day-of-week: Saturday lift drops 12%->4%
            dow = day.weekday()
            weekday_factors = {0: 0.95, 1: 1.00, 2: 1.00, 3: 1.00, 4: 1.00, 5: 1.04, 6: 0.85}
            wf = weekday_factors[dow]
            # Drift orders: slight industrial lift (no Q4, no holidays in Jun/Jul SG)
            noise = rng.normal(1.0, 0.05)
            orders_today = int(round(mean_demand * wf * noise))

            # avg_order_value +18% (industrial larger orders)
            aov_drift_mean = 40.1 * 1.18
            aov = float(rng.normal(aov_drift_mean, 5.2))

            # Rolling windows: start with pre-drift anchor
            roll_7 = mean_demand * 0.99 + rng.normal(0, 30)
            roll_28 = mean_demand * 0.98 + rng.normal(0, 25)
            orders_last = int(mean_demand * 1.0 + rng.normal(0, 40))
            ac = int(max(50, rng.normal(500 * (mean_demand / 4000.0), 20)))
            week_number = 78 + (offset // 7)
            # target: same-day fallback; next-day lookup if adjacent row exists
            target = int(round(orders_today * (1.0 + rng.normal(0, 0.04))))

            rows.append(
                {
                    "date": day.isoformat(),
                    "depot_id": depot["depot_id"],
                    "week_number": week_number,
                    "orders_last_day": orders_last,
                    "orders_7d_rolling_avg": round(float(roll_7), 2),
                    "orders_28d_rolling_avg": round(float(roll_28), 2),
                    "day_of_week": dow,
                    "is_holiday": False,
                    "active_customers": ac,
                    "customer_mix_hash": round(mix_hash, 4),
                    "avg_order_value": round(aov, 2),
                    "is_peak_season": False,
                    "orders_next_day": target,
                }
            )

    payload = {
        "scenario": "week78_drift",
        "window_start": window_start.isoformat(),
        "window_days": 30,
        "drift_description": {
            "customer_mix": "retail 55%->35%, hospitality stable 30%, industrial 15%->30%, new government 5%",
            "avg_order_value": "+18% shift (industrial larger orders)",
            "saturday_lift": "+12% -> +4% (flattened weekday pattern)",
            "customer_mix_hash_modes": "3 pre-drift -> 4 post-drift",
        },
        "rows": rows,
    }
    with open(DATA_DIR / "week78_drift.json", "w") as f:
        json.dump(payload, f, indent=2)
    return payload


# =============================================================================
# 6. Pre-baked AutoML leaderboard (30 trials, 5 families)
# =============================================================================


def _params_hash(params: dict) -> str:
    canonical = json.dumps(params, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:8]


def _alias(short_family: str, ordinal: int, dt: datetime) -> str:
    """canonical-values §12: {short_family}_{ordinal:03d}_{YYYYMMDD}_{HHMMSS}."""
    return f"{short_family}_{ordinal:03d}_{dt.strftime('%Y%m%d_%H%M%S')}"


def generate_leaderboard_json() -> dict:
    rng = _seeded_rng(AUTOML_SEED)
    # 5 families, fully-qualified (canonical-values §8.7).
    # Short-family aliases used in run_id + alias column only.
    families = [
        ("sklearn.linear_model.LinearRegression", "lr"),
        ("sklearn.linear_model.Ridge", "ridge"),
        ("sklearn.ensemble.RandomForestRegressor", "rf"),
        ("sklearn.ensemble.GradientBoostingRegressor", "gbm"),
        ("xgboost.XGBRegressor", "xgb"),
    ]

    # Authored plausible MAPE per family (best-case per family, worst-case runs
    # drawn from a uniform offset). Winner ~0.059, worst ~0.088. Live 5-trial
    # run (shard 01) produces ~0.074 for contrast.
    family_mape_band = {
        "sklearn.linear_model.LinearRegression": (0.078, 0.092),
        "sklearn.linear_model.Ridge": (0.072, 0.086),
        "sklearn.ensemble.RandomForestRegressor": (0.062, 0.081),
        "sklearn.ensemble.GradientBoostingRegressor": (0.060, 0.078),
        "xgboost.XGBRegressor": (0.059, 0.074),
    }

    base_time = datetime(2026, 4, 15, 22, 30, 0, tzinfo=timezone.utc)
    runs: list[dict] = []

    # Assign 30 trials across 5 families (6 trials each for balance)
    family_counts = {f[0]: 6 for f in families}
    ordinal_by_family: dict[str, int] = {f[1]: 0 for f in families}

    trial_order: list[tuple[str, str]] = []
    for fq, sf in families:
        for _ in range(family_counts[fq]):
            trial_order.append((fq, sf))
    # Shuffle deterministically so run_ids aren't grouped
    perm = rng.permutation(len(trial_order))
    trial_order = [trial_order[i] for i in perm]

    for i, (fq_name, short) in enumerate(trial_order):
        ordinal_by_family[short] += 1
        ord_n = ordinal_by_family[short]
        low, high = family_mape_band[fq_name]
        mape = float(rng.uniform(low, high))
        # rmse/mae scale with mape (loose proxies; walkforward CV on ~4000 mean orders)
        rmse = float(mape * 4000.0 * rng.uniform(0.15, 0.20))
        mae = float(rmse * rng.uniform(0.68, 0.74))
        fold_variance = float(rng.uniform(0.0015, 0.0045))

        # Plausible params per family
        if short == "lr":
            params = {"fit_intercept": True}
        elif short == "ridge":
            params = {"alpha": float(round(rng.uniform(0.1, 10.0), 3)), "fit_intercept": True}
        elif short == "rf":
            params = {
                "n_estimators": int(rng.choice([100, 200, 300])),
                "max_depth": int(rng.choice([6, 8, 10, 12])),
                "min_samples_split": int(rng.choice([2, 4, 8])),
                "random_state": AUTOML_SEED + i,
            }
        elif short == "gbm":
            params = {
                "n_estimators": int(rng.choice([120, 180, 240])),
                "max_depth": int(rng.choice([3, 4, 5])),
                "learning_rate": float(round(rng.uniform(0.03, 0.10), 3)),
                "random_state": AUTOML_SEED + i,
            }
        else:  # xgb
            params = {
                "n_estimators": int(rng.choice([180, 240, 300])),
                "max_depth": int(rng.choice([4, 6, 8])),
                "learning_rate": float(round(rng.uniform(0.03, 0.10), 3)),
                "subsample": float(round(rng.uniform(0.7, 1.0), 2)),
                "random_state": AUTOML_SEED + i,
            }
        ph = _params_hash(params)
        training_duration_s = float(round(rng.uniform(5.0, 25.0), 1))
        run_time = base_time + timedelta(seconds=int(rng.integers(0, 3600)))
        # UUID4 from 16 seeded bytes (numpy integers caps at int64; 128-bit needs byte construction)
        raw_bytes = rng.bytes(16)
        # Set version (4) and variant (RFC 4122) bits per UUID4 spec
        b = bytearray(raw_bytes)
        b[6] = (b[6] & 0x0F) | 0x40  # version 4
        b[8] = (b[8] & 0x3F) | 0x80  # variant RFC 4122
        run_uuid = str(uuid.UUID(bytes=bytes(b)))
        alias = _alias(short, ord_n, run_time)

        runs.append(
            {
                "run_id": run_uuid,
                "alias": alias,
                "model_class": fq_name,
                "params_hash": ph,
                "params": params,
                "metrics": {
                    "mape": round(mape, 4),
                    "rmse": round(rmse, 2),
                    "mae": round(mae, 2),
                    "fold_variance": round(fold_variance, 4),
                },
                "training_duration_s": training_duration_s,
                "tracker_run_id": run_uuid,
                "created_at": run_time.isoformat(),
            }
        )

    # Sort ascending by MAPE (winner at top)
    runs.sort(key=lambda r: r["metrics"]["mape"])

    # best_by_family (fully-qualified keys)
    best_by_family: dict[str, str] = {}
    for fq, _ in families:
        fam_runs = [r for r in runs if r["model_class"] == fq]
        if fam_runs:
            best_by_family[fq] = fam_runs[0]["alias"]

    leaderboard = {
        "generated_at": base_time.isoformat(),
        "kailash_ml_version": "pinned-by-preflight",
        "search_strategy": "bayesian",
        "n_trials": len(runs),
        "candidate_families": [f[0] for f in families],
        "eval_spec": {
            "split_strategy": "walk_forward",
            "n_splits": 6,
            "test_size": 0.2,
            "metric_optimised": "mape",
        },
        "runs": runs,
        "best_by_family": best_by_family,
    }
    with open(DATA_DIR / "leaderboard_prebaked.json", "w") as f:
        json.dump(leaderboard, f, indent=2)
    return leaderboard


# =============================================================================
# 7. Experiment aliases stub
# =============================================================================


def generate_experiment_aliases_stub() -> None:
    with open(DATA_DIR / ".experiment_aliases.json", "w") as f:
        json.dump({}, f)


# =============================================================================
# 8. PSI computation (verify drift signature)
# =============================================================================


def compute_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index between two 1-D distributions."""
    lo = float(min(reference.min(), current.min()))
    hi = float(max(reference.max(), current.max()))
    if hi <= lo:
        return 0.0
    edges = np.linspace(lo, hi, bins + 1)
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    # Laplace-smooth to avoid log(0)
    ref_p = (ref_counts + 1) / (ref_counts.sum() + bins)
    cur_p = (cur_counts + 1) / (cur_counts.sum() + bins)
    psi = float(np.sum((cur_p - ref_p) * np.log(cur_p / ref_p)))
    return psi


# =============================================================================
# MAIN
# =============================================================================


def main() -> dict:
    print("[1/7] Generating northwind_depots.csv ...")
    depots_df = generate_depots_csv()
    print(f"      -> {len(depots_df)} rows")

    print("[2/7] Generating northwind_customers.csv ...")
    customers_df = generate_customers_csv()
    print(f"      -> {len(customers_df)} rows")

    print("[3/7] Generating northwind_fleet.csv ...")
    fleet_df = generate_fleet_csv()
    print(f"      -> {len(fleet_df)} rows")

    print("[4/7] Generating northwind_demand.csv (2 years, 3 depots) ...")
    demand_df = generate_demand_csv()
    print(f"      -> {len(demand_df)} rows")

    print("[5/7] Generating week78_drift.json ...")
    drift_payload = generate_week78_drift_json()
    print(
        f"      -> {len(drift_payload['rows'])} rows, window_start={drift_payload['window_start']}"
    )

    print("[6/7] Generating leaderboard_prebaked.json ...")
    lb = generate_leaderboard_json()
    print(f"      -> {len(lb['runs'])} runs, winner MAPE={lb['runs'][0]['metrics']['mape']}")

    print("[7/7] Generating .experiment_aliases.json stub ...")
    generate_experiment_aliases_stub()

    # ---- Compute PSI on customer_mix_hash for README ----
    ref = demand_df["customer_mix_hash"].to_numpy()
    drift_rows = drift_payload["rows"]
    cur = np.array([r["customer_mix_hash"] for r in drift_rows])
    psi = compute_psi(ref, cur)
    print(f"\nPSI(customer_mix_hash | reference vs week78 drift) = {psi:.4f}")

    # Summary
    summary = {
        "depots_rows": len(depots_df),
        "customers_rows": len(customers_df),
        "fleet_rows": len(fleet_df),
        "demand_rows": len(demand_df),
        "drift_rows": len(drift_payload["rows"]),
        "leaderboard_trials": len(lb["runs"]),
        "leaderboard_families": sorted(set(r["model_class"] for r in lb["runs"])),
        "winner_alias": lb["runs"][0]["alias"],
        "winner_model_class": lb["runs"][0]["model_class"],
        "winner_mape": lb["runs"][0]["metrics"]["mape"],
        "psi_customer_mix_hash": round(psi, 4),
    }
    print("\nSummary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    return summary


if __name__ == "__main__":
    main()
