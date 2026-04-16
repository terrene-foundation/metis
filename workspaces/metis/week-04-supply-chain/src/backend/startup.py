"""Nexus startup hook: feature-store preload + alias-file bootstrap.

Shard 01 owns this narrow entrypoint. Shard 07 authors the CSV at
`data/northwind_demand.csv` and shard 09 authors `specs/schemas/demand.py`.
Both are READ here; if either is missing at startup time we log a WARNING
and continue so shard 01's tests are not blocked on shard 07/09 landing.

The startup path writes two keys into `.preflight.json` via read-modify-write:
  - `feature_store_populated: true` after register_features + store
  - (the drift_wiring flag is written by a separate shard, not here)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import polars as pl

from .ml_context import MLContext, get_ml_context, init_alias_file

log = logging.getLogger("metis.startup")


def _atomic_json_merge(path: Path, updates: dict[str, Any]) -> None:
    """Read-modify-write a JSON object with atomic rename semantics.

    This preserves any keys other shards may have already written (e.g.
    `drift_wiring: true` from shard 04's wire call) — a full overwrite
    would silently drop them.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, Any] = {}
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except json.JSONDecodeError:
            log.warning(
                "preflight.json is malformed; starting from empty",
                extra={"path": str(path)},
            )
            existing = {}
    if not isinstance(existing, dict):
        existing = {}
    existing.update(updates)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _load_demand_schema() -> Any | None:
    """Import the FeatureSchema authored by shard 09.

    Returns None if the schema file does not exist yet — startup must still
    bring the app up so shard 07/09 don't form a deadlock with shard 01.
    """
    try:
        # Expected layout: workspaces/.../week-04-supply-chain/specs/schemas/demand.py
        # The file declares `schema: FeatureSchema = FeatureSchema(...)`.
        from specs.schemas.demand import schema as demand_schema  # type: ignore
    except Exception as err:  # noqa: BLE001 — we want ALL import-time failures
        log.warning(
            "startup.demand_schema.unavailable",
            extra={"error": repr(err)},
        )
        return None
    return demand_schema


async def preload_feature_store(ctx: MLContext) -> bool:
    """Register the user_demand schema and store the CSV rows.

    Returns True when the preload succeeded end-to-end (ready to serve
    `/forecast/train`); False when CSV or schema is missing and preload was
    skipped.
    """
    schema = _load_demand_schema()
    csv_path = ctx.settings.demand_csv

    if schema is None:
        log.warning(
            "feature_store.preload.skipped.missing_schema",
            extra={"expected": "specs/schemas/demand.py"},
        )
        return False

    if not csv_path.exists():
        log.warning(
            "feature_store.preload.skipped.missing_csv",
            extra={"expected": str(csv_path)},
        )
        return False

    try:
        await ctx.feature_store.register_features(schema)
    except Exception:  # noqa: BLE001 — kailash-ml raises dialect-specific errors
        log.exception("feature_store.register_features.failed")
        return False

    try:
        df = pl.read_csv(csv_path)
    except Exception:  # noqa: BLE001
        log.exception("feature_store.csv_read.failed", extra={"path": str(csv_path)})
        return False

    try:
        # Library signature: store(features: pl.DataFrame, schema: FeatureSchema).
        n_stored = await ctx.feature_store.store(df, schema)
    except Exception:  # noqa: BLE001
        log.exception("feature_store.store.failed")
        return False

    log.info(
        "feature_store.preload.ok",
        extra={"rows": int(n_stored), "schema": getattr(schema, "name", "?")},
    )
    return True


async def run_startup() -> MLContext:
    """End-to-end startup: build context, init alias file, preload FS.

    Idempotent: calling twice does not double-register or double-store
    because (a) the ml_context singleton is cached, (b) register_features
    is a no-op when the schema already exists, (c) store upserts rows by
    entity_id + timestamp.
    """
    ctx = await get_ml_context()

    # Alias file bootstrap is belt-and-suspenders: get_ml_context already
    # called init_alias_file; we re-call to satisfy the shard 01 contract
    # that says "at startup, initialize data/.experiment_aliases.json if
    # absent". Re-initialization is a no-op when the file already exists.
    init_alias_file(ctx.settings.alias_file)

    fs_ok = await preload_feature_store(ctx)
    _atomic_json_merge(
        ctx.settings.preflight_file,
        {"feature_store_populated": bool(fs_ok)},
    )
    return ctx
