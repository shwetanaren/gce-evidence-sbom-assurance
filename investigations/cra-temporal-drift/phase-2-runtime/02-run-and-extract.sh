#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-2-runtime"

LOCAL_IMAGE="${LOCAL_IMAGE:-gce-cra-temporal-drift:nginx-stable-alpine}"
CONTAINER_NAME="${CONTAINER_NAME:-cra-temporal-drift-nginx}"

log() {
  printf '[cra-temporal-drift] %s\n' "$*" >&2
}

cleanup_container() {
  docker rm -f "$1" >/dev/null 2>&1 || true
}

command -v docker >/dev/null 2>&1 || {
  printf 'Missing required command: docker\n' >&2
  exit 1
}
docker info >/dev/null

mkdir -p "${PHASE_DIR}"
cleanup_container "${CONTAINER_NAME}"

log "Running container ${CONTAINER_NAME} from ${LOCAL_IMAGE}"
docker run -d --name "${CONTAINER_NAME}" "${LOCAL_IMAGE}" >/dev/null
trap 'cleanup_container "${CONTAINER_NAME}"' EXIT

printf '%s\n' "${CONTAINER_NAME}" >"${PHASE_DIR}/container-name.txt"

"${SCRIPT_DIR}/03-extract-from-running.sh" "${CONTAINER_NAME}"
"${SCRIPT_DIR}/04-sbom-from-running.sh" "${CONTAINER_NAME}"

log "Runtime extraction complete"
