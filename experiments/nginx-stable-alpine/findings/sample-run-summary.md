# Sample Run Summary

This summary shows how the baseline SBOM behaved once runtime evidence was
collected for each mutation scenario.

| Scenario | Static only | Runtime only | Drift summary |
| -------- | ----------- | ------------ | ------------- |
| configuration-drift | 0 | 0 | configuration-drift=5, expected-runtime-churn=9, unknown-review=1 |
| expected-runtime-churn | 0 | 0 | configuration-drift=4, expected-runtime-churn=13, unknown-review=1 |
| material-component-drift | 0 | 2 | configuration-drift=4, expected-runtime-churn=13, material-component-drift=15, unknown-review=2 |

## What This Shows

The bridge from tooling to governance is not the ability to emit an SBOM. It is
the ability to explain when that artifact still deserves trust and when runtime
evidence is needed to support the claim.

## Next-Step Suggestions

- add mounted-volume scenarios to test evidence blind spots
- compare CycloneDX output with a second inventory approach only after the
  runtime evidence model is stable
- add policy thresholds that say when runtime-only drift should block trust
- capture attestations alongside filesystem evidence for stronger CRA-style
  operational assurance

## configuration-drift

Static SBOM alone is not sufficient for runtime assurance here. Configuration evidence must accompany the baseline artifact.

- Runtime-only components: None
- Static-only components: None
- File changes:
- `C /var` -> unknown-review
- `C /var/cache` -> expected-runtime-churn
- `C /var/cache/nginx` -> expected-runtime-churn
- `A /var/cache/nginx/client_temp` -> expected-runtime-churn
- `A /var/cache/nginx/fastcgi_temp` -> expected-runtime-churn
- `A /var/cache/nginx/proxy_temp` -> expected-runtime-churn
- ... and 9 more

## expected-runtime-churn

Static SBOM alone is not sufficient for runtime assurance here. Configuration evidence must accompany the baseline artifact.

- Runtime-only components: None
- Static-only components: None
- File changes:
- `C /tmp` -> expected-runtime-churn
- `A /tmp/gce-runtime` -> expected-runtime-churn
- `A /tmp/gce-runtime/heartbeat.txt` -> expected-runtime-churn
- `C /etc` -> configuration-drift
- `C /etc/nginx` -> configuration-drift
- `C /etc/nginx/conf.d` -> configuration-drift
- ... and 12 more

## material-component-drift

Static SBOM is not sufficient for runtime trust in this scenario. Additional runtime evidence is required because the runtime inventory contains components absent from the baseline artifact.

- Runtime-only components: jq@1.8.1-r0 (library), oniguruma@6.9.10-r0 (library)
- Static-only components: None
- File changes:
- `C /etc` -> configuration-drift
- `C /etc/nginx` -> configuration-drift
- `C /etc/nginx/conf.d` -> configuration-drift
- `C /etc/nginx/conf.d/default.conf` -> configuration-drift
- `C /etc/apk` -> material-component-drift
- `C /etc/apk/world` -> material-component-drift
- ... and 28 more

