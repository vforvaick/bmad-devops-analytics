---
name: bmad-bda-pipeline-epic
description: End-to-end autonomous delivery of an entire Epic using isolated git worktrees. Use when the user says "run epic pipeline" or "deliver epic autonomously"
---

# BMAD BDA: Autonomous Epic Worktree

Deliver one BMAD epic as a continuous execution run using per-story git worktrees.

This skill is the autonomous variant of `bmad-epic-pipeline-worktree`.
It preserves the same safety model of isolated worktrees and sequential story merges, but changes the orchestration behavior so the agent keeps going until the epic is done or a hard blocker is reached.
It also owns repo closure for the epic: canonical branch selection, final synchronization, cleanup, and closeout reporting.

## Inputs

- Epic number such as `1`, `2`, `3`
- If omitted, infer the smallest epic number that still has stories not marked `done` in `_bmad-output/implementation-artifacts/sprint-status.yaml` or `docs/sprint/sprint-status.yaml`.
- If neither status file exists, do not guess; ask the user for an explicit epic number.

## Preconditions

- The current project must be a git repository.
- If `git rev-parse --is-inside-work-tree` fails, stop and tell the user this skill requires a git repo.
- A usable sprint status file must exist, unless the user explicitly provides the epic number and story selection source.
- The skill should have access to `bmad-bda-pipeline-story`.
- The skill should have access to `references/finalize-epic-checklist.md`.
- If the starting worktree is dirty, the dirty paths must be recorded up front as a preserve list before autonomous execution begins.

## Workflow

1. Verify the project is a git repository before doing anything else.
2. Determine the canonical branch for the epic run. If the current branch is not clearly the integration branch, declare an explicit canonical branch before continuing.
3. Determine the final target branch, usually `main`, that should be synchronized after the epic is complete.
4. If the starting worktree is dirty, record the exact paths that must be preserved and do not treat that dirty worktree as the implementation surface.
5. Read the sprint status file and collect all incomplete stories for the chosen epic.
6. Sort stories by story number ascending.
7. Treat the remaining stories in the epic as a single continuous todo run.
8. For each story, invoke `bmad-bda-pipeline-story {STORY_ID}` sequentially against the same canonical branch.
9. After a successful story delivery, continue immediately to the next story without asking the user to re-confirm.
10. After the last story succeeds, run one final epic-level review sweep on the aggregated candidate diff using the same automated review logic as the story pipeline, including acceptance-gap and severity reporting.
11. Stop only if a hard blocker is reached.
12. After all stories succeed, ensure story artifacts and epic status are synchronized, then execute the finalization checklist from `references/finalize-epic-checklist.md`.
13. Generate a concise epic closeout summary: delivered stories, final target branch, preserved drafts, retained branches, review outcome, accepted risks, and any recommended follow-up workflows.

## Hard Blockers

Stop the epic run only when one of these occurs:

- A story pipeline step fails and cannot be resolved locally.
- Code review or traceability gates leave unresolved blocking findings.
- The repo, worktree, or merge state is unsafe to continue automatically.
- A required external dependency, credential, or environment prerequisite is missing and cannot be worked around safely.
- The implementation reaches a real product/design ambiguity that cannot be settled from local context.

If a hard blocker occurs:

- Stop immediately at the active story.
- Preserve that story worktree for manual handling.
- Preserve the preserve-list paths from the caller worktree unchanged.
- Report the blocker, active story id, and preserved worktree path.
- Do not continue to later stories in the epic.

## Multi-Agent Rules

Use multi-agent execution inside a story only for non-blocking sidecar tasks.

Allowed sidecar tasks:

- Context extraction from PRD, architecture, epics, and prior story artifacts
- Edge-case discovery
- Test-shape and acceptance-coverage analysis
- Review and risk surfacing
- Traceability/readiness cross-checks

Implementation ownership rules:

- The active story worktree has one writing owner.
- Do not run multiple writing agents against the same story worktree.
- Do not overlap two stories from the same epic.
- Use subagents to accelerate analysis, not to fragment final write ownership.

## Story Boundary Rules

Story completion is an internal quality gate, not a user approval gate.

For each story:

1. Create or refresh the story artifact.
2. Run the configured story pipeline steps.
3. Verify tests/checks relevant to that story.
4. Commit and merge only when the story passes its gates.
5. Update story doc status and sprint status.
6. Continue automatically to the next story.

## Artifact Synchronization Rules

After each successful story:

- Ensure the story document status is `done`.
- Ensure relevant tasks/subtasks are checked off when the story document uses task lists.
- Ensure `_bmad-output/implementation-artifacts/sprint-status.yaml` or `docs/sprint/sprint-status.yaml` is updated for that story.

After the final story in the epic succeeds:

- Ensure all epic stories are marked `done`.
- Ensure the epic status itself is marked `done`.
- Do not leave artifact status behind code reality.
- Do not leave the epic living only in a side worktree when the intended target branch is `main`.

## Finalization Rules

- Finalization is mandatory, not optional cleanup.
- The final epic candidate must survive one last automated review sweep before synchronization to the target branch.
- The epic closeout must carry forward any accepted `major` findings so release-readiness can reassess them explicitly.
- Synchronize the canonical epic branch into the target branch after the last story passes.
- Verify branch equivalence after sync with a direct diff such as `git diff target..canonical`.
- Remove successful story worktrees and delete obsolete story branches.
- Report any branches intentionally retained after the epic closes and why they remain.
- Do not auto-run a retrospective workflow as part of unattended execution. Retrospective is a separate human-led follow-up.

## Communication Rules

- Report progress concisely while continuing execution.
- Do not frame each story completion as a pause point.
- Do not ask the user to approve the next story after every successful story.
- Provide a running completion table or compact status summary as the epic advances.
- Surface blockers immediately and explicitly.
- Announce the canonical branch, target branch, and preserve-list at the start of the run.

## Behavior Rules

- Run stories strictly sequentially; never overlap story worktrees for the same epic.
- Reuse the same story selection and status source throughout one epic run.
- If no incomplete stories exist, say so explicitly and stop.
- If there is no usable sprint status file, require an explicit epic number and do not auto-select.
- Preserve the safety model of isolated per-story worktrees and merge-after-success.
- The purpose of this skill is continuous epic execution, not conservative per-story user handoff.
- If branch ownership becomes ambiguous, stop and resolve that ambiguity before continuing.
