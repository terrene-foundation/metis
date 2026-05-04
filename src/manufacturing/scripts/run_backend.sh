#!/usr/bin/env bash
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
#
# Boot the LumenCircuit Industrial AI backend.
#
# Usage:
#   ./src/manufacturing/scripts/run_backend.sh
#
# Env vars:
#   METIS_API_HOST  default 127.0.0.1
#   METIS_API_PORT  default 8000

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

HOST="${METIS_API_HOST:-127.0.0.1}"
PORT="${METIS_API_PORT:-8000}"

if [[ ! -d "$ROOT/.venv" ]]; then
  echo "ERROR: $ROOT/.venv missing. Run: uv venv && uv sync"
  exit 1
fi

if [[ ! -f "$ROOT/src/manufacturing/data/boards_labelled.csv" ]]; then
  echo "Materialising LumenCircuit dataset..."
  "$ROOT/.venv/bin/python" "$ROOT/src/manufacturing/scripts/generate_data.py"
fi

cd "$ROOT/src"
exec "$ROOT/.venv/bin/python" -m uvicorn manufacturing.backend.app:app --host "$HOST" --port "$PORT" --log-level info
