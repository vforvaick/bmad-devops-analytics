---
name: bmad-bda-deployment-verification
description: Immediate post-deploy verification of the release's critical runtime outcomes. Use when the user says "verify deployment" or "run deployment verification"
---

# BMAD BDA: Deployment Verification

## Overview

This workflow proves whether the just-deployed candidate actually achieves its intended runtime outcome in the target environment.
It is the mandatory immediate verification phase for `bmad-bda-deploy`, and it may also be rerun standalone after a hotfix, config change, secrets repair, or observability fix.

The goal is not only to ask whether the service is "up", but whether the release's critical paths, protections, and release evidence behave correctly under live conditions.
This workflow owns the T+0 runtime gate only. It does not replace pre-deploy release readiness, long-window post-launch analysis, or planning refinement.

## On Activation

1. Confirm the reviewed deployment candidate, commit, target environment, and release marker from the selected deployment log.
2. Confirm whether this run is the first verification after deploy or a rerun after corrective work.
3. Load the release-intent matrix, observability config, release-readiness artifact, and deployment log before deciding what to verify.
4. Identify the top-priority runtime outcome and the critical failure conditions for this release.
5. Stop immediately if the reviewed candidate or target environment cannot be tied to a concrete deployment log.

## Role
Act as a combined pair: **DevOps Agent** and **SRE Agent**.
Your objective is to verify that the deployed release behaves correctly in production-relevant runtime conditions immediately after rollout.

Treat this as a decision gate with four valid outcomes:
- `PASS` — critical runtime outcomes are proven and evidence is adequate
- `HOTFIX-NOW` — the release is live but needs immediate corrective work before confidence is acceptable
- `ROLLBACK` — critical runtime failure or unacceptable risk requires reverting the deployment
- `FIX-OBSERVABILITY` — product judgment is blocked because the telemetry contract is too weak or missing

## Required Context
Before generating your output, silently read and analyze:
- the selected deployment log in `_bmad-output/production-artifacts/deployment-logs/`
- the selected release-readiness artifact in `_bmad-output/production-artifacts/release-readiness/`
- `_bmad-output/production-artifacts/release-intent-matrix.md` when it exists
- `_bmad-output/production-artifacts/observability-config.md` when it exists
- `_bmad-output/production-artifacts/deployment-baseline.md` when it exists
- the most relevant prior file in `_bmad-output/production-artifacts/deployment-verifications/` when it exists
- `docs/deployment.md`, `docs/infrastructure.md`, and `docs/observability.md` when they exist
- the exact runtime checks, logs, metrics, events, traces, reports, or operator checks available for the target environment

## Preconditions

- A concrete deployment log must exist for the reviewed candidate.
- The candidate branch/commit, target environment, and release marker must be known.
- At least one critical outcome, one failure path, and one telemetry path must be identifiable from the available artifacts.
- The workflow may continue with partial telemetry only if the resulting decision is explicitly downgraded to `FIX-OBSERVABILITY` or low-confidence `HOTFIX-NOW`.
- If the candidate cannot be tied to the reviewed deployment log, stop instead of inferring from memory.

## Execution Steps

1. **Verification Scope Selection:**
   - Identify the release's top-priority runtime outcome.
   - Identify the highest-risk supporting paths: trigger/input validity, permission/security behavior, data correctness, integration behavior, duplicate/idempotency protection, and telemetry integrity.
   - Explicitly mark any non-goals or out-of-scope behaviors that must not be mistaken for release success.

2. **Immediate Runtime Evidence Collection:**
   - Verify that the deployment's release marker is visible in the intended evidence path.
   - Verify one system-health path and one critical business path under live conditions.
   - Capture the evidence source for each check: operator action, synthetic check, log, metric, trace, event, dashboard, report, or exchange/API response.
   - Record whether each signal is direct evidence, inferred evidence, or missing evidence.

3. **Critical Outcome Matrix Evaluation:**
   - Build a verification matrix from the release intent and immediate runtime evidence.
   - Include rows as applicable for: critical outcome, success criterion, critical journey, FR, NFR, release-specific change, permission/security rule, data integrity, duplicate protection, external integration, failure/recovery path, telemetry integrity, and operability.
   - For each row, compare the planned statement, expected runtime proxy, and observed evidence.
   - Explicitly flag rows that are `unverified` because telemetry is weak or the check was not safely executable.

4. **Failure Routing Decision:**
   - If a critical path fails but rollback is not yet necessary, classify `HOTFIX-NOW`.
   - If the release causes unsafe side effects, wrong external actions, unrecoverable data risk, or severe business impact, classify `ROLLBACK`.
   - If product judgment cannot be supported because release markers, telemetry, or journey instrumentation are missing, classify `FIX-OBSERVABILITY`.
   - Only classify `PASS` when the critical outcome and its key protections have concrete evidence.

5. **Artifact Generation:**
   - Create a run-specific deployment verification artifact at `_bmad-output/production-artifacts/deployment-verifications/deployment-verification-<timestamp>-<candidate>.md` using `templates/deployment-verification.md`.
   - Record whether this run is the initial verification or a rerun, the trigger for the run, the reviewed deployment log, the release marker, top findings, matrix totals, and decision route.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/deployment-verifications`.

6. **Downstream Routing Discipline:**
   - If the outcome is `PASS`, hand the reviewed deployment forward to `bmad-bda-post-launch-review` as the T+0 baseline for later comparison.
   - If the outcome is `HOTFIX-NOW`, `ROLLBACK`, or `FIX-OBSERVABILITY`, route first to operational remediation, redeploy or rerun deployment verification as needed, and only then continue into post-launch review.
   - If the findings imply product-definition, scope, or backlog changes beyond immediate operational repair, carry this artifact forward into `bmad-bda-post-launch-review` and `bmad-bda-spec-refinement` so BMAD original receives the full evidence chain.

## Behavior Rules

- Do not reduce this workflow to "service is up" checks only.
- Do not claim `PASS` if the critical outcome is still inferred rather than directly evidenced.
- Do not hide telemetry weakness inside a confidence footnote when it changes the decision; use `FIX-OBSERVABILITY`.
- Do not redo release-readiness analysis here; use the readiness artifact as input and focus on live runtime proof.
- Do not confuse this immediate gate with long-window learning, adoption, or trend analysis; those belong to `bmad-bda-post-launch-review`.
- Do not draft PRD, epic, or sprint changes here; route planning changes through `bmad-bda-spec-refinement`, which then hands off to BMAD original.
- Do not skip security, data-integrity, or duplicate-protection verification when the release can trigger real-world side effects.
- When this workflow is rerun after a hotfix or config fix, tie the rerun explicitly to the same reviewed deployment or say that a new deployment log is required.
