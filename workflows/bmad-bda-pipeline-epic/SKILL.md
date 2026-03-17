# BMAD BDA: Autonomous Epic Worktree

Deliver one BMAD epic as a continuous execution run using per-story git worktrees.

This skill is the autonomous variant of `bmad-epic-pipeline-worktree`.
It preserves the same safety model of isolated worktrees and sequential story merges, but changes the orchestration behavior so the agent keeps going until the epic is done or a hard blocker is reached.

## Inputs

- Epic number such as `1`, `2`, `3`
- If omitted, infer the smallest epic number that still has stories not marked `done` in `_bmad-output/implementation-artifacts/sprint-status.yaml` or `docs/sprint/sprint-status.yaml`.
- If neither status file exists, do not guess; ask the user for an explicit epic number.

## Preconditions

- The current project must be a git repository.
- If `git rev-parse --is-inside-work-tree` fails, stop and tell the user this skill requires a git repo.
- A usable sprint status file must exist, unless the user explicitly provides the epic number and story selection source.

## Workflow

1. Verify the project is a git repository before doing anything else.
2. Read the sprint status file and collect all incomplete stories for the chosen epic.
3. Sort stories by story number ascending.
4. Treat the remaining stories in the epic as a single continuous todo run.
5. For each story, invoke `bmad-story-pipeline-worktree {STORY_ID}` sequentially.
6. After a successful story delivery, continue immediately to the next story without asking the user to re-confirm.
7. Stop only if a hard blocker is reached.
8. After all stories succeed, ensure story artifacts and epic status are synchronized and report epic completion.
9. Invoke `bmad-bmm-retrospective-lite {EPIC_ID}` to close the epic cycle, extract lessons learned, and update the roadmap with any discovered technical debt.
9. Invoke `bmad-bmm-retrospective-lite {EPIC_ID}` to close the epic cycle, extract lessons learned, and update the roadmap with any discovered technical debt.

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

## Communication Rules

- Report progress concisely while continuing execution.
- Do not frame each story completion as a pause point.
- Do not ask the user to approve the next story after every successful story.
- Provide a running completion table or compact status summary as the epic advances.
- Surface blockers immediately and explicitly.

## Behavior Rules

- Run stories strictly sequentially; never overlap story worktrees for the same epic.
- Reuse the same story selection and status source throughout one epic run.
- If no incomplete stories exist, say so explicitly and stop.
- If there is no usable sprint status file, require an explicit epic number and do not auto-select.
- Preserve the safety model of isolated per-story worktrees and merge-after-success.
- The purpose of this skill is continuous epic execution, not conservative per-story user handoff.
