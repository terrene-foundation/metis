#!/usr/bin/env bash
# run_backend.sh — start the Metis Week 4 Nexus backend on port 8000.
#
# TODO-STUDENT: you do NOT edit this script; it is the pre-built launcher.
# If it fails, read the error, then prompt Claude Code to diagnose.
#
# Per canonical-values.md §7: backend listens on localhost:8000 (env
# override KAILASH_NEXUS_PORT). Sources .env if present, falls back to
# defaults if absent. Uses `uv run` per rules/python-environment.md.

set -euo pipefail

# Resolve workspace root (parent of scripts/).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${WORKSPACE_ROOT}"

# Source .env if present, fall back to .env.example defaults otherwise.
# Only export variables that are NOT already set in the user's environment —
# otherwise a user override like `KAILASH_NEXUS_PORT=8877 ./run_backend.sh`
# gets silently clobbered.
_source_env_file() {
    local env_file="$1"
    [[ -f "${env_file}" ]] || return 0
    while IFS= read -r line; do
        # Strip comments and blank lines
        [[ -z "${line}" || "${line}" =~ ^[[:space:]]*# ]] && continue
        # Parse KEY=VALUE (allow leading "export ")
        local kv="${line#export }"
        local key="${kv%%=*}"
        key="${key// /}"
        [[ -z "${key}" ]] && continue
        # Only set if unset (indirect expansion via declare)
        if [[ -z "${!key+x}" ]]; then
            local value="${kv#*=}"
            # Strip surrounding single/double quotes
            value="${value%\"}"; value="${value#\"}"
            value="${value%\'}"; value="${value#\'}"
            export "${key}=${value}"
        fi
    done < "${env_file}"
}

if [[ -f .env ]]; then
    _source_env_file .env
elif [[ -f .env.example ]]; then
    echo "WARN: .env not found; using .env.example defaults. Copy .env.example to .env to customize." >&2
    _source_env_file .env.example
fi

HOST="${KAILASH_NEXUS_HOST:-127.0.0.1}"
PORT="${KAILASH_NEXUS_PORT:-8000}"

# Pre-flight: check the port is free so we fail with a clean message instead
# of a cryptic uvicorn error.
if lsof -iTCP:"${PORT}" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
    echo "ERROR: port ${PORT} is already in use. Kill the existing process or set KAILASH_NEXUS_PORT." >&2
    exit 2
fi

echo "Starting Metis backend on http://${HOST}:${PORT} ..."
echo "Endpoints: /health /forecast/{train,compare,predict} /optimize/solve /drift/check"
echo "All endpoints except /health return 501 until students commission them via Claude Code."
echo ""

# Use uv run per rules/python-environment.md — resolves .venv implicitly.
# Fall back to explicit .venv/bin/python if uv is not available.
if command -v uv >/dev/null 2>&1; then
    exec uv run python -m src.backend.app
elif [[ -x ".venv/bin/python" ]]; then
    exec .venv/bin/python -m src.backend.app
else
    echo "ERROR: neither 'uv' nor '.venv/bin/python' available. Run 'uv venv && uv sync' first." >&2
    exit 3
fi
