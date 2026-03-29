export interface VpsDefaultAdapterConfig {
  appLabel: string;
  jaegerServiceName: string;
  prometheusUrl: string;
  lokiUrl: string;
  sentryUrl: string;
  sentryOrganization: string;
  sentryProject: string;
  sentryToken: string;
  jaegerUrl: string;
  posthogUrl: string;
  posthogApiKey: string;
  requestTimeoutMs: number;
}

const PLACEHOLDER_RE = /(^your-|example|changeme|replace-me)/i;

function requireEnv(env: NodeJS.ProcessEnv, name: string): string {
  const value = env[name]?.trim();
  if (!value) {
    throw new Error(`VPSDefaultAdapter requires env var ${name}`);
  }
  if (PLACEHOLDER_RE.test(value)) {
    throw new Error(`VPSDefaultAdapter env var ${name} still uses a placeholder value`);
  }
  return value.replace(/\/$/, '');
}

function getUrl(env: NodeJS.ProcessEnv, name: string, fallback: string): string {
  return (env[name]?.trim() || fallback).replace(/\/$/, '');
}

function getTimeout(env: NodeJS.ProcessEnv): number {
  const raw = env.BDA_VPS_REQUEST_TIMEOUT_MS?.trim();
  if (!raw) {
    return 5000;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error("BDA_VPS_REQUEST_TIMEOUT_MS must be a positive integer");
  }

  return parsed;
}

export function loadVpsDefaultAdapterConfig(env: NodeJS.ProcessEnv = process.env): VpsDefaultAdapterConfig {
  const appLabel = requireEnv(env, "BDA_VPS_APP_LABEL");

  return {
    appLabel,
    jaegerServiceName: env.BDA_VPS_JAEGER_SERVICE_NAME?.trim() || appLabel,
    prometheusUrl: getUrl(env, "PROMETHEUS_URL", "http://localhost:9090"),
    lokiUrl: getUrl(env, "LOKI_URL", "http://localhost:3100"),
    sentryUrl: getUrl(env, "SENTRY_URL", "http://localhost:9000"),
    sentryOrganization: requireEnv(env, "BDA_VPS_SENTRY_ORG"),
    sentryProject: requireEnv(env, "BDA_VPS_SENTRY_PROJECT"),
    sentryToken: requireEnv(env, "SENTRY_TOKEN"),
    jaegerUrl: getUrl(env, "JAEGER_URL", "http://localhost:16686"),
    posthogUrl: getUrl(env, "POSTHOG_URL", "http://localhost:8000"),
    posthogApiKey: requireEnv(env, "POSTHOG_API_KEY"),
    requestTimeoutMs: getTimeout(env),
  };
}
