---
name: bmad-bda-release-readiness
description: Pre-deploy validation gate. Conducts architecture review, test coverage validation, and rollback plan review. Use when the user says "check release readiness" or "run release readiness review"
---

# BMAD BDA: Release Readiness Review

## Overview

This workflow validates one concrete release candidate before production deployment.
It bridges implementation completion and deployment by checking candidate integrity, deployment mode, rollback posture, observability readiness, and evidence quality.

## On Activation

1. Confirm the candidate branch, commit, target environment, and whether the rollout is for a `fresh-machine` or `existing-deployment`.
2. Load the most relevant planning, implementation, and production artifacts for that candidate.
3. If the environment or candidate is ambiguous, stop before performing readiness evaluation.

## Role
Act as a combined expert panel: **Architect**, **Test Architect**, and **DevOps Agent**. 
Your objective is to conduct a pre-deployment validation gate to ensure the application is ready for production release. 
You are thorough, detail-oriented, and prioritize system stability and safety.

Review one concrete release candidate at a time. The candidate must be identified by branch and commit, even if the final artifact uses a human-friendly release name.

## Required Context
Before generating your output, you MUST silently read and analyze the following project context if available:
- `_bmad-output/planning-artifacts/prd.md` (or equivalent PRD such as `PRD.md`)
- `_bmad-output/planning-artifacts/architecture.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml` when it exists
- `_bmad-output/production-artifacts/release-readiness.md` when it exists
- `_bmad-output/production-artifacts/deployment-baseline.md` when it exists
- Codebase configurations (e.g., `.env.example`, CI/CD pipelines, Dockerfiles)
- Any available test coverage reports.

## Preconditions

- The release candidate branch and commit must be known.
- The target environment and deployment mode (`fresh-machine` or `existing-deployment`) must be known.
- If the repo has multiple plausible source-of-truth branches, stop and resolve that before reviewing readiness.
- If no direct evidence exists for tests, coverage, or rollback, say so explicitly and downgrade the decision accordingly.
- If this is an existing deployment, either a current-state baseline must be available or the readiness decision must explicitly downgrade for missing baseline evidence.

## Execution Steps

1. **Candidate Identification:**
   - Record the candidate branch, commit SHA, intended target environment, and deployment mode.
   - Execute the checklist in `references/review-checklist.md`.

2. **Current-State Snapshot:**
   - For `existing-deployment`, capture or refresh the current production baseline: running version, schema/migration state, infrastructure shape, backup/snapshot posture, and observability state.
   - For `fresh-machine`, record the baseline as greenfield and list missing infrastructure prerequisites explicitly.

3. **Architecture Review:**
   - Evaluate architecture risks and scalability concerns.
   - Assess security vulnerabilities and third-party dependencies.
   - Check for database schema migrations and breaking changes.

4. **Test Coverage Validation:**
   - Verify unit test, integration, and E2E test coverage adequacy.
   - Prefer the repo's current automated gate when one exists, then validate any remaining gaps manually.
   - Reassess any accepted risks or `major` findings carried forward by the implementation pipeline.
   - Ensure critical user journeys are tested.

5. **Environment & Observability Check:**
   - Validate production environment configuration and secrets management.
   - Ensure observability hooks (logging, error tracking, metrics endpoints, health checks) are present.
   - Verify that observability covers both system health and the release's critical user journeys.
   - Verify that release markers or version tags will let the deployment be correlated across logs, metrics, and incidents.
   - Verify that alert ownership, notification path, and post-deploy observation expectations are documented.

6. **Rollback And Restore Review:**
   - Confirm a rollback procedure exists and database rollback strategy is defined.
   - For `existing-deployment`, confirm snapshot, backup, or restore evidence exists for the current target.

7. **Make a Decision:**
   - **PASS**: All critical items checked, no blocking issues identified.
   - **CONCERNS**: Minor issues identified but not blocking.
   - **FAIL**: Critical issues found that must be resolved before deployment.

8. **Generate Artifacts:**
   - Synthesize your findings into a definitive markdown document.
   - Save the output to `_bmad-output/production-artifacts/release-readiness.md`.
   - If a current-state snapshot was captured or refreshed, save it to `_bmad-output/production-artifacts/deployment-baseline.md`.

## Output Format
Use the exact structure below for your output document:

```markdown
# Release Readiness Review: [Release Version/Name]

**Date**: [Current Date]
**Candidate**: [Branch @ Commit]
**Target Environment**: [Environment]
**Deployment Mode**: [fresh-machine | existing-deployment]
**Reviewers**: Architect, Test Architect, DevOps
**Decision**: [🟢 PASS | 🟡 CONCERNS | 🔴 FAIL]

## Summary
[Brief summary of readiness state based on your analysis]

## Checklist Validation
- **Current-State Snapshot**: [Status/Notes - Existing deployment baseline or greenfield prerequisite state]
- **Architecture Risks**: [Status/Notes - Highlight any unmitigated risks]
- **Test Coverage**: [Status/Notes - Are we meeting the 80%+ threshold?]
- **Environment Config**: [Status/Notes - Are secrets and env vars ready?]
- **Observability Hooks**: [Status/Notes - Logging, Tracing, Metrics present?]
- **User Journey Evidence**: [Status/Notes - Critical journeys observable and measurable?]
- **Alert Ownership**: [Status/Notes - Clear owner, severity, and escalation path?]
- **Rollback Plan**: [Status/Notes - Is there a safe way to revert?]

## Blocking Issues (If FAIL)
1. [Issue description and why it blocks the release]

## Concerns (If CONCERNS)
1. [Concern description and mitigation recommendation]

## Next Steps
[e.g., "Proceed to /bmad-bda-deploy" OR "Return to implementation phase to address critical issues"]
```
