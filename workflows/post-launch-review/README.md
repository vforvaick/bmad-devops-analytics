# Post-Launch Review Workflow

## Overview

Evidence synthesis workflow that analyzes 24-72 hours of production data to generate actionable insights. This is the **learning** step in the deploy → monitor → learn → refine cycle.

## Trigger

24-72 hours after production deployment (configurable based on traffic volume).

## Agents Involved

- **PM** - Product perspective and prioritization
- **Analyst** - Data analysis and pattern recognition
- **SRE Agent** - Infrastructure and performance insights
- **Analytics Agent** - User behavior and feature adoption

## Duration

1-2 hours

## Inputs

### From Evidence Adapters
- Application logs (errors, warnings, info)
- Error reports (Sentry or equivalent)
- Metrics (Prometheus, system health)
- Traces (OpenTelemetry, if available)
- Analytics events (PostHog, user behavior)

### From BMAD Artifacts
- PRD (expected behavior)
- UX specifications (expected user flows)
- Architecture documentation
- Deployment log

## Outputs

- `post-launch-insights.md` - **Primary artifact** for spec refinement
- `observability-report.md` - Technical deep-dive (SRE)
- `usage-insights.md` - Product analytics (Analytics Agent)

## Analysis Dimensions

### 1. Errors and Stability

**Questions:**
- What are the top 5 errors by frequency?
- What are the top 5 errors by user impact?
- Are there any critical errors causing user-facing failures?
- What percentage of requests result in errors?

**Actionable Outputs:**
- Critical bugs → High-priority epics
- Moderate bugs → Backlog items
- Error handling gaps → Technical debt

### 2. Performance

**Questions:**
- What are the slowest endpoints (p95, p99)?
- Are there any performance regressions vs staging?
- What's the database query performance?
- Are there any timeout issues?

**Actionable Outputs:**
- Performance bottlenecks → Optimization epics
- Infrastructure limits → Scaling recommendations
- Query optimization needs → Technical stories

### 3. Feature Adoption

**Questions:**
- Which new features are being used?
- Which features are unused or underused?
- Are users discovering features as expected?
- What's the adoption rate trend?

**Actionable Outputs:**
- Unused features → Reconsider in PRD
- High adoption → Double down, expand
- Discovery issues → UX improvements

### 4. User Behavior

**Questions:**
- Where do users drop off?
- What are unexpected usage patterns?
- Are users achieving their goals?
- What flows are broken or confusing?

**Actionable Outputs:**
- Drop-off points → UX refinements
- Unexpected patterns → Product hypotheses
- Broken flows → Bug fixes or PRD updates

### 5. Infrastructure

**Questions:**
- Is infrastructure appropriately sized?
- Are there resource bottlenecks (CPU, memory, disk)?
- What's the cost vs expected?
- Are there scaling concerns?

**Actionable Outputs:**
- Over-provisioned → Cost optimization
- Under-provisioned → Scaling plan
- Architectural limits → Design review

## Synthesis Template

The final `post-launch-insights.md` should follow this structure:

```markdown
# Post-Launch Insights: [Release Name]

**Period**: [Start Date] to [End Date]
**Traffic**: [Request count, active users]
**Status**: [Overall health assessment]

## Executive Summary

3-5 sentences summarizing the most critical findings and recommended actions.

## Top Findings

### 1. [Finding Title]
- **Category**: Error / Performance / Adoption / Behavior / Infrastructure
- **Severity**: Critical / High / Medium / Low
- **Evidence**: [Specific data points]
- **Impact**: [User impact description]
- **Recommendation**: [Actionable next step]

[Repeat for top 5-7 findings]

## Detailed Analysis

### Errors and Stability
[Detailed breakdown with charts/tables]

### Performance
[Latency analysis, bottleneck identification]

### Feature Adoption
[Usage rates, adoption trends]

### User Behavior
[Flow analysis, drop-off points]

### Infrastructure
[Resource utilization, scaling needs]

## Recommendations for PRD Refinement

### New Epics (High Priority)
1. [Epic title] - [1-2 sentence justification]
2. [Epic title] - [1-2 sentence justification]

### PRD Updates
- [Section to update]: [Proposed change based on evidence]
- [Section to update]: [Proposed change based on evidence]

### Backlog Items (Medium/Low Priority)
- [Item description]
- [Item description]

## Appendix

### Metrics Summary
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Error rate | 0.5% | <1% | ✅ Pass |
| p95 latency | 450ms | <500ms | ✅ Pass |
| ... | ... | ... | ... |

### Top Errors
[Detailed error breakdown with stack traces if relevant]

### Raw Data References
- Logs: [Link to log aggregation]
- Metrics: [Link to Grafana dashboard]
- Analytics: [Link to PostHog analysis]
```

## Workflow Steps

1. **Evidence Collection** (10 min)
   - SRE Agent collects logs, metrics, traces
   - Analytics Agent collects usage data and events
   - Verify data completeness

2. **Individual Analysis** (20-30 min)
   - SRE analyzes technical health
   - Analytics analyzes user behavior
   - Each produces their specialized report

3. **Synthesis** (20-30 min)
   - PM and Analyst synthesize findings
   - Prioritize insights by user impact
   - Generate actionable recommendations

4. **Human Review** (15 min)
   - Product team reviews insights
   - Validates interpretation
   - Approves recommendations

## Decision Gates

**Proceed to Spec Refinement if:**
- Insights document is complete
- Critical issues have mitigation plans
- Recommendations are validated by human review

**Return to Monitoring if:**
- Insufficient data collected (extend observation window)
- Critical incident requiring immediate attention

## Next Step

Proceed to `bmad-phase5-spec-refinement` workflow with `post-launch-insights.md` as input.

## Example Prompt

```
/bmad-phase5-post-launch-review

Context:
- 48 hours post-deployment
- 12,500 requests processed
- 450 active users observed
- Evidence collected from all adapters

Analysis Request:
- Synthesize evidence from logs, errors, metrics, traces, analytics
- Identify top 5 findings by user impact
- Generate recommendations for PRD refinement
- Focus on actionable insights

Output: post-launch-insights.md
```

## Common Patterns

**High Error Rate**
- Root cause: Missing null checks in new feature
- Recommendation: Emergency bug fix epic

**Low Feature Adoption**
- Root cause: Feature hidden in menu, no onboarding
- Recommendation: UX improvement + in-app guidance

**Performance Regression**
- Root cause: N+1 query in dashboard
- Recommendation: Database query optimization

**Unexpected Usage**
- Root cause: Users repurposing feature for different use case
- Recommendation: Expand PRD to support discovered use case

**Infrastructure Bottleneck**
- Root cause: Database connection pool too small
- Recommendation: Configuration update + monitoring alert
