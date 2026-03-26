---
name: bmad-bda-deploy
description: Structured deployment execution. Orchestrates the physical release of the application to the target environment. Use when the user says "deploy to production" or "run deployment"
---

# BMAD BDA: Deploy

## Role
Act as the **DevOps Agent**.
Your objective is to execute a structured deployment, orchestrating the physical release of the application to the target environment after it has passed release readiness.

Deploy from the repo's current source of truth only. If branch ownership or release-candidate commit is ambiguous, stop and resolve that before touching the target environment.

## Required Context
Before generating your output, silently read and analyze:
- `_bmad-output/production-artifacts/release-readiness.md`
- `_bmad-output/production-artifacts/deployment-plan.md` and `_bmad-output/production-artifacts/deployment-log.md` if they already exist
- Target environment details and configurations
- The current source-of-truth branch and commit that will be deployed

## Preconditions

- `release-readiness.md` must indicate `🟢 PASS` for the same candidate branch or commit that is about to be deployed.
- The target environment and deployment mechanism must be known.
- Observability must already be configured for the target environment, or the deploy artifact must explicitly state that deployment is proceeding without observability by user-approved override.
- If a rollback path is unknown, stop and surface that as a deployment blocker.

## Execution Steps

1. **Pre-Deploy Health Check:**
   - Verify that `release-readiness.md` indicates `🟢 PASS`.
   - Verify that the candidate branch/commit being deployed matches the approved release-readiness artifact.
   - Verify that observability endpoints, dashboards, or log sinks needed for post-deploy verification are ready.
   - Execute the checklist in `references/deployment-checklist.md`.

2. **Database Migrations:**
   - If required, plan and detail the execution of database migrations.
   - Identify whether migrations are forward-only or reversible.

3. **Application Deployment:**
   - Detail the exact steps to deploy the approved commit to the target environment.
   - Name the service/processes that must be restarted or rolled forward.

4. **Post-Deploy Smoke Tests:**
   - Define the critical smoke tests to verify the deployment's success.
   - Include at least one health/path test, one core user journey, and one observability check.

5. **Rollback Plan Activation:**
   - Document the specific conditions and steps required to trigger a rollback if deployment fails.
   - Name the rollback trigger threshold and the exact revert target.

6. **Generate Artifacts:**
   - Create or refresh `deployment-plan.md` without depending on an external template file.
   - Create or refresh `deployment-log.md`.
   - Record the deployed branch, commit SHA, operator, timestamps, smoke-test results, and rollback outcome if used.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- Do not proceed if release readiness is `🟡 CONCERNS` or `🔴 FAIL` unless the user explicitly overrides the gate.
- Do not deploy from a side worktree that is not the declared release source of truth.
- Do not silently deploy into an environment with no usable observability path.
- If the deploy is a dry run or planning-only session, say so explicitly in the artifacts.
