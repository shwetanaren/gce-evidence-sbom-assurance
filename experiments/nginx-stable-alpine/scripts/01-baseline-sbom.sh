#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

require_docker
mkdir -p "${BASELINE_DIR}"

log "Pulling ${IMAGE_REF}"
docker pull "${IMAGE_REF}" >/dev/null

log "Writing baseline image metadata"
docker image inspect "${IMAGE_REF}" >"${BASELINE_DIR}/image-inspect.json"

log "Generating baseline CycloneDX SBOM"
syft_scan_image "${IMAGE_REF}" "${BASELINE_DIR}/sbom.cdx.json"

python3 - "${BASELINE_DIR}/sbom.cdx.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
components = data.get("components", [])
print(f"baseline components: {len(components)}")
PY
