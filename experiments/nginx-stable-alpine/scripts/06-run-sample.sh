#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

require_docker

scenarios=(
  expected-runtime-churn
  configuration-drift
  material-component-drift
)

"${SCRIPT_DIR}/01-baseline-sbom.sh"

for scenario in "${scenarios[@]}"; do
  container_name="$("${SCRIPT_DIR}/02-run-container.sh" "${scenario}")"
  trap 'cleanup_container "${container_name}"' EXIT
  "${SCRIPT_DIR}/03-apply-mutation.sh" "${scenario}" "${container_name}"
  "${SCRIPT_DIR}/04-capture-runtime-evidence.sh" "${scenario}" "${container_name}"
  "${SCRIPT_DIR}/05-compare.sh" "${scenario}"
  cleanup_container "${container_name}"
  trap - EXIT
done

python3 "${LIB_DIR}/classify_drift.py" summarize \
  --runtime-root "${RUNTIME_DIR}" \
  --markdown-out "${FINDINGS_DIR}/sample-run-summary.md"

log "Sample run complete"
log "Summary: ${FINDINGS_DIR}/sample-run-summary.md"
