import type { MaybeRef } from 'vue';
import { computed, unref } from 'vue';
import { API_ENDPOINTS } from '@/config/api';

import type {
    UnifiedSearchItem,
    UnifiedSearchParams,
    UnifiedSearchResponse,
    UnifiedSearchType,
} from '@/types/api/search';
import { createKeys, createListQuery, httpClient } from '../core';

export type { UnifiedSearchItem, UnifiedSearchParams, UnifiedSearchResponse, UnifiedSearchType };

export const searchKeys = {
    ...createKeys('search'),
    unified: (params: UnifiedSearchParams) => ['search', 'unified', params] as const,
};

export const searchApi = {
    // FTS PostgreSQL multi-entité + ranking + french_unaccent
    query: (params: UnifiedSearchParams, signal?: AbortSignal): Promise<UnifiedSearchResponse> =>
        httpClient.get(API_ENDPOINTS.SEARCH.BASE, params as unknown as Record<string, unknown>, signal),
};

export function useUnifiedSearch(
    params: MaybeRef<UnifiedSearchParams>,
    options?: { enabled?: MaybeRef<boolean>; staleTime?: number },
) {
    return createListQuery(
        computed(() => searchKeys.unified(unref(params))),
        ({ signal }) => searchApi.query(unref(params), signal),
        {
            enabled: options?.enabled,
            staleTime: options?.staleTime,
            placeholderData: (prev: UnifiedSearchResponse | undefined) => prev,
        },
    );
}
