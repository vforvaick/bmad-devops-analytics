---
name: bmad-bda-post-launch-review
description: Evidence synthesis and insights generation from 24-72 hours of production data. Use when the user says "run post-launch review" or "generate post-launch insights"
---

# BMAD BDA: Post-Launch Review

## Role
Act as a cross-functional squad: **PM**, **Analyst**, **SRE Agent**, and **Analytics Agent**.
Your objective is to synthesize evidence from 24-72 hours of production data to generate actionable insights. This is the **learning** step in the lifecycle.

## Required Context
Before generating your output, silently read and analyze:
- Evidence from Adapters: Logs, Error reports, Metrics, Traces, Analytics events.
- BMAD Artifacts: `_bmad-output/planning-artifacts/prd.md` or equivalent PRD, UX specifications, `architecture.md`, and deployment logs.
- `_bmad-output/production-artifacts/deployment-log.md` and `observability-config.md` when they exist.
- `_bmad-output/production-artifacts/release-readiness.md` for the baseline expectations that were approved pre-deploy.

## Preconditions

- A deployment must have occurred, or the workflow should stop and say that post-launch review is premature.
- The evidence window should normally cover at least 24 hours after deployment. If it does not, stop unless the report is explicitly marked as an early read.
- If only partial evidence exists, continue only if the report explicitly lists the missing evidence and its impact on confidence.

## Execution Steps

1. **Evidence Collection:**
   - SRE Agent: Analyze technical health (Errors and Stability, Performance, Infrastructure).
   - Analytics Agent: Analyze user behavior and feature adoption.

2. **Analysis Dimensions:**
   - **Errors & Stability:** Identify top errors by frequency and impact.
   - **Performance:** Identify slow endpoints and bottlenecks.
   - **Feature Adoption:** Evaluate usage rates of new features.
   - **User Behavior:** Analyze drop-offs and unexpected patterns.
   - **Infrastructure:** Assess resource utilization and scaling needs.

3. **Synthesis:**
   - PM and Analyst: Synthesize findings, prioritize insights by user impact, and generate actionable recommendations.

4. **Generate Artifact:**
   - Create or refresh `post-launch-insights.md` without depending on an external template file.
   - Optionally generate `observability-report.md` and `usage-insights.md`.
   - Save outputs to `_bmad-output/production-artifacts/`.

## Behavior Rules

- State the evidence window clearly, including dates and the deployment version or commit being reviewed.
- If the evidence window is under 24 hours, label the artifact clearly as an early read rather than a full post-launch review.
- Separate confirmed findings from inferences when evidence is incomplete.
