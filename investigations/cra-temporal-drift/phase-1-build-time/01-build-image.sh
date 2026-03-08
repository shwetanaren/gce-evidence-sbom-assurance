#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INVESTIGATION_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PHASE_DIR="${INVESTIGATION_DIR}/phase-1-build-time"
TMP_DIR="${INVESTIGATION_DIR}/.tmp"

BASE_IMAGE="${BASE_IMAGE:-nginx:stable-alpine}"
LOCAL_IMAGE="${LOCAL_IMAGE:-gce-cra-temporal-drift:nginx-stable-alpine}"
SYFT_IMAGE="${SYFT_IMAGE:-anchore/syft:latest}"

log() {
  printf '[cra-temporal-drift] %s\n' "$*" >&2
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

require_cmd docker python3
docker info >/dev/null

mkdir -p "${PHASE_DIR}" "${TMP_DIR}"
BUILD_CONTEXT="$(mktemp -d "${TMP_DIR}/build-context.XXXXXX")"
trap 'python3 - <<PY
import shutil
shutil.rmtree("'"${BUILD_CONTEXT}"'", ignore_errors=True)
PY' EXIT

cat >"${BUILD_CONTEXT}/Dockerfile" <<EOF
FROM ${BASE_IMAGE}
EOF

log "Building local investigation image ${LOCAL_IMAGE} from ${BASE_IMAGE}"
docker build -t "${LOCAL_IMAGE}" "${BUILD_CONTEXT}" >/dev/null

log "Writing build-time image manifest"
docker image inspect "${LOCAL_IMAGE}" >"${PHASE_DIR}/manifest-build.json"

log "Generating build-time CycloneDX SBOM"
syft_scan_image "${LOCAL_IMAGE}" "${PHASE_DIR}/sbom-build-time.json"

python3 - "${PHASE_DIR}/sbom-build-time.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
components = [c for c in data.get("components", []) if c.get("type") == "library"]
print(f"build-time package components: {len(components)}")
PY
