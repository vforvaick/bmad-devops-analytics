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

### 📊 Evidence Adapters (Pluggable)

- **VPS Default** - Full-stack observability (Prometheus, Sentry, PostHog, OpenTelemetry)
- **Vercel** - Logs, errors, analytics via Vercel APIs
- **Shared Hosting** - Lightweight logs, errors, custom metrics

## Installation

### Method 1: NPX (Recommended)

```bash
# In your BMAD-enabled project
npx bmad-method install

# When prompted:
# - Select "Add custom modules"
# - Enter module name: bmad-phase5
# - Or install from GitHub: vforvaick/bmad-phase5
```

### Method 2: Manual Clone

```bash
# Clone into BMAD custom modules directory
cd .bmad/custom/modules/
git clone https://github.com/vforvaick/bmad-phase5.git

# Rebuild BMAD to register agents
npx bmad-method deploy
```

### Method 3: Package.json (Future)

```json
{
  "bmadModules": {
    "bmad-phase5": "github:vforvaick/bmad-phase5"
  }
}
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

**Future Maturity Path:**
- **Mode B** - Agents draft PRD/epic changes, humans approve
- **Mode C** - Autonomous low-risk updates (experimental)

v1 only supports Mode A (safest for production).

## Evidence Pipeline

### Level C: Product Feedback (Full Stack)

```
┌──────────────────────────────────────────────────┐
│ Logs │ Errors │ Metrics │ Traces │ Analytics   │
└────────────────┬─────────────────────────────────┘
                 ↓
       Evidence Adapters (pluggable)
                 ↓
       ┌─────────────────────┐
       │ Post-Launch Insights │
       └──────────┬───────────┘
                  ↓
       ┌──────────────────────┐
       │ PRD-v2 + New Epics   │
       └──────────────────────┘
                  ↓
         Back to BMAD Sprint
```

### VPS Default Stack

- **Logs**: Winston/Pino → file rotation
- **Errors**: Sentry (self-hosted or cloud)
- **Metrics**: Prometheus + Node Exporter
- **Traces**: OpenTelemetry → Jaeger
- **Analytics**: PostHog (self-hosted)

Generated via `bmad-phase5-observability-setup` with Docker Compose.

### Adapter Contract

Any observability provider can plug in via `IEvidenceAdapter` interface:

```typescript
interface IEvidenceAdapter {
  collectLogs(since: Date): Promise<LogEntry[]>;
  collectErrors(since: Date): Promise<ErrorReport[]>;
  collectMetrics(since: Date): Promise<MetricSnapshot[]>;
  collectTraces(since: Date): Promise<TraceData[]>;
  collectAnalytics(since: Date): Promise<UsageData[]>;
  healthCheck(): Promise<AdapterHealth>;
}
```

See `adapters/` for reference implementations.

## Folder Structure

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

.bmad/
└── custom/
    └── modules/
        └── bmad-phase5/
            ├── module.yaml
            ├── agents/
            ├── workflows/
            ├── templates/
            └── adapters/
```

## Workflows Detail

### 1. Release Readiness Review

**Agent**: Architect + Test Architect + DevOps  
**Duration**: 15-30 min  
**Output**: `release-readiness.md` (PASS/CONCERNS/FAIL)

**Checklist**:
- Architecture risks evaluated
- Test coverage sufficient
- Environment config validated
- Secrets management reviewed
- Observability hooks present
- Rollback plan defined

### 2. Deployment

**Agent**: DevOps  
**Duration**: 10-60 min (depending on stack)  
**Output**: `deployment-log.md`, `rollback-plan.md`

**Steps**:
- Pre-deploy health check
- Database migrations (if any)
- Application deployment
- Smoke tests
- Rollback plan activation (if needed)

### 3. Observability Setup

**Agent**: SRE + DevOps  
**Duration**: 30-90 min (one-time)  
**Output**: `observability-config.md`, adapter manifests

**Deliverables**:
- Monitoring stack deployed (Prometheus, Sentry, etc.)
- Dashboards configured
- Alerts defined
- Evidence collection verified

### 4. Post-Launch Review

**Agent**: PM + Analyst + SRE + Analytics  
**Duration**: 1-2 hours  
**Input**: 24-72h of production evidence  
**Output**: `post-launch-insights.md`

**Analysis Dimensions**:
- Top errors and root causes
- Performance bottlenecks
- Unused/underused features
- User drop-off points
- Unexpected usage patterns
- Infrastructure issues

### 5. Spec Refinement

**Agent**: PM + Analyst  
**Duration**: 30-60 min  
**Input**: `post-launch-insights.md`  
**Output**: `PRD-v2-draft.md`, `new-epics/` (for human review)

**Translation**:
- Insights → PRD updates
- Critical bugs → high-priority epics
- Feature gaps → backlog epics
- Performance issues → technical debt stories

**Human reviews and approves before merging to official PRD.**

## Environment Support

| Environment | VPS Default | Vercel | Shared Hosting |
|-------------|-------------|--------|----------------|
| Logs | ✅ Full | ✅ API | ⚠️ App-only |
| Errors | ✅ Sentry | ✅ Sentry | ✅ Sentry Cloud |
| Metrics | ✅ Prometheus | ✅ Analytics API | ⚠️ Custom endpoint |
| Traces | ✅ OpenTelemetry | ⚠️ Limited | ❌ N/A |
| Analytics | ✅ PostHog | ✅ Vercel/PostHog | ✅ PostHog Cloud |
| Host Metrics | ✅ Node Exporter | ❌ N/A | ❌ N/A |

## Project Status

**Current**: v1.0.0-alpha  
**Baseline**: Mode A (human-in-the-loop)  
**Default Stack**: VPS with Docker Compose

**Roadmap**:
- v1.1: Vercel adapter complete implementation
- v1.2: Shared hosting adapter refinement
- v2.0: Mode B (assisted drafting)
- v3.0: Mode C (autonomous updates, experimental)

## Requirements

- BMAD Method v6+ installed
- Node.js 18+
- For VPS stack: Docker + Docker Compose
- For Vercel: Vercel CLI + API token
- For shared hosting: SSH access + basic shell

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT - See [LICENSE](LICENSE) for details.

## Credits

Developed by [vforvaick](https://github.com/vforvaick) as extension to [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD).

Inspired by the gap between implementation and production reality in spec-driven development.

## Support

- **Issues**: [GitHub Issues](https://github.com/vforvaick/bmad-phase5/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vforvaick/bmad-phase5/discussions)
- **BMAD Community**: [Discord](https://discord.gg/bmad-method)

---

**Ready to close the loop from implementation to continuous product evolution.**
