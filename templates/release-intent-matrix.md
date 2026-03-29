# Release Intent Matrix: [Release Version / Name]

**Date**: [YYYY-MM-DD]
**Candidate**: [branch @ commit]
**Target Environment**: [environment]
**Deployment Mode**: [fresh-machine | existing-deployment]
**Status**: [draft | approved-for-release-readiness]

## Summary
[2-4 sentences summarizing the release scope and what this matrix captures.]

## Ground Truth Sources
- **PRD**: [path]
- **UX Specification**: [path or N/A]
- **Architecture**: [path]
- **Epics / Stories**: [path or N/A]
- **Sprint / Release Scope Evidence**: [path or N/A]

## Comparison Rules
- Critical rows must map to observable runtime evidence or explicitly document why they cannot be measured directly.
- Rows should represent only in-scope release intent, plus any inherited platform guardrails that could cause release failure.
- Use stable IDs so later artifacts can compare against this matrix directly.

## Release Intent Matrix
| Intent ID | Layer | Source Artifact | Source Reference | Planned Statement | Runtime Proxy / Expected Evidence | Criticality | Release Scope | Notes |
|---|---|---|---|---|---|---|---|---|
| INT-001 | [business-objective | success-criterion | user-journey | FR | NFR | UX-flow | story-acceptance | release-change] | [prd.md] | [section or identifier] | [planned statement] | [metric, event, log, trace, report, or operator check] | [critical | high | medium] | [in-scope | inherited guardrail] | [notes] |

## Coverage Summary
- **Business Objectives Captured**: [count]
- **Success Criteria Captured**: [count]
- **User Journeys Captured**: [count]
- **FR Rows Captured**: [count]
- **NFR Rows Captured**: [count]
- **UX Flow Rows Captured**: [count]
- **Story / Acceptance Rows Captured**: [count]

## Open Gaps
1. [missing or weak traceability link and why it matters]

## Next Use
- **Observability Setup Should Use This**: [yes]
- **Post-Launch Review Should Compare Against This**: [yes]
