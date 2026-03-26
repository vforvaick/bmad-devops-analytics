---
name: bmad-bda-observability-setup
description: Monitoring stack configuration and observability setup. Design monitoring strategy and provision infrastructure. Use when the user says "setup observability" or "configure monitoring"
---

# BMAD BDA: Observability Setup

## Overview

This workflow establishes or refreshes the production evidence path required for the `deploy → monitor → learn → refine` loop.
It should be run before production deployment, and rerun whenever the target environment or evidence pipeline changes.

## On Activation

1. Confirm the target environment and classify it as `fresh-machine` or `existing-deployment`.
2. Determine whether the environment has a fully implemented adapter or must run in planning/manual-evidence mode.
3. Load the current architecture and any prior observability artifacts before proposing changes.

## Role
Act as a collaborative pair: **SRE Agent** and **DevOps Agent**.
Your objective is to design the monitoring strategy and provision the necessary infrastructure to establish the data pipeline for the `deploy → monitor → learn → refine` loop.

## Required Context
Before generating your output, silently read and analyze:
- The chosen target environment type (e.g., VPS, Vercel, Shared Hosting).
- `_bmad-output/planning-artifacts/architecture.md`.
- `docs/observability.md` if it exists.
- Existing production artifacts such as `_bmad-output/production-artifacts/observability-config.md` and `deployment-plan.md` if they exist.
- `adapters/` inventory for the selected environment, if present.

## Preconditions

- The deployment target or hosting model must be known.
- If the environment is unknown, stop and ask for it instead of inventing an adapter.
- If the chosen adapter is placeholder-only, do not claim that automated evidence collection already exists.

## Execution Steps

1. **Classify Environment And Evidence Mode:**
   - Determine whether the target is `fresh-machine` or `existing-deployment`.
   - Determine whether the selected environment has an implemented adapter or requires planning/manual-evidence mode.

2. **Identify Components:**
   - Determine necessary observability components based on the environment (Logs, Metrics, Traces, Errors, Analytics).
   - For existing deployments, assess current observability coverage and the gaps that must be closed before reliable post-launch review.

3. **Generate Configuration Or Evidence Contract:**
   - Create environment-specific configuration files when the adapter is implemented (for example `docker-compose.observability.yml` for VPS).
   - Otherwise, generate a manual evidence contract that states exactly which dashboards, exports, logs, or reports must be collected for post-launch review.

4. **Deploy Strategy:**
   - Provide instructions on how to deploy or refresh the monitoring stack.

5. **Health Check Verification:**
   - Detail how to verify evidence collection is working post-deployment.

6. **Generate Artifact:**
   - Create or refresh `observability-config.md` that summarizes the deployment mode, evidence mode, setup, ownership, dashboards, alert paths, and verification steps.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- Do not assume hosted adapters or vendor-specific manifests exist locally; generate only what matches the current repo and environment.
- `vps-default` may run in automated mode because an adapter exists in this repo; `vercel` and `shared-hosting` must currently degrade to planning/manual-evidence mode until implemented.
- If the work is planning-only, state what still requires infrastructure access or deployment privileges.
