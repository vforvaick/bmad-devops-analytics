# Deployment Verification: [Reviewed Deployment]

**Date**: [YYYY-MM-DD]
**Reviewed Deployment**: [branch @ commit]
**Target Environment**: [environment]
**Verification Mode**: [initial post-deploy | rerun after fix]
**Triggered By**: [deploy workflow | manual rerun | incident follow-up]
**Decision**: [PASS | HOTFIX-NOW | ROLLBACK | FIX-OBSERVABILITY]
**Confidence Level**: [high | medium | low]
**Deployment Log**: [path]
**Release Marker**: [marker]

## Summary
[2-4 sentences describing whether the deployment's critical runtime outcome is proven, what is still uncertain, and the next action.]

## Verification Inputs
- **Release Readiness**: [path]
- **Release Intent Matrix**: [path or N/A]
- **Observability Config**: [path or N/A]
- **Deployment Baseline**: [path or N/A]
- **Previous Verification**: [path or N/A]

## Critical Outcome
- **Primary Outcome To Prove**: [statement]
- **Primary Outcome Status**: [pass | partial | fail | unverified]
- **Direct Evidence**: [summary]
- **Critical Failure Risk**: [summary]

## Evidence Coverage
| Evidence Area | Expected | Observed | Status | Notes |
|---|---|---|---|---|
| Release marker | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| System health | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Critical journey | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Telemetry integrity | [expected] | [observed] | [pass/concerns/fail] | [notes] |

## Verification Matrix
| Verification Row | Layer | Planned Statement | Runtime Proxy / Expected Evidence | Observed Evidence | Status | Confidence | Recommended Route |
|---|---|---|---|---|---|---|---|
| VER-001 | [critical-outcome | success-criterion | user-journey | FR | NFR | release-change | permission-rule | data-integrity | duplicate-protection | integration | failure-path | telemetry-integrity | operability | non-goal] | [planned statement] | [expected evidence] | [observed evidence] | [matched | partial | missed | unverified | unplanned-positive | unplanned-negative] | [high | medium | low] | [none | hotfix-now | rollback | fix-observability | watch] |

## Findings
1. **[Finding Title]**
   - **Severity**: [critical | high | medium | low]
   - **Impact**: [summary]
   - **Evidence**: [summary]
   - **Route**: [hotfix-now | rollback | fix-observability | watch]

## Decision And Routing
- **Immediate Action**: [proceed | hotfix-now | rollback | fix-observability]
- **Why**: [summary]
- **Can Post-Launch Review Proceed?**: [yes | no | limited]
- **Next Recommended Workflow**: [/bmad-bda-post-launch-review | investigate | retry deployment verification | rollback]
