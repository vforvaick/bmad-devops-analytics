# BMAD DevOps Analytics (BDA): Production Lifecycle Extension

> **Extends BMAD Method with production deployment, monitoring, learning, and spec refinement workflows**

[![BMAD Compatible](https://img.shields.io/badge/BMAD-Phase%205-blue)](https://github.com/bmad-code-org/BMAD-METHOD)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

BMAD DevOps Analytics (BDA) fills the critical gap between sprint planning, implementation closure, production release, and continuous product evolution. In practice the loop becomes:

```
sprint planning → implement epics → release ready → deploy → monitor → learn → update plan → repeat
```

This extension adds seven new workflows and three custom agents to close the loop.

## What's Included

### 🤖 Three Custom Agents

- **DevOps Agent** - Deployment, infrastructure, rollback orchestration
- **SRE Agent** - Observability setup, monitoring, incident analysis
- **Analytics Agent** - Product usage analysis, feature adoption tracking

### 🔄 Seven Workflows

1. **Story Pipeline** - Deliver one user story in an isolated git worktree
2. **Epic Pipeline** - End-to-end autonomous delivery of an entire Epic
3. **Release Readiness Review** - Pre-deploy validation gate
4. **Deployment** - Structured deployment execution
5. **Observability Setup** - Monitoring stack configuration
6. **Post-Launch Review** - Evidence synthesis (24-72h post-deploy)
7. **Spec Refinement** - Translate insights to PRD/epic updates

## Installation

### Recommended Method: Manual Clone

This is the most reliable way to install custom BMAD modules in V6:

```bash
# 1. Navigate to your project root
cd your-project

# 2. Create the custom modules directory
mkdir -p _bmad/_config/custom/modules

# 3. Clone this module
git clone https://github.com/vforvaick/bmad-devops-analytics.git _bmad/_config/custom/modules/bda

# 4. Register the module
npx bmad-method install --action update --yes

# 5. Copy workflows to .agents/skills (required for IDE/Antigravity detection)
cp -r _bmad/bda/workflows/* .agents/skills/
```

> **Note:** Step 5 is required for IDEs like Cursor, Windsurf, and other Antigravity-compatible editors to detect and list the BDA skills. After copying, reload your IDE window.

## Support Matrix

- `vps-default`: fully implemented reference adapter for automated evidence collection
- `vercel`: planning/manual-evidence mode until adapter implementation is completed
- `shared-hosting`: planning/manual-evidence mode until adapter implementation is completed

Validation references:
- [docs/bda-hardening-checklist.md](docs/bda-hardening-checklist.md)
- [docs/bda-operational-test-matrix.md](docs/bda-operational-test-matrix.md)
- [docs/bda-dry-run-playbook.md](docs/bda-dry-run-playbook.md)

## Quick Start

After BMAD sprint planning has produced stories and epics:

```bash
# Step 1: Deliver implementation work
/bmad-bda-pipeline-epic
# or /bmad-bda-pipeline-story for one-off story delivery

# Step 2: Establish or refresh observability for the target environment
/bmad-bda-observability-setup

# Step 3: Run release readiness on one concrete candidate
/bmad-bda-release-readiness

# Step 4: Deploy (if PASS)
/bmad-bda-deploy

# Step 5: Wait 24-72 hours for production evidence

# Step 6: Generate insights
/bmad-bda-post-launch-review

# Step 7: Refine planning artifacts and route to next BMAD workflow
/bmad-bda-spec-refinement
```

Use `/bmad-correct-course` when post-launch evidence implies the current sprint or active epic should change immediately. Keep `bmad-bda-spec-refinement` as the production evidence distillation and draft-generation step.

## Governance Model

**Default: Human-in-the-Loop (Mode A)**
- Agents collect evidence and write insights
- Humans review and approve spec updates
- Prevents north-star drift in production

## Folder Structure (Output)

```
_bmad-output/
├── planning-artifacts/       # BMAD Phase 1-2
├── implementation-artifacts/ # BMAD Phase 3-4
└── production-artifacts/     # NEW: Phase 5
    ├── release-readiness.md
    ├── deployment-baseline.md
    ├── deployment-plan.md
    ├── deployment-log.md
    ├── rollback-plan.md
    ├── observability-config.md
    ├── observability-report.md
    ├── usage-insights.md
    ├── post-launch-insights.md
    ├── PRD-v2-draft.md
    ├── spec-refinement-log.md
    └── new-epics/
```

## Requirements

- BMAD Method v6+ installed
- Node.js 18+
- Git installed

## IDE Compatibility

BDA workflows are fully compatible with Antigravity-powered IDEs (Cursor, Windsurf, etc.). After installation, the following skills will appear in your IDE skill list:

- `bmad-bda-pipeline-story` — Deliver one story in isolated worktree
- `bmad-bda-pipeline-epic` — Autonomous epic delivery
- `bmad-bda-release-readiness` — Pre-deploy validation gate
- `bmad-bda-deploy` — Structured deployment execution
- `bmad-bda-observability-setup` — Monitoring stack setup
- `bmad-bda-post-launch-review` — Post-launch evidence synthesis
- `bmad-bda-spec-refinement` — Translate insights to spec updates

## License

MIT - See [LICENSE](LICENSE) for details.

---

**Ready to close the loop from implementation to continuous product evolution.**
