# Evidence Model

This repository treats SBOM assurance as an evidence question.

## Core Claim

A static SBOM is an artifact. Assurance depends on whether that artifact still
deserves trust after the workload is running.

## Evidence Layers

1. **Artifact evidence**
   The baseline SBOM generated from the image before runtime changes occur.
2. **Runtime evidence**
   Filesystem and package observations captured after the container has started.
3. **Interpretive evidence**
   A classification model that explains whether the observed deltas represent
   normal churn, configuration drift, or material component drift.

## Why The Classification Model Matters

Without interpretation, filesystem differences are just noise.

The point of the model is to separate:

- operationally expected changes
- behavior-changing configuration changes
- inventory-changing component changes

That is the bridge from tooling to governance. The evidence becomes useful only
once the organization can explain what changed and why it matters for trust.

## When Static SBOM May Be Enough

Static SBOM may be enough when:

- the deployment model is tightly controlled
- runtime mutation is intentionally minimized
- expected churn is explicitly scoped
- there is confidence that no material post-build component changes occur

## When Additional Evidence Is Needed

Additional runtime evidence is needed when:

- packages can be added or removed after build time
- configuration changes materially alter runtime behavior
- mounted volumes or runtime initialization change effective state
- assurance claims must withstand regulatory or customer scrutiny
