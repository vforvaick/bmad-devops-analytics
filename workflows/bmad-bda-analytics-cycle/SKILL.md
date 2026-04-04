---
name: bmad-bda-analytics-cycle
description: Orchestrate post-release evaluation and requirement refinement. Use when the user says "run analytics cycle" or "evaluate production"
---

# BMAD BDA: Analytics Cycle

**Overview**: An orchestrator workflow designed to run several days (e.g., 24-72 hours) after a release. It closes the Continuous Delivery loop by gathering production data, evaluating the release's success, and refining future specifications based on real-world evidence.

This workflow enforces **"Zero-Interruption Execution"**: all missing variables MUST be clarified upfront before execution begins.

---

## Phase 0: Upfront Clarification (Zero-Interruption Rule)

Before starting the cycle, the Orchestrator (you) MUST gather required context without pausing midway.

1.  **Scan Context**: Read existing `post-launch-insights.md` or logs to see what has recently been deployed.
2.  **Clarify Missing Variables**: If it's unclear what release to analyze, present **one single prompt** to the user. Do not pause execution again after this point.
    *   **Release Version/Date**: Which recent deployment should be analyzed?
    *   **Specific Focus Area**: Are there specific metrics (e.g., performance, user adoption) the user wants to prioritize?

---

## Phase 1: Post-Launch Review (Evidence Gathering)

Execute the logic of `bmad-bda-post-launch-review`.

1.  Synthesize evidence and insights from production data/logs for the target release.
2.  Generate or update the `post-launch-insights.md` document with empirical findings.

---

## Phase 2: Spec Refinement (Closing the Loop)

Execute the logic of `bmad-bda-spec-refinement`.

1.  Translate the insights gathered in Phase 1 into actionable updates for Product Requirement Documents (PRDs) or future Epics.
2.  Adjust priorities or technical designs based on the real-world performance of the recent release.
3.  Output a final summary of what specifications were updated and the rationale derived from the analytics.