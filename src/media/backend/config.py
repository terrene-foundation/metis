# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Read-only config surface over .env."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _media_root() -> Path:
    """Root of the media product module.

    Resolves to `<repo>/src/media/`. The backend reads its data and writes
    artifacts within this root so multiple products (retail, supply_chain,
    media, etc.) co-exist under a single `src/` tree without path collisions.
    """
    env_root = os.environ.get("METIS_MEDIA_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    # src/media/backend/config.py -> parents[1] = src/media/
    return Path(__file__).resolve().parents[1]


def _workspace_root() -> Path:
    """Active session workspace — student-facing artifacts land here."""
    env_ws = os.environ.get("METIS_WORKSPACE_ROOT")
    if env_ws:
        candidate = Path(env_ws).expanduser().resolve()
        if candidate.exists():
            return candidate
    # Default: <repo>/workspaces/metis/week-06-media/
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "workspaces" / "metis" / "week-06-media"


@dataclass(frozen=True)
class Settings:
    media_root: Path
    workspace_root: Path
    data_dir: Path
    images_dir: Path
    artifact_dir: Path
    api_host: str
    api_port: int
    log_level: str


def load_settings() -> Settings:
    media = _media_root()
    workspace = _workspace_root()
    data_dir = media / "data"
    images_dir = data_dir / "images"
    artifact_dir = workspace / "mlartifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        media_root=media,
        workspace_root=workspace,
        data_dir=data_dir,
        images_dir=images_dir,
        artifact_dir=artifact_dir,
        api_host=os.environ.get("METIS_API_HOST", "127.0.0.1"),
        api_port=int(os.environ.get("METIS_API_PORT", "8000")),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
