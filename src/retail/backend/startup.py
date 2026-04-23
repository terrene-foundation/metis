# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Startup: load data, train baselines, register drift reference, publish context."""

from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

from .config import load_settings
from .ml_context import (
    MLContext,
    build_content_recommender,
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

    sweep = load_sweep_reference(data_dir)
    drift_ref = load_drift_reference(data_dir)

    ctx = MLContext(
        customers=customers,
        products=products,
        transactions=transactions,
        baseline=baseline,
        recommender=recommender,
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
