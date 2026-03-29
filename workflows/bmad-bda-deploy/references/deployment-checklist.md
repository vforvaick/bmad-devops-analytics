# Deployment Checklist

Run this checklist before and during the deployment workflow.

## 1. Candidate Validation

- Confirm the source-of-truth branch.
- Confirm the exact commit SHA being deployed.
- Confirm that `release-readiness.md` approves the same candidate.
- Confirm the rollout mode: `fresh-machine` or `existing-deployment`.

## 2. Environment Readiness

- Confirm secrets and environment variables are present.
- Confirm network access, service accounts, and filesystem paths that deployment depends on.
- Confirm the deploy target matches the intended environment, such as staging or production.
- For existing deployments, confirm the documented baseline and observability artifacts were reviewed before any live rediscovery.
- Confirm observability sinks needed for smoke checks and post-launch review are reachable.
- Confirm the observability path can show the deployed release marker or version tag.
- Confirm at least one critical user journey and one system-health path can be verified immediately after rollout.
- For existing deployments, confirm the current production state has been snapshotted or otherwise recorded before mutation.

## 3. Safety Controls

- Confirm rollback target and rollback command.
- Confirm backup, snapshot, or restore identifiers for existing deployments.
- Confirm migration strategy and whether it is reversible.
- Confirm expected downtime or zero-downtime behavior.

## 4. Verification

- Confirm smoke tests to run immediately after deployment.
- Confirm where to inspect logs, metrics, health endpoints, and user-journey evidence.
- Confirm alert owners and the escalation path for severe post-deploy regressions.
- Confirm who or what will watch the first post-deploy interval.
