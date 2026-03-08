# Working Preferences For This Series

These instructions are specific to the `gce-evidence-sbom-assurance` series.

## Operating Style

- Keep the work simple, clean, and direct.
- Avoid "resume-driven development", excess scaffolding, portability theater, or defensive abstractions unless they are clearly needed.
- Prefer the smallest implementation that proves the point.
- Favor local tools already available in the environment over containerized fallbacks when possible.
- Keep the repo markdown-first and portfolio-friendly.

## Repo Structure

- Use one clear investigation surface at a time under `investigations/`.
- Keep one canonical artifact/output location per investigation. Do not maintain parallel output layouts.
- Add a new investigation folder when testing a new question or scenario set. Do not create a new repo unless there is a strong reason.
- Keep root structure easy to scan.

## Investigation Method

Every investigation should use this reading structure:

1. `Accuracy`
2. `Utility`
3. `Governance`
4. `Remediation`

For `Remediation`, keep guidance flexible rather than hardcoded:

- `Core requirements`
- `Context-dependent choices`
- `Stakeholder questions`

## How To Build

- Start with a clean baseline before adding more realistic drift or stress scenarios.
- When expanding scope, separate the baseline investigation from scenario-driven investigations.
- Prefer short shell scripts and plain Python over clever helpers.
- Do not add wrappers, temp-state files, Python cleanup blocks, or fallback layers unless they materially improve the investigation.

## Explanation Style

- Explain the work clearly enough that it can be reused in GitHub, Obsidian, LinkedIn, or verbal presentation.
- Make the argument explicit: this series is about evidence quality, not just artifact generation.
- When an investigation compares two states, explain why the comparison might differ in real environments.
- Distinguish clearly between:
  - build-time claim
  - runtime reality
  - evidence usefulness
  - governance meaning

## GitHub Project Conventions

- Keep project metadata simple and readable.
- The project tracks:
  - one `Repository anchor` item per repo
  - one item per investigation
- Keep deeper reasoning inside the investigation write-up, not in project field sprawl.

## Editing Bias

- Cut wording that sounds inflated, performative, or framework-heavy.
- Prefer concise README language over manifesto-style writing.
- If a script or structure feels over-engineered, simplify it.
