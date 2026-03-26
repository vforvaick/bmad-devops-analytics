---
name: bmad-bda-pipeline-story
description: Deliver one user story autonomously in an isolated git worktree. Use when the user says "run story pipeline" or "deliver next story"
---

# BMAD BDA: Story Pipeline Worktree

## Overview

This workflow delivers one BMAD story through implementation, verification, review, and merge inside an isolated git worktree.
It is the implementation entry point for BDA after BMAD sprint planning has produced a usable backlog.
Use it when one story should move from backlog to merged code without contaminating the caller worktree.

The worktree branch is disposable; the merge target is the active canonical branch for the current epic or release candidate.

## On Activation

1. Confirm the intended story id, or infer it from the active sprint status source.
2. Resolve the canonical integration branch and record its starting commit before any story worktree is created.
3. Resolve the project-local BMAD skill chain needed for story creation, implementation, review, and optional traceability.
4. Detect any existing preserved branch or worktree for the same story and treat it as a recovery state, not a fresh implementation surface.
5. Stop early if the repo, required references, or required skill chain cannot support a safe run.

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
- A usable implementation skill and both review gates must be resolvable from the local BMAD installation. If they are missing, stop before creating the worktree.

## Workflow

1. Verify the project is a git repository before doing anything else.
2. Determine the canonical branch to merge into. Default to the current branch only when it is clearly the active integration branch.
3. Resolve the story artifact and the concrete BMAD skill chain that will be used inside the worktree.
4. If the caller worktree is dirty, record the dirty paths that must be preserved and avoid using that worktree as the implementation surface.
5. Inspect whether `codex/story-{STORY_ID}` or the intended sibling worktree path already exists.
6. If an existing branch or worktree for the same story is not fully merged and cleaned up, stop and report it as a preserved recovery state instead of reusing it silently.
7. Create a sibling git worktree on branch `codex/story-{STORY_ID}` unless the repo already uses another story-branch naming convention that must be preserved for continuity.
8. In that worktree, execute the ordered steps in `references/workflow-steps.md` using the resolved project-local BMAD skills.
9. Before merge, verify whether the canonical branch moved since the worktree was created. If it did, sync the story branch with the new canonical tip and rerun the affected verification and review gates.
10. If all steps succeed and the integrated automated review gate ends in `PASS` or an explicitly accepted `PASS WITH RISKS`, commit the story branch and merge it back into the canonical branch.
11. Remove the worktree after a successful merge and delete the temporary story branch when it is no longer needed.
12. Update sprint status and story doc to `done` when those files exist.
13. If status or story docs are missing, report that explicitly and finish without fabricating updates.

## Behavior rules

- Create and manage the worktree yourself, not via a delegated installer.
- Treat the canonical branch as the source of truth for the active epic. Do not merge into a stale or ambiguous branch.
- Treat a pre-existing story branch or worktree as a failure-recovery surface unless it is clearly obsolete and fully merged.
- Preserve the worktree if any step fails or leaves unresolved blocking issues.
- Do not merge if code review or traceability reports blocking issues.
- Do not merge if the integrated automated review gate reports `FAIL`.
- Do not merge on `PASS WITH RISKS` unless the accepted risks are recorded in the story closeout.
- If the canonical branch changes mid-run, do not merge stale story code without re-syncing and re-validating.
- Report the canonical branch, story branch, worktree path, merge result, and any preserved dirty paths to the user.
- If the repo is not a git repo, stop immediately instead of attempting partial execution.
- If the workflow steps file or a required BMAD skill is missing, stop and surface that as a workflow-installation defect.
