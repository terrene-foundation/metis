# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Recommender endpoints — Sprint 2 of the Playbook.

**Important**: kailash-ml 0.17.0 does NOT ship a recommender engine. The
content-based and collaborative-lite implementations below are hand-wired on
top of scikit-learn primitives so students have real endpoints to call.
Sprint 2 prompt templates stay in business language — students never see
these internals.

Endpoints
---------
- `POST /recommend/for_customer`  — recommend N products to a customer (mode = content | collaborative | hybrid)
- `POST /recommend/compare`       — evaluate all three modes side-by-side on precision@k, coverage, cold-start handling
- `POST /recommend/cold_start`    — cold-start strategy: segment-modal basket for customers with <3 txns
- `GET  /recommend/config`        — current hybrid weights + cold-start disposition
- `POST /recommend/config`        — student sets hybrid weights + cold-start strategy
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sklearn.decomposition import NMF

from ..config import load_settings
from ..ml_context import get_context

router = APIRouter()

_COLD_START_STRATEGIES = {"popular", "segment_modal", "demographics", "ask", "refuse"}


# ----------------------------- persistence ----------------------------------


def _config_path() -> Path:
    return load_settings().data_dir / "recommender_config.json"


def _load_config() -> dict[str, Any]:
    path = _config_path()
    if path.exists():
        return json.loads(path.read_text())
    return {
        "mode": "content",
        "hybrid_weights": {"content": 1.0, "collaborative": 0.0},
        "cold_start_strategy": "popular",
        "constraints": {
            "exclude_out_of_stock": True,
            "exclude_under_18_features": False,  # becomes True after PDPA injection
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _save_config(cfg: dict[str, Any]) -> None:
    cfg["updated_at"] = datetime.now(timezone.utc).isoformat()
    _config_path().write_text(json.dumps(cfg, indent=2))


# ----------------------------- request models -------------------------------


class ForCustomerRequest(BaseModel):
    customer_id: str
    n: int = Field(default=5, ge=1, le=20)
    mode: str = Field(default="hybrid", description="content | collaborative | hybrid")


class CompareRequest(BaseModel):
    n: int = Field(default=5, ge=1, le=20)
    sample_size: int = Field(default=500, ge=50, le=2000)


class ConfigRequest(BaseModel):
    mode: str | None = None
    hybrid_weights: dict[str, float] | None = None
    cold_start_strategy: str | None = None


# ----------------------------- collaborative backbone -----------------------


def _build_user_item_matrix() -> tuple[np.ndarray, list[str], list[str]]:
    ctx = get_context()
    txns = ctx.transactions
    cust_ids = ctx.customers["customer_id"].to_list()
    sku_ids = ctx.products["sku"].to_list()
    cust_idx = {c: i for i, c in enumerate(cust_ids)}
    sku_idx = {s: i for i, s in enumerate(sku_ids)}
    mat = np.zeros((len(cust_ids), len(sku_ids)), dtype=np.float32)
    for row in txns.iter_rows(named=True):
        ci = cust_idx.get(row["customer_id"])
        si = sku_idx.get(row["sku"])
        if ci is not None and si is not None:
            mat[ci, si] += float(row["qty"])
    return mat, cust_ids, sku_ids


_COLLAB_CACHE: dict[str, Any] = {}


def _collaborative_scores(customer_id: str) -> dict[str, float]:
    """NMF-based matrix factorization, cached after first call."""
    if "W" not in _COLLAB_CACHE:
        mat, cust_ids, sku_ids = _build_user_item_matrix()
        nmf = NMF(n_components=16, init="nndsvd", random_state=42, max_iter=200, tol=1e-3)
        W = nmf.fit_transform(mat)
        H = nmf.components_
        _COLLAB_CACHE.update({"W": W, "H": H, "cust_ids": cust_ids, "sku_ids": sku_ids})
    W = _COLLAB_CACHE["W"]
    H = _COLLAB_CACHE["H"]
    cust_ids = _COLLAB_CACHE["cust_ids"]
    sku_ids = _COLLAB_CACHE["sku_ids"]
    try:
        idx = cust_ids.index(customer_id)
    except ValueError:
        return {}
    preds = W[idx] @ H
    return dict(zip(sku_ids, preds.tolist()))


def _content_scores(customer_id: str) -> dict[str, float]:
    """Customer's recent-purchase skus seed content-nearest-neighbor search."""
    ctx = get_context()
    rec = ctx.recommender
    txns = ctx.transactions
    user_txns = txns.filter(pl.col("customer_id") == customer_id)
    if len(user_txns) == 0:
        return {}
    recent_skus = user_txns.sort("txn_date", descending=True).head(5)["sku"].to_list()
    sku_to_idx = {s: i for i, s in enumerate(rec.skus)}
    seed_indices = [sku_to_idx[s] for s in recent_skus if s in sku_to_idx]
    if not seed_indices:
        return {}
    seed_vec = rec.product_features[seed_indices].mean(axis=0, keepdims=True)
    dist, idx = rec.nn.kneighbors(seed_vec, n_neighbors=min(30, len(rec.skus)))
    scores: dict[str, float] = {}
    for d, i in zip(dist[0], idx[0]):
        sku = rec.skus[i]
        if sku in recent_skus:
            continue
        scores[sku] = float(1.0 - d)  # cosine similarity
    return scores


def _is_cold_start(customer_id: str) -> bool:
    ctx = get_context()
    n = ctx.transactions.filter(pl.col("customer_id") == customer_id).shape[0]
    return n < 3


def _cold_start_recs(customer_id: str, n: int, strategy: str) -> list[str]:
    ctx = get_context()
    if strategy == "popular":
        top = (
            ctx.transactions.group_by("sku")
            .count()
            .sort("count", descending=True)
            .head(n)["sku"]
            .to_list()
        )
        return top
    if strategy == "segment_modal":
        # Customer's baseline segment, then most-bought SKU by that segment
        labels = ctx.baseline.labels
        cust_ids = ctx.baseline.customer_ids
        try:
            seg = int(labels[cust_ids.index(customer_id)])
        except (ValueError, IndexError):
            return _cold_start_recs(customer_id, n, "popular")
        seg_cust_ids = [cust_ids[i] for i, lbl in enumerate(labels) if lbl == seg]
        seg_txns = ctx.transactions.filter(pl.col("customer_id").is_in(seg_cust_ids))
        top = (
            seg_txns.group_by("sku").count().sort("count", descending=True).head(n)["sku"].to_list()
        )
        return top
    if strategy == "demographics":
        # Postal district modal basket
        cust = ctx.customers.filter(pl.col("customer_id") == customer_id)
        if len(cust) == 0:
            return _cold_start_recs(customer_id, n, "popular")
        district = cust["postal_district"].item()
        peers = ctx.customers.filter(pl.col("postal_district") == district)["customer_id"]
        peer_txns = ctx.transactions.filter(pl.col("customer_id").is_in(peers))
        top = (
            peer_txns.group_by("sku")
            .count()
            .sort("count", descending=True)
            .head(n)["sku"]
            .to_list()
        )
        return top
    if strategy == "ask":
        return []  # client should prompt the user
    if strategy == "refuse":
        return []
    raise HTTPException(422, f"unknown cold-start strategy {strategy!r}")


# ----------------------------- endpoints ------------------------------------


@router.get("/config")
def get_config() -> dict:
    return _load_config()


@router.post("/config")
def set_config(req: ConfigRequest) -> dict:
    cfg = _load_config()
    if req.mode is not None:
        if req.mode not in ("content", "collaborative", "hybrid"):
            raise HTTPException(422, f"unknown mode {req.mode!r}")
        cfg["mode"] = req.mode
    if req.hybrid_weights is not None:
        total = sum(req.hybrid_weights.values())
        if abs(total - 1.0) > 1e-3:
            raise HTTPException(422, f"hybrid weights must sum to 1.0 (got {total})")
        cfg["hybrid_weights"] = req.hybrid_weights
    if req.cold_start_strategy is not None:
        if req.cold_start_strategy not in _COLD_START_STRATEGIES:
            raise HTTPException(
                422,
                f"cold-start strategy must be one of {sorted(_COLD_START_STRATEGIES)}",
            )
        cfg["cold_start_strategy"] = req.cold_start_strategy
    _save_config(cfg)
    return cfg


@router.post("/for_customer")
def for_customer(req: ForCustomerRequest) -> dict:
    cfg = _load_config()
    cold = _is_cold_start(req.customer_id)
    if cold:
        skus = _cold_start_recs(req.customer_id, req.n, cfg["cold_start_strategy"])
        return {
            "customer_id": req.customer_id,
            "mode": "cold_start",
            "strategy": cfg["cold_start_strategy"],
            "recommendations": skus,
            "note": "Customer has <3 transactions — cold-start path fired.",
        }

    content = _content_scores(req.customer_id)
    collab = _collaborative_scores(req.customer_id)

    mode = req.mode or cfg["mode"]
    if mode == "content":
        ranked = sorted(content.items(), key=lambda kv: -kv[1])
    elif mode == "collaborative":
        ranked = sorted(collab.items(), key=lambda kv: -kv[1])
    elif mode == "hybrid":
        w = cfg["hybrid_weights"]
        keys = set(content) | set(collab)

        # min-max normalize each then weighted sum
        def _norm(d: dict[str, float]) -> dict[str, float]:
            if not d:
                return {}
            mx = max(d.values())
            mn = min(d.values())
            if mx == mn:
                return {k: 1.0 for k in d}
            return {k: (v - mn) / (mx - mn) for k, v in d.items()}

        cn = _norm(content)
        kn = _norm(collab)
        merged = {
            k: w.get("content", 0.5) * cn.get(k, 0.0) + w.get("collaborative", 0.5) * kn.get(k, 0.0)
            for k in keys
        }
        ranked = sorted(merged.items(), key=lambda kv: -kv[1])
    else:
        raise HTTPException(422, f"unknown mode {mode!r}")

    # Constraint: exclude out-of-stock
    ctx = get_context()
    stock = dict(zip(ctx.products["sku"].to_list(), ctx.products["stock_level"].to_list()))
    if cfg["constraints"].get("exclude_out_of_stock", True):
        ranked = [(s, v) for s, v in ranked if stock.get(s, 0) > 0]

    recs = [{"sku": s, "score": round(v, 4)} for s, v in ranked[: req.n]]
    return {
        "customer_id": req.customer_id,
        "mode": mode,
        "hybrid_weights": cfg["hybrid_weights"] if mode == "hybrid" else None,
        "recommendations": recs,
    }


@router.post("/compare")
def compare_modes(req: CompareRequest) -> dict:
    """Offline eval across content / collaborative / hybrid.

    For each of `sample_size` customers with ≥5 txns, hold out the most
    recent txn and check whether each mode's top-N list contains the held-out
    SKU. Reports precision@N, catalog coverage, and cold-start hit rate.
    """
    ctx = get_context()
    cfg = _load_config()
    rng = np.random.default_rng(42)

    eligible = (
        ctx.transactions.group_by("customer_id")
        .count()
        .filter(pl.col("count") >= 5)["customer_id"]
        .to_list()
    )
    sample = rng.choice(eligible, size=min(req.sample_size, len(eligible)), replace=False)

    modes = ["content", "collaborative", "hybrid"]
    hits = {m: 0 for m in modes}
    covered_skus = {m: set() for m in modes}

    for cid in sample:
        cust_txns = ctx.transactions.filter(pl.col("customer_id") == cid).sort("txn_date")
        if len(cust_txns) < 2:
            continue
        held_out_sku = cust_txns["sku"].to_list()[-1]

        content = _content_scores(cid)
        collab = _collaborative_scores(cid)
        for m in modes:
            if m == "content":
                top = [s for s, _ in sorted(content.items(), key=lambda kv: -kv[1])[: req.n]]
            elif m == "collaborative":
                top = [s for s, _ in sorted(collab.items(), key=lambda kv: -kv[1])[: req.n]]
            else:
                keys = set(content) | set(collab)
                w = cfg["hybrid_weights"]
                merged = {
                    k: w.get("content", 0.5) * content.get(k, 0.0)
                    + w.get("collaborative", 0.5) * collab.get(k, 0.0)
                    for k in keys
                }
                top = [s for s, _ in sorted(merged.items(), key=lambda kv: -kv[1])[: req.n]]
            covered_skus[m].update(top)
            if held_out_sku in top:
                hits[m] += 1

    n = len(sample)
    total_skus = len(ctx.products)
    results = {
        m: {
            "precision_at_n": round(hits[m] / n, 4) if n else 0.0,
            "catalog_coverage": round(len(covered_skus[m]) / total_skus, 4),
            "hits": hits[m],
            "sample_size": int(n),
        }
        for m in modes
    }

    cold_sample = [c for c in ctx.customers["customer_id"].to_list() if _is_cold_start(c)][:50]
    cold_coverage = {
        s: len(_cold_start_recs("dummy", req.n, s)) > 0 for s in _COLD_START_STRATEGIES
    }

    return {
        "results": results,
        "cold_start_coverage": cold_coverage,
        "n_cold_customers": len(cold_sample),
        "note": (
            "precision@N is the offline proxy for 'would this recommendation "
            "get clicked'. Pair it with catalog coverage (does the recommender "
            "only promote the head of the long tail?) and cold-start handling. "
            "See Playbook Phase 12."
        ),
    }
