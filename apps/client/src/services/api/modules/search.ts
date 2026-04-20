import { computed, unref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';

import { httpClient, createKeys, createListQuery } from '../core';

import type {
    UnifiedSearchItem,
    UnifiedSearchParams,
    UnifiedSearchResponse,
    UnifiedSearchType,
} from '@/types/api/search';
import type { MaybeRef } from 'vue';

export type { UnifiedSearchItem, UnifiedSearchParams, UnifiedSearchResponse, UnifiedSearchType };

export const searchKeys = {
    ...createKeys('search'),
    unified: (params: UnifiedSearchParams) => ['search', 'unified', params] as const,
};

export const searchApi = {
    // FTS PostgreSQL multi-entité + ranking + french_unaccent
    query: (params: UnifiedSearchParams): Promise<UnifiedSearchResponse> =>
        httpClient.get(API_ENDPOINTS.SEARCH.BASE, params as unknown as Record<string, unknown>),
};

export function useUnifiedSearch(
    params: MaybeRef<UnifiedSearchParams>,
    options?: { enabled?: MaybeRef<boolean>; staleTime?: number },
) {
    return createListQuery(
        computed(() => searchKeys.unified(unref(params))),
        () => searchApi.query(unref(params)),
        {
            enabled: options?.enabled,
            staleTime: options?.staleTime,
            placeholderData: (prev: UnifiedSearchResponse | undefined) => prev,
        },
    );
}
