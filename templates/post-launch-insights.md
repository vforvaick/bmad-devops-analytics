# Post-Launch Insights: [Release Name / Version]

**Date**: [YYYY-MM-DD]
**Reviewed Deployment**: [branch @ commit]
**Target Environment**: [environment]
**Evidence Window**: [start] to [end]
**Review Type**: [full review | early read]
**Evidence Mode**: [automated | manual-evidence]
**Overall Status**: [healthy | concerns | critical]
**Confidence Level**: [high | medium | low]

## Executive Summary
[3-5 sentences covering user impact, technical health, and recommended next action.]

## Decision Readiness
- **Can We Explain Current Health?**: [yes | partial | no]
- **Can We Explain User Impact?**: [yes | partial | no]
- **Can We Correlate Findings To This Release?**: [yes | partial | no]
- **Is Evidence Sufficient For Planning Decisions?**: [yes | partial | no]

## Evidence Coverage
| Evidence Area | Expected | Observed | Status | Notes |
|---|---|---|---|---|
| Logs | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Errors | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Metrics | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Traces | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Analytics | [expected] | [observed] | [pass/concerns/fail] | [notes] |
| Release Markers | [expected] | [observed] | [pass/concerns/fail] | [notes] |

## Top Findings
1. **[Finding Title]**
   - **Category**: [error | performance | adoption | behavior | infrastructure | evidence-gap]
   - **Severity**: [critical | high | medium | low]
   - **User Impact**: [description]
   - **Evidence**: [key facts]
   - **Recommendation**: [next action]

## Baseline Comparison
- **Expectation Match**: [matched | partial | missed]
- **Delta From Release Readiness**: [summary]
- **Delta From Deployment Baseline**: [summary or N/A]

## Detailed Analysis
### Errors And Stability
- **Error Rate**: [value and threshold]
- **Top Error**: [summary]
- **Trend**: [improving, stable, worsening]

### Performance
- **Latency Summary**: [p50/p95/p99]
- **Primary Bottleneck**: [summary]

### Feature Adoption
- **Adoption Summary**: [summary]
- **Features Below Expectation**: [list]

### User Behavior
- **Critical Journey Outcome**: [summary]
- **Largest Drop-Off**: [summary]

### Infrastructure
- **Resource Health**: [summary]
- **Scaling Signals**: [summary]

### Evidence Quality Gaps
1. [missing signal and why it matters]

## Recommended Actions
1. [P0/P1/P2 action]

## Routing Recommendation
- **Run `/bmad-correct-course` Now**: [yes | no]
- **Future Sprint Planning Update Needed**: [yes | no]
- **Notes**: [routing explanation]
