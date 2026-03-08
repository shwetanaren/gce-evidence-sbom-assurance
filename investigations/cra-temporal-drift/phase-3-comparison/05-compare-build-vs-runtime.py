#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SBOM = ROOT / "phase-1-build-time" / "sbom-build-time.json"
RUNTIME_PACKAGES = ROOT / "phase-2-runtime" / "runtime-packages.txt"
RUNNING_SBOM = ROOT / "phase-2-runtime" / "sbom-running.json"
DRIFT_REPORT = ROOT / "phase-3-comparison" / "drift-report.md"
CRA_IMPLICATION = ROOT / "phase-3-comparison" / "cra-implication.md"

PKG_LINE_RE = re.compile(r"^(?P<name>.+)-(?P<version>[0-9][A-Za-z0-9._:+~-]*(?:-r[0-9]+)?)$")


def load_sbom_packages(path: Path) -> dict[str, str]:
    payload = json.loads(path.read_text())
    packages: dict[str, str] = {}
    for component in payload.get("components", []):
        if component.get("type") != "library":
            continue
        name = component.get("name", "").strip()
        version = component.get("version", "").strip()
        if name and version:
            packages[name] = version
    return packages


def load_runtime_packages(path: Path) -> dict[str, str]:
    packages: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        match = PKG_LINE_RE.match(line)
        if not match:
            continue
        packages[match.group("name")] = match.group("version")
    return packages


def markdown_list(items: list[str], empty: str = "None") -> str:
    if not items:
        return empty
    return "\n".join(f"- `{item}`" for item in items)


def main() -> None:
    build_packages = load_sbom_packages(BUILD_SBOM)
    runtime_packages = load_runtime_packages(RUNTIME_PACKAGES)
    running_sbom_packages = load_sbom_packages(RUNNING_SBOM) if RUNNING_SBOM.exists() else {}

    build_only = sorted(name for name in build_packages if name not in runtime_packages)
    runtime_only = sorted(name for name in runtime_packages if name not in build_packages)
    version_drift = sorted(
        name
        for name in build_packages
        if name in runtime_packages and build_packages[name] != runtime_packages[name]
    )

    syft_runtime_only = sorted(
        name for name in running_sbom_packages if name not in build_packages
    )

    if runtime_only or version_drift:
        technical_accuracy = (
            "The build-time SBOM no longer fully reflects runtime reality. "
            "Static inventory evidence is insufficient on its own."
        )
        risk_reading = (
            "A stale build-time SBOM can cause false confidence in the declared "
            "software inventory. That weakens patching, exposure analysis, and "
            "any downstream assurance that depends on the inventory being current."
        )
    elif build_only:
        technical_accuracy = (
            "The runtime package view is narrower than the build-time SBOM. "
            "This suggests either extraction blind spots or non-package artifacts "
            "in the build-time inventory."
        )
        risk_reading = (
            "The organization may treat the runtime view as complete when it is "
            "actually missing part of the observed build-time inventory. This is "
            "an evidence quality problem, not necessarily a software stability success."
        )
    else:
        technical_accuracy = (
            "For this run, the build-time SBOM and live package extraction align "
            "at the package level. The trust claim holds only for this observed "
            "point in time."
        )
        risk_reading = (
            "The current runtime check does not show package drift, but the trust "
            "claim remains time-bound. Later updates, initialization logic, or "
            "deployment changes could still make the documentation stale."
        )

    governance_reading = (
        "Accuracy cannot be treated as a one-time generation event. Even when the "
        "snapshot currently aligns with runtime state, the assurance obligation is "
        "temporal and should be re-verified as the system changes."
    )

    drift_report = f"""# Drift Report

## Question

Can a static build-time SBOM still be trusted once the container is running?

## Counts

- Build-time SBOM packages: {len(build_packages)}
- Runtime extracted packages: {len(runtime_packages)}
- Running-container Syft packages: {len(running_sbom_packages)}

## Present At Build-Time Only

{markdown_list([f"{name}@{build_packages[name]}" for name in build_only])}

## Present At Runtime Only

{markdown_list([f"{name}@{runtime_packages[name]}" for name in runtime_only])}

## Version Drift

{markdown_list([f"{name}: build={build_packages[name]}, runtime={runtime_packages[name]}" for name in version_drift])}

## Running-Container Syft Cross-Check

Runtime-only packages seen by the running-container SBOM:

{markdown_list([f"{name}@{running_sbom_packages[name]}" for name in syft_runtime_only])}

## Technical Accuracy

{technical_accuracy}

## Risk

{risk_reading}

## Governance Implication

{governance_reading}
"""

    if runtime_only or version_drift:
        cra_reading = """# CRA Implication

The investigation found package-level temporal drift between build time and
runtime.

## What This Means For Article 10

- build-time documentation stopped matching observed runtime reality
- the SBOM is now a stale snapshot, not a trustworthy live representation
- organizations would need runtime verification or refresh logic to keep the
  documentation defensible

## Governance Reading

Article 10 style documentation trust cannot be treated as a one-time export
problem. It becomes a continuous evidence problem once software is deployed.
"""
    else:
        cra_reading = """# CRA Implication

The investigation did not find package-level temporal drift in this runtime
check.

## What This Means For Article 10

- the build-time SBOM still matched the observed live package inventory
- this supports a narrow trust claim for this specific runtime moment
- it does not prove that the claim will remain true over time without
  re-verification

## Governance Reading

Article 10 still points toward continuity. Even when a single runtime check
aligns with the build snapshot, the assurance claim is temporal and should be
re-checked as software, deployment conditions, or initialization logic change.
"""

    DRIFT_REPORT.write_text(drift_report)
    CRA_IMPLICATION.write_text(cra_reading)

    print(f"Wrote {DRIFT_REPORT}")
    print(f"Wrote {CRA_IMPLICATION}")


if __name__ == "__main__":
    main()
