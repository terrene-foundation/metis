"""Read-only config surface over .env.

Canonical keys enumerated in specs/scaffold-contract.md §10. Every key read
here is sourced from the process environment; shard 09 is the sole writer of
.env.example. We never hard-code ports, DB URLs, or artifact paths.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env(name: str, default: str | None = None, required: bool = False) -> str:
    """Fetch from environment with an explicit required-or-default contract."""
    value = os.environ.get(name)
    if value is None or value == "":
        if required:
            raise RuntimeError(
                f"environment variable {name!r} is required; "
                f"see .env.example (authored by shard 09) for the canonical set"
            )
        value = default or ""
    return value


def _workspace_root() -> Path:
    """Resolve the week-04 workspace root regardless of CWD at import time."""
    env_root = os.environ.get("METIS_WORKSPACE_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    # src/backend/config.py -> ../../.. -> week-04 root
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Resolved runtime settings for the Metis backend."""

    # Ports
    nexus_port: int
    mcp_port: int

    # SQLite URLs
    experiments_url: str
    registry_url: str
    features_url: str

    # Paths (absolute)
    workspace_root: Path
    artifact_dir: Path
    data_dir: Path
    alias_file: Path
    preflight_file: Path
    demand_csv: Path

    # Determinism
    random_seed: int
    automl_seed: int
    drift_seed: int

    # Flags
    automl_quick: bool


def load_settings() -> Settings:
    """Snapshot current environment into a Settings instance.

    Called lazily on first `get_ml_context()` so tests can mutate os.environ
    before the facade is constructed.
    """
    root = _workspace_root()
    artifact_dir = Path(_env("ARTIFACT_DIR", str(root / "data"))).expanduser()
    if not artifact_dir.is_absolute():
        artifact_dir = (root / artifact_dir).resolve()
    artifact_dir.mkdir(parents=True, exist_ok=True)

    data_dir = artifact_dir  # The workshop collapses ARTIFACT_DIR and data/ to one path.

    def _sqlite_url(env_name: str, default_filename: str) -> str:
        raw = _env(env_name, f"sqlite:///{data_dir / default_filename}")
        # Allow relative sqlite URLs like sqlite:///data/.experiments.db -> root-anchor it.
        if raw.startswith("sqlite:///") and not raw.startswith("sqlite:////"):
            rel = raw[len("sqlite:///") :]
            rel_path = Path(rel)
            if not rel_path.is_absolute():
                return f"sqlite:///{(root / rel_path).resolve()}"
        return raw

    return Settings(
        nexus_port=int(_env("KAILASH_NEXUS_PORT", "8000")),
        mcp_port=int(_env("KAILASH_MCP_PORT", "3001")),
        experiments_url=_sqlite_url("DATABASE_URL_EXPERIMENTS", ".experiments.db"),
        registry_url=_sqlite_url("DATABASE_URL_REGISTRY", ".registry.db"),
        features_url=_sqlite_url("DATABASE_URL_FEATURES", ".features.db"),
        workspace_root=root,
        artifact_dir=artifact_dir,
        data_dir=data_dir,
        alias_file=data_dir / ".experiment_aliases.json",
        preflight_file=data_dir / ".preflight.json",
        demand_csv=data_dir / "northwind_demand.csv",
        random_seed=int(_env("RANDOM_SEED", "42")),
        automl_seed=int(_env("AUTOML_SEED", "2026")),
        drift_seed=int(_env("DRIFT_SEED", "78")),
        automl_quick=_env("KAILASH_ML_AUTOML_QUICK", "1") == "1",
    )
