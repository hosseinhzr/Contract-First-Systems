#!/usr/bin/env bash
# Mechanical verifier: Contract-First standard + ClawHub skill layout.
# Requires: bash, python3 (stdlib only). No package installs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/verify_contract_first.py" "$ROOT"
