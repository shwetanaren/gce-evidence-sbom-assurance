# gce-evidence-sbom-assurance

This repo tests SBOM assurance as an evidence problem.

The question is simple: a container can produce an SBOM at build time, but can
that SBOM still be trusted once the container is running?

## Current Investigation

Current investigation:
[`investigations/cra-temporal-drift/`](./investigations/cra-temporal-drift/)

It uses `nginx:stable-alpine` and follows four phases:

1. capture build-time evidence
2. extract live runtime state
3. compare build-time versus runtime
4. describe what continuous verification would need to look like

## Quick Start

```bash
cd investigations/cra-temporal-drift
./phase-1-build-time/01-build-image.sh
./phase-2-runtime/02-run-and-extract.sh
python3 ./phase-3-comparison/05-compare-build-vs-runtime.py
```

## Why This Matters

CRA Article 10 is not just a documentation problem. It is an accuracy problem
over time.

A build-time SBOM is a snapshot. The real question is:

- does the runtime still match the snapshot?
- if not, how would the organization know?
- what evidence would prove that the inventory claim is still valid?

## Regulatory Extensions

This repo is one investigation in the broader Governance - Code - Evidence
series. The same method can be reused in other domains.

| Regulation | Investigation | Status |
| ---------- | ------------- | ------ |
| CRA | Temporal drift between static SBOM and runtime reality | In progress |
| DORA | Declared control state versus operational drift | Planned |
| GDPR | Consent artifact versus effective runtime state | Planned |
| EU AI Act | Model pipeline documentation versus deployed behavior | Planned |

## Repo Shape

The repo is centered on one investigation surface:

```text
investigations/
  cra-temporal-drift/
```
