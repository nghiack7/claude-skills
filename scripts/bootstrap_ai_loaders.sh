#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

args=(
  install
  --source "$ROOT/skills"
  --output "$ROOT/.generated"
)

while (($#)); do
  case "$1" in
    --cursor-repo)
      if (($# < 2)); then
        echo "missing value for --cursor-repo" >&2
        exit 1
      fi
      args+=(--cursor-repo "$2")
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

"$PYTHON_BIN" "$ROOT/scripts/universal_skill_loader.py" "${args[@]}"

echo "Shared skill adapters installed."
echo "Generated output: $ROOT/.generated"
