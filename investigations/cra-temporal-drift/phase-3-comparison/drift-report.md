# Drift Report

## Question

Can a static build-time SBOM still be trusted once the container is running?

## Counts

- Build-time SBOM packages: 72
- Runtime extracted packages: 72
- Running-container Syft packages: 72

## Present At Build-Time Only

None

## Present At Runtime Only

None

## Version Drift

None

## Running-Container Syft Cross-Check

Runtime-only packages seen by the running-container SBOM:

None

## Accuracy

For this run, the build-time SBOM and live package extraction align at the package level. The trust claim holds only for this observed point in time.

## Utility

The current runtime check does not show package drift, but the trust claim remains time-bound. The evidence is useful for this moment, but later updates, initialization logic, or deployment changes could still make the documentation stale.

## Governance

Accuracy cannot be treated as a one-time generation event. Even when the snapshot currently aligns with runtime state, the assurance obligation is temporal and should be re-verified as the system changes.

## Remediation

Use this result to guide verification design, not to hardcode a single response. Keep build-time generation as a baseline, then decide with stakeholders what deploy-time checks, runtime drift monitoring, and reconciliation thresholds are appropriate for the system context.
