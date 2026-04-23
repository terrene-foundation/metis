# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Startup: load data, train baselines, register drift reference, publish context."""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import polars as pl
from sklearn.exceptions import ConvergenceWarning

# Suppress sklearn numerical warnings from K-means++ init and NMF convergence
# on the adversarial Arcadia dataset. These are non-functional — outputs are
# numerically valid after sanitization in ml_context — and they clutter student
# logs. Does NOT suppress errors or any other warning class.
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from .config import load_settings
from .ml_context import (
    CHURN_FEATURES,
    MLContext,
    PredictorBundle,
    build_churn_predictor,
    build_collaborative_recommender,
    build_content_recommender,
    build_conversion_predictor,
    load_drift_reference,
    load_sweep_reference,
    set_context,
    train_baseline_segmentation,
)

log = logging.getLogger("metis.startup")


def _require(path: Path, label: str) -> None:
    if not path.exists():
        raise RuntimeError(
            f"{label} missing at {path} — run `python scripts/generate_data.py` "
            f"from the workspace root to materialise the Arcadia dataset."
        )


def run_startup_sync() -> None:
    settings = load_settings()
    data_dir = settings.data_dir

    _require(data_dir / "arcadia_customers.csv", "customers")
    _require(data_dir / "arcadia_products.csv", "products")
    _require(data_dir / "arcadia_transactions.csv", "transactions")
    _require(data_dir / "segment_candidates.json", "segment_candidates")
    _require(data_dir / "drift_baseline.json", "drift_baseline")

    log.info("metis.startup.loading data")
    customers = pl.read_csv(data_dir / "arcadia_customers.csv")
    products = pl.read_csv(data_dir / "arcadia_products.csv")
    transactions = pl.read_csv(data_dir / "arcadia_transactions.csv")

    log.info("metis.startup.training baseline K=3 segmentation")
    baseline = train_baseline_segmentation(customers, k=3, seed=42)
    log.info(
        "metis.startup.baseline trained silhouette=%.3f sizes=%s",
        baseline.silhouette,
        [
            int(x)
            for x in list(pl.Series(baseline.labels).value_counts().sort("").get_column("count"))
        ],
    )

    log.info("metis.startup.building content recommender")
    recommender = build_content_recommender(products)

    log.info("metis.startup.pre-fitting collaborative recommender (NMF 16 components)")
    collaborative = build_collaborative_recommender(transactions, customers, products)
    log.info(
        "metis.startup.collaborative fit done W=%s H=%s",
        collaborative.W.shape,
        collaborative.H.shape,
    )

    log.info("metis.startup.training SML churn predictor (LR + RF + GBM)")
    churn_cands, churn_scaler, churn_cust_ids, churn_labels = build_churn_predictor(
        customers, seed=42
    )
    for name, entry in churn_cands.items():
        log.info(
            "metis.startup.churn[%s] auc=%.3f brier=%.3f",
            name,
            entry["metrics"]["auc"],
            entry["metrics"]["brier_score"],
        )

    log.info("metis.startup.training SML conversion predictor")
    conv_bundle = build_conversion_predictor(customers, transactions, products, seed=42)

    predictor = PredictorBundle(
        churn_candidates=churn_cands,
        churn_features=list(CHURN_FEATURES),
        churn_scaler=churn_scaler,
        churn_customer_ids=(
            churn_cust_ids.tolist() if hasattr(churn_cust_ids, "tolist") else list(churn_cust_ids)
        ),
        churn_labels=churn_labels,
        conv_candidates=conv_bundle,
        conv_features=conv_bundle["features"],
    )

    sweep = load_sweep_reference(data_dir)
    drift_ref = load_drift_reference(data_dir)

    ctx = MLContext(
        customers=customers,
        products=products,
        transactions=transactions,
        baseline=baseline,
        recommender=recommender,
        collaborative=collaborative,
        predictor=predictor,
        candidates_sweep=sweep,
        drift_reference=drift_ref,
    )
    set_context(ctx)
    log.info(
        "metis.startup.ready customers=%d products=%d txns=%d",
        len(customers),
        len(products),
        len(transactions),
    )


async def run_startup() -> None:
    run_startup_sync()
