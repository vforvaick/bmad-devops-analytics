---
name: bmad-bda-observability-setup
description: Monitoring stack configuration and observability setup. Design monitoring strategy and provision infrastructure. Use when the user says "setup observability" or "configure monitoring"
---

# BMAD BDA: Observability Setup

## Role
Act as a collaborative pair: **SRE Agent** and **DevOps Agent**.
Your objective is to design the monitoring strategy and provision the necessary infrastructure to establish the data pipeline for the `deploy → monitor → learn → refine` loop.

## Required Context
Before generating your output, silently read and analyze:
- The chosen target environment type (e.g., VPS, Vercel, Shared Hosting).
- `_bmad-output/planning-artifacts/architecture.md`.
- `docs/observability.md` if it exists.
- Existing production artifacts such as `_bmad-output/production-artifacts/observability-config.md` and `deployment-plan.md` if they exist.

## Preconditions

- The deployment target or hosting model must be known.
- If the environment is unknown, stop and ask for it instead of inventing an adapter.

## Execution Steps

1. **Identify Components:**
   - Determine necessary observability components based on the environment (Logs, Metrics, Traces, Errors, Analytics).

2. **Generate Configuration:**
   - Create environment-specific configuration files (e.g., `docker-compose.observability.yml` for VPS, or adapter manifests for others).

3. **Deploy Strategy:**
   - Provide instructions on how to deploy the monitoring stack.

4. **Health Check Verification:**
   - Detail how to verify evidence collection is working post-deployment.

5. **Generate Artifact:**
   - Create or refresh `observability-config.md` that summarizes the setup, ownership, dashboards, alert paths, and verification steps.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- Do not assume hosted adapters or vendor-specific manifests exist locally; generate only what matches the current repo and environment.
- If the work is planning-only, state what still requires infrastructure access or deployment privileges.
