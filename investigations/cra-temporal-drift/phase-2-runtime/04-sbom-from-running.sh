#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-2-runtime"
TMP_DIR="${INVESTIGATION_DIR}/.tmp"

container_name="${1:?container name is required}"
SYFT_IMAGE="${SYFT_IMAGE:-anchore/syft:latest}"

log() {
  printf '[cra-temporal-drift] %s\n' "$*" >&2
}

ensure_syft_runtime() {
  if command -v syft >/dev/null 2>&1; then
    return
  fi

  docker image inspect "${SYFT_IMAGE}" >/dev/null 2>&1 || {
    log "Pulling ${SYFT_IMAGE} for Syft fallback"
    docker pull "${SYFT_IMAGE}" >/dev/null
  }
}

syft_scan_dir() {
  local target_dir="$1"
  local output_path="$2"

  if command -v syft >/dev/null 2>&1; then
    syft "dir:${target_dir}" -o cyclonedx-json >"${output_path}"
    return
  fi

  ensure_syft_runtime
  docker run --rm \
    -v "${target_dir}:/scan:ro" \
    "${SYFT_IMAGE}" "dir:/scan" -o cyclonedx-json >"${output_path}"
}

command -v docker >/dev/null 2>&1 || {
  printf 'Missing required command: docker\n' >&2
  exit 1
}
docker info >/dev/null

mkdir -p "${PHASE_DIR}" "${TMP_DIR}"
EXPORT_DIR="$(mktemp -d "${TMP_DIR}/runtime-rootfs.XXXXXX")"
EXPORT_TAR="${TMP_DIR}/running-container.tar"
trap 'python3 - <<PY
from pathlib import Path
import shutil

export_tar = Path("'"${EXPORT_TAR}"'")
if export_tar.exists():
    export_tar.unlink()
shutil.rmtree("'"${EXPORT_DIR}"'", ignore_errors=True)
PY' EXIT

log "Exporting running container filesystem"
docker export "${container_name}" >"${EXPORT_TAR}"
tar -xf "${EXPORT_TAR}" -C "${EXPORT_DIR}"

log "Generating CycloneDX SBOM from running container snapshot"
syft_scan_dir "${EXPORT_DIR}" "${PHASE_DIR}/sbom-running.json"
