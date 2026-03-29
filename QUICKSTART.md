# BMAD DevOps Analytics (BDA) - Quick Start Guide

## 🎯 What You'll Accomplish

Start from BMAD sprint planning outputs, implement epics with automated gates, deploy safely, observe real production behavior, and feed the evidence back into BMAD planning.

**Time Required**: 2-4 hours (first time), 30-60 min (subsequent iterations)

---

## Step 1: Installation (Existing Project)

In your existing BMAD-enabled project:

```bash
# 1. Create the custom modules directory if it doesn't exist
mkdir -p _bmad/_config/custom/modules

# 2. Clone this repository
git clone https://github.com/vforvaick/bmad-devops-analytics.git _bmad/_config/custom/modules/bda

# 3. Register the module using the BMAD CLI
npx bmad-method install --action update --yes

# 4. Copy workflows to .agents/skills (required for IDE/Antigravity detection)
cp -r _bmad/bda/workflows/* .agents/skills/

# 5. Reload your IDE window (Cmd+Shift+P → "Reload Window")
```

---

## Step 2: Implementation Delivery

Use BDA's implementation pipelines after BMAD sprint planning has produced epics and stories.

**Run one of:**

```bash
/bmad-bda-pipeline-epic
# or
/bmad-bda-pipeline-story
```

**The workflows will:**
1. Resolve the active story or epic from sprint status.
2. Deliver implementation inside isolated git worktrees.
3. Run verification, review, and traceability gates before merge.
4. Keep failed worktrees preserved for recovery instead of contaminating your main worktree.

---

## Step 3: Observability Setup

Establish or refresh the evidence pipeline before production deployment.

**Run setup workflow:**

```bash
/bmad-bda-observability-setup
```

**The agents will:**
1. Classify the target as fresh-machine or existing-deployment.
2. Design or refresh the observability path for that environment.
3. Downgrade to planning/manual-evidence mode if the selected adapter is not implemented.
4. Refresh the canonical `_bmad-output/production-artifacts/observability-config.md`.
5. Refresh `_bmad-output/production-artifacts/release-intent-matrix.md` and save run-specific history snapshots.

---

## Step 4: Release Readiness

Before deploying, ensure your code and specs are aligned.

**Run the readiness check:**

```bash
/bmad-bda-release-readiness
```

**The agents will:**
1. Read your `PRD.md` and `architecture.md`.
2. Verify test coverage.
3. Check environment configuration.
4. Generate `_bmad-output/production-artifacts/release-readiness/release-readiness-<timestamp>-<candidate>.md`.
5. Refresh canonical baseline and release-intent artifacts when needed.

**Action**: Proceed only if the decision is 🟢 **PASS**.

---

## Step 5: Deployment

Once readiness is verified, execute the deployment.

**Run deployment workflow:**

```bash
/bmad-bda-deploy
```

**The agents will:**
1. Generate `_bmad-output/production-artifacts/deployment-plans/deployment-plan-<timestamp>-<candidate>.md`.
2. Assist with (or execute) code sync to production.
3. Define rollback triggers.
4. Log the execution in `_bmad-output/production-artifacts/deployment-logs/deployment-log-<timestamp>-<candidate>.md`.

---

## Step 6: Wait & Monitor (24-72 hours)

Let the application run in production to collect real-world evidence.

---

## Step 7: Post-Launch Review

Synthesize evidence into insights.

**Run review workflow:**

```bash
/bmad-bda-post-launch-review
```

**The agents will:**
1. Analyze production logs and metrics.
2. Identify top errors and performance bottlenecks.
3. Track feature adoption.
4. Generate `_bmad-output/production-artifacts/post-launch-reviews/post-launch-insights-<timestamp>-<reviewed-deployment>.md`.
5. Generate `_bmad-output/production-artifacts/production-vs-plan/production-vs-plan-matrix-<timestamp>-<reviewed-deployment>.md`.

---

## Step 8: Spec Refinement

**Run refinement workflow:**

```bash
/bmad-bda-spec-refinement
```

**The agents will generate:**
1. **`prd-change-drafts/prd-change-draft-<timestamp>-<reviewed-deployment>.md`**: Proposed PRD changes linked to one reviewed deployment.
2. **`new-epics/<reviewed-deployment>/...`**: Draft epics for future planning work.
3. **`spec-refinement-logs/spec-refinement-log-<timestamp>-<reviewed-deployment>.md`**: Routing summary for the next BMAD workflow.
4. **`bmad-follow-ups/bmad-follow-up-<timestamp>-<reviewed-deployment>.md`**: Explicit BMAD handoff package naming the next command, inputs, and expected downstream artifact.

---

## Next Steps

Review the generated drafts, approve them, and then:

1. Use `/bmad-correct-course` if production evidence requires changes to the active sprint or in-flight epic.
2. Otherwise follow the packaged BMAD loop: `/bmad-edit-prd -> /bmad-create-epics-and-stories -> /bmad-sprint-planning`.

---

## Troubleshooting

### "Skill not found" or "Command not found"

If `/bmad-bda-...` commands aren't appearing in your IDE:

```bash
# 1. Force re-registration of module
npx bmad-method install --action update --yes

# 2. Copy workflows to .agents/skills (this is the most common fix)
cp -r _bmad/bda/workflows/* .agents/skills/

# 3. Reload your IDE window
```

### Skills Installed But Not Visible

If the skills are in `.agents/skills/` but still not showing, check that each `SKILL.md` has YAML frontmatter:

```yaml
---
name: bmad-bda-deploy
description: Your skill description here
---
```

Without this frontmatter, the IDE cannot detect or register the skill.

### Module Folder Structure

Your project structure should look like this after installation:

```text
.
├── _bmad/
│   ├── bda/                        # Installed by npx bmad-method install
│   │   └── workflows/
│   └── _config/
│       └── custom/
│           └── modules/
│               └── bda/            # Git clone source
│                   ├── module.yaml
│                   ├── agents/
│                   ├── workflows/
│                   ├── templates/
│                   └── adapters/
│
├── .agents/
│   └── skills/                     # IDE reads skills from here
│       ├── bmad-bda-deploy/
│       ├── bmad-bda-pipeline-story/
│       └── ...                     # All 7 BDA skills
│
└── [your application code]
```

## Output Pattern

- Canonical current-state artifacts stay at `_bmad-output/production-artifacts/`.
- Run-specific evidence goes into history folders such as `release-readiness/`, `deployment-plans/`, `deployment-logs/`, `post-launch-reviews/`, `production-vs-plan/`, `prd-change-drafts/`, and `bmad-follow-ups/`.
- Do not expect `PRD-v2-draft.md` or single-file `release-readiness.md` anymore.
