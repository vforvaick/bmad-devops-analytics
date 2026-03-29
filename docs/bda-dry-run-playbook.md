# BDA Dry-Run Playbook

Use this playbook to validate BDA against a real BMAD application repo before trusting it for unattended production work.

## Preparation

Choose one BMAD application repo with:

- Planning artifacts
- Implementation artifacts
- Git history
- At least one incomplete epic
- A realistic deployment target or deployment mock

Record these values before starting:

- Canonical branch name
- Target branch name
- Sprint status file path
- Target environment type
- Deployment mode: `fresh-machine` or `existing-deployment`
- Available observability path: automated or manual-evidence

## Dry Run A: Epic Pipeline

1. Start from a clean caller worktree.
2. Confirm there is at least one incomplete epic in sprint status.
3. Run `/bmad-bda-pipeline-epic`.
4. Observe whether the workflow:
   - Resolves the epic correctly
   - Creates isolated story worktrees
   - Preserves failed worktrees instead of merging
   - Re-syncs safely if branch drift occurs
5. At the end, compare canonical branch and target branch directly.

**Pass if**

- Story execution is sequential
- Failed paths are preserved, not hidden
- Final target branch and implementation artifacts agree

## Dry Run B: Fresh-Machine Release

1. Treat the target as a clean production environment.
2. Run `/bmad-bda-observability-setup`.
3. Run `/bmad-bda-release-readiness`.
4. Confirm the artifact records `fresh-machine`.
5. Confirm `release-intent-matrix.md` is refreshed and a historical snapshot is written.
6. Confirm the run-specific release-readiness artifact is written under `release-readiness/`.
7. Run `/bmad-bda-deploy` as a dry run or staging-equivalent execution.
8. Check that deploy output records:
   - Candidate branch and commit
   - Environment
   - Deployment mode
   - Smoke-test plan
   - Rollback trigger

**Pass if**

- No hidden dependency needs to be invented by the operator
- Readiness and deploy artifacts describe the same candidate and environment
- Greenfield prerequisites are explicit

## Dry Run C: Existing-Deployment Update

1. Pick a target that already has a running version.
2. Run `/bmad-bda-release-readiness`.
3. Confirm `deployment-baseline.md` is created or refreshed.
4. Inspect whether baseline contains:
   - Current running version
   - Snapshot or restore reference
   - Environment caveats
   - Observability state
5. Run `/bmad-bda-deploy` as a dry run or controlled staging-equivalent execution.
6. Confirm deployment refuses unsafe mutation when baseline evidence is missing.

**Pass if**

- Existing-state protection is explicit
- Baseline and candidate are both visible in artifacts
- Rollback posture is concrete rather than generic

## Dry Run D: Post-Launch Evidence Loop

1. Gather a real or simulated 24-72 hour evidence bundle.
2. Run `/bmad-bda-post-launch-review`.
3. Confirm the artifact names:
   - Evidence window
   - Reviewed deployment
   - Confidence gaps
   - Differences from baseline expectations
   - Explicit comparison against `release-intent-matrix.md`
4. Confirm a run-specific production-vs-plan matrix is created and contains matched, partial, missed, and unverified rows.
5. Run `/bmad-bda-spec-refinement`.
6. Confirm a release-linked PRD change draft, refinement log, and BMAD follow-up package are created.
7. Confirm the refinement output names the next routing decision:
   - `/bmad-correct-course`
   - `/bmad-edit-prd -> /bmad-create-epics-and-stories -> /bmad-sprint-planning`
8. When the route is `/bmad-correct-course`, confirm the refinement log includes:
   - trigger issue summary
   - impacted BMAD artifacts
   - recommended approach
   - evidence bundle paths
   - expected BMAD output `_bmad-output/planning-artifacts/sprint-change-proposal-{date}.md`

**Pass if**

- Production evidence becomes durable artifacts
- The next BMAD workflow is named explicitly
- The expected BMAD output artifact is named explicitly
- The BMAD follow-up package lists the exact command and required inputs
- Artifact structure matches the canonical templates instead of ad-hoc headings
- Official planning docs remain untouched until human approval

## Operator Notes

- For `vercel` and `shared-hosting`, validate the manual-evidence contract itself, not automated adapter behavior.
- For `vps-default`, validate both the observability configuration path and evidence collection assumptions.
- If any run requires hidden tribal knowledge, stop and fix the workflow docs before trusting unattended execution.

## Recommended Evidence To Capture During Validation

- Terminal transcript or summarized operator notes
- Generated artifact paths
- Git branch and commit state before and after each run
- Preserved worktree paths when failures are intentional
- Any place where the operator had to infer missing context
- Output of `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts`

## Success Standard

The dry run is successful only when another operator can repeat the same scenario from the produced docs and workflow instructions without needing your unstated assumptions.
