#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-2-runtime"

container_name="${1:?container name is required}"

log() {
  printf '[cra-temporal-drift] %s\n' "$*" >&2
}

command -v docker >/dev/null 2>&1 || {
  printf 'Missing required command: docker\n' >&2
  exit 1
}

mkdir -p "${PHASE_DIR}"

log "Extracting live package inventory from ${container_name}"
docker exec "${container_name}" sh -lc 'apk info -v | sort' >"${PHASE_DIR}/runtime-packages.txt"
