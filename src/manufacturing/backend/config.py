# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Read-only config surface over .env."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _manufacturing_root() -> Path:
    """Root of the manufacturing product module.

    Resolves to `<repo>/src/manufacturing/`. The backend reads its data and
    writes artifacts within this root so multiple products (retail,
    supply_chain, media, manufacturing, etc.) co-exist under a single `src/`
    tree without path collisions.
    """
    env_root = os.environ.get("METIS_MANUFACTURING_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    # src/manufacturing/backend/config.py -> parents[1] = src/manufacturing/
    return Path(__file__).resolve().parents[1]


def _workspace_root() -> Path:
    """Active session workspace — student-facing artifacts land here."""
    env_ws = os.environ.get("METIS_WORKSPACE_ROOT")
    if env_ws:
        candidate = Path(env_ws).expanduser().resolve()
        if candidate.exists():
            return candidate
    # Default: <repo>/workspaces/metis/week-07-manufacturing/
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "workspaces" / "metis" / "week-07-manufacturing"


@dataclass(frozen=True)
class Settings:
    manufacturing_root: Path
    workspace_root: Path
    data_dir: Path
    images_pcb_dir: Path
    images_safety_dir: Path
    artifact_dir: Path
    api_host: str
    api_port: int
    log_level: str


def load_settings() -> Settings:
    mfg = _manufacturing_root()
    workspace = _workspace_root()
    data_dir = mfg / "data"
    images_pcb_dir = data_dir / "images_pcb"
    images_safety_dir = data_dir / "images_safety"
    artifact_dir = workspace / "mlartifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        manufacturing_root=mfg,
        workspace_root=workspace,
        data_dir=data_dir,
        images_pcb_dir=images_pcb_dir,
        images_safety_dir=images_safety_dir,
        artifact_dir=artifact_dir,
        api_host=os.environ.get("METIS_API_HOST", "127.0.0.1"),
        api_port=int(os.environ.get("METIS_API_PORT", "8000")),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
