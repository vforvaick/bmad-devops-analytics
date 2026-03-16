# BMAD Phase 5: Production Lifecycle Extension

> **Extends BMAD Method with production deployment, monitoring, learning, and spec refinement workflows**

[![BMAD Compatible](https://img.shields.io/badge/BMAD-Phase%205-blue)](https://github.com/bmad-code-org/BMAD-METHOD)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

BMAD Phase 5 fills the critical gap between implementation completion and continuous product evolution. While core BMAD ends at implementation, production reality requires:

```
deploy → monitor → learn → update spec → repeat
```

This extension adds five new workflows and three custom agents to close the loop.

## What's Included

### 🤖 Three Custom Agents

- **DevOps Agent** - Deployment, infrastructure, rollback orchestration
- **SRE Agent** - Observability setup, monitoring, incident analysis
- **Analytics Agent** - Product usage analysis, feature adoption tracking

### 🔄 Five Production Workflows

1. **Release Readiness Review** - Pre-deploy validation gate
2. **Deployment** - Structured deployment execution
3. **Observability Setup** - Monitoring stack configuration
4. **Post-Launch Review** - Evidence synthesis (24-72h post-deploy)
5. **Spec Refinement** - Translate insights to PRD/epic updates

## Installation

### Recommended Method: Manual Clone

This is the most reliable way to install custom BMAD modules in V6:

```bash
# 1. Navigate to your project root
cd your-project

# 2. Create the custom modules directory
mkdir -p _bmad/_config/custom/modules

# 3. Clone this module
git clone https://github.com/vforvaick/bmad-devops-analytics.git _bmad/_config/custom/modules/bmad-devops-analytics

# 4. Register the module
npx bmad-method install --action update --yes
```

## Quick Start

After completing all BMAD Phase 1-4 epics:

```bash
# Step 1: Release readiness check
/bmad-phase5-release-readiness

# Step 2: Deploy (if PASS)
/bmad-phase5-deploy

# Step 3: Setup observability (one-time per environment)
/bmad-phase5-observability-setup

# Step 4: Wait 24-72 hours for production evidence

# Step 5: Generate insights
/bmad-phase5-post-launch-review

# Step 6: Refine spec (creates draft PRD-v2 for human review)
/bmad-phase5-spec-refinement
```

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
    ├── deployment-plan.md
    ├── deployment-log.md
    ├── rollback-plan.md
    ├── observability-config.md
    ├── observability-report.md
    ├── usage-insights.md
    ├── post-launch-insights.md
    └── PRD-v2-draft.md
```

## Requirements

- BMAD Method v6+ installed
- Node.js 18+
- Git installed

## License

MIT - See [LICENSE](LICENSE) for details.

---

**Ready to close the loop from implementation to continuous product evolution.**
