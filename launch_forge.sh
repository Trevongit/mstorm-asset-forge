#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

# Activate local virtualenv when available.
if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

# Prefer the control-room startup path when present.
if [[ -x "./scripts/conductor.sh" ]]; then
  exec ./scripts/conductor.sh dashboard
fi

# Fallback: run the forge CLI help.
exec python3 main_forge.py --help
