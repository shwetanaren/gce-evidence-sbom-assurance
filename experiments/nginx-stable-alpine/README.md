# nginx:stable-alpine Runtime Assurance Experiment

This experiment tests whether a static SBOM remains trustworthy once the image
is executed and the runtime filesystem starts to move.

## Goal

Build a repeatable experiment that compares:

- a baseline image SBOM generated with Syft
- runtime evidence captured after controlled mutations

The trust question is:

> Does the declared inventory still deserve trust once runtime behavior,
> configuration changes, or material package drift are introduced?

## Scenarios

The experiment applies three mutation scenarios to `nginx:stable-alpine`:

1. `expected-runtime-churn`
   Normal temp/cache style filesystem movement that should not be treated as a
   supply-chain surprise.
2. `configuration-drift`
   Runtime configuration changes that alter behavior without necessarily changing
   the package inventory.
3. `material-component-drift`
   Post-start package installation that materially changes the runtime software
   inventory.

## Flow

```text
baseline image -> baseline SBOM
              -> run container
              -> mutate scenario
              -> docker diff
              -> docker export
              -> Syft scan of exported filesystem
              -> compare + classify drift
              -> findings summary
```

## File Tree

```text
experiments/nginx-stable-alpine/
  README.md
  scripts/
    common.sh
    01-baseline-sbom.sh
    02-run-container.sh
    03-apply-mutation.sh
    04-capture-runtime-evidence.sh
    05-compare.sh
    06-run-sample.sh
  lib/
    classify_drift.py
  artifacts/
    baseline/
    runtime/
      expected-runtime-churn/
      configuration-drift/
      material-component-drift/
  findings/
    sample-run-summary.md
```

## Run

Run the full sample:

```bash
./scripts/06-run-sample.sh
```

Run the steps manually:

```bash
./scripts/01-baseline-sbom.sh
container_name="$(./scripts/02-run-container.sh)"
./scripts/03-apply-mutation.sh expected-runtime-churn "$container_name"
./scripts/04-capture-runtime-evidence.sh expected-runtime-churn "$container_name"
./scripts/05-compare.sh expected-runtime-churn
docker rm -f "$container_name"
```

## Outputs

Each scenario produces:

- `docker-diff.txt`
- `filesystem.tar`
- `runtime-sbom.cdx.json`
- `classification.json`
- `report.md`

The experiment also produces:

- baseline image SBOM
- a sample findings summary

## CRA-Oriented Reading

This is relevant to CRA-style operationalization because it tests whether the
artifact used to represent component inventory still supports trustworthy
operational assurance after deployment.

The experiment does not claim direct legal compliance. It demonstrates the
evidence gap between:

- producing an inventory artifact
- proving that the artifact still reflects operational reality

## Limitations

- mounted volumes are out of scope for this first pass
- runtime memory state is not captured
- containerized Syft scanning relies on exported filesystem snapshots
- package-level comparison is only as strong as what Syft can identify in the
  exported root filesystem
- runtime churn can create noise that needs policy judgment, not just tooling
