import { onMounted, onScopeDispose } from 'vue';

import type { UsePrefetchIdleReturn } from '@/types/composables/performance';

const DEFAULT_CRITICAL_ROUTES = ['/projects', '/blog', '/stacks', '/experience', '/contact'];
const DEFAULT_IDLE_TIMEOUT = 8000;
const ROUTE_PREFETCH_INTERVAL = 1500;

export function useIdlePrefetch(routes?: string[], idleTimeout?: number): UsePrefetchIdleReturn {
    const criticalRoutes = routes ?? DEFAULT_CRITICAL_ROUTES;
    const timeout = idleTimeout ?? DEFAULT_IDLE_TIMEOUT;

    const prefetchRoute = async (path: string) => {
        try {
            await preloadRouteComponents(path);
        } catch (error) {
            if (import.meta.dev) {
                console.warn(`[usePrefetch] Failed to prefetch route: ${path}`, error);
            }
        }
    };

    const timers = new Set<ReturnType<typeof setTimeout>>();
    let idleId: number | null = null;

    const startPrefetch = () => {
        if (!import.meta.client) {
            return;
        }

        const scheduleTask = (callback: () => void) => {
            if ('requestIdleCallback' in window) {
                idleId = window.requestIdleCallback(callback, { timeout });
            } else {
                const t = setTimeout(callback, 2000);
                timers.add(t);
            }
        };

        scheduleTask(() => {
            criticalRoutes.forEach((route, index) => {
                const t = setTimeout(() => {
                    timers.delete(t);
                    prefetchRoute(route);
                }, index * ROUTE_PREFETCH_INTERVAL);
                timers.add(t);
            });
        });
    };

    const stopPrefetch = () => {
        timers.forEach(clearTimeout);
        timers.clear();
        if (idleId !== null && import.meta.client && 'cancelIdleCallback' in window) {
            window.cancelIdleCallback(idleId);
            idleId = null;
        }
    };

    onMounted(() => {
        startPrefetch();
    });

    onScopeDispose(() => {
        stopPrefetch();
    });

    return {
        prefetchRoute,
        startPrefetch,
    };
}
