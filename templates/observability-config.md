# Observability Configuration: [Environment / Release Context]

**Date**: [YYYY-MM-DD]
**Target Environment**: [environment]
**Deployment Mode**: [fresh-machine | existing-deployment]
**Evidence Mode**: [automated | manual-evidence]
**Release Candidate**: [branch @ commit | unknown]
**Primary Owners**: [owner names, team, or agents]
**Assessment Mode**: [docs-first | docs-plus-live-verification]

## Summary
[2-4 sentences describing observability readiness and any major gaps.]

## Existing State Assessment
- **Source Documents Reviewed**: [paths or N/A]
- **Live Environment Inspection Needed**: [yes | no]
- **Existing Observability Stack**: [none | partial | established]
- **Reuse / Extend / Replace Decision**: [decision and reason]

## Critical Service Inventory
| Service / Component | Type | Criticality | Primary Signal | Owner |
|---|---|---|---|---|
| [name] | [api, db, worker, frontend, external] | [critical | high | medium] | [health/error/latency/etc.] | [owner] |

## Critical User Journeys
| Journey | Success Signal | Failure Signal | Evidence Source | Threshold / Guardrail |
|---|---|---|---|---|
| [journey] | [event or metric] | [event or symptom] | [dashboard/report/log] | [threshold] |

## Telemetry Contract
### Logs
- **Structured Logging**: [enabled/disabled and format]
- **Retention**: [duration]
- **Redaction / PII Rules**: [rules]
- **Primary Sink**: [destination]

### Errors
- **Error Tracking Path**: [tool or manual path]
- **Grouping Strategy**: [strategy]
- **Escalation Trigger**: [trigger]

### Metrics
- **Golden Signals**: [availability, latency, error rate, saturation coverage]
- **SLI / Guardrails**: [list]
- **Dashboard Locations**: [links or paths]

### Traces
- **Trace Coverage**: [critical paths covered or not]
- **Sampling Strategy**: [rate or policy]

### Analytics
- **Tracked Business Events**: [list]
- **Attribution Limits**: [known blind spots]

## Release Correlation
- **Release Marker Strategy**: [annotation, version tag, build id]
- **Verification Method**: [how operator confirms visibility]
- **Baseline Comparison Path**: [how existing deployment state is compared]

## Alerts And Escalation
| Alert Class | Trigger | Severity | Owner | Notification Path | First Response Expectation |
|---|---|---|---|---|---|
| [class] | [trigger] | [sev] | [owner] | [channel] | [expectation] |

## Runbook Links
1. [Alert / Failure Mode] - [runbook path or concise response steps]

## Verification Plan
- **Infrastructure Check**: [how to verify]
- **Service Health Check**: [how to verify]
- **Critical Journey Check**: [how to verify]
- **Release Marker Check**: [how to verify]

## Observation Window
- **Window**: [24h | 48h | 72h]
- **Review Cadence**: [for example 15m, 1h, daily]
- **Minimum Evidence Bundle For Post-Launch Review**: [logs, metrics, errors, analytics, exports]

## Current Gaps
1. [Gap description, impact, and closure plan]
