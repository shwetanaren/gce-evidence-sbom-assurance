#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ARTIFACTS_DIR="${EXPERIMENT_DIR}/artifacts"
BASELINE_DIR="${ARTIFACTS_DIR}/baseline"
RUNTIME_DIR="${ARTIFACTS_DIR}/runtime"
FINDINGS_DIR="${EXPERIMENT_DIR}/findings"
LIB_DIR="${EXPERIMENT_DIR}/lib"

IMAGE_REF="${IMAGE_REF:-nginx:stable-alpine}"
SYFT_IMAGE="${SYFT_IMAGE:-anchore/syft:latest}"
CONTAINER_PREFIX="${CONTAINER_PREFIX:-gce-sbom}"

scenario_dir() {
  printf '%s/%s\n' "${RUNTIME_DIR}" "$1"
}

container_name_for() {
  printf '%s-%s\n' "${CONTAINER_PREFIX}" "$1"
}

log() {
  printf '[gce-sbom] %s\n' "$*" >&2
}

require_cmd() {
  local cmd
  for cmd in "$@"; do
    command -v "${cmd}" >/dev/null 2>&1 || {
      printf 'Missing required command: %s\n' "${cmd}" >&2
      exit 1
    }
  done
}

require_docker() {
  require_cmd docker tar python3
  docker info >/dev/null 2>&1 || {
    printf 'Docker daemon is not available.\n' >&2
    exit 1
  }
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

syft_scan_image() {
  local image_ref="$1"
  local output_path="$2"

  if command -v syft >/dev/null 2>&1; then
    syft "docker:${image_ref}" -o cyclonedx-json >"${output_path}"
    return
  fi

  ensure_syft_runtime
  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    "${SYFT_IMAGE}" "docker:${image_ref}" -o cyclonedx-json >"${output_path}"
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

cleanup_container() {
  docker rm -f "$1" >/dev/null 2>&1 || true
}
