#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


CHURN_PREFIXES = (
    "/tmp/",
    "/var/tmp/",
    "/run/",
    "/var/run/",
    "/var/cache/",
    "/var/log/",
)
CONFIG_PREFIXES = (
    "/etc/",
    "/usr/local/etc/",
)
MATERIAL_PREFIXES = (
    "/lib/",
    "/usr/lib/",
    "/usr/bin/",
    "/usr/sbin/",
    "/bin/",
    "/sbin/",
    "/etc/apk/",
)


@dataclass(frozen=True)
class Component:
    name: str
    version: str
    kind: str
    purl: str

    @property
    def key(self) -> str:
        return self.purl or f"{self.kind}:{self.name}@{self.version}"

    def label(self) -> str:
        base = self.name or "unknown"
        if self.version:
            base = f"{base}@{self.version}"
        if self.kind:
            base = f"{base} ({self.kind})"
        return base


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare = subparsers.add_parser("compare")
    compare.add_argument("--scenario", required=True)
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--runtime", required=True)
    compare.add_argument("--docker-diff", required=True)
    compare.add_argument("--json-out", required=True)
    compare.add_argument("--markdown-out", required=True)

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("--runtime-root", required=True)
    summarize.add_argument("--markdown-out", required=True)

    return parser.parse_args()


def load_components(path: Path) -> dict[str, Component]:
    payload = json.loads(path.read_text())
    components: dict[str, Component] = {}
    for raw in payload.get("components", []):
        if raw.get("type") == "file":
            continue
        component = Component(
            name=raw.get("name", ""),
            version=raw.get("version", ""),
            kind=raw.get("type", ""),
            purl=raw.get("purl", ""),
        )
        components[component.key] = component
    return components


def classify_path(path: str) -> tuple[str, str]:
    normalized = f"{path}/" if not path.endswith("/") else path
    if normalized.startswith("/etc/apk/"):
        return (
            "material-component-drift",
            "Path sits in package management state and signals a runtime inventory change.",
        )
    if normalized.startswith(CHURN_PREFIXES):
        return (
            "expected-runtime-churn",
            "Path sits in a temp/cache/run/log area that commonly changes at runtime.",
        )
    if normalized.startswith(CONFIG_PREFIXES):
        return (
            "configuration-drift",
            "Path sits in configuration space and can alter runtime behavior without changing packages.",
        )
    if normalized.startswith(MATERIAL_PREFIXES):
        return (
            "material-component-drift",
            "Path sits in package or executable space and likely changes the software inventory.",
        )
    return ("unknown-review", "Path does not match a known policy bucket and needs review.")


def parse_docker_diff(path: Path) -> list[dict[str, str]]:
    changes = []
    if not path.exists():
        return changes

    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        op, changed_path = parts
        classification, reason = classify_path(changed_path)
        changes.append(
            {
                "operation": op,
                "path": changed_path,
                "classification": classification,
                "reason": reason,
            }
        )
    return changes


def component_to_dict(component: Component) -> dict[str, str]:
    return {
        "name": component.name,
        "version": component.version,
        "type": component.kind,
        "purl": component.purl,
        "label": component.label(),
    }


def build_report(args: argparse.Namespace) -> dict:
    baseline = load_components(Path(args.baseline))
    runtime = load_components(Path(args.runtime))
    file_changes = parse_docker_diff(Path(args.docker_diff))

    baseline_only = [baseline[key] for key in sorted(set(baseline) - set(runtime))]
    runtime_only = [runtime[key] for key in sorted(set(runtime) - set(baseline))]

    classifications = {}
    for change in file_changes:
        classifications.setdefault(change["classification"], 0)
        classifications[change["classification"]] += 1

    if runtime_only:
        recommendation = (
            "Static SBOM is not sufficient for runtime trust in this scenario. "
            "Additional runtime evidence is required because the runtime inventory "
            "contains components absent from the baseline artifact."
        )
    elif any(item["classification"] == "configuration-drift" for item in file_changes):
        recommendation = (
            "Static SBOM alone is not sufficient for runtime assurance here. "
            "Configuration evidence must accompany the baseline artifact."
        )
    elif file_changes:
        recommendation = (
            "Static SBOM may be acceptable only if expected runtime churn is "
            "explicitly scoped and monitored. Runtime evidence is still useful "
            "to prove that no material drift occurred."
        )
    else:
        recommendation = (
            "Baseline and runtime evidence align for this scenario. Static SBOM "
            "remains defensible for inventory claims within this narrow scope."
        )

    return {
        "scenario": args.scenario,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_component_count": len(baseline),
        "runtime_component_count": len(runtime),
        "components_static_only": [component_to_dict(item) for item in baseline_only],
        "components_runtime_only": [component_to_dict(item) for item in runtime_only],
        "file_changes": file_changes,
        "classification_counts": classifications,
        "recommendation": recommendation,
    }


def summarize_labels(items: list[dict[str, str]], limit: int = 12) -> str:
    if not items:
        return "None"
    labels = [item["label"] for item in items[:limit]]
    if len(items) > limit:
        labels.append(f"... and {len(items) - limit} more")
    return ", ".join(labels)


def summarize_file_changes(file_changes: list[dict[str, str]], limit: int = 8) -> str:
    if not file_changes:
        return "None"
    rendered = []
    for item in file_changes[:limit]:
        rendered.append(f"`{item['operation']} {item['path']}` -> {item['classification']}")
    if len(file_changes) > limit:
        rendered.append(f"... and {len(file_changes) - limit} more")
    return "\n".join(f"- {line}" for line in rendered)


def markdown_report(data: dict) -> str:
    return f"""# Scenario Report: {data['scenario']}

## Inventory Delta

- Baseline inventory components: {data['baseline_component_count']}
- Runtime inventory components: {data['runtime_component_count']}
- Static SBOM only: {len(data['components_static_only'])}
- Runtime scan only: {len(data['components_runtime_only'])}

## Components Present In Static SBOM Only

{summarize_labels(data['components_static_only'])}

## Components Present In Runtime Scan Only

{summarize_labels(data['components_runtime_only'])}

## File-Level Changes From docker diff

{summarize_file_changes(data['file_changes'])}

## Classification Counts

{json.dumps(data['classification_counts'], indent=2, sort_keys=True)}

## Assurance Reading

{data['recommendation']}
"""


def write_compare(args: argparse.Namespace) -> None:
    data = build_report(args)
    Path(args.json_out).write_text(json.dumps(data, indent=2, sort_keys=True))
    Path(args.markdown_out).write_text(markdown_report(data))


def write_summary(args: argparse.Namespace) -> None:
    runtime_root = Path(args.runtime_root)
    rows = []
    details = []

    for report_path in sorted(runtime_root.glob("*/classification.json")):
        data = json.loads(report_path.read_text())
        scenario = data["scenario"]
        rows.append(
            "| {scenario} | {static_only} | {runtime_only} | {counts} |".format(
                scenario=scenario,
                static_only=len(data["components_static_only"]),
                runtime_only=len(data["components_runtime_only"]),
                counts=", ".join(
                    f"{key}={value}"
                    for key, value in sorted(data["classification_counts"].items())
                )
                or "none",
            )
        )
        details.append(
            f"""## {scenario}

{data['recommendation']}

- Runtime-only components: {summarize_labels(data['components_runtime_only'], limit=8)}
- Static-only components: {summarize_labels(data['components_static_only'], limit=8)}
- File changes:
{summarize_file_changes(data['file_changes'], limit=6)}
"""
        )

    markdown = """# Sample Run Summary

This summary shows how the baseline SBOM behaved once runtime evidence was
collected for each mutation scenario.

| Scenario | Static only | Runtime only | Drift summary |
| -------- | ----------- | ------------ | ------------- |
{rows}

## What This Shows

The bridge from tooling to governance is not the ability to emit an SBOM. It is
the ability to explain when that artifact still deserves trust and when runtime
evidence is needed to support the claim.

## Next-Step Suggestions

- add mounted-volume scenarios to test evidence blind spots
- compare CycloneDX output with a second inventory approach only after the
  runtime evidence model is stable
- add policy thresholds that say when runtime-only drift should block trust
- capture attestations alongside filesystem evidence for stronger CRA-style
  operational assurance

{details}
""".format(rows="\n".join(rows), details="\n".join(details))

    Path(args.markdown_out).write_text(markdown)


def main() -> None:
    args = parse_args()
    if args.command == "compare":
        write_compare(args)
    else:
        write_summary(args)


if __name__ == "__main__":
    main()
