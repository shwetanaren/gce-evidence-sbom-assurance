# Scenario Report: material-component-drift

## Inventory Delta

- Baseline inventory components: 73
- Runtime inventory components: 75
- Static SBOM only: 0
- Runtime scan only: 2

## Components Present In Static SBOM Only

None

## Components Present In Runtime Scan Only

jq@1.8.1-r0 (library), oniguruma@6.9.10-r0 (library)

## File-Level Changes From docker diff

- `C /etc` -> configuration-drift
- `C /etc/nginx` -> configuration-drift
- `C /etc/nginx/conf.d` -> configuration-drift
- `C /etc/nginx/conf.d/default.conf` -> configuration-drift
- `C /etc/apk` -> material-component-drift
- `C /etc/apk/world` -> material-component-drift
- `C /lib` -> material-component-drift
- `C /lib/apk` -> material-component-drift
- ... and 26 more

## Classification Counts

{
  "configuration-drift": 4,
  "expected-runtime-churn": 13,
  "material-component-drift": 15,
  "unknown-review": 2
}

## Assurance Reading

Static SBOM is not sufficient for runtime trust in this scenario. Additional runtime evidence is required because the runtime inventory contains components absent from the baseline artifact.
