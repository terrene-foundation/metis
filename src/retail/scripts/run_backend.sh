#!/usr/bin/env bash
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
# Boot the Arcadia Retail backend.
#
# Run from the repo root:
#   bash src/retail/scripts/run_backend.sh
#
# Honors env: METIS_API_HOST (default 127.0.0.1), METIS_API_PORT (default 8000),
# LOG_LEVEL (default info).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"

if [[ ! -f .venv/bin/uvicorn ]]; then
  echo "✗ .venv/bin/uvicorn missing — run 'uv sync' at the repo root first." >&2
  exit 1
fi

export PYTHONPATH="src/retail:${PYTHONPATH:-}"
HOST="${METIS_API_HOST:-127.0.0.1}"
PORT="${METIS_API_PORT:-8000}"
LOG="${LOG_LEVEL:-info}"

echo "metis.retail.backend starting on http://${HOST}:${PORT} (log=${LOG})"
exec .venv/bin/uvicorn backend.app:app --host "$HOST" --port "$PORT" --log-level "$LOG"
