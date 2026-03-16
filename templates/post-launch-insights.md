# Post-Launch Insights: [Release Name/Version]

**Period**: [Start Date] to [End Date]  
**Traffic**: [Total requests], [Active users]  
**Status**: 🟢 Healthy | 🟡 Concerns | 🔴 Critical Issues  
**Generated**: [Timestamp]

---

## Executive Summary

[3-5 sentences summarizing the most critical findings and recommended actions. Focus on user impact and business priorities.]

**Key Takeaways:**
- 🔴 **Critical**: [Most urgent finding]
- 🟡 **Important**: [High-priority finding]
- 🟢 **Success**: [What worked well]

---

## Top Findings

### Finding #1: [Title - e.g., "Payment Processing Errors"]

**Category**: 🔴 Error / 🟡 Performance / 🔵 Adoption / 🟣 Behavior / 🟠 Infrastructure  
**Severity**: Critical | High | Medium | Low  
**User Impact**: [Description of how this affects users]

**Evidence:**
- [Specific metric]: [Value]
- [Data point]: [Details]
- [Observation]: [Description]

**Root Cause Analysis:**
[Brief analysis of why this is happening]

**Recommendation:**
[Specific, actionable next step with priority]

---

### Finding #2: [Title]

**Category**: [Category]  
**Severity**: [Severity]  
**User Impact**: [Impact description]

**Evidence:**
- [Metric/data point]
- [Metric/data point]

**Root Cause Analysis:**
[Analysis]

**Recommendation:**
[Action item]

---

### Finding #3: [Title]

[Repeat structure for top 5-7 findings]

---

## Detailed Analysis

### 1. Errors and Stability

**Overall Error Rate**: [X%] (Target: <1%)

#### Top Errors by Frequency

| Error | Count | % of Total | First Seen | User Impact |
|-------|-------|------------|------------|-------------|
| [Error message] | [Count] | [%] | [Date] | [High/Med/Low] |
| [Error message] | [Count] | [%] | [Date] | [High/Med/Low] |
| [Error message] | [Count] | [%] | [Date] | [High/Med/Low] |

#### Top Errors by User Impact

1. **[Error Title]**
   - **Frequency**: [Count] occurrences
   - **Affected Users**: [Count] users
   - **Impact**: [Description]
   - **Stack Trace**: [Link to error tracking]

2. **[Error Title]**
   - [Details]

#### Error Trend
[Description of whether errors are increasing, decreasing, or stable]

#### Recommendations
- [ ] Fix critical errors (P0)
- [ ] Add error handling for [scenario]
- [ ] Improve error messages for [case]

---

### 2. Performance

**Overall Latency**:
- **p50**: [X]ms (Target: <200ms)
- **p95**: [X]ms (Target: <500ms)
- **p99**: [X]ms (Target: <1000ms)

#### Slowest Endpoints

| Endpoint | p50 | p95 | p99 | Request Count | Status |
|----------|-----|-----|-----|---------------|--------|
| [Route] | [X]ms | [X]ms | [X]ms | [Count] | 🔴/🟡/🟢 |
| [Route] | [X]ms | [X]ms | [X]ms | [Count] | 🔴/🟡/🟢 |

#### Performance Bottlenecks

1. **[Bottleneck Title]**
   - **Component**: [Database/API/Backend/Frontend]
   - **Evidence**: [Metric data]
   - **Root Cause**: [Analysis]
   - **Impact**: [User experience impact]

2. **[Bottleneck Title]**
   - [Details]

#### Database Performance
- **Query Count**: [X] queries/sec
- **Slowest Queries**: [List top 3]
- **Connection Pool**: [X]% utilization

#### Recommendations
- [ ] Optimize [endpoint/query]
- [ ] Add caching for [resource]
- [ ] Consider CDN for [assets]
- [ ] Scale [component] if traffic increases

---

### 3. Feature Adoption

**New Features Released**: [Count]

#### Adoption Rates

| Feature | Active Users | Adoption Rate | Usage Frequency | Trend |
|---------|--------------|---------------|-----------------|-------|
| [Feature] | [Count] | [X%] | [X] times/user | 📈/📊/📉 |
| [Feature] | [Count] | [X%] | [X] times/user | 📈/📊/📉 |

#### High Adoption Features ✅
- **[Feature Name]**: [X%] adoption, [observations]
- **[Feature Name]**: [X%] adoption, [observations]

**Why it worked**: [Analysis]

#### Low Adoption Features ⚠️
- **[Feature Name]**: [X%] adoption, [observations]
- **[Feature Name]**: [X%] adoption, [observations]

**Hypotheses for low adoption**:
- [Possible reason 1]
- [Possible reason 2]

#### Recommendations
- [ ] Double down on [high-adoption feature]
- [ ] Improve discoverability of [low-adoption feature]
- [ ] Reconsider [unused feature] in PRD
- [ ] Add onboarding for [feature]

---

### 4. User Behavior

#### User Flow Analysis

**Critical Flows Analyzed**: [Count]

#### Drop-off Points

| Flow | Step | Drop-off Rate | Users Affected | Severity |
|------|------|---------------|----------------|----------|
| [Flow name] | [Step name] | [X%] | [Count] | 🔴/🟡/🟢 |
| [Flow name] | [Step name] | [X%] | [Count] | 🔴/🟡/🟢 |

#### Top Drop-off: [Flow Name]

```
Step 1: [Name]     → [X]% proceed
Step 2: [Name]     → [X]% proceed
Step 3: [Name]     → [X]% proceed  ⚠️ [Y]% drop off here
Step 4: [Name]     → [X]% proceed
```

**Why users drop off at Step 3**:
- [Hypothesis 1 based on evidence]
- [Hypothesis 2 based on evidence]

#### Unexpected Usage Patterns

1. **[Pattern Description]**
   - **Observation**: [What users are doing]
   - **Expected**: [What was designed]
   - **Frequency**: [How often]
   - **Implication**: [What this means]

2. **[Pattern Description]**
   - [Details]

#### User Segmentation Insights

**Power Users** ([X]% of total):
- [Behavior pattern]
- [Feature usage]

**Casual Users** ([X]% of total):
- [Behavior pattern]
- [Feature usage]

#### Recommendations
- [ ] Fix drop-off at [step]
- [ ] Support discovered use case: [description]
- [ ] Simplify [complex flow]
- [ ] Add guidance at [confusion point]

---

### 5. Infrastructure

**Overall Health**: 🟢 Good | 🟡 Acceptable | 🔴 Needs Attention

#### Resource Utilization

| Resource | Average | Peak | Threshold | Status |
|----------|---------|------|-----------|--------|
| CPU | [X%] | [X%] | 80% | 🔴/🟡/🟢 |
| Memory | [X%] | [X%] | 80% | 🔴/🟡/🟢 |
| Disk | [X%] | [X%] | 90% | 🔴/🟡/🟢 |
| Network | [X] Mbps | [X] Mbps | [X] Mbps | 🔴/🟡/🟢 |

#### Scaling Observations

**Current Capacity**: [Description]  
**Traffic Pattern**: [Pattern description]  
**Projected Growth**: [Estimate]

#### Infrastructure Issues

1. **[Issue Title]**
   - **Impact**: [Description]
   - **Frequency**: [How often]
   - **Mitigation**: [Current workaround]

#### Cost Analysis

**Current Cost**: $[X]/month  
**Cost per User**: $[X]  
**Efficiency**: [Assessment]

#### Recommendations
- [ ] Scale [component] to handle [scenario]
- [ ] Optimize [resource] usage
- [ ] Add monitoring for [metric]
- [ ] Consider [architectural change]

---

## Recommendations for PRD Refinement

### New Epics (High Priority)

#### 1. [Epic Title] - Priority: P0

**Problem**: [Problem statement from evidence]  
**Evidence**: [Reference to findings]  
**Proposed Solution**: [High-level approach]  
**Estimated Effort**: [S/M/L/XL]  
**Success Criteria**: [How to measure success]

#### 2. [Epic Title] - Priority: P1

[Details]

#### 3. [Epic Title] - Priority: P1

[Details]

---

### PRD Updates Required

#### Section: [PRD Section Name]

**Current Text**:
> [Quote from current PRD]

**Proposed Change**:
> [Updated text based on evidence]

**Justification**: [Why this change is needed, backed by findings]

---

#### Section: [PRD Section Name]

[Repeat for each section needing update]

---

### Backlog Items (Medium/Low Priority)

- [ ] **[Item Title]** (P2) - [Brief description and justification]
- [ ] **[Item Title]** (P2) - [Brief description and justification]
- [ ] **[Item Title]** (P3) - [Brief description and justification]

---

## Next Sprint Recommendations

Based on production evidence, recommend prioritizing:

1. **[Epic/Story Title]** - [Justification based on user impact]
2. **[Epic/Story Title]** - [Justification based on frequency]
3. **[Epic/Story Title]** - [Justification based on business value]

**Estimated Sprint Capacity**: [X] story points  
**Recommended Focus**: [Error fixes / New features / Performance / UX]

---

## Appendix

### A. Metrics Summary

| Metric | Value | Target | Status | Change vs Previous |
|--------|-------|--------|--------|-------------------|
| Uptime | [X%] | 99.9% | 🔴/🟡/🟢 | [+/-X%] |
| Error Rate | [X%] | <1% | 🔴/🟡/🟢 | [+/-X%] |
| p95 Latency | [X]ms | <500ms | 🔴/🟡/🟢 | [+/-X ms] |
| Active Users | [X] | [Target] | 🔴/🟡/🟢 | [+/-X%] |
| Conversion Rate | [X%] | [Target%] | 🔴/🟡/🟢 | [+/-X%] |

### B. Raw Data References

- **Logs**: [Link to log aggregation dashboard]
- **Metrics**: [Link to Grafana dashboard]
- **Errors**: [Link to Sentry project]
- **Analytics**: [Link to PostHog analysis]
- **Traces**: [Link to Jaeger UI]

### C. Evidence Collection Details

**Data Sources**:
- Logs: [Source and volume]
- Errors: [Source and count]
- Metrics: [Source and retention]
- Traces: [Sample rate]
- Analytics: [Events tracked]

**Evidence Quality**:
- ✅ Complete: [List complete data sources]
- ⚠️ Partial: [List partial data sources]
- ❌ Missing: [List missing data sources]

### D. Comparison to Baseline

[If this is not the first post-launch review, compare to previous iteration]

| Metric | Previous | Current | Change | Assessment |
|--------|----------|---------|--------|------------|
| Error Rate | [X%] | [X%] | [+/-X%] | [Better/Same/Worse] |
| p95 Latency | [X]ms | [X]ms | [+/-X ms] | [Better/Same/Worse] |
| Feature Adoption | [X%] | [X%] | [+/-X%] | [Better/Same/Worse] |

---

## Review and Approval

**Prepared by**: [SRE Agent + Analytics Agent + Analyst]  
**Reviewed by**: [PM Name - Human]  
**Date**: [Review Date]  
**Status**: ⏳ Pending Review | ✅ Approved | 🔄 Revisions Needed

**Next Steps**:
1. Product team reviews findings
2. Prioritizes recommendations
3. Runs `/bda-spec-refinement`
4. Approves PRD changes and new epics
5. Proceeds to sprint planning with refined spec

---

**This document serves as the evidence base for BMAD spec refinement. All recommendations should be validated by human review before updating official PRD.**
