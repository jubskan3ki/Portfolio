import { onMounted } from 'vue';

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

    const startPrefetch = () => {
        if (!import.meta.client) {
            return;
        }

        const scheduleTask = (callback: () => void) => {
            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(callback, { timeout });
            } else {
                setTimeout(callback, 2000);
            }
        };

        scheduleTask(() => {
            criticalRoutes.forEach((route, index) => {
                setTimeout(() => {
                    prefetchRoute(route);
                }, index * ROUTE_PREFETCH_INTERVAL);
            });
        });
    };

    onMounted(() => {
        startPrefetch();
    });

    return {
        prefetchRoute,
        startPrefetch,
    };
}
