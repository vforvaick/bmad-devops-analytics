# Shared Hosting Adapter

## Overview

Lightweight implementation of `IEvidenceAdapter` for restricted shared hosting environments where Docker or root access is not available.

## Status

🚧 **Planning / Manual Evidence Mode**

This adapter is not yet implemented as an automated `IEvidenceAdapter`.
Today, `bmad-bda-observability-setup` should treat shared hosting as a manual-evidence environment and generate an evidence contract instead of claiming automated collection is ready.

## Planned Capabilities

- **Logs**: Application-level file logs (e.g. rotating log files)
- **Errors**: Cloud-based Sentry integration
- **Metrics**: Custom application endpoints
- **Analytics**: Cloud-based PostHog

## Current Operating Mode

Use these BDA workflows in this order:

1. Run `/bmad-bda-observability-setup`
2. Record the exact hosting panel, log locations, metrics endpoints, and third-party tools available
3. Export or capture evidence manually during the 24-72 hour observation window
4. Feed that evidence bundle into `/bmad-bda-post-launch-review`

## Manual Evidence Contract

Collect the following evidence for the reviewed deployment:

- Deployment identifier: hostname, deployment timestamp, git commit if available, and operator notes
- Access/error logs: exported application or web server logs for the review window
- Error data: Sentry or equivalent hosted error reports, or explicit confirmation that none exist
- Metrics data: application health endpoints, provider dashboards, cron/resource stats, or exported screenshots
- Analytics data: PostHog, GA4, or equivalent product analytics exports for the same window
- Config notes: panel changes, backup ids, rollback path, and any hosting limitations affecting confidence

## Automation Target

The future automated adapter should implement:

- `collectLogs`
- `collectErrors`
- `collectMetrics`
- `collectAnalytics`
- `healthCheck`

Tracing may be unsupported on some shared-hosting providers; if so, the adapter should report that limitation explicitly.
