#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE="${IMAGE:-nginx:stable-alpine}"
CONTAINER_NAME="${CONTAINER_NAME:-cra-temporal-drift-nginx}"

command -v docker >/dev/null 2>&1 || {
  printf 'Missing required command: docker\n' >&2
  exit 1
}
docker info >/dev/null

docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
docker run -d --name "${CONTAINER_NAME}" "${IMAGE}" >/dev/null
trap 'docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true' EXIT

"${SCRIPT_DIR}/03-extract-from-running.sh" "${CONTAINER_NAME}"
"${SCRIPT_DIR}/04-sbom-from-running.sh" "${CONTAINER_NAME}"
