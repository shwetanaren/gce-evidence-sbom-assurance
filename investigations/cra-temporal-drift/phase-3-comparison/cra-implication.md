# CRA Implication

The investigation did not find package-level temporal drift in this runtime
check.

## What This Means For Article 10

- the build-time SBOM still matched the observed live package inventory
- this supports a narrow trust claim for this specific runtime moment
- it does not prove that the claim will remain true over time without
  re-verification

## Governance

Article 10 still points toward continuity. Even when a single runtime check
aligns with the build snapshot, the assurance claim is temporal and should be
re-checked as software, deployment conditions, or initialization logic change.

## Remediation

### Core requirements

- keep build-time SBOM generation as the baseline
- add periodic or event-driven re-verification
- define what evidence preserves trust over time

### Context-dependent choices

- whether deploy-time gating is enough or runtime monitoring is also needed
- how much drift is acceptable for low-risk versus high-risk systems
- whether supplementary evidence should be package-level, filesystem-level, or both

### Stakeholder questions

- which stakeholders rely on the SBOM as a trust artifact
- what freshness standard they expect
- when a previously accurate SBOM should be treated as stale
