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

    runtime_sbom_only = sorted(
        name for name in running_sbom_packages if name not in build_packages
    )

    if runtime_only or version_drift:
        accuracy_reading = (
            "The build-time SBOM no longer fully reflects runtime reality. "
            "Static inventory evidence is insufficient on its own."
        )
        utility_reading = (
            "A stale build-time SBOM can cause false confidence in the declared "
            "software inventory. That weakens patching, exposure analysis, and "
            "other decisions that depend on the inventory being current."
        )
    elif build_only:
        accuracy_reading = (
            "The runtime package view is narrower than the build-time SBOM. "
            "This suggests either extraction blind spots or non-package artifacts "
            "in the build-time inventory."
        )
        utility_reading = (
            "The runtime view may look decisive while actually hiding evidence "
            "quality problems. Decisions based on it would need caution because "
            "the extraction method may be incomplete."
        )
    else:
        accuracy_reading = (
            "For this run, the build-time SBOM and live package extraction align "
            "at the package level. The trust claim holds only for this observed "
            "point in time."
        )
        utility_reading = (
            "The current runtime check does not show package drift, but the trust "
            "claim remains time-bound. The evidence is useful for this moment, "
            "but later updates, initialization logic, or deployment changes could "
            "still make the documentation stale."
        )

    governance_reading = (
        "Accuracy cannot be treated as a one-time generation event. Even when the "
        "snapshot currently aligns with runtime state, the assurance obligation is "
        "temporal and should be re-verified as the system changes."
    )

    remediation_reading = (
        "Use this result to guide verification design, not to hardcode a single "
        "response. Keep build-time generation as a baseline, then decide with "
        "stakeholders what deploy-time checks, runtime drift monitoring, and "
        "reconciliation thresholds are appropriate for the system context."
    )

    drift_report = f"""# Drift Report

## Question

Can a static build-time SBOM still be trusted once the container is running?

## Counts

- Build-time SBOM packages: {len(build_packages)}
- Runtime extracted packages: {len(runtime_packages)}
- Running-container SBOM packages: {len(running_sbom_packages)}

## Present At Build-Time Only

{markdown_list([f"{name}@{build_packages[name]}" for name in build_only])}

## Present At Runtime Only

{markdown_list([f"{name}@{runtime_packages[name]}" for name in runtime_only])}

## Version Drift

{markdown_list([f"{name}: build={build_packages[name]}, runtime={runtime_packages[name]}" for name in version_drift])}

## Running-Container SBOM Cross-Check

Runtime-only packages seen by the running-container SBOM:

{markdown_list([f"{name}@{running_sbom_packages[name]}" for name in runtime_sbom_only])}

## Accuracy

{accuracy_reading}

## Utility

{utility_reading}

## Governance

{governance_reading}

## Remediation

{remediation_reading}
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

## Governance

Article 10 style documentation trust cannot be treated as a one-time export
problem. It becomes a continuous evidence problem once software is deployed.

## Remediation

### Core requirements

- generate a build-time SBOM baseline
- verify it again at deploy time or release acceptance
- monitor for runtime drift where the operating model permits it
- reconcile stale documentation when drift is detected

### Context-dependent choices

- how often to verify
- which environments need runtime checks
- what level of drift should block release or trigger escalation

### Stakeholder questions

- who owns the accuracy claim after deployment
- who decides whether runtime drift is acceptable
- what evidence is sufficient for regulators, customers, or internal assurance
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
"""

    DRIFT_REPORT.write_text(drift_report)
    CRA_IMPLICATION.write_text(cra_reading)

    print(f"Wrote {DRIFT_REPORT}")
    print(f"Wrote {CRA_IMPLICATION}")


if __name__ == "__main__":
    main()
