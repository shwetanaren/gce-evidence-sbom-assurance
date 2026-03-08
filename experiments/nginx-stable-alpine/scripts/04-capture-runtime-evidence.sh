#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

require_docker

scenario="${1:?scenario is required}"
container_name="${2:?container name is required}"
target_dir="$(scenario_dir "${scenario}")"
rootfs_dir="${target_dir}/rootfs"

mkdir -p "${target_dir}"
rm -rf "${rootfs_dir}"
mkdir -p "${rootfs_dir}"

log "Capturing docker diff for ${scenario}"
docker diff "${container_name}" >"${target_dir}/docker-diff.txt"

log "Capturing container metadata"
docker inspect "${container_name}" >"${target_dir}/container-inspect.json"

log "Exporting runtime filesystem"
docker export "${container_name}" >"${target_dir}/filesystem.tar"

log "Extracting runtime filesystem snapshot"
tar -xf "${target_dir}/filesystem.tar" -C "${rootfs_dir}"

log "Generating runtime CycloneDX SBOM"
syft_scan_dir "${rootfs_dir}" "${target_dir}/runtime-sbom.cdx.json"

if [[ "${KEEP_EXTRACTED_ROOTFS:-0}" != "1" ]]; then
  log "Removing extracted filesystem working directory"
  python3 - "${rootfs_dir}" <<'PY'
import shutil
import sys

shutil.rmtree(sys.argv[1], ignore_errors=True)
PY
fi
