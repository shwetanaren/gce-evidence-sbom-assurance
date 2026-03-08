# CRA Temporal Drift

Testing if static SBOMs can be trusted at runtime.

CRA Article 10 turns this into a time problem:

- build-time documentation is a snapshot
- deployed software is a running system
- trust depends on whether the documentation still reflects runtime reality

## Investigation Question

Can you trust a static SBOM once the container is running?

## Investigation Design

The current test uses `nginx:stable-alpine`.

1. generate a build-time SBOM and image manifest
2. run the container and extract actual installed packages from live state
3. optionally generate an SBOM from the running container snapshot
4. compare build-time versus runtime package inventories
5. interpret what that means for CRA Article 10 style documentation trust

## Structure

```text
investigations/cra-temporal-drift/
├── README.md
├── phase-1-build-time/
│   ├── 01-build-image.sh
│   ├── sbom-build-time.json
│   └── manifest-build.json
├── phase-2-runtime/
│   ├── 02-run-and-extract.sh
│   ├── 03-extract-from-running.sh
│   ├── 04-sbom-from-running.sh
│   ├── runtime-packages.txt
│   └── sbom-running.json
├── phase-3-comparison/
│   ├── 05-compare-build-vs-runtime.py
│   ├── drift-report.md
│   └── cra-implication.md
└── phase-4-remediation/
    └── continuous-sbom-verification-architecture.md
```

## Run

```bash
./phase-1-build-time/01-build-image.sh
./phase-2-runtime/02-run-and-extract.sh
python3 ./phase-3-comparison/05-compare-build-vs-runtime.py
```

## What To Look For

The interesting output is not only whether a drift exists.

It is whether the organization can tell:

- what the build-time claim was
- what the runtime reality is
- whether they still align
- what kind of assurance process would be needed if they do not

## Analysis Convention

Every investigation in this repo should read through the same three layers:

1. **Technical Accuracy**
   Does the build-time claim still match observed technical reality?
2. **Risk**
   What can go wrong if the claim drifts or becomes stale?
3. **Governance Implication**
   What does that mean for the regulation, control, or assurance obligation?

That keeps the repo simple, fast to scan, and consistent across future labs.
