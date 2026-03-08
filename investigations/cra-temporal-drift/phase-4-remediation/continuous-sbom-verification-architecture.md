# Continuous SBOM Verification Architecture

If CRA-style documentation trust is temporal, then the remediation pattern is
not "generate a better snapshot." It is "continuously verify whether the
snapshot still reflects deployed reality."

## Suggested Architecture

1. **Build-time generation**
   Produce the SBOM at image build or image intake time.
2. **Runtime extraction**
   Periodically extract actual installed packages from the running workload.
3. **Runtime cross-check**
   Optionally generate a second runtime SBOM view from the live container
   filesystem.
4. **Drift policy**
   Define what counts as:
   - acceptable stability
   - version drift
   - undeclared runtime additions
   - extraction blind spots
5. **Assurance decision**
   Decide whether the original SBOM:
   - still holds
   - needs refresh
   - should be accompanied by runtime evidence
   - should be rejected as stale

## Minimal Operating Pattern

- build-time SBOM captured automatically
- runtime package extraction on a schedule or deployment event
- comparison report generated automatically
- exceptions routed to engineering and governance review

## Why This Matters

This turns SBOM assurance from a tooling output into a governable evidence
process. That is the real bridge from security tooling to CRA-oriented
documentation trust.
