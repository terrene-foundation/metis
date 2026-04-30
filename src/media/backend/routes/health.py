# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Health + readiness endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from ..ml_context import get_context

router = APIRouter()


@router.get("/health")
def health() -> dict:
    try:
        ctx = get_context()
        return {
            "status": "ok",
            "posts": len(ctx.posts),
            "image_posts": (
                int(ctx.posts["has_image"].sum()) if "has_image" in ctx.posts.columns else 0
            ),
            "text_posts": (
                int(ctx.posts["has_text"].sum()) if "has_text" in ctx.posts.columns else 0
            ),
            "multi_modal_posts": (
                int(ctx.posts["has_image_and_text"].sum())
                if "has_image_and_text" in ctx.posts.columns
                else 0
            ),
            "image_baseline_macro_f1": round(ctx.image_baseline.macro_f1, 4),
            "text_baseline_macro_f1": round(ctx.text_baseline.macro_f1, 4),
            "fusion_baseline_macro_f1": round(ctx.fusion_baseline.macro_f1, 4),
            "drift_baselines_registered": ctx.drift_baselines_registered,
        }
    except RuntimeError as exc:
        return {"status": "degraded", "reason": str(exc)}
