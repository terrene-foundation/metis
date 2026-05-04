#!/usr/bin/env bash
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
PORT="${METIS_VIEWER_PORT:-3000}"
exec python3 -m http.server "$PORT"
