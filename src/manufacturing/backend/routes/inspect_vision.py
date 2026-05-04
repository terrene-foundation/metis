# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Sprint 1 — Vision QC inspector (transfer-learning, 3-architecture leaderboard)."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..ml_context import (
    SAFETY_CRITICAL_HARD_FLOOR,
    VISION_CLASSES,
    get_context,
)

router = APIRouter(prefix="/inspect/vision")
log = logging.getLogger("metis.manufacturing.vision")


def _serialise_arch_entry(arch: str, entry: Any) -> dict[str, Any]:
    return {
        "arch": arch,
        "why": entry.family_why,
        "macro_f1": entry.macro_f1,
        "embedding_dim": entry.embedding_dim,
        "per_class": entry.per_class,
        "threshold": entry.threshold,
    }


@router.get("/leaderboard")
def leaderboard() -> dict[str, Any]:
    ctx = get_context()
    vb = ctx.vision_baseline
    rows = [_serialise_arch_entry(arch, entry) for arch, entry in vb.candidates.items()]
    rows.sort(key=lambda r: r["macro_f1"], reverse=True)
    return {
        "classes": list(VISION_CLASSES),
        "chosen_arch": vb.chosen_arch,
        "stage": vb.stage,
        "promoted_thresholds": vb.promoted_thresholds,
        "wsh_safety_floor": SAFETY_CRITICAL_HARD_FLOOR,
        "leaderboard": rows,
    }


class TrainRequest(BaseModel):
    arch: str | None = Field(default=None, description="Optional: re-fit only one arch.")
    seed: int = 20260504


@router.post("/train")
def retrain(req: TrainRequest) -> dict[str, Any]:
    """Re-fit the vision leaderboard with a new seed.

    Pedagogical hook: students see the leaderboard move when the seed changes,
    confirming the synthetic baseline is real (not hardcoded).
    """
    from ..ml_context import build_vision_baseline, set_context

    ctx = get_context()
    new_baseline = build_vision_baseline(
        ctx.boards, ctx.vision_embeddings, ctx.vision_image_ids, seed=req.seed
    )
    # Preserve promoted thresholds across retrain (Phase 6 deliverable persists).
    new_baseline.promoted_thresholds = dict(ctx.vision_baseline.promoted_thresholds)
    new_baseline.stage = ctx.vision_baseline.stage
    new_ctx = ctx
    new_ctx.vision_baseline = new_baseline
    set_context(new_ctx)
    log.info(
        "vision.retrain.ok arch=%s macro_f1=%.3f seed=%d",
        new_baseline.chosen_arch,
        new_baseline.macro_f1,
        req.seed,
    )
    return leaderboard()


class ScoreRequest(BaseModel):
    image_id: str


@router.post("/score")
def score(req: ScoreRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.image_id not in ctx.vision_image_ids:
        raise HTTPException(status_code=404, detail=f"unknown image_id {req.image_id}")
    idx = ctx.vision_image_ids.index(req.image_id)
    chosen_arch = ctx.vision_baseline.chosen_arch
    entry = ctx.vision_baseline.candidates[chosen_arch]
    X = ctx.vision_embeddings[chosen_arch][idx : idx + 1]
    X_std = entry.scaler.transform(X)
    proba = entry.model.predict_proba(X_std)[0]
    if len(proba) < len(VISION_CLASSES):
        full = np.zeros(len(VISION_CLASSES), dtype=np.float32)
        for src_idx, cls_int in enumerate(entry.model.classes_):
            full[int(cls_int)] = proba[src_idx]
        proba = full
    per_class = {c: round(float(proba[i]), 4) for i, c in enumerate(VISION_CLASSES)}
    chosen = max(per_class, key=per_class.get)  # type: ignore[arg-type]
    label_lookup = dict(zip(ctx.boards["image_id"].to_list(), ctx.boards["class_label"].to_list()))
    return {
        "image_id": req.image_id,
        "arch": chosen_arch,
        "per_class": per_class,
        "chosen_class": chosen,
        "ground_truth": label_lookup.get(req.image_id),
    }


class ThresholdRequest(BaseModel):
    class_name: str
    threshold: float
    action: str = Field(description="auto_pass | manual_review | auto_fail")


@router.post("/threshold")
def set_threshold(req: ThresholdRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.class_name not in VISION_CLASSES:
        raise HTTPException(status_code=404, detail=f"unknown class {req.class_name}")
    if req.action not in ("auto_pass", "manual_review", "auto_fail"):
        raise HTTPException(status_code=422, detail=f"unknown action {req.action}")
    if not 0.0 <= req.threshold <= 1.0:
        raise HTTPException(status_code=422, detail="threshold must be in [0, 1]")
    if req.class_name == "safety_critical_defect" and req.threshold < SAFETY_CRITICAL_HARD_FLOOR:
        raise HTTPException(
            status_code=409,
            detail=(
                f"safety_critical_defect threshold {req.threshold} below WSH hard "
                f"floor {SAFETY_CRITICAL_HARD_FLOOR} (IPC-A-610 Class 3 + WSH Act). "
                f"This class is structurally hard, not cost-balanced."
            ),
        )
    ctx.vision_baseline.promoted_thresholds[req.class_name] = req.threshold
    log.info(
        "vision.threshold.ok class=%s threshold=%.3f action=%s",
        req.class_name,
        req.threshold,
        req.action,
    )
    return {
        "class": req.class_name,
        "threshold": req.threshold,
        "action": req.action,
        "promoted_thresholds": ctx.vision_baseline.promoted_thresholds,
    }


class PromoteRequest(BaseModel):
    arch: str
    to_stage: str = Field(description="staging | shadow | production | archived")


@router.post("/promote")
def promote(req: PromoteRequest) -> dict[str, Any]:
    ctx = get_context()
    if req.arch not in ctx.vision_baseline.candidates:
        raise HTTPException(status_code=404, detail=f"unknown arch {req.arch}")
    legal_transitions = {
        "staging": {"shadow", "archived"},
        "shadow": {"production", "archived", "staging"},
        "production": {"archived", "shadow"},
        "archived": {"staging"},
    }
    current_stage = ctx.vision_baseline.stage
    if req.to_stage not in legal_transitions.get(current_stage, set()):
        raise HTTPException(
            status_code=409,
            detail=(
                f"illegal transition {current_stage} -> {req.to_stage}; "
                f"legal: {sorted(legal_transitions.get(current_stage, set()))}"
            ),
        )
    # Defensive WSH gate: cannot promote a vision baseline whose
    # safety_critical_defect threshold is below the hard floor.
    if req.to_stage in {"shadow", "production"}:
        sc = ctx.vision_baseline.promoted_thresholds.get(
            "safety_critical_defect", SAFETY_CRITICAL_HARD_FLOOR
        )
        if sc < SAFETY_CRITICAL_HARD_FLOOR:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"refused promotion to {req.to_stage}: safety_critical_defect "
                    f"threshold {sc} below WSH hard floor {SAFETY_CRITICAL_HARD_FLOOR}"
                ),
            )
    ctx.vision_baseline.chosen_arch = req.arch
    ctx.vision_baseline.macro_f1 = ctx.vision_baseline.candidates[req.arch].macro_f1
    ctx.vision_baseline.stage = req.to_stage
    log.info(
        "vision.promote.ok arch=%s from=%s to=%s",
        req.arch,
        current_stage,
        req.to_stage,
    )
    return {
        "arch": req.arch,
        "from_stage": current_stage,
        "to_stage": req.to_stage,
        "macro_f1": ctx.vision_baseline.macro_f1,
    }


@router.get("/registry")
def registry() -> dict[str, Any]:
    ctx = get_context()
    return {
        "current": {
            "arch": ctx.vision_baseline.chosen_arch,
            "stage": ctx.vision_baseline.stage,
            "macro_f1": ctx.vision_baseline.macro_f1,
            "promoted_thresholds": ctx.vision_baseline.promoted_thresholds,
        },
        "candidates": {
            arch: {
                "macro_f1": entry.macro_f1,
                "why": entry.family_why,
            }
            for arch, entry in ctx.vision_baseline.candidates.items()
        },
    }
