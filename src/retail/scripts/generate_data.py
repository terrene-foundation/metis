# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
# https://creativecommons.org/licenses/by/4.0/
"""Generate the Arcadia Retail customer / product / transaction dataset.

Design goals (per value-auditor stress test — see START_HERE.md §8 "weakest link"):

1. **Ambiguous K.** Silhouette across K=2..10 has no dominant peak. K=3, 5, 7 are all
   locally plausible. The student's Trust-Plane decision on K must be defended in
   business terms, not statistics — which is the point of Phase 6.
2. **Proxy-leakage vectors.** `postal_district` secretly correlates with `income_tier`
   (proxy for a protected class in PDPA terms). `weekend_browse_fraction` secretly
   correlates with `age_band`. Phase 2 data audit and Phase 7 red-team must catch this.
3. **Cold-start subset.** ~15 % of customers are "new" (less than 3 transactions,
   joined in the last 30 days of the 24-month window). The recommender decision in
   Sprint 2 hinges on how these customers are handled.
4. **Seven latent segments, five of which merge into three at low K.** The student
   who accepts K=3 silently buries two actionable segments inside a generic "casual
   shopper" blob — a lesson that silhouette alone cannot teach.

Output (written to `data/`):

- `arcadia_customers.csv`       — 5 000 customer rows, 14 features
- `arcadia_products.csv`        —   400 SKU rows, 9 features
- `arcadia_transactions.csv`    — 120 000 transaction rows, 6 features
- `segment_baseline.json`       — baseline K=3 K-Means result (silhouette, labels)
- `segment_candidates.json`     — pre-baked K-sweep 2..10 for comparison against live runs
- `drift_baseline.json`         — DriftMonitor reference distribution for the training window
- `scenarios/pdpa_redline.json` — Sprint 2 injection: "legal just blocked under-18 browse data"
- `scenarios/catalog_drift.json` — Sprint 3 injection: 30-day window with shifted product mix
- `README.md`                   — enumerates every file + which endpoint / phase consumes it

Determinism: every random call routes through `rng = np.random.default_rng(SEED)`.
Re-running this script is idempotent given the same seed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SEED = 2026_04_23
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SCEN_DIR = DATA_DIR / "scenarios"

N_CUSTOMERS = 5_000
N_PRODUCTS = 400
N_TRANSACTIONS = 120_000
HORIZON_DAYS = 24 * 30  # 24 months

# -- Latent segments (ground truth — NEVER exposed to the student) ------------
# Seven latent archetypes. At K=3, segments 1+2+6 merge into "casual" and the
# signal collapses. At K=5 or K=7, real differentiation emerges.
SEGMENTS = [
    # name,                    size_frac, avg_basket, visit_freq_wk, weekend_skew, luxury_affinity, new_customer
    ("weekend_browser_bargain", 0.18, 35.0, 0.8, 0.78, 0.10, False),
    ("weekday_luxury_regular", 0.10, 180.0, 2.5, 0.15, 0.85, False),
    ("family_bulk_weekly", 0.22, 95.0, 1.2, 0.55, 0.30, False),
    ("new_digital_native", 0.15, 45.0, 0.6, 0.45, 0.40, True),
    ("lapsed_reactivatable", 0.12, 60.0, 0.15, 0.50, 0.35, False),
    ("corporate_gifter_seasonal", 0.08, 250.0, 0.25, 0.35, 0.70, False),
    ("casual_long_tail", 0.15, 50.0, 0.6, 0.50, 0.40, False),
]
assert abs(sum(s[1] for s in SEGMENTS) - 1.0) < 1e-6

# Postal-to-income proxy (PDPA RED FLAG — student must catch this in Phase 2/7)
POSTAL_INCOME_MAP = {
    "01": "high",
    "02": "high",
    "03": "high",  # Orchard / Tanglin / Newton
    "10": "high",
    "11": "high",  # Bukit Timah
    "15": "mid",
    "16": "mid",
    "17": "mid",
    "23": "mid",
    "24": "mid",
    "52": "low",
    "53": "low",
    "54": "low",  # Woodlands
    "76": "low",
    "77": "low",
    "78": "low",  # Sengkang / Punggol
}
POSTAL_DISTRICTS = list(POSTAL_INCOME_MAP.keys())


@dataclass
class Customer:
    customer_id: str
    signup_date: str
    age_band: str
    postal_district: str
    income_tier: str  # NOT exposed to clustering; evaluation-only
    latent_segment: str  # NOT exposed to clustering; evaluation-only
    total_spend_24mo: float
    avg_basket_size: float
    visits_per_week: float
    weekend_browse_fraction: float
    luxury_category_fraction: float
    distinct_categories: int
    days_since_last_visit: int
    marketing_email_open_rate: float


@dataclass
class Product:
    sku: str
    category: str
    subcategory: str
    price: float
    luxury_flag: bool
    stock_level: int
    avg_rating: float
    n_reviews: int
    seasonal: bool


def _choose_segment(rng: np.random.Generator) -> tuple[int, tuple]:
    probs = np.array([s[1] for s in SEGMENTS])
    idx = int(rng.choice(len(SEGMENTS), p=probs))
    return idx, SEGMENTS[idx]


def _gen_customers(rng: np.random.Generator) -> list[Customer]:
    today = datetime(2026, 4, 23)
    rows: list[Customer] = []
    for i in range(N_CUSTOMERS):
        _, (seg_name, _, avg_basket, visit_freq, weekend_skew, luxury_aff, is_new) = (
            _choose_segment(rng)
        )

        # Postal district is chosen to correlate with BOTH segment and income.
        # Luxury segments skew to high-income districts; bargain segments skew low.
        if luxury_aff > 0.6:
            district = rng.choice(POSTAL_DISTRICTS[:5])  # high-income
        elif luxury_aff < 0.2:
            district = rng.choice(POSTAL_DISTRICTS[-6:])  # low-income
        else:
            district = rng.choice(POSTAL_DISTRICTS)
        income = POSTAL_INCOME_MAP[str(district)]

        # Age band correlates with weekend-browse fraction (proxy leakage #2).
        if weekend_skew > 0.7:
            age_band = rng.choice(["18-24", "25-34"], p=[0.6, 0.4])
        elif weekend_skew < 0.2:
            age_band = rng.choice(["35-44", "45-54", "55+"], p=[0.3, 0.4, 0.3])
        else:
            age_band = rng.choice(
                ["18-24", "25-34", "35-44", "45-54", "55+"],
                p=[0.15, 0.25, 0.25, 0.2, 0.15],
            )

        if is_new:
            signup_offset = int(rng.integers(0, 30))
            visits = max(1, int(rng.integers(1, 3)))  # fewer than 3 txns
        else:
            signup_offset = int(rng.integers(30, HORIZON_DAYS))
            visits = max(1, int(rng.poisson(visit_freq * (signup_offset / 7.0))))
        signup_date = today - timedelta(days=signup_offset)

        basket = max(5.0, rng.normal(avg_basket, avg_basket * 0.25))
        total_spend = basket * visits * (1.0 + 0.1 * rng.standard_normal())
        weekend_frac = float(np.clip(weekend_skew + rng.normal(0, 0.08), 0.0, 1.0))
        luxury_frac = float(np.clip(luxury_aff + rng.normal(0, 0.10), 0.0, 1.0))
        distinct_cats = int(np.clip(rng.poisson(3 + luxury_aff * 4), 1, 12))
        days_since_last = int(
            rng.integers(0, 7) if not is_new else rng.integers(0, 30),
        )
        if seg_name == "lapsed_reactivatable":
            days_since_last = int(rng.integers(60, 180))
        email_open = float(np.clip(rng.beta(2 + luxury_aff * 3, 3), 0.0, 1.0))

        rows.append(
            Customer(
                customer_id=f"C{i:05d}",
                signup_date=signup_date.strftime("%Y-%m-%d"),
                age_band=age_band,
                postal_district=str(district),
                income_tier=income,
                latent_segment=seg_name,
                total_spend_24mo=round(total_spend, 2),
                avg_basket_size=round(basket, 2),
                visits_per_week=round(visits / max(signup_offset / 7.0, 1.0), 3),
                weekend_browse_fraction=round(weekend_frac, 3),
                luxury_category_fraction=round(luxury_frac, 3),
                distinct_categories=distinct_cats,
                days_since_last_visit=days_since_last,
                marketing_email_open_rate=round(email_open, 3),
            )
        )
    return rows


def _gen_products(rng: np.random.Generator) -> list[Product]:
    categories = [
        ("Apparel", ["Casual", "Formal", "Sport", "Seasonal"]),
        ("Home", ["Kitchen", "Bath", "Decor"]),
        ("Beauty", ["Skincare", "Cosmetics", "Fragrance"]),
        ("Electronics", ["Audio", "Mobile", "Wearables"]),
        ("Grocery", ["Pantry", "Fresh", "Frozen"]),
    ]
    rows: list[Product] = []
    for i in range(N_PRODUCTS):
        cat, subs = categories[i % len(categories)]
        sub = str(rng.choice(subs))
        luxury = bool(rng.random() < 0.18)
        base_price = rng.lognormal(4.5, 0.8) if luxury else rng.lognormal(3.0, 0.7)
        price = float(np.clip(base_price, 5.0, 2000.0))
        stock = int(rng.integers(0, 500))
        # New products: 10% have <5 reviews (recommender cold-start surface)
        is_new_sku = bool(rng.random() < 0.10)
        n_reviews = int(rng.integers(0, 5)) if is_new_sku else int(rng.integers(10, 2000))
        avg_rating = (
            float(rng.uniform(3.8, 4.8)) if n_reviews > 10 else float(rng.uniform(3.0, 5.0))
        )
        seasonal = sub in {"Seasonal", "Fresh"}
        rows.append(
            Product(
                sku=f"SKU{i:04d}",
                category=cat,
                subcategory=sub,
                price=round(price, 2),
                luxury_flag=luxury,
                stock_level=stock,
                avg_rating=round(avg_rating, 2),
                n_reviews=n_reviews,
                seasonal=seasonal,
            )
        )
    return rows


def _gen_transactions(
    rng: np.random.Generator, customers: list[Customer], products: list[Product]
) -> pl.DataFrame:
    today = datetime(2026, 4, 23)
    rows: list[dict] = []
    sku_price = {p.sku: p.price for p in products}
    luxury_skus = [p.sku for p in products if p.luxury_flag]
    mass_skus = [p.sku for p in products if not p.luxury_flag]
    for c in customers:
        signup_dt = datetime.strptime(c.signup_date, "%Y-%m-%d")
        days_active = (today - signup_dt).days
        if days_active <= 0:
            continue
        n_txn = max(1, int(c.visits_per_week * (days_active / 7.0)))
        n_txn = min(n_txn, 50)  # cap per customer
        for _ in range(n_txn):
            offset = int(rng.integers(0, days_active))
            txn_dt = signup_dt + timedelta(days=offset)
            pool = luxury_skus if rng.random() < c.luxury_category_fraction else mass_skus
            sku = str(rng.choice(pool))
            qty = int(rng.integers(1, 4))
            rows.append(
                {
                    "txn_id": f"T{len(rows):07d}",
                    "customer_id": c.customer_id,
                    "sku": sku,
                    "txn_date": txn_dt.strftime("%Y-%m-%d"),
                    "qty": qty,
                    "amount": round(sku_price[sku] * qty, 2),
                }
            )
            if len(rows) >= N_TRANSACTIONS:
                break
        if len(rows) >= N_TRANSACTIONS:
            break
    return pl.DataFrame(rows)


def _run_k_sweep(customers_df: pl.DataFrame) -> dict:
    """Baseline K-sweep across K=2..10. Cached as `segment_candidates.json`.

    Uses the six numeric behavioural columns the student will see. The latent
    segment label is NEVER used — this mirrors what the student's Phase 4 call
    produces. Purpose: students compare their live run against this reference.
    """
    feature_cols = [
        "total_spend_24mo",
        "avg_basket_size",
        "visits_per_week",
        "weekend_browse_fraction",
        "luxury_category_fraction",
        "distinct_categories",
        "days_since_last_visit",
        "marketing_email_open_rate",
    ]
    X = customers_df.select(feature_cols).to_numpy()
    X_std = StandardScaler().fit_transform(X)
    sweep = []
    for k in range(2, 11):
        km = KMeans(n_clusters=k, n_init="auto", random_state=SEED)
        labels = km.fit_predict(X_std)
        sil = float(silhouette_score(X_std, labels)) if k > 1 else None  # type: ignore[arg-type]
        sweep.append(
            {
                "k": k,
                "silhouette": sil,
                "inertia": float(km.inertia_),
                "segment_sizes": np.bincount(labels).tolist(),
            }
        )
    return {
        "algorithm": "kmeans",
        "features": feature_cols,
        "sweep": sweep,
        "seed": SEED,
        "note": "Reference k-sweep — compare against live runs in Phase 4.",
    }


def _baseline_k3(customers_df: pl.DataFrame) -> dict:
    feature_cols = [
        "total_spend_24mo",
        "avg_basket_size",
        "visits_per_week",
        "weekend_browse_fraction",
        "luxury_category_fraction",
        "distinct_categories",
        "days_since_last_visit",
        "marketing_email_open_rate",
    ]
    X = customers_df.select(feature_cols).to_numpy()
    X_std = StandardScaler().fit_transform(X)
    km = KMeans(n_clusters=3, n_init="auto", random_state=SEED)
    labels = km.fit_predict(X_std)
    sil = float(silhouette_score(X_std, labels))
    return {
        "model_name": "customer_segmentation",
        "version": "baseline-v1",
        "algorithm": "kmeans",
        "k": 3,
        "features": feature_cols,
        "silhouette_score": sil,
        "inertia": float(km.inertia_),
        "segment_sizes": np.bincount(labels).tolist(),
        "centroids": km.cluster_centers_.tolist(),
        "seed": SEED,
        "note": (
            "The pre-built baseline. Students CRITIQUE this in Sprint 1; their "
            "Phase 4-8 decisions either confirm K=3 or promote a better K."
        ),
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SCEN_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    print(f"[generate_data] seed={SEED}")

    customers = _gen_customers(rng)
    customers_df = pl.DataFrame([c.__dict__ for c in customers])
    customers_df.write_csv(DATA_DIR / "arcadia_customers.csv")
    print(f"[generate_data] customers: {len(customers_df):,} rows → arcadia_customers.csv")

    products = _gen_products(rng)
    products_df = pl.DataFrame([p.__dict__ for p in products])
    products_df.write_csv(DATA_DIR / "arcadia_products.csv")
    print(f"[generate_data] products:  {len(products_df):,} rows → arcadia_products.csv")

    txns_df = _gen_transactions(rng, customers, products)
    txns_df.write_csv(DATA_DIR / "arcadia_transactions.csv")
    print(f"[generate_data] txns:      {len(txns_df):,} rows → arcadia_transactions.csv")

    sweep = _run_k_sweep(customers_df)
    (DATA_DIR / "segment_candidates.json").write_text(json.dumps(sweep, indent=2))
    print("[generate_data] k-sweep K=2..10 → segment_candidates.json")
    print("[generate_data]   silhouettes:", [round(s["silhouette"], 3) for s in sweep["sweep"]])

    baseline = _baseline_k3(customers_df)
    (DATA_DIR / "segment_baseline.json").write_text(json.dumps(baseline, indent=2))
    print(
        f"[generate_data] baseline K=3 silhouette={baseline['silhouette_score']:.3f} → segment_baseline.json"
    )

    # Sprint 2 injection — PDPA red-line on under-18 browse data
    (SCEN_DIR / "pdpa_redline.json").write_text(
        json.dumps(
            {
                "scenario_id": "pdpa_redline",
                "sprint": 2,
                "phase": 11,
                "event": (
                    "Legal has flagged that using under-18 browsing history for "
                    "personalization violates PDPA §13. The weekend_browse_fraction "
                    "feature, when joined with age_band=18-24, effectively infers "
                    "under-18 behaviour. Re-classify: is this a hard constraint?"
                ),
                "expected_trust_plane_response": (
                    "Hard constraint (law). Drop weekend_browse_fraction for under-21 "
                    "age bands OR drop age_band as a feature. Document in journal."
                ),
            },
            indent=2,
        )
    )

    # Sprint 3 injection — catalog drift (new product line shifts category mix)
    (SCEN_DIR / "catalog_drift.json").write_text(
        json.dumps(
            {
                "scenario_id": "catalog_drift",
                "sprint": 3,
                "phase": 13,
                "event": (
                    "Arcadia launched a new 'wellness' category 30 days ago. It now "
                    "accounts for 12 % of transactions. The customer_segmentation "
                    "model was trained before the launch. Check drift."
                ),
                "expected_trust_plane_response": (
                    "Expect segment-membership churn >20 % for customers who adopted "
                    "wellness. Decision: retrain cadence, or hold and monitor?"
                ),
            },
            indent=2,
        )
    )

    # Drift baseline — reference distribution over the six clustering features
    feat_summary = {
        c: {
            "mean": float(customers_df[c].mean()),
            "std": float(customers_df[c].std()),
            "min": float(customers_df[c].min()),
            "max": float(customers_df[c].max()),
            "p50": float(customers_df[c].median()),
        }
        for c in (
            "total_spend_24mo",
            "avg_basket_size",
            "visits_per_week",
            "weekend_browse_fraction",
            "luxury_category_fraction",
            "distinct_categories",
            "days_since_last_visit",
            "marketing_email_open_rate",
        )
    }
    (DATA_DIR / "drift_baseline.json").write_text(
        json.dumps(
            {
                "model_name": "customer_segmentation",
                "window": "signup_offset >= 30 (established customers, pre-wellness-launch)",
                "n_customers": len(customers_df),
                "features": feat_summary,
            },
            indent=2,
        )
    )

    readme = f"""# Arcadia Retail — Data Files

Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by `scripts/generate_data.py` (seed {SEED}).

| File | Role | Consumed by |
| --- | --- | --- |
| `arcadia_customers.csv` | {N_CUSTOMERS:,} customers × 14 features | `/segment/*`, `/recommend/*`, `fs_preload` |
| `arcadia_products.csv`  | {N_PRODUCTS:,} SKUs × 9 features | `/recommend/*` |
| `arcadia_transactions.csv` | {len(txns_df):,} txns × 6 features | `/recommend/*`, drift windows |
| `segment_baseline.json` | pre-built K=3 baseline; students critique it | Phase 4 / Phase 5 |
| `segment_candidates.json` | pre-baked k-sweep 2..10 | Phase 4 comparison against live runs |
| `drift_baseline.json` | reference distribution for `DriftMonitor` | Phase 13 |
| `scenarios/pdpa_redline.json` | Sprint 2 injection (Phase 11 re-classification) | scenario_inject.py |
| `scenarios/catalog_drift.json` | Sprint 3 injection (Phase 13 drift) | scenario_inject.py |

**Ground truth the student must NEVER see:**

- `latent_segment` column (7 archetypes) — grader-only.
- `income_tier` column — PDPA proxy leakage surface (Phase 2 / Phase 7 red flag).
- The K-sweep has no dominant silhouette peak: student must defend K in business terms.
"""
    (DATA_DIR / "README.md").write_text(readme)
    print("[generate_data] drift baseline + scenarios + README written")
    print("[generate_data] DONE.")


if __name__ == "__main__":
    main()
