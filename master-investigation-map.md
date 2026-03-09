# Master Investigation Map

This is the canonical map for the CRA investigation program.

It links each investigation to:

- one learning pillar
- one primary CRA requirement
- one core evidence question

The demo product can be reused across multiple investigations. The
investigation is the unit of learning; the vulnerable app is the test surface.

| Investigation | Content Pillar | CRA Requirement | Core Evidence Question |
| ------------- | -------------- | --------------- | ---------------------- |
| cra-001-sbom-generation | Software Transparency | R3 | Can the product generate a usable SBOM at build time? |
| cra-002-sbom-format-comparison | Software Transparency | R3 | Do different SBOM formats preserve materially equivalent component evidence? |
| cra-003-dependency-graph | Software Transparency | R3 | Does dependency graphing reveal relationships the basic inventory misses? |
| cra-004-license-compliance | Software Transparency | R12 | Does the software evidence support defensible license and documentation claims? |
| cra-005-sbom-drift-detection | Software Transparency | R3 | Can runtime state diverge from build-time inventory claims and still look compliant on paper? |
| cra-006-dependency-vulnerability-scan | Vulnerability Discovery | R2 | Do dependency scanners find known vulnerable components accurately enough to act on? |
| cra-007-sast-analysis | Vulnerability Discovery | R8 | Does static analysis identify exploitable code weaknesses with enough precision to be useful? |
| cra-008-secret-detection | Vulnerability Discovery | R5 | Can secret detection distinguish real exposure signals from development noise? |
| cra-009-configuration-security | Vulnerability Discovery | R4 | Do configuration checks surface insecure defaults that change the product risk profile? |
| cra-010-cryptography-audit | Vulnerability Discovery | R5 | Does the product use weak or inappropriate cryptography in ways the evidence can clearly show? |
| cra-011-secure-ci-pipeline | Secure Development Lifecycle | R1 | Does the delivery pipeline demonstrate secure-by-design practice rather than only good intent? |
| cra-012-security-gates | Secure Development Lifecycle | R1 | Are security gates defined and enforced in a way that actually blocks unsafe releases? |
| cra-013-automated-code-review | Secure Development Lifecycle | R1 | Can automated review meaningfully improve development decisions before merge time? |
| cra-014-policy-as-code | Secure Development Lifecycle | R1 | Can policy checks turn security expectations into reviewable and repeatable controls? |
| cra-015-threat-modeling | Secure Development Lifecycle | R1 | Does the threat model help explain why the investigation findings matter? |
| cra-016-container-security-scan | Supply Chain Security | R8 | Do container scans expose exploitable image-level weaknesses in a way teams can trust? |
| cra-017-base-image-risk-analysis | Supply Chain Security | R8 | How much product risk is inherited from the chosen base image? |
| cra-018-artifact-signing | Supply Chain Security | R7 | Can the build output be verified as the intended artifact and not a substituted one? |
| cra-019-build-provenance | Supply Chain Security | R7 | Can the organization prove how the artifact was built and from what inputs? |
| cra-020-reproducible-builds | Supply Chain Security | R3 | Can the same source and process reproduce materially the same build evidence? |
| cra-021-attack-surface-mapping | Runtime Security | R8 | What attackable interfaces are actually exposed when the product is running? |
| cra-022-web-security-testing | Runtime Security | R8 | Do live application tests reveal exploitable behavior that static evidence missed? |
| cra-023-authentication-security | Runtime Security | R6 | Is authentication and access control behavior defensible when tested at runtime? |
| cra-024-least-privilege-execution | Runtime Security | R6 | Does the running service execute with avoidable privilege? |
| cra-025-secure-update-mechanism | Runtime Security | R7 | Does the product enforce trustworthy update behavior in practice, not just in design? |
| cra-026-cve-monitoring | Vulnerability Lifecycle | R2 | Can the organization notice newly relevant CVEs after release? |
| cra-027-patch-management | Vulnerability Lifecycle | R11 | Is there a credible path from finding to patch to deployed fix? |
| cra-028-vulnerability-disclosure | Vulnerability Lifecycle | R10 | Is there a clear process for external reporting and internal handling of product vulnerabilities? |
| cra-029-security-advisory-publication | Vulnerability Lifecycle | R10 | Can the organization communicate confirmed issues in a usable advisory format? |
| cra-030-cra-readiness-assessment | Vulnerability Lifecycle | R12 | Does the combined evidence support a realistic CRA readiness story? |

## GitHub Project Mapping

The GitHub Project should stay simple:

- one `Repository anchor` item per repo
- one item per investigation

Each item should answer two practical questions:

- what am I working on?
- why does it matter?

The detailed reasoning belongs in the investigation write-up, not in project
field sprawl.
