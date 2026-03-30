# Deployment Log: [Release Version / Name]

**Date**: [YYYY-MM-DD]
**Start Time**: [timestamp]
**End Time**: [timestamp]
**Operator**: [name or agent]
**Execution Mode**: [live | dry-run | planning-only]

## Deployment Identity
- **Candidate**: [branch @ commit]
- **Target Environment**: [environment]
- **Deployment Mode**: [fresh-machine | existing-deployment]
- **Release Marker / Version Tag**: [marker]

## Actions Performed
1. [action]
2. [action]
3. [action]

## Migration Outcome
- **Executed**: [yes | no]
- **Result**: [success | failed | skipped]
- **Notes**: [notes]

## Smoke Test Results
| Check | Result | Notes |
|---|---|---|
| System health path | [pass/fail] | [notes] |
| Critical user journey | [pass/fail] | [notes] |
| Release marker visible | [pass/fail] | [notes] |
| Observability signal visible | [pass/fail] | [notes] |

## Protection And Rollback
- **Baseline / Snapshot Reference**: [id or N/A]
- **Rollback Triggered**: [yes | no]
- **Rollback Target**: [target or N/A]
- **Rollback Outcome**: [success | failed | N/A]

## Incidents And Deviations
1. [issue, deviation, or N/A]

## Operational Decisions
- **Decision Records**: [_bmad-output/production-artifacts/operational-decisions/operational-decision-record-<timestamp>-<decision>.md | none]
- **Open Alignment Debt**: [summary or N/A]

## Final Status
- **Deployment Result**: [success | failed | partial]
- **Immediate Confidence**: [high | medium | low]
- **Deployment Verification**: [_bmad-output/production-artifacts/deployment-verifications/deployment-verification-<timestamp>-<candidate>.md | pending | N/A]
- **Next Recommended Workflow**: [/bmad-bda-deployment-verification | /bmad-bda-post-launch-review | investigate | retry]
