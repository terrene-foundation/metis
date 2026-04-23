# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Segmentation endpoints — Sprint 1 of the Playbook.

Endpoints
---------
- `GET  /segment/baseline`              — K=3 baseline already shipped
- `GET  /segment/candidates`            — pre-baked K=2..10 sweep for comparison
- `POST /segment/fit`                   — run a K-sweep live with requested range + algorithm
- `POST /segment/name`                  — student submits cluster names + differentiated actions
- `POST /segment/promote`               — transition a (k, algorithm) choice staging→shadow→production
- `GET  /segment/registry`              — current registry state
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
from sklearn.cluster import DBSCAN, KMeans, SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from ..config import load_settings
from ..ml_context import CLUSTER_FEATURES, get_context

router = APIRouter()


# ----------------------------- persistence ----------------------------------


def _registry_path() -> Path:
    return load_settings().data_dir / "segment_registry.json"


def _load_registry() -> dict[str, Any]:
    path = _registry_path()
    if path.exists():
        return json.loads(path.read_text())
    return {
        "versions": {
            "baseline-v1": {
                "algorithm": "kmeans",
                "k": 3,
                "stage": "staging",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "note": "pre-built baseline",
            }
        },
        "production": None,
        "shadow": None,
    }


def _save_registry(state: dict[str, Any]) -> None:
    _registry_path().write_text(json.dumps(state, indent=2))


# ----------------------------- request models ------------------------------


class FitRequest(BaseModel):
    algorithm: str = Field(default="kmeans", description="kmeans | dbscan | spectral")
    k_range: list[int] = Field(default_factory=lambda: [3, 5, 7])
    eps: float | None = Field(default=None, description="DBSCAN eps; ignored otherwise")
    min_samples: int = Field(default=10, description="DBSCAN min_samples; ignored otherwise")
    seed: int = Field(default=42)


class NameRequest(BaseModel):
    version: str
    names: dict[int, str]
    actions: dict[int, str]


class PromoteRequest(BaseModel):
    version: str
    to_stage: str  # staging -> shadow -> production -> archived


# ----------------------------- helpers --------------------------------------


def _feature_matrix() -> tuple[np.ndarray, list[str]]:
    ctx = get_context()
    X = ctx.customers.select(CLUSTER_FEATURES).to_numpy()
    ids = ctx.customers["customer_id"].to_list()
    return StandardScaler().fit_transform(X), ids


def _fit_kmeans(X: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, float, float]:
    km = KMeans(n_clusters=k, n_init="auto", random_state=seed)
    labels = km.fit_predict(X)
    sil = float(silhouette_score(X, labels))  # type: ignore[arg-type]
    return labels, sil, float(km.inertia_)


def _fit_spectral(X: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, float]:
    sc = SpectralClustering(
        n_clusters=k,
        random_state=seed,
        assign_labels="kmeans",
        affinity="nearest_neighbors",
        n_neighbors=15,
    )
    labels = sc.fit_predict(X)
    sil = float(silhouette_score(X, labels))  # type: ignore[arg-type]
    return labels, sil


def _fit_dbscan(X: np.ndarray, eps: float, min_samples: int) -> tuple[np.ndarray, float, int]:
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_
    # silhouette excludes noise (label = -1)
    mask = labels != -1
    if mask.sum() < 2 or len(set(labels[mask])) < 2:
        sil = -1.0
    else:
        sil = float(silhouette_score(X[mask], labels[mask]))  # type: ignore[arg-type]
    n_noise = int((labels == -1).sum())
    return labels, sil, n_noise


# ----------------------------- endpoints ------------------------------------


@router.get("/baseline")
def get_baseline() -> dict:
    ctx = get_context()
    sizes = {int(k): int(v) for k, v in zip(*np.unique(ctx.baseline.labels, return_counts=True))}
    return {
        "version": "baseline-v1",
        "algorithm": "kmeans",
        "k": ctx.baseline.k,
        "silhouette": round(ctx.baseline.silhouette, 4),
        "inertia": round(ctx.baseline.inertia, 2),
        "segment_sizes": sizes,
        "features": list(CLUSTER_FEATURES),
        "stage": ctx.baseline.stage,
        "note": (
            "Pre-built baseline. Students CRITIQUE this via Phase 4-8 of the "
            "Playbook: run alternative K values, run a non-KMeans algorithm, "
            "choose metric + threshold, red-team, promote a better version."
        ),
    }


@router.get("/candidates")
def get_candidates() -> dict:
    """Pre-baked K-sweep from the data generator. Student compares live runs against this."""
    ctx = get_context()
    return ctx.candidates_sweep


@router.post("/fit")
def fit_segmentation(req: FitRequest) -> dict:
    """Run a (possibly multi-K) clustering sweep live.

    The response emulates what kailash-ml's `ClusteringEngine.sweep_k` would
    return — a list of per-K results with silhouette + size distribution. For
    DBSCAN we ignore `k_range` and return a single result.
    """
    X, _ids = _feature_matrix()

    results: list[dict] = []
    if req.algorithm == "kmeans":
        for k in req.k_range:
            if k < 2 or k > 15:
                continue
            labels, sil, inertia = _fit_kmeans(X, k, req.seed)
            sizes = np.bincount(labels).tolist()
            results.append(
                {
                    "k": k,
                    "silhouette": round(sil, 4),
                    "inertia": round(inertia, 2),
                    "segment_sizes": sizes,
                }
            )
    elif req.algorithm == "spectral":
        for k in req.k_range:
            if k < 2 or k > 10:
                continue
            labels, sil = _fit_spectral(X, k, req.seed)
            sizes = np.bincount(labels).tolist()
            results.append(
                {
                    "k": k,
                    "silhouette": round(sil, 4),
                    "segment_sizes": sizes,
                }
            )
    elif req.algorithm == "dbscan":
        if req.eps is None:
            raise HTTPException(422, "DBSCAN requires `eps`.")
        labels, sil, n_noise = _fit_dbscan(X, req.eps, req.min_samples)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        results.append(
            {
                "k": n_clusters,
                "silhouette": round(sil, 4),
                "noise_points": n_noise,
                "eps": req.eps,
                "min_samples": req.min_samples,
            }
        )
    else:
        raise HTTPException(422, f"unknown algorithm {req.algorithm!r}")

    return {
        "algorithm": req.algorithm,
        "seed": req.seed,
        "sweep": results,
        "note": (
            "Silhouette alone does not tell you the right K. Pair this with "
            "the stability check (run `/segment/fit` with a different seed and "
            "compare segment assignments) and with business actionability "
            "(can marketing run K different campaigns?). See Playbook Phase 6."
        ),
    }


@router.post("/name")
def name_segments(req: NameRequest) -> dict:
    """Student declares what each cluster IS and what to DO with it.

    This is the Phase 5 deliverable — a named segment sheet, not a leaderboard row.
    Validates one-action-per-segment (two clusters with the same action collapse).
    """
    if len(set(req.actions.values())) != len(req.actions):
        raise HTTPException(
            422,
            (
                "Two clusters got the same action — collapse them or differentiate. "
                "One-action-per-segment is the Phase 5 rule."
            ),
        )
    state = _load_registry()
    entry = state["versions"].setdefault(req.version, {})
    entry["names"] = req.names
    entry["actions"] = req.actions
    entry["named_at"] = datetime.now(timezone.utc).isoformat()
    _save_registry(state)
    return {"version": req.version, "named": True, "count": len(req.names)}


@router.post("/promote")
def promote(req: PromoteRequest) -> dict:
    """Transition a version through the stage lifecycle.

    Legal transitions: staging → {shadow, archived}; shadow → {production, archived, staging};
    production → {archived, shadow}; archived → {staging}. Promoting a version to
    production auto-archives any existing production version.
    """
    state = _load_registry()
    if req.version not in state["versions"]:
        raise HTTPException(404, f"version {req.version!r} not registered")
    entry = state["versions"][req.version]
    current = entry.get("stage", "staging")

    legal = {
        "staging": {"shadow", "archived"},
        "shadow": {"production", "archived", "staging"},
        "production": {"archived", "shadow"},
        "archived": {"staging"},
    }
    if req.to_stage not in legal.get(current, set()):
        raise HTTPException(
            409,
            (
                f"illegal transition {current}→{req.to_stage}. Legal from {current}: "
                f"{sorted(legal.get(current, set()))}."
            ),
        )

    # Auto-archive any existing production if promoting to production
    if req.to_stage == "production" and state.get("production"):
        prev = state["production"]
        state["versions"][prev]["stage"] = "archived"
    entry["stage"] = req.to_stage
    entry["transitioned_at"] = datetime.now(timezone.utc).isoformat()
    if req.to_stage == "production":
        state["production"] = req.version
    if req.to_stage == "shadow":
        state["shadow"] = req.version
    _save_registry(state)
    return {"version": req.version, "from_stage": current, "to_stage": req.to_stage}


@router.get("/registry")
def get_registry() -> dict:
    return _load_registry()


@router.get("/stability")
def stability_probe(seed: int = 99) -> dict:
    """Refit the baseline K with a new seed and measure Jaccard on segment pairs.

    Phase 7 red-team tool: if a student accepts a K without checking this,
    they miss that cluster assignments flip on re-seed.
    """
    ctx = get_context()
    X, _ = _feature_matrix()
    labels_new, sil_new, _ = _fit_kmeans(X, ctx.baseline.k, seed)

    # Pairwise Jaccard: for N customers, how often do two customers in the
    # same segment stay in the same segment?
    N = len(labels_new)
    rng = np.random.default_rng(seed)
    sample = rng.choice(N, size=min(2000, N), replace=False)
    L0 = ctx.baseline.labels[sample]
    L1 = labels_new[sample]
    same0 = L0[:, None] == L0[None, :]
    same1 = L1[:, None] == L1[None, :]
    # exclude self-pairs
    mask = ~np.eye(len(sample), dtype=bool)
    intersect = (same0 & same1 & mask).sum()
    union = (same0 | same1) & mask
    jaccard = float(intersect / union.sum()) if union.sum() > 0 else 0.0

    return {
        "baseline_seed": 42,
        "probe_seed": seed,
        "k": ctx.baseline.k,
        "silhouette_baseline": round(ctx.baseline.silhouette, 4),
        "silhouette_probe": round(sil_new, 4),
        "jaccard_same_pair": round(jaccard, 4),
        "interpretation": (
            "Jaccard ≥ 0.8 → segments are stable. <0.8 → cluster assignments "
            "are seed-dependent; don't promote this K."
        ),
    }
