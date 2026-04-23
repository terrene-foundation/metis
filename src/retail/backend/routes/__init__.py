# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Router assembly — mounts all endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from . import allocate, drift, health, predict, recommend, segment, state


def build_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health.router)
    router.include_router(state.router, prefix="/state", tags=["state"])
    router.include_router(segment.router, prefix="/segment", tags=["segment"])
    router.include_router(predict.router, prefix="/predict", tags=["predict"])
    router.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
    router.include_router(allocate.router, prefix="/allocate", tags=["allocate"])
    router.include_router(drift.router, prefix="/drift", tags=["drift"])
    return router
