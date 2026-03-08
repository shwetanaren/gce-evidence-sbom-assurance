# Scenario Report: expected-runtime-churn

## Inventory Delta

- Baseline inventory components: 73
- Runtime inventory components: 73
- Static SBOM only: 0
- Runtime scan only: 0

## Components Present In Static SBOM Only

None

## Components Present In Runtime Scan Only

None

## File-Level Changes From docker diff

- `C /tmp` -> expected-runtime-churn
- `A /tmp/gce-runtime` -> expected-runtime-churn
- `A /tmp/gce-runtime/heartbeat.txt` -> expected-runtime-churn
- `C /etc` -> configuration-drift
- `C /etc/nginx` -> configuration-drift
- `C /etc/nginx/conf.d` -> configuration-drift
- `C /etc/nginx/conf.d/default.conf` -> configuration-drift
- `C /run` -> expected-runtime-churn
- ... and 10 more

## Classification Counts

{
  "configuration-drift": 4,
  "expected-runtime-churn": 13,
  "unknown-review": 1
}

## Assurance Reading

Static SBOM alone is not sufficient for runtime assurance here. Configuration evidence must accompany the baseline artifact.
