# gce-evidence-sbom-assurance

SBOM assurance as an evidence problem, not just an artifact problem.

This repository tests whether an SBOM generated from a static container image
remains trustworthy when checked against runtime filesystem reality.

The immediate experiment starts with `nginx:stable-alpine` and asks a simple
question:

> Is a baseline image SBOM enough, or do we need additional runtime evidence to
> trust the declared inventory?

## Current Experiment

The first lab lives in
[`experiments/nginx-stable-alpine/`](./experiments/nginx-stable-alpine/).

It implements a repeatable flow that:

1. generates a baseline CycloneDX SBOM from the static image with Syft
2. runs the image as a container
3. applies three runtime mutation scenarios
4. captures runtime evidence with `docker diff`, `docker export`, and a Syft
   scan of the exported filesystem
5. compares baseline inventory against runtime evidence
6. classifies the drift and explains what it means for assurance

## Quick Start

```bash
cd experiments/nginx-stable-alpine
./scripts/06-run-sample.sh
```

Artifacts are written into:

- `experiments/nginx-stable-alpine/artifacts/baseline/`
- `experiments/nginx-stable-alpine/artifacts/runtime/`
- `experiments/nginx-stable-alpine/findings/`

## Repository Layout

```text
experiments/nginx-stable-alpine/
  README.md
  scripts/
  lib/
  artifacts/
  findings/
docs/
```

This repo stays markdown-first and portfolio-friendly:

- runnable scripts are kept small and readable
- findings are written as markdown, not hidden in notebook output
- the evidence model is explicit, so the governance argument is inspectable

## Why This Matters

An image can produce an SBOM and still fail as trustworthy evidence at runtime.

That happens when:

- normal runtime churn changes the observed filesystem surface
- configuration drift alters what the software actually does
- material component drift adds or removes packages after the baseline artifact

The governance problem is not only whether tooling can emit an SBOM. The real
question is whether the declared inventory still deserves trust when operations
change the runtime state.

## Regulatory Extensions

This repo is one lab in the broader Governance - Code - Evidence series. The
same evidence-assurance logic can be applied to other regulations and operating
contexts.

| Regulation | Investigation | Status |
| ---------- | ------------- | ------ |
| CRA | nginx SBOM runtime trust | In progress |
| DORA | Terraform drift versus declared control state | Planned |
| GDPR | Consent state reconciliation versus proof claims | Planned |
| EU AI Act | ML pipeline provenance versus operational reality | Planned |

## Methodology

Three-layer evaluation:

1. **Accuracy:** Does the artifact match observed runtime reality?
2. **Utility:** Does the evidence help manage actual risk?
3. **Governance:** Does the assurance posture support regulatory or customer
   proof needs?

## Supporting Docs

- [`experiments/nginx-stable-alpine/README.md`](./experiments/nginx-stable-alpine/README.md)
- [`docs/evidence-model.md`](./docs/evidence-model.md)
