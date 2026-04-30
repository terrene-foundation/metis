# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Router assembly — mounts all moderation endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from . import (
    drift,
    health,
    moderate_fusion,
    moderate_image,
    moderate_text,
    queue,
    state,
)


def build_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health.router)
    router.include_router(state.router, prefix="/state", tags=["state"])
    router.include_router(moderate_image.router, prefix="/moderate/image", tags=["moderate-image"])
    router.include_router(moderate_text.router, prefix="/moderate/text", tags=["moderate-text"])
    router.include_router(
        moderate_fusion.router, prefix="/moderate/fusion", tags=["moderate-fusion"]
    )
    router.include_router(drift.router, prefix="/drift", tags=["drift"])
    router.include_router(queue.router, prefix="/queue", tags=["queue"])
    return router
