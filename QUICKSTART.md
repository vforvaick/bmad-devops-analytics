# BMAD DevOps Analytics (BDA) - Quick Start Guide

## 🎯 What You'll Accomplish

Complete the production lifecycle loop: deploy your BMAD project, monitor it, learn from production evidence, and refine your specs for the next iteration.

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

## Step 2: Release Readiness (15-30 minutes)

Before deploying, ensure your code and specs are aligned.

**Run the readiness check:**

```bash
/bmad-bda-release-readiness
```

**The agents will:**
1. Read your `PRD.md` and `architecture.md`.
2. Verify test coverage.
3. Check environment configuration.
4. Generate `_bmad-output/production-artifacts/release-readiness.md`.

**Action**: Proceed only if the decision is 🟢 **PASS**.

---

## Step 3: Deployment (10-60 minutes)

Once readiness is verified, execute the deployment.

**Run deployment workflow:**

```bash
/bmad-bda-deploy
```

**The agents will:**
1. Generate a detailed `deployment-plan.md`.
2. Assist with (or execute) code sync to production.
3. Define rollback triggers.
4. Log the execution in `deployment-log.md`.

---

## Step 4: Observability Setup (One-time)

Establish the evidence pipeline.

**Run setup workflow:**

```bash
/bmad-bda-observability-setup
```

**The agents will:**
1. Provision or configure your monitoring stack (e.g., Docker Compose for VPS).
2. Verify that logs, metrics, and analytics are flowing.
3. Generate `observability-config.md`.

---

## Step 5: Wait & Monitor (24-72 hours)

Let the application run in production to collect real-world evidence.

---

## Step 6: Post-Launch Review (1-2 hours)

Synthesize evidence into insights.

**Run review workflow:**

```bash
/bmad-bda-post-launch-review
```

**The agents will:**
1. Analyze production logs and metrics.
2. Identify top errors and performance bottlenecks.
3. Track feature adoption.
4. Generate `post-launch-insights.md`.

---

## Step 7: Spec Refinement (30-60 minutes)

**Run refinement workflow:**

```bash
/bmad-bda-spec-refinement
```

**The agents will generate:**
1. **PRD-v2-draft.md**: Proposed updates to your Product Requirements Document.
2. **New Epic Proposals**: Drafts for the next sprint based on evidence.

---

## Next Steps

Review the generated drafts, approve them, and move the new epics into your Phase 2 **Sprint Planning**.

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
