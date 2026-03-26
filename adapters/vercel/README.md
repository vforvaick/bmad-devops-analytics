# Vercel Adapter

## Overview

Implementation of `IEvidenceAdapter` for applications hosted on Vercel. Integrates with Vercel's built-in analytics, logging, and performance monitoring.

## Status

🚧 **Planning / Manual Evidence Mode**

This adapter is not yet implemented as an automated `IEvidenceAdapter`.
Today, `bmad-bda-observability-setup` should treat Vercel as a manual-evidence environment and generate an evidence contract instead of claiming automated collection is ready.

## Planned Capabilities

- **Logs**: Vercel Runtime Logs API
- **Errors**: Vercel Error tracking / Sentry integration
- **Metrics**: Vercel Web Vitals / Analytics
- **Analytics**: PostHog integration

## Current Operating Mode

Use these BDA workflows in this order:

1. Run `/bmad-bda-observability-setup`
2. Record the exact Vercel projects, environments, dashboards, and third-party tools used
3. Export or capture evidence manually during the 24-72 hour observation window
4. Feed that evidence bundle into `/bmad-bda-post-launch-review`

## Manual Evidence Contract

Collect the following evidence for the reviewed deployment:

- Deployment identifier: Vercel deployment URL, git commit, and environment
- Runtime logs: exported Vercel runtime logs for the review window
- Error data: Vercel errors or Sentry issues with counts and affected users
- Performance data: Web Vitals, slow routes, cold start notes, and latency outliers
- Analytics data: PostHog, Amplitude, Mixpanel, or equivalent exported for the same window
- Config notes: feature flags, rollback target, and any incident/operator interventions

## Automation Target

The future automated adapter should implement:

- `collectLogs`
- `collectErrors`
- `collectMetrics`
- `collectAnalytics`
- `healthCheck`

Tracing may remain optional if the deployed application does not emit traces.
