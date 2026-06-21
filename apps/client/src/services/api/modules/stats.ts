import { API_ENDPOINTS } from '@/config/api';
import type { DashboardOverview } from '@/types/api/stats';
import { createKeys, createRealtimeQuery, httpClient } from '../core';

export const statsKeys = {
    ...createKeys('stats'),
    overview: () => ['stats', 'overview'] as const,
    history: (limit: number) => ['stats', 'history', 'activities', limit] as const,
};

export const statsApi = {
    getOverview: (signal?: AbortSignal): Promise<DashboardOverview> =>
        httpClient.get(API_ENDPOINTS.STATS.OVERVIEW, undefined, signal),

    getActivity: <T = unknown>(limit?: number): Promise<T> =>
        httpClient.get(`${API_ENDPOINTS.STATS.ACTIVITY}${limit ? `?limit=${limit}` : ''}`),

    getStats: <T = unknown>(): Promise<T> => httpClient.get(API_ENDPOINTS.STATS.BASE),
};

export function useDashboardOverview() {
    return createRealtimeQuery(statsKeys.overview(), ({ signal }) => statsApi.getOverview(signal));
}
