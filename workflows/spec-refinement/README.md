# Spec Refinement Workflow

## Overview

Translates production insights from post-launch review into concrete PRD updates and new epic proposals. This completes the feedback loop: `deploy → monitor → learn → **update spec**`.

## Trigger

After `bmad-phase5-post-launch-review` completes and human validates insights.

## Agents Involved

- **PM** - Product prioritization and PRD ownership
- **Analyst** - Data-driven justification and impact assessment

## Duration

30-60 minutes

## Inputs

- `post-launch-insights.md` - Primary input
- `PRD.md` - Current product requirements document
- `architecture.md` - Architecture documentation
- `_bmad-output/planning-artifacts/epics/` - Existing epics

## Outputs

- `PRD-v2-draft.md` - **Draft PRD updates** (for human review)
- `new-epics/` - Draft epic proposals with justification
- `spec-refinement-log.md` - Change log and rationale

## Workflow Steps

### 1. Insight Categorization (5-10 min)

Categorize each finding from `post-launch-insights.md`:

| Category | Action Type | Priority |
|----------|-------------|----------|
| **Critical Bugs** | Emergency Epic | P0 |
| **Feature Gaps** | PRD Update + Epic | P1 |
| **UX Issues** | PRD Update + Story | P1-P2 |
| **Performance** | Technical Epic | P2 |
| **Unused Features** | PRD Removal/Revision | P2 |
| **Unexpected Usage** | PRD Expansion | P2-P3 |
| **Infrastructure** | Operations Epic | P3 |

### 2. PRD Updates (15-20 min)

For each insight requiring PRD change:

**Template:**
```markdown
## PRD Section: [Section Name]

### Current Text
> [Quote existing PRD text]

### Proposed Change
> [New text based on production evidence]

### Justification
**Evidence**: [Reference to post-launch-insights.md]
**User Impact**: [Description of user impact]
**Priority**: [P0/P1/P2/P3]

### Change Type
- [ ] Addition (new requirement)
- [ ] Modification (update existing requirement)
- [ ] Removal (feature not working as expected)
- [ ] Clarification (ambiguous requirement)
```

**Common PRD Update Patterns:**

**Feature Gap Discovered:**
```markdown
### Current
User authentication via email/password only.

### Proposed
User authentication via email/password, Google OAuth, and GitHub OAuth.

### Justification
Evidence: 35% of users attempted social login (post-launch-insights.md, Finding #2)
User Impact: Reduces signup friction, increases conversion
Priority: P1
```

**Unused Feature:**
```markdown
### Current
Advanced search with 12 filter options...

### Proposed
Basic search with 4 most-used filters (name, date, status, category).
Move advanced filters to "power user" mode.

### Justification
Evidence: Only 2% of users used advanced filters; 89% used basic search (post-launch-insights.md, Finding #5)
User Impact: Simplifies UI for 98% of users
Priority: P2
```

**Unexpected Usage:**
```markdown
### Current
Export feature supports CSV format.

### Proposed
Export feature supports CSV, JSON, and Excel formats.

### Justification
Evidence: 45% of support tickets requested non-CSV export formats (post-launch-insights.md, Finding #7)
User Impact: Reduces support burden, improves user satisfaction
Priority: P1
```

### 3. Epic Generation (15-20 min)

For each high-priority insight:

**Epic Template:**
```markdown
# Epic: [Title]

**Priority**: [P0/P1/P2/P3]
**Category**: [Feature / Bug / Performance / UX / Infrastructure]
**Estimated Effort**: [S/M/L/XL]

## Problem Statement
[Description of the issue discovered in production]

## Evidence from Production
- **Source**: post-launch-insights.md, Finding #[N]
- **Data Points**: [Key metrics, error counts, user impact]
- **User Impact**: [Description of how this affects users]

## Proposed Solution
[High-level solution approach]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Dependencies
- [Other epics or infrastructure requirements]

## Related PRD Sections
- [Links to affected PRD sections]

## Acceptance Criteria (Draft)
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

## Notes
[Additional context or considerations]
```

**Example Epic:**

```markdown
# Epic: Fix Payment Processing Error Handling

**Priority**: P0
**Category**: Bug
**Estimated Effort**: M

## Problem Statement
Payment processing errors are not handled gracefully, causing users to see generic error messages and lose trust in the checkout process. 8% of transactions are failing due to insufficient error handling.

## Evidence from Production
- **Source**: post-launch-insights.md, Finding #1
- **Data Points**: 
  - 287 payment errors in 48h (8% of transactions)
  - Top error: "Card declined" shown as "Unknown error"
  - Users abandoning after error: 92%
- **User Impact**: High - directly affects revenue and trust

## Proposed Solution
Implement comprehensive error handling for payment gateway responses:
- Map gateway error codes to user-friendly messages
- Add retry logic for transient failures
- Implement fallback payment methods
- Log detailed error context for debugging

## Success Criteria
- [ ] Error rate < 2% (accounting for legitimate declines)
- [ ] User-facing errors are actionable
- [ ] Retry recovery rate > 30%
- [ ] Post-error completion rate > 50%

## Dependencies
- None (can be implemented immediately)

## Related PRD Sections
- Section 3.4: Payment Processing
- Section 5.2: Error Handling

## Acceptance Criteria (Draft)
- [ ] All payment gateway error codes mapped to user messages
- [ ] Retry logic implemented with exponential backoff
- [ ] Error logging includes full context
- [ ] Unit tests cover all error scenarios
- [ ] Integration tests validate error handling

## Notes
This should be prioritized immediately as it directly impacts revenue.
```

### 4. Impact Assessment (10 min)

Summarize the proposed changes:

```markdown
# Spec Refinement Impact Summary

**PRD Updates**: [Count] sections affected
**New Epics**: [Count] proposed
**Estimated Total Effort**: [Total effort in story points or weeks]

## Priority Breakdown
- **P0 (Critical)**: [Count] epics
- **P1 (High)**: [Count] epics
- **P2 (Medium)**: [Count] epics
- **P3 (Low)**: [Count] epics

## Categories
- **Bugs**: [Count]
- **Features**: [Count]
- **Performance**: [Count]
- **UX**: [Count]
- **Infrastructure**: [Count]

## Recommended Next Sprint Focus
Based on evidence, recommend prioritizing:
1. [Epic title] - [Justification]
2. [Epic title] - [Justification]
3. [Epic title] - [Justification]
```

## Governance: Human Review Gate

**CRITICAL**: All outputs are **DRAFTS** for human review. No automatic PRD updates.

### Human Review Checklist

- [ ] PRD updates align with product vision
- [ ] Epic priorities reflect business priorities
- [ ] Effort estimates are reasonable
- [ ] No north-star drift detected
- [ ] Evidence interpretation is sound
- [ ] Recommendations are actionable

### Approval Process

1. **PM reviews drafts**
2. **Product team discusses in refinement meeting**
3. **Approved changes are manually merged** to official PRD
4. **Approved epics are manually added** to backlog
5. **Next sprint planning** incorporates refined spec

## Next Step

**After human approval:**
- Merge `PRD-v2-draft.md` changes to official `PRD.md`
- Move approved epics to `_bmad-output/planning-artifacts/epics/`
- Proceed to BMAD sprint planning with refined spec

**Loop closes:**
```
Implementation (Phase 4)
    ↓
Deploy (Phase 5.2)
    ↓
Monitor (Phase 5.3)
    ↓
Learn (Phase 5.4)
    ↓
Refine Spec (Phase 5.5) ← YOU ARE HERE
    ↓
Sprint Planning (Phase 2) ← BACK TO BMAD CORE
```

## Example Prompt

```
/bmad-phase5-spec-refinement

Context:
- post-launch-insights.md completed
- 7 findings identified (3 P0, 2 P1, 2 P2)
- PRD needs updates in sections 3, 5, 7
- Ready to generate epic proposals

Request:
- Review each finding from post-launch-insights.md
- Draft PRD updates with justification
- Generate epic proposals for P0 and P1 findings
- Summarize impact and recommended next sprint focus

Output:
- PRD-v2-draft.md
- new-epics/ directory with draft epic documents
- spec-refinement-log.md

Remember: These are drafts for human review and approval.
```

## Common Patterns

### Pattern 1: Critical Bug → Emergency Epic

```
Evidence: High-severity error affecting 15% of users
→ P0 Epic with immediate fix
→ No PRD change (bug, not design issue)
→ Fast-track to implementation
```

### Pattern 2: Feature Gap → PRD Update + Epic

```
Evidence: Users requesting missing capability
→ Update PRD to include requirement
→ Generate P1 epic to implement
→ Include in next sprint
```

### Pattern 3: Unused Feature → PRD Simplification

```
Evidence: Feature unused by 95% of users
→ Update PRD to remove or simplify feature
→ Generate P2 epic to deprecate/simplify
→ Backlog for future sprint
```

### Pattern 4: Unexpected Usage → PRD Expansion

```
Evidence: Users repurposing feature creatively
→ Expand PRD to officially support use case
→ Generate P2 epic to improve support
→ Validate hypothesis first
```

## Maturity Path (Future)

**v1 (Current): Mode A - Manual Review**
- All changes require human approval
- Safest, prevents drift

**v2 (Future): Mode B - Assisted Drafting**
- Agent can merge low-risk PRD clarifications
- Human approves structural changes

**v3 (Future): Mode C - Autonomous Updates**
- Agent autonomously commits certain change types
- Human reviews afterward
- High risk, experimental only

v1 is production-ready. v2 and v3 are roadmap items.
