---
name: bmad-bda-spec-refinement
description: Translate production insights to PRD/epic updates. Completes the deploy-monitor-learn-refine feedback loop. Use when the user says "refine specs" or "run spec refinement"
---

# BMAD BDA: Spec Refinement

## Overview

This workflow converts post-launch evidence into draft planning artifacts that fit BMAD's normal planning loop.
It keeps production evidence, proposed PRD changes, and new epic proposals in explicit draft form, and it routes active-sprint corrections into `/bmad-correct-course` instead of silently mixing concerns.

## On Activation

1. Confirm that a concrete post-launch review artifact exists under `_bmad-output/production-artifacts/post-launch-reviews/` and identifies a concrete reviewed deployment.
2. Load the authoritative planning artifacts and the current sprint status when available.
3. Determine whether the evidence implies future planning work, immediate course correction, or both.

## Role
Act as the **PM** and **Analyst** duo.
Your objective is to translate production insights from the post-launch review into concrete PRD updates and new epic proposals. This completes the feedback loop: `deploy → monitor → learn → update spec`.

## Required Context
Before generating your output, silently read and analyze:
- the selected post-launch review in `_bmad-output/production-artifacts/post-launch-reviews/`
- the selected comparison matrix in `_bmad-output/production-artifacts/production-vs-plan/` when it exists
- `_bmad-output/production-artifacts/release-intent-matrix.md` when it exists
- `_bmad-output/planning-artifacts/prd.md` or equivalent PRD
- `_bmad-output/planning-artifacts/architecture.md`
- Existing epic definitions in `_bmad-output/planning-artifacts/epics.md` or the repo's equivalent epic index
- `_bmad-output/implementation-artifacts/sprint-status.yaml` when it exists
- `_bmad/bmm/workflows/4-implementation/bmad-correct-course/workflow.md` when BMAD original docs are available locally

## Preconditions

- A selected post-launch review artifact must exist.
- If the repo has no authoritative PRD or epic index, stop and report that refinement cannot safely update planning artifacts.
- If evidence implies changes to the current sprint or active epic, route those as a `bmad-correct-course` handoff instead of silently treating them as future planning only.

## Execution Steps

1. **Insight Categorization:**
   - Categorize each finding from the selected post-launch review and production-vs-plan matrix (e.g., Critical Bug -> Emergency Epic P0, Feature Gap -> PRD Update + Epic P1).
   - Classify each finding as `future-planning`, `correct-course-now`, or `both`.

2. **Draft PRD Updates:**
   - For each insight requiring a PRD change, propose the exact text modification using a `Current Text` vs `Proposed Change` format, along with its justification, source matrix row, and priority.

3. **Generate Epic Proposals:**
   - Create detailed drafts for new epics to address high-priority insights (P0/P1). Include Problem Statement, Evidence, Proposed Solution, Success Criteria, Dependencies, and the production-vs-plan matrix rows that justify the epic.

4. **Impact Assessment And Routing:**
   - Summarize the total PRD updates and new epics proposed, estimating effort and categorizing by priority. Recommend the focus for the next sprint.
   - When any item is `correct-course-now`, produce an explicit handoff section aligned to BMAD original `bmad-correct-course`: issue summary, impact analysis across PRD/epics/architecture/UX, recommended approach, and detailed change proposals backed by production evidence.
   - State that the expected BMAD output of that handoff is `_bmad-output/planning-artifacts/sprint-change-proposal-{date}.md`.
   - When items are future-only, route them to the standard BMAD planning loop in order: human review of draft artifacts -> `/bmad-edit-prd` when PRD text should change -> `/bmad-create-epics-and-stories` when backlog structure must change -> `/bmad-sprint-planning` when sprint execution should be refreshed.
   - Distinguish between product-definition gaps, delivery gaps, and observability-only gaps so the next workflow is not over-rotated toward the wrong fix.

5. **Generate Artifacts:**
   - Create a run-specific PRD change draft using `templates/prd-change-draft.md` at `_bmad-output/production-artifacts/prd-change-drafts/prd-change-draft-<timestamp>-<reviewed-deployment>.md`.
   - Create draft epics in `_bmad-output/production-artifacts/new-epics/<reviewed-deployment>/` when separate epic files are appropriate, otherwise generate a draft sectioned proposal in that folder.
   - Create a run-specific summary `spec-refinement-log` using `templates/spec-refinement-log.md` at `_bmad-output/production-artifacts/spec-refinement-logs/spec-refinement-log-<timestamp>-<reviewed-deployment>.md` that names the recommended BMAD follow-up workflow, the expected next artifact, and the exact evidence package to carry forward.
   - When local command execution is available, validate generated artifacts with `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts/prd-change-drafts _bmad-output/production-artifacts/spec-refinement-logs`.

> **CRITICAL RULE:** All generated files MUST explicitly state they are **DRAFTS** pending human review. Do NOT automatically overwrite the official PRD file or existing epics.
