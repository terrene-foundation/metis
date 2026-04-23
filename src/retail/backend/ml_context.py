# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Shared ML state for the Arcadia backend.

Loaded once at startup (`startup.run_startup`) and read by every route. The
baseline segmentation model and content-based recommender are pre-trained here
so the student never waits on training to start the lesson.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

CLUSTER_FEATURES = [
    "total_spend_24mo",
    "avg_basket_size",
    "visits_per_week",
    "weekend_browse_fraction",
    "luxury_category_fraction",
    "distinct_categories",
    "days_since_last_visit",
    "marketing_email_open_rate",
]


@dataclass
class BaselineSegmentation:
    """Pre-trained K=3 baseline the student critiques in Phase 4-8."""

    model: KMeans
    scaler: StandardScaler
    silhouette: float
    inertia: float
    labels: np.ndarray
    customer_ids: list[str]
    feature_columns: list[str] = field(default_factory=lambda: list(CLUSTER_FEATURES))
    k: int = 3
    stage: str = "staging"  # staging -> shadow -> production


@dataclass
class ContentRecommender:
    """Content-based nearest-neighbour recommender over product embeddings."""

    nn: NearestNeighbors
    product_features: np.ndarray
    skus: list[str]
    feature_columns: list[str]


@dataclass
class MLContext:
    customers: pl.DataFrame
    products: pl.DataFrame
    transactions: pl.DataFrame
    baseline: BaselineSegmentation
    recommender: ContentRecommender
    candidates_sweep: dict[str, Any]
    drift_reference: dict[str, Any]


# Populated by startup.run_startup; routes import and read.
_CTX: MLContext | None = None


def set_context(ctx: MLContext) -> None:
    global _CTX
    _CTX = ctx


def get_context() -> MLContext:
    if _CTX is None:
        raise RuntimeError("ML context not initialised — startup must run first")
    return _CTX


def train_baseline_segmentation(
    customers: pl.DataFrame, k: int = 3, seed: int = 42
) -> BaselineSegmentation:
    X = customers.select(CLUSTER_FEATURES).to_numpy()
    scaler = StandardScaler().fit(X)
    X_std = scaler.transform(X)
    km = KMeans(n_clusters=k, n_init="auto", random_state=seed)
    labels = km.fit_predict(X_std)
    sil = float(silhouette_score(X_std, labels))  # type: ignore[arg-type]
    return BaselineSegmentation(
        model=km,
        scaler=scaler,
        silhouette=sil,
        inertia=float(km.inertia_),
        labels=labels,
        customer_ids=customers["customer_id"].to_list(),
    )


def build_content_recommender(products: pl.DataFrame) -> ContentRecommender:
    """One-hot category × price-tier × luxury → nearest-neighbour content rec."""
    feat_df = products.with_columns(
        [
            pl.col("price").log().alias("log_price"),
            pl.col("luxury_flag").cast(pl.Int8).alias("luxury_int"),
            pl.col("avg_rating").fill_null(0.0),
            pl.col("n_reviews").log1p().alias("log_reviews"),
        ]
    )
    # One-hot category + subcategory
    cat_dummies = feat_df.select("category").to_dummies()
    subcat_dummies = feat_df.select("subcategory").to_dummies()
    numeric = feat_df.select(["log_price", "luxury_int", "avg_rating", "log_reviews"])
    X = pl.concat([numeric, cat_dummies, subcat_dummies], how="horizontal").to_numpy()
    X_std = StandardScaler().fit_transform(X)
    nn = NearestNeighbors(n_neighbors=10, metric="cosine").fit(X_std)
    return ContentRecommender(
        nn=nn,
        product_features=X_std,
        skus=products["sku"].to_list(),
        feature_columns=(
            list(numeric.columns) + list(cat_dummies.columns) + list(subcat_dummies.columns)
        ),
    )


def load_sweep_reference(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "segment_candidates.json"
    return json.loads(path.read_text())


def load_drift_reference(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "drift_baseline.json"
    return json.loads(path.read_text())
