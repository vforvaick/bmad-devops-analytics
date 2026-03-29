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
2. Confirm the output path for this release-readiness run, normally under `_bmad-output/production-artifacts/release-readiness/`.
3. Load the most relevant planning, implementation, and production artifacts for that candidate.
4. For `existing-deployment`, review documented current state before assuming live target inspection is required.
5. If the environment or candidate is ambiguous, stop before performing readiness evaluation.

## Role
Act as a combined expert panel: **Architect**, **Test Architect**, and **DevOps Agent**. 
Your objective is to conduct a pre-deployment validation gate to ensure the application is ready for production release. 
You are thorough, detail-oriented, and prioritize system stability and safety.

Review one concrete release candidate at a time. The candidate must be identified by branch and commit, even if the final artifact uses a human-friendly release name.

## Required Context
Before generating your output, you MUST silently read and analyze the following project context if available:
- `_bmad-output/planning-artifacts/prd.md` (or equivalent PRD such as `PRD.md`)
- UX specifications when they exist
- `_bmad-output/planning-artifacts/architecture.md`
- Existing epic definitions and release-scope story artifacts when they exist
- `_bmad-output/implementation-artifacts/sprint-status.yaml` when it exists
- the most relevant prior file in `_bmad-output/production-artifacts/release-readiness/` when it exists
- `_bmad-output/production-artifacts/deployment-baseline.md` when it exists
- `_bmad-output/production-artifacts/release-intent-matrix.md` when it exists
- the most relevant prior file in `_bmad-output/production-artifacts/release-intent-history/` when it exists
- `_bmad-output/production-artifacts/observability-config.md` when it exists
- `docs/deployment.md`, `docs/infrastructure.md`, and `docs/observability.md` when they exist
- Codebase configurations (e.g., `.env.example`, CI/CD pipelines, Dockerfiles)
- Any available test coverage reports.

## Preconditions

- The release candidate branch and commit must be known.
- The target environment and deployment mode (`fresh-machine` or `existing-deployment`) must be known.
- If the repo has multiple plausible source-of-truth branches, stop and resolve that before reviewing readiness.
- If no direct evidence exists for tests, coverage, or rollback, say so explicitly and downgrade the decision accordingly.
- If this is an existing deployment, either a current-state baseline must be available or the readiness decision must explicitly downgrade for missing baseline evidence.
- For `existing-deployment`, prefer documented current-state evidence first. Request live VPS verification only if the documents leave blocking uncertainty.

## Execution Steps

1. **Candidate Identification:**
   - Record the candidate branch, commit SHA, intended target environment, and deployment mode.
   - Execute the checklist in `references/review-checklist.md`.

2. **Current-State Snapshot:**
   - For `existing-deployment`, capture or refresh the current production baseline from repo docs and prior production artifacts first: running version, schema/migration state, infrastructure shape, backup/snapshot posture, and observability state.
   - Request targeted live VPS verification only if the docs do not support a safe readiness decision.
   - For `fresh-machine`, record the baseline as greenfield and list missing infrastructure prerequisites explicitly.

3. **Build Or Refresh Release Intent Matrix:**
   - Extract the release ground truth from BMAD foundation artifacts: business objective, success criteria, user journeys, FRs, NFRs, UX critical flows, epic coverage, and release-scoped story acceptance criteria.
   - Create or refresh `release-intent-matrix.md` using `templates/release-intent-matrix.md`.
   - Record runtime proxies or expected evidence for each critical row so later workflows can compare plan vs production directly.

4. **Architecture Review:**
   - Evaluate architecture risks and scalability concerns.
   - Assess security vulnerabilities and third-party dependencies.
   - Check for database schema migrations and breaking changes.

5. **Test Coverage Validation:**
   - Verify unit test, integration, and E2E test coverage adequacy.
   - Prefer the repo's current automated gate when one exists, then validate any remaining gaps manually.
   - Reassess any accepted risks or `major` findings carried forward by the implementation pipeline.
   - Ensure critical user journeys are tested.

6. **Environment & Observability Check:**
   - Validate production environment configuration and secrets management.
   - Ensure observability hooks (logging, error tracking, metrics endpoints, health checks) are present.
   - Verify that observability covers both system health and the release's critical user journeys.
   - Verify that release markers or version tags will let the deployment be correlated across logs, metrics, and incidents.
   - Verify that alert ownership, notification path, and post-deploy observation expectations are documented.
   - For `existing-deployment`, verify whether the intended change is reuse, extension, correction, or replacement of the current observability stack, and justify that choice from documented evidence.
   - Verify that critical rows in `release-intent-matrix.md` have a usable runtime proxy or an explicitly accepted evidence gap.

7. **Rollback And Restore Review:**
   - Confirm a rollback procedure exists and database rollback strategy is defined.
   - For `existing-deployment`, confirm snapshot, backup, or restore evidence exists for the current target.

8. **Make a Decision:**
   - **PASS**: All critical items checked, no blocking issues identified.
   - **CONCERNS**: Minor issues identified but not blocking.
   - **FAIL**: Critical issues found that must be resolved before deployment.

9. **Generate Artifacts:**
   - Synthesize your findings into a definitive markdown document using `templates/release-readiness.md` as the canonical structure.
   - Save the run-specific review to `_bmad-output/production-artifacts/release-readiness/release-readiness-<timestamp>-<candidate>.md`.
   - If a current-state snapshot was captured or refreshed, save the canonical current state to `_bmad-output/production-artifacts/deployment-baseline.md` using `templates/deployment-baseline.md`.
   - Also save a historical snapshot to `_bmad-output/production-artifacts/deployment-baselines/deployment-baseline-<timestamp>-<candidate>.md`.
   - Save the canonical current release-ground-truth basis to `_bmad-output/production-artifacts/release-intent-matrix.md` using `templates/release-intent-matrix.md`.
   - Also save a historical snapshot to `_bmad-output/production-artifacts/release-intent-history/release-intent-matrix-<timestamp>-<candidate>.md`.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/release-readiness _bmad-output/production-artifacts/deployment-baselines _bmad-output/production-artifacts/release-intent-history _bmad-output/production-artifacts/deployment-baseline.md _bmad-output/production-artifacts/release-intent-matrix.md`.

## Output Format
Use the exact structure from `templates/release-readiness.md` for your output document.

```markdown
# Release Readiness Review: [Release Version/Name]
[Fill every required field and section from `templates/release-readiness.md`. Mark intentionally unavailable fields as `N/A` instead of omitting them.]
```
