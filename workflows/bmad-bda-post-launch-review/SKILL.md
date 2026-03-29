---
name: bmad-bda-post-launch-review
description: Evidence synthesis and insights generation from 24-72 hours of production data. Use when the user says "run post-launch review" or "generate post-launch insights"
---

# BMAD BDA: Post-Launch Review

## Overview

This workflow turns 24-72 hours of production evidence into an explicit BMAD feedback package.
It compares observed production behavior against the approved release expectations and current deployment baseline, then produces durable artifacts for refinement or course correction.

## On Activation

1. Confirm which deployment version or commit is being reviewed.
2. Confirm the evidence window and whether this is a full review or an early read.
3. Confirm whether evidence is arriving from an implemented adapter or from a manual evidence bundle.

## Role
Act as a cross-functional squad: **PM**, **Analyst**, **SRE Agent**, and **Analytics Agent**.
Your objective is to synthesize evidence from 24-72 hours of production data to generate actionable insights. This is the **learning** step in the lifecycle.

## Required Context
Before generating your output, silently read and analyze:
- Evidence from Adapters: Logs, Error reports, Metrics, Traces, Analytics events.
- BMAD Artifacts: `_bmad-output/planning-artifacts/prd.md` or equivalent PRD, UX specifications, `architecture.md`, and deployment logs.
- the selected deployment log in `_bmad-output/production-artifacts/deployment-logs/` and the current `observability-config.md` when they exist.
- the selected release-readiness artifact in `_bmad-output/production-artifacts/release-readiness/` for the baseline expectations that were approved pre-deploy.
- `_bmad-output/production-artifacts/deployment-baseline.md` when it exists.
- `_bmad-output/production-artifacts/release-intent-matrix.md` when it exists.
- the selected historical release-intent matrix in `_bmad-output/production-artifacts/release-intent-history/` when it exists.

## Preconditions

- A deployment must have occurred, or the workflow should stop and say that post-launch review is premature.
- The evidence window should normally cover at least 24 hours after deployment. If it does not, stop unless the report is explicitly marked as an early read.
- If only partial evidence exists, continue only if the report explicitly lists the missing evidence and its impact on confidence.
- The evidence source must be known, either via an implemented adapter path or an explicit manual evidence bundle.
- `observability-config.md` should define the expected telemetry contract or the report must explicitly say that confidence is reduced because the contract was missing or incomplete.
- `release-intent-matrix.md` should exist for a full plan-vs-production comparison. If it does not, the report must explicitly downgrade confidence and say the comparison chain is incomplete.

## Execution Steps

1. **Evidence Collection:**
   - SRE Agent: Analyze technical health (Errors and Stability, Performance, Infrastructure).
   - Analytics Agent: Analyze user behavior and feature adoption.
   - Validate whether the minimum evidence promised by `observability-config.md` actually arrived.

2. **Plan And Baseline Comparison:**
   - Compare observed production evidence row-by-row against the release-intent matrix snapshot tied to the reviewed deployment.
   - Compare observed behavior to the expectations approved in the selected release-readiness artifact.
   - Compare observed runtime state to `deployment-baseline.md` when the deployment updated an existing environment.
   - Compare observed evidence quality to the intended telemetry contract: missing dashboards, missing alerts, missing release markers, or missing journey instrumentation are findings, not footnotes.
   - Create a run-specific `production-vs-plan-matrix` artifact using `templates/production-vs-plan-matrix.md`.

3. **Analysis Dimensions:**
   - **Errors & Stability:** Identify top errors by frequency and impact.
   - **Performance:** Identify slow endpoints and bottlenecks.
   - **Feature Adoption:** Evaluate usage rates of new features.
   - **User Behavior:** Analyze drop-offs and unexpected patterns.
   - **Infrastructure:** Assess resource utilization and scaling needs.
   - **Plan Fidelity:** State which planned success criteria, journeys, FRs, NFRs, UX critical flows, and acceptance-critical behaviors were matched, partially matched, missed, or left unverified.
   - **Operational Decision Readiness:** State whether the evidence is sufficient to answer health, user impact, rollback hindsight, and next-step planning questions with confidence.

4. **Synthesis:**
   - PM and Analyst: Synthesize findings, prioritize insights by user impact, and generate actionable recommendations.
   - Explicitly separate confirmed production issues, evidence-quality gaps, and future optimization opportunities.

5. **Generate Artifact:**
   - Create a run-specific post-launch review at `_bmad-output/production-artifacts/post-launch-reviews/post-launch-insights-<timestamp>-<reviewed-deployment>.md` using `templates/post-launch-insights.md`.
   - Create a run-specific comparison matrix at `_bmad-output/production-artifacts/production-vs-plan/production-vs-plan-matrix-<timestamp>-<reviewed-deployment>.md` using `templates/production-vs-plan-matrix.md`.
   - Optionally generate run-specific artifacts in `_bmad-output/production-artifacts/observability-reports/` and `_bmad-output/production-artifacts/usage-insights/`.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/post-launch-reviews _bmad-output/production-artifacts/production-vs-plan _bmad-output/production-artifacts/observability-reports _bmad-output/production-artifacts/usage-insights`.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- State the evidence window clearly, including dates and the deployment version or commit being reviewed.
- If the evidence window is under 24 hours, label the artifact clearly as an early read rather than a full post-launch review.
- Separate confirmed findings from inferences when evidence is incomplete.
- Treat missing telemetry on a critical path as a real finding because it weakens operational confidence and BMAD feedback quality.
- If evidence implies immediate replanning of active sprint work, state that clearly so `bmad-bda-spec-refinement` or `/bmad-correct-course` can route the next step explicitly.
- Use the canonical template headings and fill missing values with `N/A` rather than inventing alternate structures.
- Do not stop at infrastructure or aggregate metrics; compare production reality against the release-ground-truth rows derived from BMAD planning artifacts.
