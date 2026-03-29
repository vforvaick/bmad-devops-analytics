# Release Readiness Review: [Release Version/Name]

**Date**: [YYYY-MM-DD]
**Candidate**: [branch @ commit]
**Target Environment**: [environment]
**Deployment Mode**: [fresh-machine | existing-deployment]
**Reviewers**: Architect, Test Architect, DevOps
**Decision**: [PASS | CONCERNS | FAIL]
**Evidence Freshness**: [fresh | partially stale | stale]

## Summary
[2-5 sentences summarizing release readiness, major risks, and why the decision is justified.]

## Candidate Control
- **Source Of Truth Branch**: [branch]
- **Candidate Commit**: [sha]
- **Competing Branch Ambiguity**: [none | describe ambiguity]
- **Target Change Scope**: [services, migrations, user-facing features]

## Checklist Validation
- **Current-State Snapshot**: [pass | concerns | fail] - [notes]
- **Architecture Risks**: [pass | concerns | fail] - [notes]
- **Test Coverage**: [pass | concerns | fail] - [notes]
- **Environment Config**: [pass | concerns | fail] - [notes]
- **Observability Hooks**: [pass | concerns | fail] - [notes]
- **User Journey Evidence**: [pass | concerns | fail] - [notes]
- **Alert Ownership**: [pass | concerns | fail] - [notes]
- **Rollback Plan**: [pass | concerns | fail] - [notes]

## Open Risks
1. **[Risk Title]**
   - **Severity**: [critical | high | medium | low]
   - **Impact**: [user, system, operational]
   - **Mitigation**: [what reduces risk before or after deploy]

## Blocking Issues
1. [Issue description and why it blocks release]

## Non-Blocking Concerns
1. [Concern description, owner, and mitigation]

## Deployment Preconditions
- [ ] Candidate branch and commit still match this review
- [ ] Required secrets and environment variables are present
- [ ] Baseline or greenfield prerequisites are recorded
- [ ] Observability contract is available
- [ ] Rollback path is concrete and tested enough for this release

## Evidence References
- **Planning Artifacts**: [paths]
- **Implementation Evidence**: [paths]
- **Production Baseline**: [path or N/A]
- **Observability Config**: [path or N/A]

## Next Steps
- **Recommended Workflow**: [/bmad-bda-deploy | return to implementation]
- **Operator Notes**: [any important caveats]
