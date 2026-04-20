import { useHoverPrefetch } from './useHoverPrefetch';
import { useIdlePrefetch } from './useIdlePrefetch';

import type { PrefetchOptions, UsePrefetchReturn } from '@/types/composables/performance';

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

export { useCardPrefetch } from './useHoverPrefetch';
