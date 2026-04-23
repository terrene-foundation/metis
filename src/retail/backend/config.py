# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Read-only config surface over .env."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _retail_root() -> Path:
    """Root of the retail product module.

    Resolves to `<repo>/src/retail/`. The backend reads its data and writes
    artifacts within this root so multiple products (supply_chain, retail,
    etc.) co-exist under a single `src/` tree without path collisions.
    """
    env_root = os.environ.get("METIS_RETAIL_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    # src/retail/backend/config.py -> parents[1] = src/retail/
    return Path(__file__).resolve().parents[1]


def _workspace_root() -> Path:
    """Active session workspace — student-facing artifacts land here."""
    env_ws = os.environ.get("METIS_WORKSPACE_ROOT")
    if env_ws:
        candidate = Path(env_ws).expanduser().resolve()
        if candidate.exists():
            return candidate
    # Default: <repo>/workspaces/metis/week-05-retail/
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "workspaces" / "metis" / "week-05-retail"


@dataclass(frozen=True)
class Settings:
    retail_root: Path
    workspace_root: Path
    data_dir: Path
    artifact_dir: Path
    api_host: str
    api_port: int
    log_level: str


def load_settings() -> Settings:
    retail = _retail_root()
    workspace = _workspace_root()
    data_dir = retail / "data"
    artifact_dir = workspace / "mlartifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        retail_root=retail,
        workspace_root=workspace,
        data_dir=data_dir,
        artifact_dir=artifact_dir,
        api_host=os.environ.get("METIS_API_HOST", "127.0.0.1"),
        api_port=int(os.environ.get("METIS_API_PORT", "8000")),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
