# BMAD BDA: Spec Refinement

## Role
Act as the **PM** and **Analyst** duo.
Your objective is to translate production insights from the post-launch review into concrete PRD updates and new epic proposals. This completes the feedback loop: `deploy → monitor → learn → update spec`.

## Required Context
Before generating your output, silently read and analyze:
- `_bmad-output/production-artifacts/post-launch-insights.md`
- `_bmad-output/planning-artifacts/PRD.md`
- `_bmad-output/planning-artifacts/architecture.md`
- Existing epics in `_bmad-output/planning-artifacts/epics/`

## Execution Steps

1. **Insight Categorization:**
   - Categorize each finding from `post-launch-insights.md` (e.g., Critical Bug -> Emergency Epic P0, Feature Gap -> PRD Update + Epic P1).

2. **Draft PRD Updates:**
   - For each insight requiring a PRD change, propose the exact text modification using a `Current Text` vs `Proposed Change` format, along with its justification and priority.

3. **Generate Epic Proposals:**
   - Create detailed drafts for new epics to address high-priority insights (P0/P1). Include Problem Statement, Evidence, Proposed Solution, Success Criteria, and Dependencies.

4. **Impact Assessment:**
   - Summarize the total PRD updates and new epics proposed, estimating effort and categorizing by priority. Recommend the focus for the next sprint.

5. **Generate Artifacts:**
   - Create `PRD-v2-draft.md` (save to `_bmad-output/production-artifacts/PRD-v2-draft.md`).
   - Create draft epics in `_bmad-output/production-artifacts/new-epics/`.
   - Create a summary `spec-refinement-log.md` (save to `_bmad-output/production-artifacts/spec-refinement-log.md`).

> **CRITICAL RULE:** All generated files MUST explicitly state they are **DRAFTS** pending human review. Do NOT automatically overwrite the official `PRD.md` or existing epics.
