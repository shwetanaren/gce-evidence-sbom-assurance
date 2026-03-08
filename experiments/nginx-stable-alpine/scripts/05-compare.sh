#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

scenario="${1:?scenario is required}"
target_dir="$(scenario_dir "${scenario}")"

python3 "${LIB_DIR}/classify_drift.py" compare \
  --scenario "${scenario}" \
  --baseline "${BASELINE_DIR}/sbom.cdx.json" \
  --runtime "${target_dir}/runtime-sbom.cdx.json" \
  --docker-diff "${target_dir}/docker-diff.txt" \
  --json-out "${target_dir}/classification.json" \
  --markdown-out "${target_dir}/report.md"
