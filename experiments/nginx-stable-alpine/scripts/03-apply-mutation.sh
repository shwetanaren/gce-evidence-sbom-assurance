#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

require_docker

scenario="${1:?scenario is required}"
container_name="${2:?container name is required}"
target_dir="$(scenario_dir "${scenario}")"

mkdir -p "${target_dir}"

case "${scenario}" in
  expected-runtime-churn)
    log "Applying expected runtime churn"
    docker exec "${container_name}" sh -lc '
      mkdir -p /tmp/gce-runtime /var/cache/nginx/client_temp
      printf "runtime-generated\n" >/tmp/gce-runtime/heartbeat.txt
      printf "cache\n" >/var/cache/nginx/client_temp/request.cache
      touch /var/log/nginx/access.log
    '
    ;;
  configuration-drift)
    log "Applying configuration drift"
    docker exec "${container_name}" sh -lc '
      cat >/etc/nginx/conf.d/runtime-drift.conf <<EOF
server {
    listen 8080;
    location /runtime-drift {
        return 200 "runtime-drift";
    }
}
EOF
    '
    ;;
  material-component-drift)
    log "Applying material component drift"
    docker exec "${container_name}" sh -lc '
      apk add --no-cache jq >/tmp/gce-apk-install.log
    '
    ;;
  *)
    printf 'Unknown scenario: %s\n' "${scenario}" >&2
    exit 1
    ;;
esac

printf '%s\n' "${scenario}" >"${target_dir}/scenario.txt"
