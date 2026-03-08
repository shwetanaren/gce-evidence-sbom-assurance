#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-1-build-time"

BASE_IMAGE="${BASE_IMAGE:-nginx:stable-alpine}"
command -v docker >/dev/null 2>&1 || {
  printf 'Missing required command: docker\n' >&2
  exit 1
}
command -v trivy >/dev/null 2>&1 || {
  printf 'Missing required command: trivy\n' >&2
  exit 1
}

docker info >/dev/null
mkdir -p "${PHASE_DIR}"

docker pull "${BASE_IMAGE}" >/dev/null
docker image inspect "${BASE_IMAGE}" >"${PHASE_DIR}/manifest-build.json"
trivy image --format cyclonedx --output "${PHASE_DIR}/sbom-build-time.json" "${BASE_IMAGE}"
