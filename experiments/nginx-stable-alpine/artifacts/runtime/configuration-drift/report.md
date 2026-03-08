# Scenario Report: configuration-drift

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

- `C /var` -> unknown-review
- `C /var/cache` -> expected-runtime-churn
- `C /var/cache/nginx` -> expected-runtime-churn
- `A /var/cache/nginx/client_temp` -> expected-runtime-churn
- `A /var/cache/nginx/fastcgi_temp` -> expected-runtime-churn
- `A /var/cache/nginx/proxy_temp` -> expected-runtime-churn
- `A /var/cache/nginx/scgi_temp` -> expected-runtime-churn
- `A /var/cache/nginx/uwsgi_temp` -> expected-runtime-churn
- ... and 7 more

## Classification Counts

{
  "configuration-drift": 5,
  "expected-runtime-churn": 9,
  "unknown-review": 1
}

## Assurance Reading

Static SBOM alone is not sufficient for runtime assurance here. Configuration evidence must accompany the baseline artifact.
