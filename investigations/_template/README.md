# Investigation Template

Use this structure for every investigation in `gce-evidence-sbom-assurance`.

The goal is to keep each investigation easy to build, easy to read, and
consistent across the repo.

## Recommended Shape

```text
investigations/<investigation-name>/
├── README.md
├── phase-1-build-time/
├── phase-2-runtime/
├── phase-3-comparison/
└── phase-4-remediation/
```

## Required Reading Structure

Every investigation should be readable through these sections:

### Accuracy

- what the original claim was
- what was observed in practice
- whether they matched

### Utility

- whether the evidence is useful for decisions
- what can and cannot be concluded from it
- what blind spots remain

### Governance

- what the result means for the regulation, policy, or assurance obligation
- whether point-in-time evidence is enough
- what continuity or maintenance requirement follows

### Remediation

Use remediation as guidance, not a fixed answer.

#### Core requirements

- what minimum controls or verification steps should exist

#### Context-dependent choices

- what should vary by system criticality, operating model, or regulatory context

#### Stakeholder questions

- what should be decided with engineering, security, compliance, product, or
  operations stakeholders

## Three-Layer Audit Lens

Use the reading structure above together with this audit lens:

### Layer 1: Product Reality

- what is technically true in the source, image, configuration, or runtime
- whether the issue is observable, reproducible, and scoped correctly

### Layer 2: Evidence Quality

- what evidence detects the issue
- what evidence misses it or overstates it
- whether the result is trustworthy enough for decisions

### Layer 3: CRA Meaning

- which CRA requirement the result primarily informs
- what the finding contributes to governance interpretation
- what it still does not prove

This keeps the investigation grounded in fact, assurance value, and regulatory
meaning rather than stopping at tool output.

## GitHub Project Guidance

Keep project items simple:

- `Theme` = topic area
- `Layer` = dominant lens
- `Focus` = exact investigation topic
- `Role` = repository position only
- `Status` = maturity

Do not overload project fields with the full analysis structure. The
`Accuracy / Utility / Governance / Remediation` method belongs in the
investigation write-up, not in project metadata.
