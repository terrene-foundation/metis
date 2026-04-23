# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Health + readiness endpoints."""

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
            "customers": len(ctx.customers),
            "products": len(ctx.products),
            "transactions": len(ctx.transactions),
            "baseline_silhouette": round(ctx.baseline.silhouette, 4),
            "baseline_k": ctx.baseline.k,
            "baseline_stage": ctx.baseline.stage,
        }
    except RuntimeError as exc:
        return {"status": "degraded", "reason": str(exc)}
