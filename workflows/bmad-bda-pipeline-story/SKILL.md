---
name: bmad-bda-pipeline-story
description: Deliver one user story autonomously in an isolated git worktree. Use when the user says "run story pipeline" or "deliver next story"
---

# BMAD BDA: Story Pipeline Worktree

Deliver one story through the BMAD pipeline inside an isolated git worktree.

Use this workflow when one story should move from backlog to merged code without contaminating the caller worktree.
The worktree branch is disposable; the merge target is the active canonical branch for the current epic or release candidate.

## Inputs

- Story id format: `X-Y`
- If omitted, try to infer the first story not marked `done` from `_bmad-output/implementation-artifacts/sprint-status.yaml` or `docs/sprint/sprint-status.yaml`.
- If neither status file exists, do not guess; ask the user for an explicit story id.

## Preconditions

- The current project must be a git repository.
- If `git rev-parse --is-inside-work-tree` fails, stop and tell the user this skill requires a git repo.
- A story source must exist, either from `_bmad-output/implementation-artifacts/sprint-status.yaml`, `docs/sprint/sprint-status.yaml`, or an explicit story artifact path.
- The referenced `references/workflow-steps.md` file must exist. If it is missing, stop and fix the skill installation instead of improvising hidden steps.
- The review rubric in `references/review-gate-rubric.md` must exist. If it is missing, stop and repair the workflow installation instead of silently skipping final review.

## Workflow

1. Verify the project is a git repository before doing anything else.
2. Determine the canonical branch to merge into. Default to the current branch if it is the declared epic branch or clean enough to act as the current integration branch.
3. If the caller worktree is dirty, record the dirty paths that must be preserved and avoid using that worktree as the implementation surface.
4. Create a sibling git worktree on branch `codex/story-{STORY_ID}` unless the repo already uses another story-branch naming convention that must be preserved for continuity.
5. In that worktree, execute the ordered steps in `references/workflow-steps.md` using the project-local BMAD skills.
6. If all steps succeed and the integrated automated review gate ends in `PASS` or an explicitly accepted `PASS WITH RISKS`, commit the story branch and merge it back into the canonical branch.
7. Remove the worktree after a successful merge and delete the temporary story branch when it is no longer needed.
8. Update sprint status and story doc to `done` when those files exist.
9. If status or story docs are missing, report that explicitly and finish without fabricating updates.

## Behavior rules

- Create and manage the worktree yourself, not via a delegated installer.
- Treat the canonical branch as the source of truth for the active epic. Do not merge into a stale or ambiguous branch.
- Preserve the worktree if any step fails or leaves unresolved blocking issues.
- Do not merge if code review or traceability reports blocking issues.
- Do not merge if the integrated automated review gate reports `FAIL`.
- Do not merge on `PASS WITH RISKS` unless the accepted risks are recorded in the story closeout.
- Report the canonical branch, story branch, worktree path, merge result, and any preserved dirty paths to the user.
- If the repo is not a git repo, stop immediately instead of attempting partial execution.
- If the workflow steps file or a required BMAD skill is missing, stop and surface that as a workflow-installation defect.
