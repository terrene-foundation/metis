# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Route assembly for the LumenCircuit backend."""

from __future__ import annotations

from fastapi import APIRouter

from . import (
    agent,
    drift,
    health,
    inspect_vision,
    optimize_rl,
    predict_maintenance,
    queue,
    state,
)


def build_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health.router)
    router.include_router(inspect_vision.router)
    router.include_router(predict_maintenance.router)
    router.include_router(optimize_rl.router)
    router.include_router(agent.router)
    router.include_router(drift.router)
    router.include_router(queue.router)
    router.include_router(state.router)
    return router
