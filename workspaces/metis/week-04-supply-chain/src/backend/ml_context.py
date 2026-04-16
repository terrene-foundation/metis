"""Facade over kailash-ml engines sharing a single ConnectionManager.

This module is the single construction site for FeatureStore, ModelRegistry,
ExperimentTracker, DriftMonitor, and InferenceServer. Every route handler in
src/backend/routes/ imports `get_ml_context()` and reaches the engines through
the returned facade. Constructing engines elsewhere is BLOCKED by policy
(orphan-detection and facade-manager-detection rules).

Invariant (shard 01): all four stateful engines share a single
`ConnectionManager.id` — asserted by tests/integration/test_ml_context_wiring.py.
Because kailash-ml's ConnectionManager takes one URL, "shared" requires one
SQLite file for all engines. The three separate DATABASE_URL_* env vars from
canonical-values.md §7 are retained as informational keys; the shard invariant
("one ConnectionManager instance") overrides, so at runtime we collapse to a
single shared URL (`METIS_ML_DB_URL`, default `sqlite:///data/.ml.db`). This
deviation is called out in the shard deliverable.

Key helpers:
  - get_ml_context()                  — singleton facade
  - reset_ml_context()                — test-only teardown
  - derive_model_version_id(n, v)    — "{name}_v{version}"
  - parse_model_version_id(mvid)     — (name, version)
  - resolve_experiment_run_id(id)    — accepts UUID4 or alias; raises on unknown
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from kailash_ml.engines.drift_monitor import DriftMonitor
from kailash_ml.engines.experiment_tracker import (
    ExperimentTracker,
    RunNotFoundError,
)
from kailash_ml.engines.feature_store import ConnectionManager, FeatureStore
from kailash_ml.engines.inference_server import InferenceServer
from kailash_ml.engines.model_registry import (
    LocalFileArtifactStore,
    ModelRegistry,
)

from .config import Settings, load_settings

log = logging.getLogger("metis.ml_context")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class ExperimentRunIdUnresolvable(KeyError):
    """Raised when an experiment_run_id cannot be resolved via alias OR tracker."""


class ModelVersionIdMalformed(ValueError):
    """Raised when `{name}_v{version}` parsing fails."""


# ---------------------------------------------------------------------------
# Derived-ID helpers (canonical-values.md §5)
# ---------------------------------------------------------------------------


_MODEL_VERSION_ID_RE = re.compile(r"^(?P<name>.+)_v(?P<version>\d+)$")


def derive_model_version_id(name: str, version: int) -> str:
    """Compose the workshop's derived model-version display ID."""
    if not isinstance(name, str) or not name:
        raise ModelVersionIdMalformed("model name must be a non-empty string")
    if not isinstance(version, int) or version < 1:
        raise ModelVersionIdMalformed("model version must be a positive int")
    return f"{name}_v{version}"


def parse_model_version_id(mvid: str) -> tuple[str, int]:
    """Split `{name}_v{version}` back into (name, version).

    Raises ModelVersionIdMalformed on any input that doesn't match the regex.
    """
    if not isinstance(mvid, str):
        raise ModelVersionIdMalformed("model_version_id must be a string")
    match = _MODEL_VERSION_ID_RE.match(mvid)
    if not match:
        raise ModelVersionIdMalformed(
            f"model_version_id {mvid!r} invalid; expected format <name>_v<int>"
        )
    return match.group("name"), int(match.group("version"))


# ---------------------------------------------------------------------------
# Experiment alias file I/O
# ---------------------------------------------------------------------------


def _is_uuid4(value: str) -> bool:
    """Accept the canonical UUID4 hyphenated form (36 chars).

    We validate via `uuid.UUID` rather than regex to catch the narrow cases
    that look right but aren't valid hex.
    """
    if not isinstance(value, str) or len(value) != 36:
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.version == 4


def init_alias_file(alias_path: Path) -> None:
    """Create `data/.experiment_aliases.json` as `{}` if it doesn't exist.

    Shard 02's first train call appends to this file; we bootstrap it here so
    the append path has a predictable starting state.
    """
    if alias_path.exists():
        return
    alias_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = alias_path.with_suffix(alias_path.suffix + ".tmp")
    tmp.write_text("{}\n", encoding="utf-8")
    os.replace(tmp, alias_path)
    log.info("ml_context.alias_file.initialized", extra={"path": str(alias_path)})


def _load_aliases(alias_path: Path) -> dict[str, str]:
    if not alias_path.exists():
        return {}
    try:
        with alias_path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError:
        log.warning(
            "ml_context.alias_file.invalid_json; treating as empty",
            extra={"path": str(alias_path)},
        )
        return {}
    if not isinstance(raw, dict):
        return {}
    # Keep only string -> string entries to keep downstream typing honest.
    return {str(k): str(v) for k, v in raw.items() if isinstance(v, str)}


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------


@dataclass
class MLContext:
    """Runtime bundle of kailash-ml engines + metadata.

    Every engine below was constructed with `self.conn` (the single shared
    ConnectionManager). That identity is what
    test_ml_context_wiring.py asserts.
    """

    settings: Settings
    conn: ConnectionManager
    feature_store: FeatureStore
    model_registry: ModelRegistry
    experiment_tracker: ExperimentTracker
    drift_monitor: DriftMonitor
    inference_server: InferenceServer

    async def close(self) -> None:
        """Release the shared connection (tests and graceful shutdown)."""
        try:
            await self.drift_monitor.shutdown()
        except Exception:  # noqa: BLE001 — best-effort teardown
            log.warning("ml_context.close.drift_shutdown_failed", exc_info=True)
        try:
            await self.conn.close()
        except Exception:  # noqa: BLE001
            log.warning("ml_context.close.conn_close_failed", exc_info=True)

    # --- Alias resolver (canonical-values.md §12) ------------------------

    async def resolve_experiment_run_id(self, id_or_alias: str) -> str:
        """Return the canonical UUID4 for an alias OR pass through a UUID4.

        Raises ExperimentRunIdUnresolvable when neither interpretation
        resolves via ExperimentTracker.get_run.
        """
        if not isinstance(id_or_alias, str) or not id_or_alias:
            raise ExperimentRunIdUnresolvable("id_or_alias must be a non-empty string")

        # Case 1: input is already a UUID4 — confirm against the tracker.
        if _is_uuid4(id_or_alias):
            try:
                await self.experiment_tracker.get_run(id_or_alias)
            except RunNotFoundError as err:
                raise ExperimentRunIdUnresolvable(
                    f"run_id {id_or_alias!r} not found in ExperimentTracker"
                ) from err
            return id_or_alias

        # Case 2: input is an alias — look up in the alias file, then confirm.
        aliases = _load_aliases(self.settings.alias_file)
        if id_or_alias in aliases:
            canonical = aliases[id_or_alias]
            try:
                await self.experiment_tracker.get_run(canonical)
            except RunNotFoundError as err:
                raise ExperimentRunIdUnresolvable(
                    f"alias {id_or_alias!r} maps to {canonical!r} but tracker " f"has no such run"
                ) from err
            return canonical

        raise ExperimentRunIdUnresolvable(
            f"{id_or_alias!r} is neither a valid UUID4 nor a known alias in "
            f"{self.settings.alias_file}"
        )


# Module-level singleton. Rebuilt by `reset_ml_context()` in tests.
_ctx: Optional[MLContext] = None
_ctx_lock = asyncio.Lock()


async def _build_context(settings: Settings | None = None) -> MLContext:
    """Construct a fresh MLContext with a single shared ConnectionManager."""
    s = settings or load_settings()

    # Init the alias file bootstrap as part of context construction so the
    # first call to resolve_experiment_run_id on a fresh workspace has a
    # valid starting dict. Shard 02 appends atomically from there.
    init_alias_file(s.alias_file)

    # One URL, one ConnectionManager — shared by every engine below.
    shared_url = os.environ.get("METIS_ML_DB_URL") or f"sqlite:///{s.data_dir / '.ml.db'}"
    conn = ConnectionManager(shared_url)
    await conn.initialize()

    feature_store = FeatureStore(conn)
    artifact_store = LocalFileArtifactStore(root_dir=s.artifact_dir / "artifacts")
    model_registry = ModelRegistry(conn, artifact_store=artifact_store)
    experiment_tracker = ExperimentTracker(conn, artifact_root=str(s.artifact_dir / "mlartifacts"))
    drift_monitor = DriftMonitor(conn)
    inference_server = InferenceServer(model_registry)

    log.info(
        "ml_context.built",
        extra={
            "conn_id": id(conn),
            "shared_url": shared_url,
            "artifact_dir": str(s.artifact_dir),
        },
    )

    return MLContext(
        settings=s,
        conn=conn,
        feature_store=feature_store,
        model_registry=model_registry,
        experiment_tracker=experiment_tracker,
        drift_monitor=drift_monitor,
        inference_server=inference_server,
    )


async def get_ml_context(settings: Settings | None = None) -> MLContext:
    """Return the singleton MLContext, constructing it on first call.

    Concurrent callers race through the asyncio lock so the engines are
    constructed exactly once.
    """
    global _ctx
    if _ctx is not None:
        return _ctx
    async with _ctx_lock:
        if _ctx is None:
            _ctx = await _build_context(settings)
    return _ctx


async def reset_ml_context() -> None:
    """Drop and close the singleton. Intended for test teardown."""
    global _ctx
    async with _ctx_lock:
        if _ctx is not None:
            await _ctx.close()
            _ctx = None
