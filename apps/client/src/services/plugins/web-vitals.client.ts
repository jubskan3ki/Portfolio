import { API_ENDPOINTS } from '@/config/api';

import type { Router } from 'vue-router';

interface WebVitalsPayload {
    name: string;
    value: number;
    rating: 'good' | 'needs-improvement' | 'poor';
    delta: number;
    id: string;
    page: string;
    url: string;
    userAgent: string;
    language: string;
    viewport: {
        width?: number;
        height?: number;
    };
    connectionType: string | null;
    isMobile: boolean | null;
    timestamp: string;
}

const clampSampleRate = (value: string | number | undefined, fallback: number): number => {
    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
        return fallback;
    }
    return Math.max(0, Math.min(1, parsed));
};

// Use relative URL so requests go through the Nuxt proxy (avoids CORS issues with sendBeacon)
const getWebVitalsEndpoint = (): string => API_ENDPOINTS.STATS.WEB_VITALS;

export default defineNuxtPlugin((nuxtApp) => {
    if (!import.meta.client) {
        return;
    }

    const runtimeConfig = useRuntimeConfig();
    const sampleRate = clampSampleRate(
        runtimeConfig.public.webVitalsSampleRate as string | number | undefined,
        import.meta.dev ? 1 : 0.2,
    );

    if (Math.random() > sampleRate) {
        return;
    }

    const endpoint = getWebVitalsEndpoint();

    // Dynamic import — only load web-vitals library when actually sampling
    void import('web-vitals').then(({ onCLS, onFCP, onINP, onLCP, onTTFB }) => {
        const sendMetric = (metric: {
            name: string;
            value: number;
            rating: 'good' | 'needs-improvement' | 'poor';
            delta: number;
            id: string;
        }): void => {
            try {
                const route = (nuxtApp.$router as Router).currentRoute.value;
                const browserNavigator = navigator as Navigator & {
                    connection?: { effectiveType?: string };
                    userAgentData?: { mobile?: boolean };
                };
                const connection = browserNavigator.connection;
                const payload: WebVitalsPayload = {
                    name: metric.name,
                    value: metric.value,
                    rating: metric.rating,
                    delta: metric.delta,
                    id: metric.id,
                    page: route.path,
                    url: window.location.href,
                    userAgent: navigator.userAgent || '',
                    language: navigator.language || '',
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight,
                    },
                    connectionType: connection?.effectiveType ?? null,
                    isMobile: browserNavigator.userAgentData?.mobile ?? window.matchMedia('(max-width: 768px)').matches,
                    timestamp: new Date().toISOString(),
                };

                const body = JSON.stringify(payload);
                if (navigator.sendBeacon) {
                    const blob = new Blob([body], { type: 'application/json' });
                    navigator.sendBeacon(endpoint, blob);
                    return;
                }

                void fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body,
                    keepalive: true,
                    credentials: 'omit',
                });
            } catch {
                // Silently swallow — web vitals are non-critical telemetry
            }
        };

        onLCP(sendMetric);
        onCLS(sendMetric);
        onINP(sendMetric);
        onFCP(sendMetric);
        onTTFB(sendMetric);
    });
});
