import { API_ENDPOINTS } from '@/config/api';

import type {
    AnyMetricWithAttribution,
    WebVitalsAttribution,
    WebVitalsPayload,
} from '@/types/services/web-vitals';
import type { Router } from 'vue-router';
import type {
    CLSMetricWithAttribution,
    FCPMetricWithAttribution,
    INPMetricWithAttribution,
    LCPMetricWithAttribution,
    TTFBMetricWithAttribution,
} from 'web-vitals/attribution';

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

    if (import.meta.dev) {
        return;
    }

    const runtimeConfig = useRuntimeConfig();
    const sampleRate = clampSampleRate(
        runtimeConfig.public.webVitalsSampleRate as string | number | undefined,
        0.2,
    );

    if (Math.random() > sampleRate) {
        return;
    }

    const endpoint = getWebVitalsEndpoint();

    // Registration en idle: ne concurrence pas hydration/paint. web-vitals utilise buffered:true donc capture rétroactive OK
    const scheduleInit = (cb: () => void): void => {
        type WindowWithIdle = Window & {
            requestIdleCallback?: (cb: IdleRequestCallback, opts?: { timeout: number }) => number;
        };
        const ric = (window as WindowWithIdle).requestIdleCallback;
        if (typeof ric === 'function') {
            ric(() => cb(), { timeout: 3000 });
        } else {
            setTimeout(cb, 1500);
        }
    };

    scheduleInit(() => void import('web-vitals/attribution').then(({ onCLS, onFCP, onINP, onLCP, onTTFB }) => {
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
                // telemetry non-critique
            }
        };

        onLCP(sendMetric);
        onCLS(sendMetric);
        onINP(sendMetric);
        onFCP(sendMetric);
        onTTFB(sendMetric);
    }));
});
