# Production vs Plan Matrix: [Reviewed Deployment]

**Date**: [YYYY-MM-DD]
**Reviewed Deployment**: [branch @ commit]
**Target Environment**: [environment]
**Evidence Window**: [start] to [end]
**Confidence Level**: [high | medium | low]

## Summary
[2-4 sentences summarizing overall match between plan and production reality.]

## Comparison Inputs
- **Release Intent Matrix**: [path]
- **Observability Config**: [path]
- **Release Readiness**: [path]
- **Deployment Baseline**: [path or N/A]

## Production vs Plan Matrix
| Intent ID | Layer | Planned Statement | Expected Evidence | Observed Evidence | Status | Confidence | User Impact | Recommended Route |
|---|---|---|---|---|---|---|---|---|
| INT-001 | [layer] | [planned statement] | [expected evidence] | [observed evidence] | [matched | partial | missed | unverified | unplanned-positive | unplanned-negative] | [high | medium | low] | [summary] | [none | fix-observability | refine-plan | correct-course] |

## Comparison Totals
- **Matched Rows**: [count]
- **Partial Rows**: [count]
- **Missed Rows**: [count]
- **Unverified Rows**: [count]
- **Unexpected Positive Rows**: [count]
- **Unexpected Negative Rows**: [count]

## Highest-Risk Deltas
1. [delta and why it matters]

## Routing Recommendation
- **Immediate Correct Course Needed**: [yes | no]
- **Future Refinement Needed**: [yes | no]
- **Observability Fix Needed Before Stronger Judgment**: [yes | no]
