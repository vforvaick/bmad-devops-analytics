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
5. **Observability Setup** - Production evidence contract, monitoring stack, and alert/runbook setup
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

# 5. Sync BDA workflows + agents into your IDE skill registry and agent manifest
python3 _bmad/bda/scripts/sync-bda-assets.py --project-root .
```

> **Note:** Step 5 registers BDA workflows in `.agents/skills/`, creates BDA agent wrappers, and merges the BDA agents into `_bmad/_config/agent-manifest.csv` so party mode and other manifest-driven tooling can discover them. After syncing, reload your IDE window.

## Support Matrix

- `vps-default`: fully implemented reference adapter for automated evidence collection
- `vercel`: planning/manual-evidence mode until adapter implementation is completed
- `shared-hosting`: planning/manual-evidence mode until adapter implementation is completed

Validation references:
- [docs/bda-hardening-checklist.md](docs/bda-hardening-checklist.md)
- [docs/bda-operational-test-matrix.md](docs/bda-operational-test-matrix.md)
- [docs/bda-dry-run-playbook.md](docs/bda-dry-run-playbook.md)

Verification commands:
- `python3 -m unittest discover -s tests -v`
- `python3 scripts/sync-bda-assets.py --project-root . --copy`

Canonical artifact schemas:
- [templates/release-readiness.md](templates/release-readiness.md)
- [templates/release-intent-matrix.md](templates/release-intent-matrix.md)
- [templates/observability-config.md](templates/observability-config.md)
- [templates/deployment-plan.md](templates/deployment-plan.md)
- [templates/deployment-log.md](templates/deployment-log.md)
- [templates/post-launch-insights.md](templates/post-launch-insights.md)
- [templates/production-vs-plan-matrix.md](templates/production-vs-plan-matrix.md)
- [templates/prd-change-draft.md](templates/prd-change-draft.md)
- [templates/spec-refinement-log.md](templates/spec-refinement-log.md)
- [templates/bmad-follow-up.md](templates/bmad-follow-up.md)

Artifact validator:
- `python3 scripts/validate-production-artifacts.py _bmad-output/production-artifacts`
- `python3 scripts/validate-production-artifacts.py --allow-placeholders templates`

## Quick Start

After BMAD sprint planning has produced stories and epics:

```bash
# Step 1: Deliver implementation work
/bmad-bda-pipeline-epic
# or /bmad-bda-pipeline-story for one-off story delivery

# Step 2: Establish or refresh observability for the target environment
# This now defines the production evidence contract, critical journey telemetry,
# release markers, release-intent matrix, alerts, and the 24-72h observation plan.
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

Use `/bmad-correct-course` when post-launch evidence implies the current sprint or active epic should change immediately. Keep `bmad-bda-spec-refinement` as the production evidence distillation and draft-generation step that prepares the handoff package for BMAD original.
When the changes are future-planning only, the intended BMAD follow-up is: human review of BDA drafts -> `/bmad-edit-prd` -> `/bmad-create-epics-and-stories` -> `/bmad-sprint-planning`.

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
    ├── release-intent-matrix.md
    ├── deployment-baseline.md
    ├── observability-config.md
    ├── release-intent-history/
    ├── deployment-baselines/
    ├── observability-config-history/
    ├── release-readiness/
    ├── deployment-plans/
    ├── deployment-logs/
    ├── observability-reports/
    ├── usage-insights/
    ├── post-launch-reviews/
    ├── production-vs-plan/
    ├── prd-change-drafts/
    ├── spec-refinement-logs/
    ├── bmad-follow-ups/
    └── new-epics/
```

Current-state artifacts stay stable at the top level. Run-specific evidence and review artifacts belong in timestamped/history folders.
All production artifacts should follow the canonical schema in `templates/`. If a field does not apply, write `N/A` instead of silently dropping the section.
Use `scripts/validate-production-artifacts.py` to enforce the schema after workflow runs.
The intended comparison chain is: BMAD planning docs -> current `release-intent-matrix.md` plus history snapshot -> current `observability-config.md` plus history snapshot -> `production-vs-plan/production-vs-plan-matrix-<timestamp>-<reviewed-deployment>.md` -> `spec-refinement-logs/spec-refinement-log-<timestamp>-<reviewed-deployment>.md` -> `bmad-follow-ups/bmad-follow-up-<timestamp>-<reviewed-deployment>.md` -> BMAD original follow-up (`/bmad-correct-course` for active-sprint changes, or `/bmad-edit-prd` -> `/bmad-create-epics-and-stories` -> `/bmad-sprint-planning` for future planning).

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

The sync step also exposes these agent skills:

- `bmad-devops` — Deployment and rollback specialist
- `bmad-sre` — Observability and incident specialist
- `bmad-analytics` — Product analytics and behavior specialist

## License

MIT - See [LICENSE](LICENSE) for details.

---

**Ready to close the loop from implementation to continuous product evolution.**
