export interface LogEntry {
  timestamp: Date;
  level: string;
  message: string;
  metadata: Record<string, any>;
}

export interface ErrorReport {
  id: string;
  title: string;
  message: string;
  count: number;
  userCount: number;
  firstSeen: Date;
  lastSeen: Date;
  level: string;
  stacktrace?: any;
}

export interface MetricSnapshot {
  name: string;
  value: number;
  timestamp: Date;
  labels: Record<string, string>;
}

export interface TraceData {
  traceId: string;
  spans: Array<{
    spanId: string;
    operationName: string;
    startTime: number;
    duration: number;
    tags: any[];
  }>;
}

export interface UsageData {
  event: string;
  distinctId: string;
  properties: Record<string, any>;
  timestamp: Date;
}

export interface AdapterHealth {
  healthy: boolean;
  services: Array<{ service: string; healthy: boolean }>;
  timestamp: Date;
}

export interface IEvidenceAdapter {
  name: string;
  environment: string;

  collectLogs(since: Date): Promise<LogEntry[]>;
  collectErrors(since: Date): Promise<ErrorReport[]>;
  collectMetrics(since: Date): Promise<MetricSnapshot[]>;
  collectTraces(since: Date): Promise<TraceData[]>;
  collectAnalytics(since: Date): Promise<UsageData[]>;
  healthCheck(): Promise<AdapterHealth>;
}
