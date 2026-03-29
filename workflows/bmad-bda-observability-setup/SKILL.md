---
name: bmad-bda-observability-setup
description: Monitoring stack configuration and observability setup. Design monitoring strategy and provision infrastructure. Use when the user says "setup observability" or "configure monitoring"
---

# BMAD BDA: Observability Setup

## Overview

This workflow establishes or refreshes the production evidence contract required for the `deploy → monitor → learn → refine` loop.
It should be run before production deployment, and rerun whenever the target environment or evidence pipeline changes.
It is complete only when the team can answer production health, user impact, rollback posture, and post-launch learning questions from evidence instead of guesswork.

## On Activation

1. Confirm the target environment and classify it as `fresh-machine` or `existing-deployment`.
2. Determine whether the environment has a fully implemented adapter or must run in planning/manual-evidence mode.
3. For `existing-deployment`, assess the current state from repo docs and production artifacts first; do not default to live VPS inspection.
4. Identify the release candidate's critical services and critical user journeys before proposing changes.
5. Load the current architecture and any prior observability artifacts before proposing changes.

## Role
Act as a collaborative pair: **SRE Agent** and **DevOps Agent**.
Your objective is to design the monitoring strategy and provision the necessary infrastructure to establish the data pipeline for the `deploy → monitor → learn → refine` loop.
Treat observability as an operational quality contract, not a dashboard shopping exercise.

## Required Context
Before generating your output, silently read and analyze:
- The chosen target environment type (e.g., VPS, Vercel, Shared Hosting).
- `_bmad-output/planning-artifacts/prd.md` or equivalent PRD when it exists.
- UX specifications when they exist, especially for critical user journeys.
- `_bmad-output/planning-artifacts/architecture.md`.
- Existing epic and story planning artifacts when they exist, especially release-scope coverage maps and acceptance criteria.
- `docs/observability.md` if it exists.
- `docs/deployment.md`, `docs/infrastructure.md`, or equivalent environment notes when they exist.
- `_bmad-output/production-artifacts/release-intent-matrix.md` when it exists.
- the most relevant prior file in `_bmad-output/production-artifacts/release-intent-history/` when it exists.
- Existing production artifacts such as `_bmad-output/production-artifacts/observability-config.md` and files under `_bmad-output/production-artifacts/deployment-plans/` if they exist.
- Existing production artifacts such as `_bmad-output/production-artifacts/deployment-baseline.md` and files under `_bmad-output/production-artifacts/deployment-logs/` when they exist.
- the most relevant file in `_bmad-output/production-artifacts/observability-config-history/` and `_bmad-output/production-artifacts/observability-reports/` when they exist.
- `adapters/` inventory for the selected environment, if present.

## Preconditions

- The deployment target or hosting model must be known.
- If the environment is unknown, stop and ask for it instead of inventing an adapter.
- If the chosen adapter is placeholder-only, do not claim that automated evidence collection already exists.
- At least one critical service boundary and one critical user journey must be identifiable from the available planning artifacts.
- For `existing-deployment`, prefer a docs-first assessment from repo and prior production artifacts. Request live VPS inspection only when the documents leave material uncertainty.

## Execution Steps

1. **Classify Environment And Evidence Mode:**
   - Determine whether the target is `fresh-machine` or `existing-deployment`.
   - Determine whether the selected environment has an implemented adapter or requires planning/manual-evidence mode.
   - Determine whether this run can remain `docs-first` or requires `docs-plus-live-verification` because critical state is still unknown.

2. **Assess Existing State Before Designing Changes:**
   - For `fresh-machine`, record that the environment is greenfield and list the assumed bootstrap state explicitly.
   - For `existing-deployment`, review repo docs and prior production artifacts to determine the currently deployed application shape, observability stack, and known caveats.
   - Prefer extending or correcting the documented current stack. Do not propose a replacement stack when the evidence indicates the right action is to update what already exists.
   - If docs and artifacts are insufficient to make a safe decision, stop and request targeted live verification instead of inventing missing infrastructure facts.

3. **Inventory Critical Paths:**
   - List the critical services, data stores, background jobs, and external dependencies that can break production.
   - List the critical user journeys and business events that must be observable after deployment.
   - For `existing-deployment`, record current coverage and the gaps that must be closed before reliable post-launch review.

4. **Build Or Refresh Release Intent Matrix:**
   - Extract the release ground truth from BMAD artifacts: executive summary, success criteria, user journeys, FRs, NFRs, UX critical flows, release-scoped story acceptance criteria, and explicit release changes.
   - Create or refresh `release-intent-matrix.md` using `templates/release-intent-matrix.md`.
   - Every critical row must trace back to a source artifact and define the expected runtime proxy or operator check.

5. **Define The Telemetry Contract:**
   - For each critical service, define the minimum evidence set: health, structured logs, errors, latency, throughput, saturation, and dependency status when applicable.
   - For each critical user journey, define the success signal, failure signal, and the event or report used to measure it.
   - Map the release-intent rows to telemetry coverage in `observability-config.md`, including coverage gaps for rows that cannot yet be observed well.
   - Define the minimum SLI or guardrail thresholds required for release-readiness and post-launch review, even if no formal SLO program exists yet.
   - Require release markers or version tags so metrics, logs, and incidents can be correlated to one deployment candidate.

6. **Design Alerting, Ownership, And Runbooks:**
   - Define alert conditions for hard failures, severe degradation, and silent business regressions where feasible.
   - Name the owner, notification path, severity, and expected first response for each top-level alert class.
   - Provide concise runbook guidance for the highest-risk alerts, including rollback triggers when known.
   - State retention, sampling, redaction, privacy, and cost controls for the chosen evidence path.

7. **Generate Configuration Or Evidence Contract:**
   - Create environment-specific configuration files when the adapter is implemented (for example `docker-compose.observability.yml` for VPS).
   - Otherwise, generate a manual evidence contract that states exactly which dashboards, exports, logs, traces, error feeds, or analytics reports must be collected for post-launch review.
   - For `existing-deployment`, include how baseline observability state will be captured before rollout and whether the plan is reuse, extension, cleanup, or replacement.
   - When an observability stack already exists, document the intended change against that existing stack rather than describing a greenfield install by default.

8. **Deploy Or Refresh Strategy:**
   - Provide instructions on how to deploy or refresh the monitoring stack.
   - Include deployment annotations or release marker steps so the upcoming rollout is visible in the evidence system.

9. **Verification And Observation Plan:**
   - Detail how to verify evidence collection is working post-deployment.
   - Include one verification for infrastructure health, one for service health, one for a critical user journey, and one for release marker visibility.
   - Define the 24-72 hour observation window, review cadence, and minimum evidence bundle required by `bmad-bda-post-launch-review`.

10. **Generate Artifact:**
   - Create or refresh the canonical current release-intent matrix at `_bmad-output/production-artifacts/release-intent-matrix.md` using `templates/release-intent-matrix.md`.
   - Also save a historical snapshot at `_bmad-output/production-artifacts/release-intent-history/release-intent-matrix-<timestamp>-<candidate>.md`.
   - Create or refresh the canonical current observability config at `_bmad-output/production-artifacts/observability-config.md` using `templates/observability-config.md`.
   - Also save a historical snapshot at `_bmad-output/production-artifacts/observability-config-history/observability-config-<timestamp>-<candidate>.md`.
   - When useful, create or refresh a run-specific observability report at `_bmad-output/production-artifacts/observability-reports/observability-report-<timestamp>-<candidate>.md`.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/release-intent-matrix.md _bmad-output/production-artifacts/release-intent-history _bmad-output/production-artifacts/observability-config.md _bmad-output/production-artifacts/observability-config-history _bmad-output/production-artifacts/observability-reports`.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- Do not assume hosted adapters or vendor-specific manifests exist locally; generate only what matches the current repo and environment.
- `vps-default` may run in automated mode because an adapter exists in this repo; `vercel` and `shared-hosting` must currently degrade to planning/manual-evidence mode until implemented.
- If the work is planning-only, state what still requires infrastructure access or deployment privileges.
- For `existing-deployment`, default to docs-first assessment and reuse/update decisions. Live VPS inspection is a fallback for unresolved risk, not the first move.
- Do not call observability "ready" if it only captures infrastructure health but cannot answer whether critical user journeys are succeeding.
- Do not rely on logs, metrics, traces, or analytics in isolation; define how they connect to release decisions and post-launch learning.
- Do not ignore baseline drift, alert ownership, or evidence retention just because the first deployment is small.
- Do not invent ad-hoc section headings when a canonical template exists; fill the template completely and note any intentionally omitted sections as `N/A`.
- Do not invent a brand-new observability stack when existing docs or artifacts indicate the right action is to extend, repair, or rationalize the current one.
- Do not treat PRD, UX, epics, or stories as narrative background only; extract concrete comparison rows into `release-intent-matrix.md`.
