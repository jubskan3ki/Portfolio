<template>
    <main class="status-page">
        <header class="status-header">
            <h1>Status</h1>
            <div v-if="data" class="status-banner" :style="{ background: statusColor(overallStatus) }">
                {{ statusLabel(overallStatus) }}
            </div>
        </header>

        <section v-if="pending" class="status-loading">Chargement…</section>

        <section v-else-if="error" class="status-error">
            Impossible de récupérer le status ({{ error.message }}).
        </section>

        <template v-else-if="data">
            <section class="metrics">
                <div class="metric">
                    <span class="metric-label">Disponibilité 30 j</span>
                    <span class="metric-value">
                        {{ data.uptime_30d_pct !== null ? data.uptime_30d_pct.toFixed(3) + ' %' : '|' }}
                    </span>
                    <span class="metric-target">SLO {{ (data.slo_targets.availability * 100).toFixed(1) }} %</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Disponibilité 24 h</span>
                    <span class="metric-value">
                        {{ data.uptime_1d_pct !== null ? data.uptime_1d_pct.toFixed(3) + ' %' : '|' }}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Latence p95 (5 min)</span>
                    <span class="metric-value">
                        {{
                            data.latency_p95_seconds !== null
                                ? (data.latency_p95_seconds * 1000).toFixed(0) + ' ms'
                                : '|'
                        }}
                    </span>
                    <span class="metric-target">
                        SLO &lt; {{ (data.slo_targets.latency_p95_seconds * 1000).toFixed(0) }} ms
                    </span>
                </div>
            </section>

            <section class="services">
                <h2>Services</h2>
                <ul>
                    <li v-for="svc in data.services" :key="svc.name">
                        <span class="service-dot" :style="{ background: statusColor(svc.status) }"></span>
                        <span class="service-name">{{ svc.name }}</span>
                        <span class="service-status">{{ statusLabel(svc.status) }}</span>
                    </li>
                </ul>
            </section>

            <section class="incidents">
                <h2>Incidents récents</h2>
                <p v-if="data.incidents.length === 0" class="incidents-empty">Aucun incident enregistré récemment.</p>
                <ul v-else>
                    <li v-for="(incident, i) in data.incidents" :key="i">
                        <span class="incident-name">{{ incident.name }}</span>
                        <span class="incident-severity" :class="'severity-' + incident.severity">
                            {{ incident.severity }}
                        </span>
                        <time>{{ new Date(incident.started_at).toLocaleString('fr-FR') }}</time>
                    </li>
                </ul>
            </section>

            <footer class="status-footer">
                Mis à jour automatiquement toutes les 60 secondes ·
                <button type="button" @click="refresh()">rafraîchir maintenant</button>
            </footer>
        </template>
    </main>
</template>

<script setup lang="ts">
    import type { StatusPayload } from '@/types/api/status';

    const { data, pending, error, refresh } = await useFetch<StatusPayload>('/api/public/status/', {
        server: true,
        lazy: false,
        key: 'public-status',
    });

    const statusLabel = (s: string) =>
        ({ green: 'Opérationnel', amber: 'Dégradé', red: 'Incident', unknown: 'Inconnu' })[s] || s;

    const statusColor = (s: string) =>
        ({ green: '#16a34a', amber: '#f59e0b', red: '#dc2626', unknown: '#6b7280' })[s] || '#6b7280';

    const overallStatus = computed(() => {
        if (!data.value) {
            return 'unknown';
        }
        const statuses = data.value.services.map((s) => s.status);
        if (statuses.includes('red')) {
            return 'red';
        }
        if (statuses.includes('amber')) {
            return 'amber';
        }
        if (statuses.every((s) => s === 'green')) {
            return 'green';
        }
        return 'unknown';
    });

    useSeoMeta({
        title: 'Status | Portfolio',
        description: 'Disponibilité et performance en temps réel.',
        robots: 'noindex, nofollow',
    });

    // Auto-refresh every 60s on client side.
    if (import.meta.client) {
        setInterval(() => refresh(), 60_000);
    }
</script>

<style scoped lang="scss">
    .status-page {
        max-width: 960px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    .status-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    .status-banner {
        padding: 0.5rem 1rem;
        border-radius: 999px;
        color: white;
        font-weight: 600;
    }

    .metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background: var(--color-surface, #fff);
    }

    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0.25rem 0;
    }

    .metric-target {
        font-size: 0.75rem;
        color: #9ca3af;
    }

    .services ul,
    .incidents ul {
        list-style: none;
        padding: 0;
        margin: 0.75rem 0;
    }

    .services li {
        display: grid;
        grid-template-columns: 12px 1fr auto;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f3f4f6;
    }

    .service-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .incidents li {
        display: grid;
        grid-template-columns: 1fr auto auto;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f3f4f6;
    }

    .incident-severity {
        font-size: 0.75rem;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        text-transform: uppercase;
    }

    .severity-page {
        background: #fef2f2;
        color: #dc2626;
    }
    .severity-ticket {
        background: #fffbeb;
        color: #d97706;
    }

    .incidents-empty {
        color: #6b7280;
        padding: 1rem 0;
    }

    .status-footer {
        margin-top: 2rem;
        color: #6b7280;
        font-size: 0.85rem;

        button {
            background: none;
            border: 0;
            color: inherit;
            text-decoration: underline;
            cursor: pointer;
        }
    }

    .status-error {
        color: #dc2626;
        padding: 1rem;
        border: 1px solid currentcolor;
        border-radius: 8px;
    }
</style>
