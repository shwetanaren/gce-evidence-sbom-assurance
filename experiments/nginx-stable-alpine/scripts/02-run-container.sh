#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

require_docker

scenario="${1:-sample}"
container_name="$(container_name_for "${scenario}")"

cleanup_container "${container_name}"

log "Starting container ${container_name} from ${IMAGE_REF}"
docker run -d --name "${container_name}" "${IMAGE_REF}" >/dev/null

printf '%s\n' "${container_name}"
