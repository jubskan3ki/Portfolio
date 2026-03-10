import { useHoverPrefetch } from './useHoverPrefetch';
import { useIdlePrefetch } from './useIdlePrefetch';

import type { PrefetchOptions, UsePrefetchReturn } from '@/types/composables/performance';

/**
 * Unified prefetch composable supporting multiple strategies:
 * - 'hover': Prefetch TanStack Query data on mouse hover/focus (for cards, links)
 * - 'idle': Prefetch route components during idle time (for layout-level preloading)
 */
export function usePrefetch<S extends PrefetchOptions['strategy']>(
    options: PrefetchOptions & { strategy: S },
): UsePrefetchReturn<S> {
    if (options.strategy === 'hover') {
        return useHoverPrefetch(options.delay) as UsePrefetchReturn<S>;
    }

    if (options.strategy === 'idle') {
        return useIdlePrefetch(options.routes, options.delay) as UsePrefetchReturn<S>;
    }

    throw new Error(`[usePrefetch] Unsupported strategy: "${options.strategy}"`);
}

// Re-export convenience helpers
export { useCardPrefetch } from './useHoverPrefetch';
