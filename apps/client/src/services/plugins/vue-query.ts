import {
    VueQueryPlugin,
    QueryClient,
    MutationCache,
    hydrate,
    dehydrate,
    type DehydratedState,
    type VueQueryPluginOptions,
} from '@tanstack/vue-query';

import { setBaseUrl } from '@/config/api';
import { isApiError } from '@/services/utils/errors/guards';
import { useAlertStore } from '@/stores/alert';

import type { Pinia } from 'pinia';

export default defineNuxtPlugin((nuxtApp) => {
    // API base URL via runtime config, SSR-safe (apiBaseServer > public.apiBase)
    const config = useRuntimeConfig();
    const apiBase = import.meta.server
        ? ((config as Record<string, unknown>).apiBaseServer as string) || (config.public?.apiBase as string) || ''
        : (config.public?.apiBase as string) || '';
    if (apiBase) {
        setBaseUrl(apiBase);
    }

    const mutationCache = new MutationCache({
        onError: (error, _variables, _context, mutation) => {
            if (mutation.meta?.suppressGlobalError) {
                return;
            }

            if (isApiError(error)) {
                // AUTH gérée par plugin auth, VALIDATION gérée par les forms
                if (error.code === 'AUTH_ERROR') {
                    return;
                }
                if (error.code === 'VALIDATION_ERROR') {
                    return;
                }
            }

            const alertStore = useAlertStore(nuxtApp.$pinia as Pinia);
            alertStore.add({
                type: 'error',
                message: isApiError(error) ? error.message : 'Une erreur inattendue est survenue',
                dismissible: true,
            });
        },
    });

    const queryClient = new QueryClient({
        mutationCache,
        defaultOptions: {
            queries: {
                staleTime: 1000 * 60 * 5,
                gcTime: 1000 * 60 * 60,
                // Pas de retry sur NETWORK_ERROR (API down), sinon max 2
                retry: import.meta.server
                    ? 0
                    : (failureCount, error) => {
                        if (isApiError(error) && error.code === 'NETWORK_ERROR') {
                            return false;
                        }
                        return failureCount < 2;
                    },
                retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
                refetchOnWindowFocus: false,
                refetchOnReconnect: true,
            },
            mutations: {
                retry: 1,
            },
        },
    });

    const options: VueQueryPluginOptions = { queryClient };

    nuxtApp.vueApp.use(VueQueryPlugin, options);

    // SSR: ne déshydrate que les queries critiques above-fold (réduit payload hydration)
    if (import.meta.server) {
        nuxtApp.hooks.hook('app:rendered', () => {
            if (nuxtApp.payload) {
                const dehydratedState = dehydrate(queryClient, {
                    shouldDehydrateQuery: (query) => {
                        // Skip non-success: pending promises crashent devalue
                        if (query.state.status !== 'success') {
                            return false;
                        }
                        const key = query.queryKey;
                        const criticalPrefixes = [
                            'stacks',
                            'articles',
                            'projects',
                            'experiences',
                            'site-settings',
                        ];
                        return typeof key[0] === 'string' && criticalPrefixes.includes(key[0]);
                    },
                });
                // Strip promise fields résiduels non sérialisables par devalue
                if (dehydratedState.queries) {
                    for (const q of dehydratedState.queries) {
                        delete (q as unknown as Record<string, unknown>).promise;
                    }
                }
                nuxtApp.payload.vueQueryState = dehydratedState;
            }
        });
    }

    if (import.meta.client) {
        nuxtApp.hooks.hook('app:created', () => {
            const state = nuxtApp.payload?.vueQueryState as DehydratedState | undefined;
            if (state) {
                hydrate(queryClient, state);
            }
        });
    }

    return {
        provide: {
            queryClient,
        },
    };
});
