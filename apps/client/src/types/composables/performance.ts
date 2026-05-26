// Types pour les composables performance/

import type { Ref } from 'vue';

// usePrefetch | unified prefetch composable

export interface PrefetchOptions {
    strategy: 'hover' | 'idle' | 'visible';
    routes?: string[];
    delay?: number;
}

export interface PrefetchConfig {
    queryKey: readonly unknown[];
    queryFn: () => Promise<unknown>;
    staleTime?: number;
}

export interface HoverHandlers {
    onMouseenter: () => void;
    onMouseleave: () => void;
    onFocus: () => void;
    onBlur: () => void;
}

export interface UsePrefetchHoverReturn {
    prefetch: (config: PrefetchConfig, delay?: number) => void;
    cancelPrefetch: (queryKey: readonly unknown[]) => void;
    isInCache: (queryKey: readonly unknown[]) => boolean;
    createHoverHandlers: (config: PrefetchConfig, delay?: number) => HoverHandlers;
    prefetchedKeys: Ref<Set<string>>;
}

export interface UsePrefetchIdleReturn {
    prefetchRoute: (path: string) => Promise<void>;
    startPrefetch: () => void;
}

export type UsePrefetchReturn<S extends PrefetchOptions['strategy']> = S extends 'hover'
    ? UsePrefetchHoverReturn
    : S extends 'idle'
      ? UsePrefetchIdleReturn
      : never;

// useViewportTrigger

export interface UseViewportTriggerOptions {
    /** Distance before the element enters viewport to start loading */
    rootMargin?: string;
    /** Once triggered, stay triggered (default: true) */
    once?: boolean;
    /** Force immediate on server for SSR-critical content (default: false) */
    ssrEager?: boolean;
}
