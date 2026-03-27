# BDA Operational Test Matrix

This matrix defines the minimum validation scenarios required before claiming BDA is production-ready on a real BMAD project.

## Scope

Validate these three scenarios in order:

1. Epic implementation flow
2. Fresh-machine deployment flow
3. Existing-deployment update flow

Do not skip scenario 3 just because scenario 2 passes. They protect different failure modes.

## Scenario 1: Epic Implementation Flow

**Goal:** Prove that BDA can take a sprint-planned epic from incomplete stories to synchronized implementation artifacts without contaminating the caller worktree.

**Entry Conditions**

- A BMAD project exists with `sprint-status.yaml`
- At least one epic contains incomplete stories
- Required local BMAD skills for story creation, implementation, review, and traceability are installed
- Git repo is healthy

**Primary Workflow Path**

1. Run `/bmad-bda-pipeline-epic`
2. Allow it to infer or select one incomplete epic
3. Observe sequential story execution
4. Verify final epic closeout and target-branch synchronization

**Must Verify**

- Story worktrees are isolated
- A failed story preserves its worktree instead of merging partial work
- Story and sprint artifacts are updated only after gates pass
- Final target branch matches the canonical epic branch after sync
- Accepted risks are carried into epic closeout when relevant

**Required Artifacts**

- Updated story artifacts
- Updated sprint status artifact
- Epic closeout summary in conversation or generated notes

**Failure Signals**

- Story branch reused silently after a previous failed run
- Merge proceeds after blocking review or traceability findings
- Canonical branch drift is ignored
- Epic code lands on target branch but story/sprint artifacts lag behind

## Scenario 2: Fresh-Machine Deployment Flow

**Goal:** Prove that BDA can prepare and execute a first deployment into a clean production target.

**Entry Conditions**

- Release candidate branch and commit are known
- Target environment is a clean or newly provisioned machine
- Observability path has been configured or explicitly waived

**Primary Workflow Path**

1. Run `/bmad-bda-observability-setup`
2. Run `/bmad-bda-release-readiness`
3. Run `/bmad-bda-deploy`
4. Run `/bmad-bda-post-launch-review` after the evidence window
5. Run `/bmad-bda-spec-refinement`

**Must Verify**

- Readiness records `fresh-machine`
- Greenfield prerequisites are explicit in readiness and deploy artifacts
- Observability config defines critical service telemetry, critical journey evidence, release markers, and alert ownership
- Deploy logs capture candidate, operator, smoke checks, release marker, and rollback posture
- Post-launch review identifies the exact reviewed deployment
- Post-launch review flags missing telemetry as a confidence issue instead of silently proceeding
- Spec refinement routes output either to normal sprint planning or to `/bmad-correct-course`

**Required Artifacts**

- `release-readiness.md`
- `deployment-plan.md`
- `deployment-log.md`
- `observability-config.md`
- `post-launch-insights.md`
- `PRD-v2-draft.md`
- `spec-refinement-log.md`

**Failure Signals**

- Deploy proceeds without a known target environment
- Deploy claims success without smoke evidence
- Post-launch review cannot identify the deployed commit
- Spec refinement overwrites official planning docs instead of creating drafts

## Scenario 3: Existing-Deployment Update Flow

**Goal:** Prove that BDA can safely update an already-running production environment.

**Entry Conditions**

- A real deployment already exists
- Current running version can be identified
- Backup, snapshot, or restore posture exists or can be captured
- Candidate branch and commit are known

**Primary Workflow Path**

1. Run `/bmad-bda-observability-setup` if observability is stale or missing
2. Run `/bmad-bda-release-readiness`
3. Confirm `deployment-baseline.md` is created or refreshed
4. Run `/bmad-bda-deploy`
5. Observe production for the evidence window
6. Run `/bmad-bda-post-launch-review`

**Must Verify**

- Readiness records `existing-deployment`
- Current-state baseline includes running version, restore path, and environment notes
- Observability setup records current coverage gaps and how they will be closed before or during rollout
- Deploy refuses to mutate production without baseline evidence unless explicitly overridden
- Post-launch review compares observed behavior against both release expectations and baseline state

**Required Artifacts**

- `deployment-baseline.md`
- `release-readiness.md`
- `deployment-plan.md`
- `deployment-log.md`
- `post-launch-insights.md`

**Failure Signals**

- Existing deployment updated without a captured baseline
- Rollback plan exists only conceptually, not concretely
- Post-launch review treats an update like a greenfield deployment and ignores the prior baseline

## Manual-Evidence Environments

For `vercel` and `shared-hosting`, the workflow is valid only if:

- `bmad-bda-observability-setup` explicitly declares manual-evidence mode
- The operator can name the evidence sources before deployment
- The same evidence contract is used during post-launch review

Do not claim automated observability validation on those environments until a real adapter exists.

## Exit Criteria

BDA should be considered operationally validated only when:

- All three scenarios have been run at least once on a real BMAD project
- No scenario revealed an unhandled blocker in the workflow instructions
- Generated artifacts are complete and internally consistent
- Operators can rerun the same path without improvising hidden steps
