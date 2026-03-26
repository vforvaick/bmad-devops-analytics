# Finalize Epic Checklist

Run this checklist after the last story in the epic is merged into the canonical epic branch.

## 1. Sync Artifacts

- Mark all completed stories `done`.
- Mark the epic itself `done` in the active sprint status file.
- Update roadmap, retrospective, and other implementation artifacts that should reflect epic completion.

## 2. Revalidate the Canonical Branch

- Run the broadest verification or release-readiness gate that the epic changed enough to justify.
- Refresh any production-artifact evidence that is now stale because of the final story merges.

## 3. Sync to the Target Branch

- Merge or otherwise synchronize the canonical epic branch into the target branch, usually `main`.
- Preserve any caller-worktree draft files that were explicitly declared in the preserve list.
- Do not claim completion until the target branch contains the same code and artifact state as the canonical epic branch.

## 4. Verify Equivalence

- Compare the target branch to the canonical branch directly.
- Treat non-empty diffs as an incomplete epic closure unless every remaining diff is an intentional preserved draft.

## 5. Cleanup

- Remove successful story worktrees.
- Delete temporary story branches that are fully merged or obsolete.
- If the canonical epic branch is no longer needed after synchronization, archive or delete it.

## 6. Report Closure

- Report final target branch commit, any preserved drafts, and any intentionally retained branches.
- State clearly whether the repo now has one source of truth again.
- Recommend retrospective only as an optional manual next step, not an automatic pipeline step.
