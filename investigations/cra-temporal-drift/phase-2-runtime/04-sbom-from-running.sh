#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-2-runtime"

container_name="${1:?container name is required}"

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
EXPORT_DIR="$(mktemp -d)"
EXPORT_TAR="${EXPORT_DIR}/running-container.tar"
trap 'rm -rf "${EXPORT_DIR}"' EXIT

docker export "${container_name}" >"${EXPORT_TAR}"
tar -xf "${EXPORT_TAR}" -C "${EXPORT_DIR}"
trivy rootfs --format cyclonedx --output "${PHASE_DIR}/sbom-running.json" "${EXPORT_DIR}"
