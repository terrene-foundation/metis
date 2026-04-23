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
from sklearn.decomposition import NMF
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
class CollaborativeRecommender:
    """NMF-factorized user×item matrix. Pre-fit at startup.

    Scores for customer i, sku j = W[i] @ H[:, j]. O(1) lookup once fit.
    """

    W: np.ndarray
    H: np.ndarray
    customer_ids: list[str]
    skus: list[str]
    customer_idx: dict[str, int]
    sku_idx: dict[str, int]
    n_components: int = 16

    def scores_for(self, customer_id: str) -> dict[str, float]:
        i = self.customer_idx.get(customer_id)
        if i is None:
            return {}
        preds = self.W[i] @ self.H
        return dict(zip(self.skus, preds.tolist()))


@dataclass
class PredictorBundle:
    """Pre-trained SML churn + conversion classifiers.

    Both are a leaderboard of 3 family-diverse candidates: logistic regression
    (linear), random forest (tree bag), gradient-boosted trees (ensemble, the
    king for tabular). Trained at startup so /predict/score is instant; live
    /predict/train re-runs when students want to see the sweep.
    """

    # churn: label = days_since_last_visit > 90
    churn_candidates: dict[str, dict]  # name -> {model, auc, precision@0.3, recall@0.3, brier, ...}
    churn_features: list[str]
    churn_scaler: StandardScaler | None
    churn_customer_ids: list[str]
    churn_labels: np.ndarray
    # conversion: label = (customer, sku) had >=1 txn in last 90 days on category
    conv_candidates: dict[str, dict]
    conv_features: list[str]


@dataclass
class MLContext:
    customers: pl.DataFrame
    products: pl.DataFrame
    transactions: pl.DataFrame
    baseline: BaselineSegmentation
    recommender: ContentRecommender
    collaborative: CollaborativeRecommender
    predictor: PredictorBundle
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


CHURN_FEATURES = [
    "total_spend_24mo",
    "avg_basket_size",
    "visits_per_week",
    "weekend_browse_fraction",
    "luxury_category_fraction",
    "distinct_categories",
    # NOTE: days_since_last_visit is excluded — direct leakage (it IS the label).
    "marketing_email_open_rate",
]


def _evaluate_binary(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.3) -> dict:
    """Return the orchestrator-readable metrics for a binary classifier."""
    from sklearn.metrics import (
        average_precision_score,
        brier_score_loss,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    y_pred = (y_prob >= threshold).astype(int)
    try:
        auc = float(roc_auc_score(y_true, y_prob))
    except ValueError:
        auc = float("nan")
    return {
        "auc": round(auc, 4),
        "avg_precision": round(float(average_precision_score(y_true, y_prob)), 4),
        "precision_at_threshold": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall_at_threshold": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "brier_score": round(float(brier_score_loss(y_true, y_prob)), 4),
        "threshold": threshold,
        "base_rate": round(float(y_true.mean()), 4),
    }


def build_churn_predictor(
    customers: pl.DataFrame,
    seed: int = 42,
) -> tuple[dict[str, dict], StandardScaler, np.ndarray, np.ndarray]:
    """Train a 3-family SML leaderboard for churn prediction.

    Label: days_since_last_visit > 90 (we're calling them 'churned').
    Feature set: behavioural features EXCLUDING days_since_last_visit (leakage).
    """
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    X = customers.select(CHURN_FEATURES).to_numpy()
    y = (customers["days_since_last_visit"].to_numpy() > 90).astype(int)
    scaler = StandardScaler().fit(X)
    X_std = scaler.transform(X)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X_std, y, test_size=0.25, random_state=seed, stratify=y
    )

    families = {
        "logistic_regression": (
            "linear (reads features linearly; highly interpretable; fast)",
            LogisticRegression(max_iter=500, random_state=seed),
        ),
        "random_forest": (
            "tree bag (handles non-linear; robust; less interpretable than LR)",
            RandomForestClassifier(n_estimators=200, max_depth=8, random_state=seed, n_jobs=-1),
        ),
        "gradient_boosted": (
            "ensemble — the king for tabular data (captures interactions; slowest to train)",
            GradientBoostingClassifier(
                n_estimators=200, max_depth=4, learning_rate=0.05, random_state=seed
            ),
        ),
    }

    results: dict[str, dict] = {}
    for name, (why, model) in families.items():
        model.fit(X_tr, y_tr)
        y_prob_te = model.predict_proba(X_te)[:, 1]
        metrics = _evaluate_binary(y_te, y_prob_te, threshold=0.3)
        # feature importance (best-effort per family)
        try:
            if hasattr(model, "feature_importances_"):
                fi = dict(zip(CHURN_FEATURES, model.feature_importances_.tolist()))
            elif hasattr(model, "coef_"):
                fi = dict(zip(CHURN_FEATURES, np.abs(model.coef_[0]).tolist()))
            else:
                fi = {}
        except Exception:
            fi = {}
        results[name] = {
            "family": why,
            "metrics": metrics,
            "feature_importance": {k: round(v, 4) for k, v in fi.items()},
            "model": model,
        }

    return results, scaler, customers["customer_id"].to_numpy(), y


def build_conversion_predictor(
    customers: pl.DataFrame,
    transactions: pl.DataFrame,
    products: pl.DataFrame,
    seed: int = 42,
) -> dict:
    """Train a conversion-category SML leaderboard.

    Cheap pedagogical formulation: "did customer C buy ANY product in category X
    in the last 90 days?" — (customer, category) pairs as features, binary label.
    Three candidates, same shape as churn. Returned without the model objects
    to keep the bundle lean — scoring uses the stored leaderboard.
    """
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    # Build features: customer row + category one-hot
    txn_cat = transactions.join(products.select(["sku", "category"]), on="sku", how="left")
    categories = sorted(products["category"].unique().to_list())

    # Recent transactions (last 90 days)
    recent = txn_cat.sort("txn_date", descending=True).head(30_000)
    customer_cats = recent.group_by(["customer_id", "category"]).agg(
        pl.col("qty").sum().alias("qty")
    )

    # Build (customer, category) positive pairs
    pos_pairs = customer_cats.select(["customer_id", "category"]).with_columns(
        pl.lit(1).alias("label")
    )
    # Negative pairs: random sample of (customer, category) not in positives
    rng = np.random.default_rng(seed)
    pos_set = {(r[0], r[1]) for r in pos_pairs.iter_rows()}
    all_cust = customers["customer_id"].to_list()
    neg_rows = []
    while len(neg_rows) < len(pos_set):
        c = rng.choice(all_cust)
        cat = rng.choice(categories)
        if (c, cat) not in pos_set:
            neg_rows.append((c, cat, 0))
    neg_pairs = pl.DataFrame(
        neg_rows,
        schema={"customer_id": pl.Utf8, "category": pl.Utf8, "label": pl.Int32},
        orient="row",
    )
    pos_pairs = pos_pairs.with_columns(pl.col("label").cast(pl.Int32))
    pairs = pl.concat([pos_pairs, neg_pairs], how="vertical")

    # Join customer features + one-hot category
    feat_df = pairs.join(customers, on="customer_id", how="left")
    cat_dummies = feat_df.select("category").to_dummies()
    num_cols = [
        "total_spend_24mo",
        "avg_basket_size",
        "visits_per_week",
        "weekend_browse_fraction",
        "luxury_category_fraction",
        "distinct_categories",
        "marketing_email_open_rate",
    ]
    numeric = feat_df.select(num_cols)
    X = pl.concat([numeric, cat_dummies], how="horizontal").to_numpy()
    y = feat_df["label"].to_numpy()

    scaler = StandardScaler().fit(X)
    X_std = scaler.transform(X)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_std, y, test_size=0.25, random_state=seed, stratify=y
    )

    families = {
        "logistic_regression": LogisticRegression(max_iter=500, random_state=seed),
        "random_forest": RandomForestClassifier(
            n_estimators=150, max_depth=8, random_state=seed, n_jobs=-1
        ),
        "gradient_boosted": GradientBoostingClassifier(
            n_estimators=150, max_depth=4, learning_rate=0.08, random_state=seed
        ),
    }
    results: dict[str, dict] = {}
    for name, model in families.items():
        model.fit(X_tr, y_tr)
        y_prob = model.predict_proba(X_te)[:, 1]
        results[name] = {"metrics": _evaluate_binary(y_te, y_prob, threshold=0.5)}
    return {
        "features": num_cols + list(cat_dummies.columns),
        "candidates": results,
    }


def build_collaborative_recommender(
    transactions: pl.DataFrame,
    customers: pl.DataFrame,
    products: pl.DataFrame,
    n_components: int = 16,
    seed: int = 42,
) -> CollaborativeRecommender:
    """Pre-fit NMF on the user-item matrix at startup.

    Vectorized construction via polars pivot (not Python row iteration).
    5000 × 400 matrix → NMF with 16 components → fits in ~1-2s on this size.
    """
    cust_ids = customers["customer_id"].to_list()
    sku_ids = products["sku"].to_list()
    cust_idx = {c: i for i, c in enumerate(cust_ids)}
    sku_idx = {s: i for i, s in enumerate(sku_ids)}

    # Aggregate transactions to customer × sku qty sum, then pivot
    agg = transactions.group_by(["customer_id", "sku"]).agg(
        pl.col("qty").sum().cast(pl.Float32).alias("qty")
    )
    pivot = agg.pivot(values="qty", index="customer_id", on="sku", aggregate_function="first")

    mat = np.zeros((len(cust_ids), len(sku_ids)), dtype=np.float32)
    pivot_cust_ids = pivot["customer_id"].to_list()
    for col in pivot.columns:
        if col == "customer_id":
            continue
        sj = sku_idx.get(col)
        if sj is None:
            continue
        col_vals = pivot[col].fill_null(0.0).to_numpy()
        for k, c_id in enumerate(pivot_cust_ids):
            i = cust_idx.get(c_id)
            if i is not None:
                mat[i, sj] = col_vals[k]

    # log1p dampens the long-tail heavy hitters (stability for NMF matmul)
    mat_log = np.log1p(mat)

    nmf = NMF(
        n_components=n_components,
        init="nndsvd",
        random_state=seed,
        max_iter=400,
        tol=1e-4,
        solver="cd",
    )
    W = nmf.fit_transform(mat_log)
    H = nmf.components_
    # Sanitize any residual non-finite values from extreme sparse rows
    W = np.nan_to_num(W, nan=0.0, posinf=0.0, neginf=0.0)
    H = np.nan_to_num(H, nan=0.0, posinf=0.0, neginf=0.0)
    return CollaborativeRecommender(
        W=W,
        H=H,
        customer_ids=cust_ids,
        skus=sku_ids,
        customer_idx=cust_idx,
        sku_idx=sku_idx,
        n_components=n_components,
    )


def load_sweep_reference(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "segment_candidates.json"
    return json.loads(path.read_text())


def load_drift_reference(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "drift_baseline.json"
    return json.loads(path.read_text())
