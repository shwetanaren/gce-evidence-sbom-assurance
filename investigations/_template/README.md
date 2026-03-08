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

### Technical Accuracy

- what the original claim was
- what was observed in practice
- whether they matched

### Risk

- what can go wrong if the claim is stale or incomplete
- what blind spots remain
- when the organization would make a wrong decision if it trusted the artifact

### Governance Implication

- what the result means for the regulation, policy, or assurance obligation
- whether point-in-time evidence is enough
- what continuity or maintenance requirement follows

## Optional Fourth Section

### Remediation

- what process or architecture would keep the claim trustworthy over time

## GitHub Project Guidance

Keep project items simple:

- `Theme` = topic area
- `Layer` = dominant lens
- `Focus` = exact investigation topic
- `Role` = repository position only
- `Status` = maturity

Do not overload project fields with the full analysis structure. The three-layer
model belongs in the investigation write-up, not in project metadata.
