# Release Readiness Review Workflow

## Overview

Pre-deployment validation gate that ensures the application is ready for production release. Conducted by Architect, Test Architect, and DevOps Agent.

## Trigger

When all BMAD Phase 4 (Implementation) epics are complete and team is ready to deploy.

## Agents Involved

- **Architect** - Architecture and infrastructure risks
- **Test Architect** - Test coverage and quality validation
- **DevOps Agent** - Deployment readiness and operational concerns

## Duration

15-30 minutes

## Inputs

- PRD (Product Requirements Document)
- Architecture documentation
- Test coverage reports
- Codebase
- Environment configurations

## Outputs

- `release-readiness.md` - Comprehensive readiness report
- Decision: **PASS** / **CONCERNS** / **FAIL**

## Checklist

### Architecture Review

- [ ] Architecture risks identified and mitigated
- [ ] Scalability concerns addressed
- [ ] Security vulnerabilities assessed
- [ ] Third-party dependencies reviewed
- [ ] Database schema migrations planned
- [ ] Breaking changes documented

### Test Coverage

- [ ] Unit test coverage meets threshold (target: 80%+)
- [ ] Integration tests cover critical paths
- [ ] E2E tests validate key user journeys
- [ ] Performance tests completed
- [ ] Security tests performed
- [ ] Test environments validated

### Environment Configuration

- [ ] Production environment configuration complete
- [ ] Environment variables documented
- [ ] Secrets management configured
- [ ] Database connection strings validated
- [ ] External service endpoints configured
- [ ] Feature flags configured (if applicable)

### Observability Hooks

- [ ] Logging instrumentation present
- [ ] Error tracking configured (Sentry)
- [ ] Metrics endpoints exposed
- [ ] Health check endpoints implemented
- [ ] Tracing instrumentation added (if applicable)
- [ ] Analytics events defined

### Rollback Plan

- [ ] Rollback procedure documented
- [ ] Database rollback strategy defined
- [ ] Previous version available for rollback
- [ ] Rollback success criteria defined
- [ ] Team trained on rollback procedure
- [ ] Rollback tested in staging (recommended)

### Documentation

- [ ] Deployment runbook created
- [ ] Known issues documented
- [ ] Post-deploy smoke tests defined
- [ ] Support team briefed
- [ ] Change communication prepared

## Decision Criteria

### PASS
All critical items checked, no blocking issues identified. Proceed to deployment.

### CONCERNS
Minor issues identified but not blocking. Document concerns and proceed with caution.

### FAIL
Critical issues found that must be resolved before deployment. Return to implementation phase.

## Template Output

See `templates/release-readiness.md` for detailed output format.

## Next Step

If **PASS** or **CONCERNS**: Proceed to `bmad-phase5-deploy` workflow.
If **FAIL**: Return to implementation phase to address critical issues.

## Example Prompt

```
/bmad-phase5-release-readiness

Context:
- All epics from sprint 3 completed
- Test coverage at 85%
- Staging environment validated
- Ready for production deployment

Review:
- Architecture risks
- Test coverage adequacy
- Environment configuration
- Observability readiness
- Rollback plan

Output: release-readiness.md with PASS/CONCERNS/FAIL decision
```

## Common Issues

**Architecture Risks**
- Insufficient horizontal scaling strategy
- Single point of failure not addressed
- Database connection pooling not configured

**Test Coverage Gaps**
- Critical payment flow not covered by E2E tests
- Error handling paths not tested
- Performance under load not validated

**Configuration Issues**
- Production secrets not set up
- CORS configuration missing for production domain
- Feature flags not configured

**Observability Gaps**
- Error tracking not configured
- No health check endpoint
- Logging too verbose or insufficient

**Rollback Concerns**
- Database migration not reversible
- No rollback procedure documented
- Previous version not available
