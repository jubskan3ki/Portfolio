import { API_ENDPOINTS } from '@/config/api';

import type { Router } from 'vue-router';
import type {
    CLSMetricWithAttribution,
    FCPMetricWithAttribution,
    INPMetricWithAttribution,
    LCPMetricWithAttribution,
    TTFBMetricWithAttribution,
} from 'web-vitals/attribution';

type AnyMetricWithAttribution
    = | CLSMetricWithAttribution
        | FCPMetricWithAttribution
        | INPMetricWithAttribution
        | LCPMetricWithAttribution
        | TTFBMetricWithAttribution;

interface WebVitalsAttribution {
    // LCP — quel élément est responsable du rendu le plus lourd
    lcpElement?: string;
    lcpUrl?: string;
    lcpTimeToFirstByte?: number;
    lcpResourceLoadDuration?: number;
    lcpElementRenderDelay?: number;
    // CLS — quelle balise a bougé et de combien
    clsLargestShiftTarget?: string;
    clsLargestShiftValue?: number;
    clsLoadState?: string;
    // INP — quelle interaction a causé le délai
    inpInteractionTarget?: string;
    inpInteractionType?: string;
    inpInputDelay?: number;
    inpProcessingDuration?: number;
    inpPresentationDelay?: number;
    // TTFB — décomposition du temps réseau
    ttfbWaitingDuration?: number;
    ttfbDnsDuration?: number;
    ttfbConnectionDuration?: number;
    ttfbRequestDuration?: number;
    // FCP
    fcpTimeToFirstByte?: number;
    fcpFirstByteToFCP?: number;
    fcpLoadState?: string;
}

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
    attribution: WebVitalsAttribution;
}

const clampSampleRate = (value: string | number | undefined, fallback: number): number => {
    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
        return fallback;
    }
    return Math.max(0, Math.min(1, parsed));
};

const getWebVitalsEndpoint = (): string => API_ENDPOINTS.STATS.WEB_VITALS;

const extractAttribution = (metric: AnyMetricWithAttribution): WebVitalsAttribution => {
    switch (metric.name) {
        case 'LCP': {
            const a = (metric as LCPMetricWithAttribution).attribution;
            return {
                lcpUrl: a.url,
                lcpTimeToFirstByte: a.timeToFirstByte,
                lcpResourceLoadDuration: a.resourceLoadDuration,
                lcpElementRenderDelay: a.elementRenderDelay,
            };
        }
        case 'CLS': {
            const a = (metric as CLSMetricWithAttribution).attribution;
            return {
                clsLargestShiftTarget: a.largestShiftTarget,
                clsLargestShiftValue: a.largestShiftValue,
                clsLoadState: a.loadState,
            };
        }
        case 'INP': {
            const a = (metric as INPMetricWithAttribution).attribution;
            return {
                inpInteractionTarget: a.interactionTarget,
                inpInteractionType: a.interactionType,
                inpInputDelay: a.inputDelay,
                inpProcessingDuration: a.processingDuration,
                inpPresentationDelay: a.presentationDelay,
            };
        }
        case 'TTFB': {
            const a = (metric as TTFBMetricWithAttribution).attribution;
            return {
                ttfbWaitingDuration: a.waitingDuration,
                ttfbDnsDuration: a.dnsDuration,
                ttfbConnectionDuration: a.connectionDuration,
                ttfbRequestDuration: a.requestDuration,
            };
        }
        case 'FCP': {
            const a = (metric as FCPMetricWithAttribution).attribution;
            return {
                fcpTimeToFirstByte: a.timeToFirstByte,
                fcpFirstByteToFCP: a.firstByteToFCP,
                fcpLoadState: a.loadState,
            };
        }
        default:
            return {};
    }
};

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

    void import('web-vitals/attribution').then(({ onCLS, onFCP, onINP, onLCP, onTTFB }) => {
        const sendMetric = (metric: AnyMetricWithAttribution): void => {
            try {
                const route = (nuxtApp.$router as Router).currentRoute.value;
                const browserNavigator = navigator as Navigator & {
                    connection?: { effectiveType?: string };
                    userAgentData?: { mobile?: boolean };
                };
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
                    connectionType: browserNavigator.connection?.effectiveType ?? null,
                    isMobile:
                        browserNavigator.userAgentData?.mobile
                        ?? window.matchMedia('(max-width: 768px)').matches,
                    timestamp: new Date().toISOString(),
                    attribution: extractAttribution(metric),
                };

                const body = JSON.stringify(payload);
                if (navigator.sendBeacon) {
                    const blob = new Blob([body], { type: 'application/json' });
                    navigator.sendBeacon(endpoint, blob);
                    return;
                }

                void fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
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
