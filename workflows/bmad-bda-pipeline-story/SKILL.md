---
name: bmad-bda-pipeline-story
description: Deliver one user story autonomously in an isolated git worktree. Use when the user says "run story pipeline" or "deliver next story"
---

# BMAD BDA: Story Pipeline Worktree

Deliver one story through the BMAD pipeline inside an isolated git worktree.

## Inputs

- Story id format: `X-Y`
- If omitted, try to infer the first story not marked `done` from `_bmad-output/implementation-artifacts/sprint-status.yaml` or `docs/sprint/sprint-status.yaml`.
- If neither status file exists, do not guess; ask the user for an explicit story id.

## Preconditions

- The current project must be a git repository.
- If `git rev-parse --is-inside-work-tree` fails, stop and tell the user this skill requires a git repo.

## Workflow

1. Verify the project is a git repository before doing anything else.
2. Create a sibling git worktree on branch `feature/story-{STORY_ID}`.
3. In that worktree, run the configured steps from `references/workflow-steps.md` using the project-local BMAD skills.
4. If all steps succeed and no blocking review or trace gate remains, commit and merge the branch.
5. Remove the worktree after a successful merge.
6. Update sprint status and story doc to `done` when those files exist.
7. If status or story docs are missing, report that explicitly and finish without fabricating updates.

## Behavior rules

- Create and manage the worktree yourself, not via a delegated installer.
- Preserve the worktree if any step fails or leaves unresolved blocking issues.
- Do not merge if code review or traceability reports blocking issues.
- If the repo is not a git repo, stop immediately instead of attempting partial execution.
- Keep the user informed of branch path, merge result, and any preserved worktree path.
