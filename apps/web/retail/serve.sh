#!/usr/bin/env bash
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
# Serve the retail viewer on http://localhost:3000
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
PORT="${PORT:-3000}"
echo "metis.retail.viewer http://127.0.0.1:${PORT}"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
