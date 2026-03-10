import { useQueryClient } from '@tanstack/vue-query';
import { computed, onUnmounted, ref } from 'vue';

import { CACHE_TIMES } from '@/services/api/core/cache';

import type { PrefetchConfig, UsePrefetchHoverReturn } from '@/types/composables/performance';

const DEFAULT_HOVER_DELAY = 150;

export function useHoverPrefetch(defaultDelay?: number): UsePrefetchHoverReturn {
    const queryClient = useQueryClient();
    const prefetchedKeys = ref<Set<string>>(new Set());
    const hoverTimeouts = new Map<string, ReturnType<typeof setTimeout>>();
    const delay = defaultDelay ?? DEFAULT_HOVER_DELAY;

    const prefetch = (config: PrefetchConfig, overrideDelay?: number) => {
        const keyString = JSON.stringify(config.queryKey);

        if (prefetchedKeys.value.has(keyString)) {
            return;
        }

        if (hoverTimeouts.has(keyString)) {
            clearTimeout(hoverTimeouts.get(keyString));
        }

        const timeout = setTimeout(() => {
            queryClient.prefetchQuery({
                queryKey: config.queryKey,
                queryFn: config.queryFn,
                staleTime: config.staleTime ?? CACHE_TIMES.DETAIL,
            });
            prefetchedKeys.value.add(keyString);
            hoverTimeouts.delete(keyString);
        }, overrideDelay ?? delay);

        hoverTimeouts.set(keyString, timeout);
    };

    const cancelPrefetch = (queryKey: readonly unknown[]) => {
        const keyString = JSON.stringify(queryKey);
        if (hoverTimeouts.has(keyString)) {
            clearTimeout(hoverTimeouts.get(keyString));
            hoverTimeouts.delete(keyString);
        }
    };

    const isInCache = (queryKey: readonly unknown[]): boolean => {
        return !!queryClient.getQueryData(queryKey);
    };

    const createHoverHandlers = (config: PrefetchConfig, overrideDelay?: number) => {
        return {
            onMouseenter: () => prefetch(config, overrideDelay),
            onMouseleave: () => cancelPrefetch(config.queryKey),
            onFocus: () => prefetch(config, overrideDelay),
            onBlur: () => cancelPrefetch(config.queryKey),
        };
    };

    onUnmounted(() => {
        hoverTimeouts.forEach((timeout) => clearTimeout(timeout));
        hoverTimeouts.clear();
    });

    return {
        prefetch,
        cancelPrefetch,
        isInCache,
        createHoverHandlers,
        prefetchedKeys,
    };
}

/**
 * Convenience helper for card components: encapsulates the common
 * "prefetch detail on hover" pattern used by ArticleCard, ProjectCard, StackCard.
 */
export function useCardPrefetch(
    slug: () => string | undefined,
    queryKey: (s: string) => readonly unknown[],
    queryFn: (s: string) => Promise<unknown>,
) {
    const { createHoverHandlers } = useHoverPrefetch();

    return computed(() => {
        const s = slug();
        if (!s) {
            return {};
        }
        return createHoverHandlers({
            queryKey: queryKey(s),
            queryFn: () => queryFn(s),
            staleTime: CACHE_TIMES.DETAIL,
        });
    });
}
