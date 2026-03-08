# sbom-reality-checker

Evaluate SBOM standards for audit efficacy: SPDX vs. CycloneDX

Governance ??? Code ??? Evidence
# SBOM Reality Checker: Standards Evaluation

**Governance  Code  Evidence**

I audit where SBOM claims meet container realityand evaluate which standard enables better audit.

## The Test

Same container. Two standards. One runtime. Compare efficacy.

## Standards Tested

- **SPDX:** Linux Foundation, ISO, legal-focused
- **CycloneDX:** OWASP, security-focused, VEX-ready

## The Finding

Both drift. CycloneDX enables faster automated audit. SPDX carries more legal weight.  
For continuous compliance: **CycloneDX + verification tooling**.

## How to Run

```bash
# SPDX version
cd standards/spdx
./01-generate-sbom.sh && ./02-extract-runtime.sh && python3 03-compare.py

# CycloneDX version  
cd standards/cyclonedx
./01-generate-sbom.sh && ./02-extract-runtime.sh && python3 03-compare.py

# Compare
cat compare-standards/spdx-vs-cyclonedx-drift.md
```

## Governance Code Evidence

Testing where compliance claims meet technical reality.

## Series: [Regulation] Claims vs. Reality

| Regulation | Investigation | Status |
|-----------|---------------|--------|
| CRA | nginx SBOM accuracy | In progress |
| DORA | Terraform drift | Planned |
| GDPR | Consent state reconciliation | Planned |
| EU AI Act | ML pipeline provenance | Planned |

## Methodology

Three-layer audit:
1. **Accuracy:** Does the artifact match reality?
2. **Utility:** Does it help manage risk?
3. **Governance:** Does it satisfy regulation?

[Investigations](#) | [Methodology](#) | [Contact](#)
