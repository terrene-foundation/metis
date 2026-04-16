"""Route mounting for the Metis Nexus backend.

Per scaffold-contract.md §2, this module:
  - Mounts the fully PRE-BUILT routes: /health.
  - Ships 501-stub registrations for the STUDENT-COMMISSIONED endpoints
    (/forecast/*, /optimize/solve, /drift/check). Registrations live from
    commit 1 so orphan-detection Rule 1 is satisfied the moment the scaffold
    lands. Students replace handler bodies, not registrations.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import drift, forecast, health, optimize


def build_router() -> APIRouter:
    """Compose the top-level router mounted by `app.include_router`."""
    router = APIRouter()
    router.include_router(health.router)
    router.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
    router.include_router(optimize.router, prefix="/optimize", tags=["optimize"])
    router.include_router(drift.router, prefix="/drift", tags=["drift"])
    return router


__all__ = ["build_router"]
