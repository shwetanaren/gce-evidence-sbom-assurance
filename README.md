# gce-evidence-sbom-assurance

This repo is a CRA investigation workspace focused on evidence quality.

The current repo stays narrow on purpose: one active investigation surface at a
time under `investigations/`, with the broader CRA program mapped at the root so
it is clear what this repo is testing and how it fits into the larger workspace.

## What This Repo Is For

The current investigation asks a simple question:

Can a container produce an SBOM at build time, but drift away from that claim
once the container is actually running?

That makes this repo an evidence problem first, not just an artifact generation
exercise.

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

## Core Reference Files

- [`cra-requirements-reference.md`](./cra-requirements-reference.md)
- [`master-investigation-map.md`](./master-investigation-map.md)
- [`investigations/_template/README.md`](./investigations/_template/README.md)

## Method

Every investigation should be read through two complementary structures.

First, the write-up structure:

1. Accuracy
2. Utility
3. Governance
4. Remediation

Second, the three-layer audit lens:

1. Product reality
2. Evidence quality
3. CRA meaning

This keeps the work grounded in what is technically true, what the evidence can
actually support, and what the result means for CRA-oriented assurance.

## How This Maps To The Larger Workspace

The broader `CRA-Labs` workspace is intended to look like this:

```text
CRA-Labs/
  cra-demo-product/
  pillar-01-software-transparency/
  pillar-02-vulnerability-discovery/
  pillar-03-secure-development/
  pillar-04-supply-chain-security/
  pillar-05-runtime-security/
  pillar-06-vulnerability-lifecycle/
```

In that model:

- `cra-demo-product` is the intentionally vulnerable target system
- the pillar folders hold investigations
- this repo remains one investigation workspace with one active surface

## Why This Matters

CRA evidence is not only about producing documentation. It is about whether the
evidence remains accurate enough to support a defensible security claim over
time.

A build-time SBOM is a snapshot. The real questions are:

- does runtime still match the snapshot?
- if not, how would the organization know?
- what evidence would prove the claim is still trustworthy?
