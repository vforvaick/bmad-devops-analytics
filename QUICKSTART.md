# BMAD Phase 5 - Quick Start Guide

## 🎯 What You'll Accomplish

Complete the production lifecycle loop: deploy your BMAD project, monitor it, learn from production evidence, and refine your specs for the next iteration.

**Time Required**: 2-4 hours (first time), 30-60 min (subsequent iterations)

---

## Prerequisites

✅ **Completed BMAD Phase 1-4**
- All epics finished
- Tests passing
- Ready to deploy

✅ **Infrastructure Ready**
- VPS with root access (recommended), OR
- Vercel/shared hosting with adapter support

✅ **BMAD Method Installed**
- `npx bmad-method --version` shows v6+

---

## Step 1: Install BMAD Phase 5 (5 minutes)

### Option A: NPX Install (Recommended)

```bash
cd your-bmad-project/

npx bmad-method install
# When prompted:
# - Select "Add custom modules"
# - Enter: bmad-phase5
# OR GitHub: vforvaick/bmad-phase5
```

### Option B: Manual Clone

```bash
cd your-bmad-project/.bmad/custom/modules/
git clone https://github.com/vforvaick/bmad-phase5.git

cd ../../..
npx bmad-method deploy
```

### Verify Installation

```bash
# Check that new workflows are available
npx bmad-method workflows list | grep phase5

# Should show:
# - bmad-phase5-release-readiness
# - bmad-phase5-deploy
# - bmad-phase5-observability-setup
# - bmad-phase5-post-launch-review
# - bmad-phase5-spec-refinement
```

---

## Step 2: Release Readiness Review (15-30 minutes)

**Run the workflow:**

```bash
/bmad-phase5-release-readiness
```

**The workflow will check:**
- Architecture risks
- Test coverage
- Environment configuration
- Observability hooks
- Rollback plan

**Output:** `_bmad-output/production-artifacts/release-readiness.md`

**Decision:**
- ✅ **PASS** → Continue to Step 3
- ⚠️ **CONCERNS** → Review concerns, decide if acceptable
- ❌ **FAIL** → Fix critical issues, run again

---

## Step 3: Deploy (10-60 minutes)

**Run the deployment workflow:**

```bash
/bmad-phase5-deploy

# Follow agent prompts for:
# - Deployment target (VPS, Vercel, etc.)
# - Database migrations (if any)
# - Smoke tests
```

**Output:** 
- `deployment-plan.md` - What will be deployed
- `deployment-log.md` - What actually happened
- `rollback-plan.md` - How to undo if needed

**Manual steps may be required** depending on your infrastructure.

---

## Step 4: Observability Setup (30-90 minutes, one-time)

**For VPS (Full Stack):**

```bash
/bmad-phase5-observability-setup

Environment: vps-default
```

This generates Docker Compose configuration for:
- Prometheus (metrics)
- Loki (logs)
- Sentry (errors)
- Jaeger (traces)
- PostHog (analytics)

**Deploy the stack:**

```bash
cd _bmad-output/production-artifacts/
docker-compose -f docker-compose.observability.yml up -d

# Verify services
docker-compose ps
```

**For Vercel/Shared Hosting:**

```bash
/bmad-phase5-observability-setup

Environment: vercel
# OR
Environment: shared-hosting
```

Follow adapter-specific instructions in `observability-config.md`.

**Configure your application:**

Add generated environment variables to your app:

```bash
# From .env.observability
SENTRY_DSN=...
PROMETHEUS_PORT=9100
POSTHOG_API_KEY=...
```

See `adapters/vps-default/README.md` for instrumentation code examples.

---

## Step 5: Wait for Evidence (24-72 hours)

🕐 **Let your application run in production**

During this time:
- Users interact with your app
- Logs accumulate
- Errors are tracked (if any)
- Metrics are collected
- Analytics events fire

**What's being collected:**
- Application logs (info, warnings, errors)
- Error reports with stack traces
- Request latency and throughput
- Infrastructure metrics (CPU, memory)
- User behavior and feature usage

**Minimum viable evidence:**
- At least 100 requests
- At least 10 unique users (if user-facing)
- 24 hours of metrics

---

## Step 6: Post-Launch Review (1-2 hours)

**Run the review workflow:**

```bash
/bmad-phase5-post-launch-review

Evidence period: Last 48 hours
Analysis focus: All dimensions (errors, performance, adoption, behavior, infrastructure)
```

**The agents will:**
1. **SRE Agent** - Analyzes technical health (errors, performance, infrastructure)
2. **Analytics Agent** - Analyzes user behavior and feature adoption
3. **PM + Analyst** - Synthesize findings into actionable insights

**Output:** `post-launch-insights.md`

**Review the insights document:**

```bash
cat _bmad-output/production-artifacts/post-launch-insights.md
```

Look for:
- 🔴 **Critical issues** (P0) - High error rates, severe bugs
- 🟡 **Opportunities** (P1-P2) - Feature gaps, UX improvements
- 🟢 **Validations** (P3) - What worked well

---

## Step 7: Spec Refinement (30-60 minutes)

**Run refinement workflow:**

```bash
/bmad-phase5-spec-refinement

Input: post-launch-insights.md
Output: Draft PRD updates and new epic proposals
```

**The agents will generate:**

1. **PRD-v2-draft.md**
   - Proposed updates to your Product Requirements Document
   - Each change backed by production evidence
   - Categorized by priority (P0, P1, P2, P3)

2. **new-epics/** directory
   - Draft epic documents for high-priority findings
   - Problem statement, evidence, proposed solution
   - Success criteria and acceptance criteria

3. **spec-refinement-log.md**
   - Summary of all proposed changes
   - Impact assessment
   - Recommended next sprint focus

**🚨 CRITICAL: Human Review Required**

All outputs are **DRAFTS**. You must:

1. Review each proposed PRD change
2. Validate evidence interpretation
3. Approve or reject each epic
4. Ensure no "north-star drift"

**Approve changes:**

```bash
# Manually merge approved PRD changes
cp _bmad-output/production-artifacts/PRD-v2-draft.md _bmad-output/planning-artifacts/PRD.md

# Move approved epics to backlog
mv _bmad-output/production-artifacts/new-epics/fix-payment-errors.md \
   _bmad-output/planning-artifacts/epics/
```

---

## Step 8: Back to BMAD Sprint Planning

🔄 **The loop closes!**

You now have:
- ✅ Refined PRD based on production evidence
- ✅ New epics prioritized by real user impact
- ✅ Data-driven backlog for next sprint

**Continue with BMAD core workflow:**

```bash
# BMAD Phase 2: Planning
/bmad-sprint-plan

# Use refined PRD and new epics
# Agents will see production insights context
```

---

## Complete Lifecycle Diagram

```
┌─────────────────────────────────────────────────────┐
│ BMAD Phase 1-4: Analysis → Implementation         │
│ (Standard BMAD workflow)                            │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Phase 5.1: Release Readiness [15-30 min]           │
│ → release-readiness.md (PASS/CONCERNS/FAIL)         │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Phase 5.2: Deploy [10-60 min]                       │
│ → deployment-log.md, rollback-plan.md               │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Phase 5.3: Observability Setup [30-90 min, once]   │
│ → docker-compose.observability.yml, config          │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ [WAIT: 24-72 hours for production evidence]         │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Phase 5.4: Post-Launch Review [1-2 hours]          │
│ → post-launch-insights.md                           │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Phase 5.5: Spec Refinement [30-60 min]             │
│ → PRD-v2-draft.md, new-epics/                      │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ [Human Review & Approval]                            │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│ Back to BMAD Sprint Planning (Phase 2)              │
│ with refined specs ← LOOP COMPLETE                   │
└──────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### "Workflow not found"

```bash
# Rebuild BMAD to register module
npx bmad-method deploy

# Verify module loaded
cat .bmad/config.json | grep bmad-phase5
```

### "Evidence collection failed"

```bash
# Check observability stack health
docker-compose -f docker-compose.observability.yml ps

# View logs
docker-compose -f docker-compose.observability.yml logs sentry
docker-compose -f docker-compose.observability.yml logs prometheus

# Test endpoints
curl http://localhost:9090/-/healthy  # Prometheus
curl http://localhost:3100/ready      # Loki
```

### "Not enough evidence"

Extend observation window:

```bash
/bmad-phase5-post-launch-review

Evidence period: Last 7 days  # Instead of 48 hours
Minimum samples: 50           # Lower threshold
```

### "Agents not producing good insights"

Provide more context:

```bash
# Before running post-launch-review, update PRD with:
# - Expected traffic volume
# - Critical user journeys
# - Known limitations
# - Success metrics
```

---

## What's Next?

### Iteration 2+

For subsequent releases, the workflow is faster:

1. ✅ **Observability already set up** (skip Step 4)
2. ✅ **Familiar workflow** (faster execution)
3. ✅ **Baseline for comparison** (compare to previous insights)

**Typical iteration time: 30-60 minutes** (excluding 24-72h wait)

### Advanced Usage

**Mode B (Future): Assisted Drafting**
- Agents draft and create PRs for low-risk PRD changes
- Human reviews and merges

**Mode C (Future): Autonomous Updates**
- Agents auto-commit certain change types
- Human reviews afterward

**v1 is Mode A only** (safest for production).

### Custom Adapters

Create your own evidence adapter:

```bash
cp -r .bmad/custom/modules/bmad-phase5/adapters/vps-default \
      .bmad/custom/modules/bmad-phase5/adapters/my-custom-stack

# Edit my-custom-stack/adapter.ts
# Implement IEvidenceAdapter interface
```

---

## Support

**Issues**: [GitHub Issues](https://github.com/vforvaick/bmad-phase5/issues)
**Discussions**: [GitHub Discussions](https://github.com/vforvaick/bmad-phase5/discussions)
**BMAD Community**: [Discord](https://discord.gg/bmad-method)

---

**🎉 Congratulations! You've closed the loop from implementation to continuous product evolution.**

---

## Appendix: Folder Structure After Phase 5

```
your-project/
├── _bmad-output/
│   ├── planning-artifacts/
│   │   ├── PRD.md (← May be updated from PRD-v2-draft.md)
│   │   ├── architecture.md
│   │   └── epics/ (← New epics added from post-launch)
│   ├── implementation-artifacts/
│   │   └── stories/
│   └── production-artifacts/ (← NEW in Phase 5)
│       ├── release-readiness.md
│       ├── deployment-plan.md
│       ├── deployment-log.md
│       ├── rollback-plan.md
│       ├── observability-config.md
│       ├── docker-compose.observability.yml
│       ├── observability-report.md
│       ├── usage-insights.md
│       ├── post-launch-insights.md
│       ├── PRD-v2-draft.md
│       ├── new-epics/
│       │   ├── fix-payment-errors.md
│       │   └── improve-onboarding-ux.md
│       └── spec-refinement-log.md
│
├── .bmad/
│   └── custom/
│       └── modules/
│           └── bmad-phase5/
│               ├── module.yaml
│               ├── agents/
│               ├── workflows/
│               ├── templates/
│               └── adapters/
│
└── [your application code]
```
