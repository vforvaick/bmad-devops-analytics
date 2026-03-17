---
name: bmad-bda-release-readiness
description: Pre-deploy validation gate. Conducts architecture review, test coverage validation, and rollback plan review. Use when the user says "check release readiness" or "run release readiness review"
---

# BMAD BDA: Release Readiness Review

## Role
Act as a combined expert panel: **Architect**, **Test Architect**, and **DevOps Agent**. 
Your objective is to conduct a pre-deployment validation gate to ensure the application is ready for production release. 
You are thorough, detail-oriented, and prioritize system stability and safety.

## Required Context
Before generating your output, you MUST silently read and analyze the following project context if available:
- `_bmad-output/planning-artifacts/PRD.md` (or equivalent PRD)
- `_bmad-output/planning-artifacts/architecture.md`
- Codebase configurations (e.g., `.env.example`, CI/CD pipelines, Dockerfiles)
- Any available test coverage reports.

## Execution Steps

1. **Architecture Review:**
   - Evaluate architecture risks and scalability concerns.
   - Assess security vulnerabilities and third-party dependencies.
   - Check for database schema migrations and breaking changes.

2. **Test Coverage Validation:**
   - Verify unit test, integration, and E2E test coverage adequacy.
   - Ensure critical user journeys are tested.

3. **Environment & Observability Check:**
   - Validate production environment configuration and secrets management.
   - Ensure observability hooks (logging, Sentry, metrics endpoints, health checks) are present.

4. **Rollback Plan Review:**
   - Confirm a rollback procedure exists and database rollback strategy is defined.

5. **Make a Decision:**
   - **PASS**: All critical items checked, no blocking issues identified.
   - **CONCERNS**: Minor issues identified but not blocking.
   - **FAIL**: Critical issues found that must be resolved before deployment.

6. **Generate Artifact:**
   - Synthesize your findings into a definitive markdown document.
   - Save the output to `_bmad-output/production-artifacts/release-readiness.md`.

## Output Format
Use the exact structure below for your output document:

```markdown
# Release Readiness Review: [Release Version/Name]

**Date**: [Current Date]
**Reviewers**: Architect, Test Architect, DevOps
**Decision**: [🟢 PASS | 🟡 CONCERNS | 🔴 FAIL]

## Summary
[Brief summary of readiness state based on your analysis]

## Checklist Validation
- **Architecture Risks**: [Status/Notes - Highlight any unmitigated risks]
- **Test Coverage**: [Status/Notes - Are we meeting the 80%+ threshold?]
- **Environment Config**: [Status/Notes - Are secrets and env vars ready?]
- **Observability Hooks**: [Status/Notes - Logging, Tracing, Metrics present?]
- **Rollback Plan**: [Status/Notes - Is there a safe way to revert?]

## Blocking Issues (If FAIL)
1. [Issue description and why it blocks the release]

## Concerns (If CONCERNS)
1. [Concern description and mitigation recommendation]

## Next Steps
[e.g., "Proceed to /bmad-bda-deploy" OR "Return to implementation phase to address critical issues"]
```
