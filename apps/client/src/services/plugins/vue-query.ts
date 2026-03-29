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
    // Initialize API base URL from Nuxt runtime config (SSR-safe)
    const config = useRuntimeConfig();
    const apiBase = import.meta.server
        ? ((config as Record<string, unknown>).apiBaseServer as string) || (config.public?.apiBase as string) || ''
        : (config.public?.apiBase as string) || '';
    if (apiBase) {
        setBaseUrl(apiBase);
    }

    // Global mutation error handler — catches unhandled mutation errors
    const mutationCache = new MutationCache({
        onError: (error, _variables, _context, mutation) => {
            // Allow per-mutation opt-out
            if (mutation.meta?.suppressGlobalError) {
                return;
            }

            if (isApiError(error)) {
                // Auth errors handled by auth plugin interceptor
                if (error.code === 'AUTH_ERROR') {
                    return;
                }
                // Validation errors handled at form level
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
                staleTime: 1000 * 60 * 5, // 5 minutes
                gcTime: 1000 * 60 * 60, // 1 hour (garbage collection)
                // Smart retry: never retry network errors (API down), retry server errors only
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

    // SSR: Dehydrate only above-fold critical queries to reduce hydration payload
    if (import.meta.server) {
        nuxtApp.hooks.hook('app:rendered', () => {
            if (nuxtApp.payload) {
                const dehydratedState = dehydrate(queryClient, {
                    shouldDehydrateQuery: (query) => {
                        // Only dehydrate successful queries — pending promises crash devalue
                        if (query.state.status !== 'success') {
                            return false;
                        }
                        const key = query.queryKey;
                        const criticalPrefixes = ['stacks'];
                        return typeof key[0] === 'string' && criticalPrefixes.includes(key[0]);
                    },
                });
                // Strip any residual promise fields that devalue cannot serialize
                if (dehydratedState.queries) {
                    for (const q of dehydratedState.queries) {
                        delete (q as unknown as Record<string, unknown>).promise;
                    }
                }
                nuxtApp.payload.vueQueryState = dehydratedState;
            }
        });
    }

    // Client: Hydrate state from server
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
