# gce-evidence-sbom-assurance

This repository investigates SBOM assurance as a temporal evidence problem.

The central question is not only whether software can produce an SBOM at build
time. It is whether that build-time snapshot still deserves trust once the
container is actually running.

## Current Investigation

The current investigation lives in
[`investigations/cra-temporal-drift/`](./investigations/cra-temporal-drift/).

It asks:

> Can you trust a static SBOM once the container is running?

The investigation uses `nginx:stable-alpine` and follows a clean four-phase
flow:

1. capture build-time evidence
2. extract live runtime state
3. compare build-time versus runtime
4. explain the remediation architecture needed for continuous trust

## Quick Start

```bash
cd investigations/cra-temporal-drift
./phase-1-build-time/01-build-image.sh
./phase-2-runtime/02-run-and-extract.sh
python3 ./phase-3-comparison/05-compare-build-vs-runtime.py
```

## Why This Matters

CRA Article 10 is fundamentally an evidence problem.

If technical documentation is supposed to reflect reality, then a build-time
SBOM on its own is only a snapshot. The trust question becomes temporal:

- does the runtime still match the snapshot?
- if not, how would the organization know?
- what evidence would prove that the inventory claim is still valid?

## Regulatory Extensions

This repo is one lab in the broader Governance - Code - Evidence series. The
same assurance logic can later be applied to other regulatory domains.

| Regulation | Investigation | Status |
| ---------- | ------------- | ------ |
| CRA | Temporal drift between static SBOM and runtime reality | In progress |
| DORA | Declared control state versus operational drift | Planned |
| GDPR | Consent artifact versus effective runtime state | Planned |
| EU AI Act | Model pipeline documentation versus deployed behavior | Planned |

## Repo Shape

The repo is now centered on a single investigation surface instead of multiple
parallel experiment layouts:

```text
investigations/
  cra-temporal-drift/
```
