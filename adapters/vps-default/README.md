# VPS Default Adapter - Full Stack Observability

## Overview

Reference implementation of `IEvidenceAdapter` for VPS environments with root access. Provides complete observability stack with logs, errors, metrics, traces, and analytics.
For `existing-deployment` environments, the default operating model is `docs-first`: assess the current deployment and observability state from repo docs and prior production artifacts before proposing live changes on the VPS.

## Stack Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Logs** | Winston/Pino + Loki | Application and system logs |
| **Errors** | Sentry | Error tracking and alerting |
| **Metrics** | Prometheus + Node Exporter | Application and infrastructure metrics |
| **Traces** | OpenTelemetry + Jaeger | Distributed tracing |
| **Analytics** | PostHog (self-hosted) | Product analytics and feature flags |

## Prerequisites

- VPS with root access
- Docker 24+ and Docker Compose 2+
- Ubuntu 22.04+ or Debian 12+ (recommended)
- Minimum 2GB RAM, 20GB disk
- Ports available: 3000 (Grafana), 9090 (Prometheus), 9000 (Sentry), 8000 (PostHog), 16686 (Jaeger)

## Assessment Modes

### Greenfield VPS

- Treat the host as `fresh-machine`
- Define bootstrap prerequisites explicitly
- Generate initial stack and app instrumentation plan from the canonical templates

### Brownfield VPS

- Treat the host as `existing-deployment`
- Review `deployment-baseline.md`, `observability-config.md`, `deployment-log.md`, and any repo docs first
- Decide whether the right action is to reuse, extend, repair, simplify, or replace the current stack
- Request live VPS verification only for unresolved facts that matter to safe deployment or observability changes

Do not default to replacing an existing Grafana, Prometheus, Loki, Sentry, or other stack just because this adapter can provision one.

## Installation

### 1. Run Observability Setup Workflow

```bash
/bmad-bda-observability-setup

Environment: vps-default
Stack: Prometheus, Sentry, PostHog, OpenTelemetry
```

This generates:
- `docker-compose.observability.yml`
- `prometheus.yml`
- `.env.observability`
- `observability-config.md`

For `existing-deployment`, these files should describe the intended delta against the current stack, not silently assume a brand-new install.

### Adapter Runtime Contract

The automated adapter now fails fast if its identity values are still placeholders. Configure these values before relying on automated evidence collection:

```bash
cp adapters/vps-default/.env.example .env.observability
```

Required values:

- `BDA_VPS_APP_LABEL`
- `BDA_VPS_SENTRY_ORG`
- `BDA_VPS_SENTRY_PROJECT`
- `SENTRY_TOKEN`
- `POSTHOG_API_KEY`

Optional values:

- `BDA_VPS_JAEGER_SERVICE_NAME`
- `BDA_VPS_REQUEST_TIMEOUT_MS`
- `PROMETHEUS_URL`
- `LOKI_URL`
- `SENTRY_URL`
- `JAEGER_URL`
- `POSTHOG_URL`

### 2. Deploy Stack

```bash
# Review generated configuration
cat docker-compose.observability.yml

# Deploy observability stack
docker-compose -f docker-compose.observability.yml up -d

# Verify all services running
docker-compose -f docker-compose.observability.yml ps
```

### 3. Configure Application

Add environment variables to your application:

```bash
# Sentry
SENTRY_DSN=http://your-sentry-dsn

# Prometheus (expose metrics endpoint)
METRICS_PORT=9100

# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# PostHog
POSTHOG_API_KEY=your-posthog-key
POSTHOG_HOST=http://localhost:8000
```

### 4. Instrument Application

#### Logging (Winston example)

```javascript
const winston = require('winston');
const LokiTransport = require('winston-loki');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new LokiTransport({
      host: 'http://localhost:3100',
      labels: { app: process.env.BDA_VPS_APP_LABEL },
      json: true,
    }),
  ],
});

logger.info('Application started', { version: '1.0.0' });
```

#### Error Tracking (Sentry)

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});

// Use in error handlers
app.use(Sentry.Handlers.errorHandler());
```

#### Metrics (Prometheus)

```javascript
const client = require('prom-client');

const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
});
register.registerMetric(httpRequestDuration);

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

#### Tracing (OpenTelemetry)

```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
});

sdk.start();
```

#### Analytics (PostHog)

```javascript
const { PostHog } = require('posthog-node');

const posthog = new PostHog(
  process.env.POSTHOG_API_KEY,
  { host: process.env.POSTHOG_HOST }
);

// Track events
posthog.capture({
  distinctId: userId,
  event: 'feature_used',
  properties: { feature: 'export_csv' },
});
```

## Docker Compose Configuration

Generated `docker-compose.observability.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
    restart: unless-stopped

  sentry:
    image: sentry:latest
    ports:
      - "9000:9000"
    environment:
      SENTRY_SECRET_KEY: ${SENTRY_SECRET_KEY}
      SENTRY_POSTGRES_HOST: postgres
      SENTRY_REDIS_HOST: redis
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: sentry
      POSTGRES_USER: sentry
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "4318:4318"    # OTLP HTTP
    environment:
      COLLECTOR_OTLP_ENABLED: true
    restart: unless-stopped

  posthog:
    image: posthog/posthog:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://posthog:${POSTGRES_PASSWORD}@postgres-posthog/posthog
      REDIS_URL: redis://redis-posthog:6379
    depends_on:
      - postgres-posthog
      - redis-posthog
    restart: unless-stopped

  postgres-posthog:
    image: postgres:14
    environment:
      POSTGRES_DB: posthog
      POSTGRES_USER: posthog
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-posthog-data:/var/lib/postgresql/data
    restart: unless-stopped

  redis-posthog:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
  loki-data:
  postgres-data:
  postgres-posthog-data:
```

## Adapter Implementation

```typescript
// adapters/vps-default/VPSAdapter.ts

import { IEvidenceAdapter, LogEntry, ErrorReport, MetricSnapshot, TraceData, UsageData, AdapterHealth } from '../IEvidenceAdapter';
import axios from 'axios';

export class VPSDefaultAdapter implements IEvidenceAdapter {
  name = 'vps-default';
  environment = 'vps' as const;

  private appLabel = process.env.BDA_VPS_APP_LABEL!;
  private prometheusUrl = process.env.PROMETHEUS_URL || 'http://localhost:9090';
  private lokiUrl = process.env.LOKI_URL || 'http://localhost:3100';
  private sentryUrl = process.env.SENTRY_URL || 'http://localhost:9000';
  private sentryOrg = process.env.BDA_VPS_SENTRY_ORG!;
  private sentryProject = process.env.BDA_VPS_SENTRY_PROJECT!;
  private jaegerUrl = process.env.JAEGER_URL || 'http://localhost:16686';
  private posthogUrl = process.env.POSTHOG_URL || 'http://localhost:8000';

  async collectLogs(since: Date): Promise<LogEntry[]> {
    const query = `{app="${this.appLabel}"}`;
    const start = Math.floor(since.getTime() / 1000) * 1e9; // nanoseconds
    
    const response = await axios.get(`${this.lokiUrl}/loki/api/v1/query_range`, {
      params: { query, start },
    });

    return response.data.data.result.flatMap((stream: any) =>
      stream.values.map(([timestamp, line]: [string, string]) => ({
        timestamp: new Date(parseInt(timestamp) / 1e6),
        level: this.parseLogLevel(line),
        message: line,
        metadata: this.parseLogMetadata(line),
      }))
    );
  }

  async collectErrors(since: Date): Promise<ErrorReport[]> {
    // Use Sentry API to fetch errors
    const response = await axios.get(`${this.sentryUrl}/api/0/projects/${this.sentryOrg}/${this.sentryProject}/issues/`, {
      headers: { Authorization: `Bearer ${process.env.SENTRY_TOKEN}` },
      params: { start: since.toISOString() },
    });

    return response.data.map((issue: any) => ({
      id: issue.id,
      title: issue.title,
      message: issue.metadata.value,
      count: issue.count,
      userCount: issue.userCount,
      firstSeen: new Date(issue.firstSeen),
      lastSeen: new Date(issue.lastSeen),
      level: issue.level,
      stacktrace: issue.metadata.stacktrace,
    }));
  }

  async collectMetrics(since: Date): Promise<MetricSnapshot[]> {
    const queries = [
      'rate(http_requests_total[5m])',
      'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
      'process_cpu_seconds_total',
      'process_resident_memory_bytes',
    ];

    const snapshots = await Promise.all(
      queries.map(async (query) => {
        const response = await axios.get(`${this.prometheusUrl}/api/v1/query`, {
          params: { query, time: Math.floor(since.getTime() / 1000) },
        });
        
        return {
          name: query,
          value: parseFloat(response.data.data.result[0]?.value[1] || 0),
          timestamp: new Date(),
          labels: response.data.data.result[0]?.metric || {},
        };
      })
    );

    return snapshots;
  }

  async collectTraces(since: Date): Promise<TraceData[]> {
    const response = await axios.get(`${this.jaegerUrl}/api/traces`, {
      params: {
        service: this.appLabel,
        start: since.getTime() * 1000, // microseconds
        limit: 100,
      },
    });

    return response.data.data.map((trace: any) => ({
      traceId: trace.traceID,
      spans: trace.spans.map((span: any) => ({
        spanId: span.spanID,
        operationName: span.operationName,
        startTime: span.startTime,
        duration: span.duration,
        tags: span.tags,
      })),
    }));
  }

  async collectAnalytics(since: Date): Promise<UsageData[]> {
    const response = await axios.post(`${this.posthogUrl}/api/query`, {
      query: {
        kind: 'EventsQuery',
        select: ['*'],
        where: [`timestamp >= '${since.toISOString()}'`],
      },
    }, {
      headers: { Authorization: `Bearer ${process.env.POSTHOG_API_KEY}` },
    });

    return response.data.results.map((event: any) => ({
      event: event.event,
      distinctId: event.distinct_id,
      properties: event.properties,
      timestamp: new Date(event.timestamp),
    }));
  }

  async healthCheck(): Promise<AdapterHealth> {
    const services = [
      { name: 'Prometheus', url: `${this.prometheusUrl}/-/healthy` },
      { name: 'Loki', url: `${this.lokiUrl}/ready` },
      { name: 'Jaeger', url: `${this.jaegerUrl}/` },
      { name: 'PostHog', url: `${this.posthogUrl}/_health` },
    ];

    const checks = await Promise.all(
      services.map(async (service) => {
        try {
          await axios.get(service.url, { timeout: 5000 });
          return { service: service.name, healthy: true };
        } catch {
          return { service: service.name, healthy: false };
        }
      })
    );

    const allHealthy = checks.every((c) => c.healthy);
    
    return {
      healthy: allHealthy,
      services: checks,
      timestamp: new Date(),
    };
  }

  private parseLogLevel(line: string): string {
    if (line.includes('"level":"error"')) return 'error';
    if (line.includes('"level":"warn"')) return 'warn';
    if (line.includes('"level":"info"')) return 'info';
    return 'debug';
  }

  private parseLogMetadata(line: string): Record<string, any> {
    try {
      return JSON.parse(line);
    } catch {
      return {};
    }
  }
}
```

## Dashboards

Pre-configured Grafana dashboards are included in `dashboards/`:

- `application-overview.json` - Request rate, latency, errors
- `infrastructure.json` - CPU, memory, disk, network
- `business-metrics.json` - Feature usage, conversions

Import these in Grafana UI after deployment.

## Troubleshooting

**Services won't start:**
```bash
# Check Docker logs
docker-compose -f docker-compose.observability.yml logs

# Common issue: Port conflicts
sudo lsof -i :9090  # Check if Prometheus port is used
```

**Application can't connect:**
```bash
# Verify network connectivity
docker network ls
docker network inspect bda_default

# Check application is in same network
docker-compose ps
```

**High resource usage:**
```bash
# Reduce retention periods in prometheus.yml:
storage:
  tsdb:
    retention.time: 7d  # Default is 15d

# Reduce PostHog batch size
```

## Cost Optimization

**For low-traffic applications:**
- Reduce Prometheus retention to 3-7 days
- Use Sentry cloud free tier instead of self-hosted
- Use PostHog cloud free tier
- Disable tracing (Jaeger) if not needed

**Estimated resource usage:**
- Full stack: 2GB RAM, 20GB disk
- Minimal (logs + errors + metrics): 1GB RAM, 10GB disk

## Next Steps

After deployment:
1. Verify health check: `http://your-vps:9090/-/healthy`
2. Access Grafana: `http://your-vps:3000` (admin/admin)
3. Configure application instrumentation
4. Wait 24-72h for evidence collection
5. Run `/bmad-bda-post-launch-review`
