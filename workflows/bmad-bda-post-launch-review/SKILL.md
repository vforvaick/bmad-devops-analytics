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
- BMAD Artifacts: `_bmad-output/planning-artifacts/PRD.md`, UX specifications, `architecture.md`, and deployment logs.

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
   - Create `post-launch-insights.md` using the structure from `templates/post-launch-insights.md`.
   - Optionally generate `observability-report.md` and `usage-insights.md`.
   - Save outputs to `_bmad-output/production-artifacts/`.
