# Continuous SBOM Verification Architecture

If CRA-style documentation trust is temporal, then remediation is not "generate
a better snapshot." It is "keep deciding whether the snapshot still deserves
trust."

## Core Requirements

- generate the SBOM at build time as a baseline
- verify the baseline again at deploy or release acceptance
- define a way to detect runtime drift where the operating model allows it
- reconcile or refresh documentation when the evidence no longer aligns

## Context-Dependent Choices

These should not be hardcoded across every environment.

They depend on system criticality, operating model, and stakeholder tolerance.

- whether verification happens only at deploy or also during runtime
- whether package-level checks are enough or filesystem-level evidence is needed
- what amount of drift is acceptable before trust is considered broken
- how often evidence must be refreshed

## Stakeholder Questions

These questions should be discussed explicitly with engineering, security,
compliance, product, and operations stakeholders:

- who owns the SBOM accuracy claim after deployment?
- who decides whether observed drift is acceptable?
- what evidence standard is required for regulators, customers, or auditors?
- when should a previously accurate SBOM be treated as stale?

## Suggested Operating Pattern

1. Build-time generation
2. Deploy-time verification
3. Runtime drift monitoring where justified
4. Alerting, review, and reconciliation

## Why This Matters

This turns SBOM assurance from a tooling output into a governable evidence
process. That is the bridge from security tooling to CRA-oriented documentation
trust.
