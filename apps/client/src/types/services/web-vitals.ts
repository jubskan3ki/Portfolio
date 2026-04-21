// Types for the web-vitals client plugin | payload sent to the backend

import type {
    CLSMetricWithAttribution,
    FCPMetricWithAttribution,
    INPMetricWithAttribution,
    LCPMetricWithAttribution,
    TTFBMetricWithAttribution,
} from 'web-vitals/attribution';

export type AnyMetricWithAttribution
    = | CLSMetricWithAttribution
        | FCPMetricWithAttribution
        | INPMetricWithAttribution
        | LCPMetricWithAttribution
        | TTFBMetricWithAttribution;

export interface WebVitalsAttribution {
    lcpElement?: string;
    lcpUrl?: string;
    lcpTimeToFirstByte?: number;
    lcpResourceLoadDuration?: number;
    lcpElementRenderDelay?: number;
    clsLargestShiftTarget?: string;
    clsLargestShiftValue?: number;
    clsLoadState?: string;
    inpInteractionTarget?: string;
    inpInteractionType?: string;
    inpInputDelay?: number;
    inpProcessingDuration?: number;
    inpPresentationDelay?: number;
    ttfbWaitingDuration?: number;
    ttfbDnsDuration?: number;
    ttfbConnectionDuration?: number;
    ttfbRequestDuration?: number;
    fcpTimeToFirstByte?: number;
    fcpFirstByteToFCP?: number;
    fcpLoadState?: string;
}

export interface WebVitalsPayload {
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
