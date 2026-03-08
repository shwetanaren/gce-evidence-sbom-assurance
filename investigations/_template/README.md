# Investigation Template

Use this structure for every investigation in `gce-evidence-sbom-assurance`.

The point is to keep each lab fast to build, easy to read, and consistent across
technical, risk, and governance layers.

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

Every investigation should be explainable through these sections:

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

Use remediation as guidance, not a hardcoded answer.

#### Core requirements

- what minimum controls or verification steps should exist

#### Context-dependent choices

- what should vary by system criticality, operating model, or regulatory context

#### Stakeholder questions

- what should be decided with engineering, security, compliance, product, or
  operations stakeholders

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
