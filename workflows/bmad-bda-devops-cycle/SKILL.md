---
name: bmad-bda-devops-cycle
description: Orchestrate the entire continuous delivery pipeline. Use when the user says "run devops cycle" or "deploy epic"
---

# BMAD BDA: DevOps Cycle

**Overview**: An end-to-end wrapper workflow that orchestrates the entire continuous delivery pipeline: from code implementation, through pre-deploy quality gates, physical deployment, and immediate post-deployment verification.

This workflow enforces **"Zero-Interruption Execution"**: all missing variables, deployment targets, and authorization choices MUST be clarified upfront before any execution begins.

**Core Innovation**: If a quality gate (like test coverage or a build check) fails during the Preparation phase, the cycle does **not** immediately abort or suggest a new epic. Instead, it enters an **Auto-Remediation (Hotfix) Loop** to patch the code or tests, re-evaluate readiness, and seamlessly continue to Deployment.

---

## Phase 0: Upfront Clarification (Zero-Interruption Rule)

Before starting the pipeline, the Orchestrator (you) MUST gather all required context.

1.  **Scan Context**: Read `adapter.ts`, `.env`, and existing `deployment-baseline.md` to identify the current infrastructure.
2.  **Clarify Missing Variables**: If critical details are missing, present **one single multi-choice prompt** to the user. Do not pause execution again after this point.
    *   **Scope**: Which Epic or Story ID is being delivered?
    *   **Target Environment**: Staging, Production, or a specific VPS/Vercel instance?
    *   **Execution Mode**:
        *   *Full-Auto*: Proceed from Development straight through Deployment without pausing.
        *   *Semi-Auto*: Pause after Development and Quality Gates to ask for final human approval before Deployment.

---

## Phase 1: Development & Implementation

Execute the autonomous delivery of the requested scope in an isolated Git worktree.

*   If the scope is an Epic, execute the logic of `bmad-bda-pipeline-epic`.
*   If the scope is a Story, execute the logic of `bmad-bda-pipeline-story`.

*Result:* The code is implemented, tests are written, and the worktree is merged back to the main branch.

---

## Phase 2: Preparation (Pre-Deploy Setup & Quality Gate)

1.  **Observability Check**: Quickly assess if new observability infrastructure is required for this release (via `bmad-bda-observability-setup`). If it already exists and is sufficient, skip this step.
2.  **Release Readiness Review**: Execute the logic of `bmad-bda-release-readiness`. This is the primary quality gate.
    *   Assess Architecture.
    *   Validate Test Coverage.
    *   Review Rollback Plan.

---

## Phase 3: Auto-Remediation (The Hotfix Loop)

If Phase 2 (Release Readiness) returns `FAILED` or `BLOCKED` due to coding errors, failing tests, or insufficient coverage:

1.  **Do Not Abort or Pivot to Correct-Course**: Assume this is a localized code/test issue, not a fundamental epic failure.
2.  **Hotfix**: Immediately analyze the error output or test failure. Apply a targeted hotfix/patch to the codebase or test suite.
    *   **Guardrail Rule**: You are strictly FORBIDDEN from disabling existing tests, suppressing errors (e.g., using `@ts-ignore`), or lowering the minimum test coverage threshold to force a pass. The fix MUST be a legitimate logical correction or a valid new test.
3.  **Re-Evaluate**: Re-run the Release Readiness check.
4.  **Limit**: You may retry this Hotfix Loop up to **2 times**. If the gate still fails after the 2nd hotfix attempt, *then* abort the DevOps Cycle and report the persistent error to the user.

---

## Phase 4: Deployment (Execution)

Once the Release Readiness gate is `PASSED` (or if Semi-Auto mode was chosen, once human approval is granted):

1.  Execute the physical deployment using the logic from `bmad-bda-deploy`.
2.  Ensure the code is shipped to the target environment identified in Phase 0.

---

## Phase 5: Evaluate (Immediate Verification)

Sesaat (immediately) after a successful deployment:

1.  Trigger the logic of `bmad-bda-deployment-verification`.
2.  Run smoke tests and verify runtime logs in the target environment to ensure no critical crash occurred during startup.
3.  Output a final, concise status report summarizing the entire cycle.