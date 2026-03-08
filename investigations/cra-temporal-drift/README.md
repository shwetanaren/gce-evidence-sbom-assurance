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
3. generate an SBOM from the exported runtime filesystem
4. compare build-time versus runtime package inventories
5. explain what that means for CRA-style documentation trust

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

The point is not only to find drift.

The point is to show whether an organization can tell:

- what the build-time claim was
- what the runtime reality is
- whether they still align
- what kind of follow-up evidence would be needed if they do not

## Analysis Convention

Every investigation in this repo uses the same method:

1. **Accuracy**
   Does the claim still match observed reality?
2. **Utility**
   Is the evidence useful for decisions, or does it leave important blind spots?
3. **Governance**
   What does that mean for the regulation, control, or assurance obligation?
4. **Remediation**
   What should be done next, including context-dependent choices?

This keeps the repo simple and consistent across future investigations.
