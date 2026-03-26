# Story Pipeline Steps

Use these steps inside the isolated story worktree. Do not skip or silently reorder them.

## 1. Story Context

- Confirm the story id and locate its source artifact.
- If the story artifact does not exist yet, create or refresh it with the project's story-creation skill before implementation starts.
- Extract acceptance criteria, dependencies, and any release-readiness constraints that affect the story.

## 2. Test Shape

- Decide whether acceptance tests, regression tests, or coverage-only additions are needed for this story.
- Use the project's BMAD testing skill chain when it exists, such as `bmad-testarch-atdd`, `bmad-testarch-automate`, or equivalent local testing workflows.
- Record any deliberate test-scope narrowing so the final merge is explainable.

## 3. Implementation

- Implement the story using the project-local BMAD dev workflow, usually `bmad-dev-story` when a populated story file exists, otherwise the most specific local dev skill available.
- Keep all writes inside the story worktree.
- If the story is a follow-up hardening task, prefer the smallest code change that closes the stated gate.

## 4. Verification

- Run the smallest test set that proves the story and its regressions first.
- Run any broader suite or release gate that the story explicitly affects.
- Do not proceed to merge while known blocking failures remain unresolved.

## 5. Review Gate

- Run `bmad-review-adversarial-general` on the story diff.
- Run `bmad-review-edge-case-hunter` on the same diff.
- When a spec or story file exists, run an explicit acceptance audit against its acceptance criteria and stated constraints.
- Normalize and deduplicate findings, then classify them using `references/review-gate-rubric.md`.
- Produce a structured review result with these sections:
  - `Decision: PASS | PASS WITH RISKS | FAIL`
  - `Blocking Findings`
  - `Major Findings`
  - `Minor Findings`
  - `Acceptance Gaps`
  - `Follow-up Notes`
- Treat `blocking` findings as merge blockers.
- Treat `major` findings as mergeable only when the story closeout records the accepted risk explicitly.
- Run traceability or acceptance-audit workflow when the repo uses one, such as `bmad-testarch-trace`.
- If `major` or `minor` findings are accepted as non-blocking, document why before merging.

## 6. Artifact Sync

- Mark the story document `done` only after code, tests, and review gates pass.
- Update `_bmad-output/implementation-artifacts/sprint-status.yaml` or the repo's active sprint status file.
- Update any roadmap or implementation artifact that the project uses to reflect newly completed work.

## 7. Merge and Cleanup

- Commit the story branch with a message that reflects the delivered outcome.
- Merge back into the declared canonical branch.
- Remove the successful worktree and delete the temporary story branch.
- If merge fails or a blocker remains, preserve the worktree and report the exact reason.
