import { IEvidenceAdapter, LogEntry, ErrorReport, MetricSnapshot, TraceData, UsageData, AdapterHealth } from '../IEvidenceAdapter';
import axios from 'axios';

export class VPSDefaultAdapter implements IEvidenceAdapter {
  name = 'vps-default';
  environment = 'vps' as const;

  private prometheusUrl = process.env.PROMETHEUS_URL || 'http://localhost:9090';
  private lokiUrl = process.env.LOKI_URL || 'http://localhost:3100';
  private sentryUrl = process.env.SENTRY_URL || 'http://localhost:9000';
  private jaegerUrl = process.env.JAEGER_URL || 'http://localhost:16686';
  private posthogUrl = process.env.POSTHOG_URL || 'http://localhost:8000';

  async collectLogs(since: Date): Promise<LogEntry[]> {
    const query = `{app="your-app-name"}`;
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
    const response = await axios.get(`${this.sentryUrl}/api/0/projects/your-org/your-project/issues/`, {
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
        service: 'your-app-name',
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
