"""GET /health — typed-boolean readiness probe.

Contract per canonical-values.md §8.6:
    { ok: bool, db: bool, feature_store: bool, drift_wiring: bool,
      registry_runs: int, nexus_port: int }

All status flags are booleans (not string literals). `scripts/preflight.py`
and the Viewer preflight banner both parse strictly. The endpoint returns
HTTP 200 even when partially-ready so callers can see which specific
component is down.
"""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter

from ..ml_context import get_ml_context

router = APIRouter()
log = logging.getLogger("metis.routes.health")


async def _probe_db(conn) -> bool:
    """Ping the shared ConnectionManager with a trivial SELECT."""
    try:
        row = await conn.fetchone("SELECT 1 AS one")
    except Exception:  # noqa: BLE001 — health must never raise
        log.warning("health.db_probe.failed", exc_info=True)
        return False
    return bool(row)


async def _probe_feature_store(ctx) -> bool:
    """Prefer the .preflight.json flag; fall back to list_schemas()."""
    pf = ctx.settings.preflight_file
    if pf.exists():
        try:
            data = json.loads(pf.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        if isinstance(data, dict) and "feature_store_populated" in data:
            return bool(data["feature_store_populated"])
    try:
        schemas = await ctx.feature_store.list_schemas()
        return len(schemas) > 0
    except Exception:  # noqa: BLE001
        log.warning("health.feature_store_probe.failed", exc_info=True)
        return False


async def _probe_drift_wiring(ctx) -> bool:
    """Read `.preflight.json.drift_wiring` written by drift_wiring.wire()."""
    pf = ctx.settings.preflight_file
    if not pf.exists():
        return False
    try:
        data = json.loads(pf.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if not isinstance(data, dict):
        return False
    return bool(data.get("drift_wiring", False))


async def _probe_registry_runs(ctx) -> int:
    try:
        models = await ctx.model_registry.list_models()
    except Exception:  # noqa: BLE001
        log.warning("health.registry_probe.failed", exc_info=True)
        return 0
    # list_models may return names or (name, version) pairs depending on lib;
    # the contract field is a count of registered runs/model versions.
    if not models:
        return 0
    try:
        return int(len(models))
    except Exception:  # noqa: BLE001
        return 0


@router.get("/health")
async def health_check() -> dict:
    ctx = await get_ml_context()

    db_ok = await _probe_db(ctx.conn)
    fs_ok = await _probe_feature_store(ctx)
    drift_ok = await _probe_drift_wiring(ctx)
    registry_runs = await _probe_registry_runs(ctx)

    return {
        "ok": bool(db_ok),
        "db": bool(db_ok),
        "feature_store": bool(fs_ok),
        "drift_wiring": bool(drift_ok),
        "registry_runs": int(registry_runs),
        "nexus_port": int(ctx.settings.nexus_port),
    }
