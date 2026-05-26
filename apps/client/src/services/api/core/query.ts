import { useQuery } from '@tanstack/vue-query';
import type { MaybeRef } from 'vue';
import { computed, unref } from 'vue';

import type { QueryOptions, QueryPreset } from '@/types/services/api';
import { CACHE_TIMES } from './cache';

const QUERY_PRESETS: Record<QueryPreset, { staleTime: number; refetchInterval?: number }> = {
    list: { staleTime: CACHE_TIMES.LIST },
    detail: { staleTime: CACHE_TIMES.DETAIL },
    static: { staleTime: CACHE_TIMES.STATIC },
    realtime: { staleTime: CACHE_TIMES.REALTIME, refetchInterval: CACHE_TIMES.REALTIME },
};

function createQuery<TData, TSelect = TData>(
    preset: QueryPreset,
    queryKey: MaybeRef<readonly unknown[]>,
    queryFn: () => Promise<TData>,
    options?: QueryOptions<TData, TSelect>,
) {
    return useQuery({
        queryKey: computed(() => unref(queryKey)),
        queryFn,
        ...QUERY_PRESETS[preset],
        ...options,
    });
}

export const createListQuery = <TData, TSelect = TData>(
    queryKey: MaybeRef<readonly unknown[]>,
    queryFn: () => Promise<TData>,
    options?: QueryOptions<TData, TSelect>,
) => createQuery<TData, TSelect>('list', queryKey, queryFn, options);

export const createDetailQuery = <TData, TSelect = TData>(
    queryKey: MaybeRef<readonly unknown[]>,
    queryFn: () => Promise<TData>,
    options?: QueryOptions<TData, TSelect>,
) => createQuery<TData, TSelect>('detail', queryKey, queryFn, options);

export const createStaticQuery = <TData, TSelect = TData>(
    queryKey: MaybeRef<readonly unknown[]>,
    queryFn: () => Promise<TData>,
    options?: QueryOptions<TData, TSelect>,
) => createQuery<TData, TSelect>('static', queryKey, queryFn, options);

export const createRealtimeQuery = <TData, TSelect = TData>(
    queryKey: MaybeRef<readonly unknown[]>,
    queryFn: () => Promise<TData>,
    options?: QueryOptions<TData, TSelect>,
) => createQuery<TData, TSelect>('realtime', queryKey, queryFn, options);
