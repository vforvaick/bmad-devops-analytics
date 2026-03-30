---
name: bmad-bda-deploy
description: Structured deployment execution. Orchestrates the physical release of the application to the target environment. Use when the user says "deploy to production" or "run deployment"
---

# BMAD BDA: Deploy

## Overview

This workflow executes one production deployment for a candidate that has already passed release readiness.
It supports both `fresh-machine` and `existing-deployment` rollouts, with explicit protection for current-state snapshotting, rollback posture, immediate deployment verification, and post-deploy evidence handling.

## On Activation

1. Confirm the approved candidate branch and commit from the selected release-readiness artifact under `_bmad-output/production-artifacts/release-readiness/`.
2. Confirm the target environment and classify the rollout as `fresh-machine` or `existing-deployment`.
3. Load any existing deployment baseline, observability configuration, and prior deployment artifacts before planning execution.
4. For `existing-deployment`, rely on the documented baseline and observability plan first; do not default to rediscovery on the live VPS.
5. Stop immediately if branch ownership, rollback posture, or target environment identity is ambiguous.
6. Treat `bmad-bda-deployment-verification` as a mandatory immediate phase of this workflow, not an optional follow-up.

## Role
Act as the **DevOps Agent**.
Your objective is to execute a structured deployment, orchestrating the physical release of the application to the target environment after it has passed release readiness.

Deploy from the repo's current source of truth only. If branch ownership or release-candidate commit is ambiguous, stop and resolve that before touching the target environment.

## Required Context
Before generating your output, silently read and analyze:
- the selected approved file in `_bmad-output/production-artifacts/release-readiness/`
- `_bmad-output/production-artifacts/deployment-baseline.md` if it exists
- the most relevant file in `_bmad-output/production-artifacts/deployment-baselines/` if it exists
- `_bmad-output/production-artifacts/observability-config.md` if it exists
- the most relevant files in `_bmad-output/production-artifacts/observability-config-history/`, `_bmad-output/production-artifacts/deployment-plans/`, and `_bmad-output/production-artifacts/deployment-logs/` if they exist
- the most relevant file in `_bmad-output/production-artifacts/deployment-verifications/` if it exists
- the most relevant files in `_bmad-output/production-artifacts/operational-decisions/` if they exist
- `docs/deployment.md` and `docs/infrastructure.md` when they exist
- Target environment details and configurations
- The current source-of-truth branch and commit that will be deployed

## Preconditions

- The selected release-readiness artifact must indicate `🟢 PASS` for the same candidate branch or commit that is about to be deployed.
- The target environment and deployment mechanism must be known.
- The rollout mode must be known: `fresh-machine` or `existing-deployment`.
- Observability must already be configured for the target environment, or the deploy artifact must explicitly state that deployment is proceeding without observability by user-approved override.
- The observability path must include release markers or another explicit way to correlate evidence to this deployment candidate.
- The deployment verification path must be known, either by executing `bmad-bda-deployment-verification` inline or by explicitly recording why verification is blocked.
- If a rollback path is unknown, stop and surface that as a deployment blocker.
- If this is an `existing-deployment`, do not mutate production until the current-state snapshot or backup posture has been captured and recorded, unless the user explicitly overrides.
- If this is an `existing-deployment`, do not improvise the target shape from memory. Use the documented baseline and observability artifacts unless the user explicitly requests fresh live discovery.

## Execution Steps

1. **Pre-Deploy Health Check:**
   - Verify that the selected release-readiness artifact indicates `🟢 PASS`.
   - Verify that the candidate branch/commit being deployed matches the approved release-readiness artifact.
   - Verify that the rollout mode and target environment match the approved release-readiness artifact.
   - Verify that observability endpoints, dashboards, or log sinks needed for post-deploy verification are ready.
   - Verify that at least one critical user journey and one system-health path can be checked immediately after rollout.
   - Execute the checklist in `references/deployment-checklist.md`.

2. **Current-State Protection:**
   - For `existing-deployment`, capture or refresh the current baseline from documented evidence first: running version, restore point, backup/snapshot ids, important services, environment-specific caveats, and observability state.
   - Request live verification only when the documented baseline is materially incomplete for safe deployment.
   - For `fresh-machine`, record the bootstrap prerequisites that must exist before the first release can be considered successful.

3. **Database Migrations:**
   - If required, plan and detail the execution of database migrations.
   - Identify whether migrations are forward-only or reversible.

4. **Application Deployment:**
   - Detail the exact steps to deploy the approved commit to the target environment.
   - Name the service/processes that must be restarted or rolled forward.

5. **Immediate Post-Deploy Verification Preparation:**
   - Define the critical smoke tests and the deeper runtime checks required by `bmad-bda-deployment-verification`.
   - Include at least one health/path test, one core user journey, one release-marker verification, one observability check, and one release-specific critical outcome proof.

6. **Deviation And Decision Capture:**
   - If this deployment proceeds through a gate override, missing-but-accepted evidence, temporary mitigation, manual step substitution, or rollback-threshold change, create an operational decision record using `templates/operational-decision-record.md`.
   - Save it at `_bmad-output/production-artifacts/operational-decisions/operational-decision-record-<timestamp>-<decision>.md`.
   - Link the decision record from the deployment log so later workflows can reconcile the operational choice against BMAD ground truth.

7. **Mandatory Deployment Verification:**
   - Execute `bmad-bda-deployment-verification` immediately after rollout as part of this workflow.
   - Treat the deployment as incomplete until the verification decision is recorded as `PASS`, `HOTFIX-NOW`, `ROLLBACK`, or `FIX-OBSERVABILITY`.
   - If the deployment remains live but verification fails, record the exact route and whether a rerun of `bmad-bda-deployment-verification` is required after corrective work.

8. **Rollback Plan Activation:**
   - Document the specific conditions and steps required to trigger a rollback if deployment fails.
   - Name the rollback trigger threshold and the exact revert target.

9. **Generate Artifacts:**
   - Create or refresh the canonical current `deployment-baseline.md` when current-state protection data was collected, using `templates/deployment-baseline.md`.
   - Also save a historical snapshot at `_bmad-output/production-artifacts/deployment-baselines/deployment-baseline-<timestamp>-<candidate>.md`.
   - Create a run-specific deployment plan at `_bmad-output/production-artifacts/deployment-plans/deployment-plan-<timestamp>-<candidate>.md` using `templates/deployment-plan.md`.
   - Create a run-specific deployment log at `_bmad-output/production-artifacts/deployment-logs/deployment-log-<timestamp>-<candidate>.md` using `templates/deployment-log.md`.
   - Create or refresh a run-specific deployment verification artifact at `_bmad-output/production-artifacts/deployment-verifications/deployment-verification-<timestamp>-<candidate>.md` by executing `bmad-bda-deployment-verification`.
   - Create or refresh any required operational decision records at `_bmad-output/production-artifacts/operational-decisions/`.
   - Record the deployment mode, target environment, deployed branch, commit SHA, operator, timestamps, smoke-test results, deployment-verification decision, release marker or version tag, baseline snapshot identifiers, and rollback outcome if used.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/deployment-baseline.md _bmad-output/production-artifacts/deployment-baselines _bmad-output/production-artifacts/deployment-plans _bmad-output/production-artifacts/deployment-logs _bmad-output/production-artifacts/deployment-verifications _bmad-output/production-artifacts/operational-decisions`.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- Do not proceed if release readiness is `🟡 CONCERNS` or `🔴 FAIL` unless the user explicitly overrides the gate.
- Do not deploy from a side worktree that is not the declared release source of truth.
- Do not silently deploy into an environment with no usable observability path.
- Do not mark a deployment successful until evidence for the release marker and immediate verification path is visible or the artifact clearly records why verification is blocked.
- Do not mutate an existing production deployment without recording the current-state protection posture or explicit user override.
- Do not rediscover or replace an existing VPS deployment shape by default when release-readiness and baseline artifacts already provide the intended current state.
- Do not skip `bmad-bda-deployment-verification` just because smoke tests passed.
- Do not leave an override, waiver, or temporary mitigation undocumented; create an operational decision record when deploy-time behavior or accepted risk changes.
- If the deploy is a dry run or planning-only session, say so explicitly in the artifacts.
- Do not skip required template sections; use `N/A` where a field genuinely does not apply.
