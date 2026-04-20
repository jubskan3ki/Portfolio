// Public status payload — served by the backend on /api/public/status/

export interface ServiceStatus {
    name: string;
    status: 'green' | 'amber' | 'red' | 'unknown';
    up: boolean;
}

export interface Incident {
    name: string;
    severity: string;
    started_at: string;
    ended_at: string;
}

export interface StatusPayload {
    uptime_30d_pct: number | null;
    uptime_1d_pct: number | null;
    latency_p95_seconds: number | null;
    services: ServiceStatus[];
    incidents: Incident[];
    slo_targets: { availability: number; latency_p95_seconds: number };
}
