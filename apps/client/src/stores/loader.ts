// Store Pinia pour la gestion des loaders
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

import { TimeoutManager } from '@/services/utils/timeoutManager';

import type { LoaderItem, LoaderOptions, LoaderPosition } from '@/types/stores/loader';

export const useLoaderStore = defineStore('loader', () => {
    // SSR-safe: each store instance gets its own TimeoutManager
    const delayTimeouts = new TimeoutManager();

    // State
    const loaders = ref<LoaderItem[]>([]);
    const isLoading = computed(() => loaders.value.length > 0);

    // Getters
    const isLoadingById = computed(() => (id: string) => {
        return loaders.value.some((loader) => loader.id === id);
    });

    const fullscreenLoaders = computed(() => {
        return loaders.value.filter((loader) => loader.position === 'fullscreen');
    });

    const containerLoaders = computed(() => {
        return loaders.value.filter((loader) => loader.position === 'container');
    });

    // Actions
    function start(options: LoaderOptions = {}): string {
        const id = options.id ?? `loader-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

        const loader: LoaderItem = {
            id,
            position: options.position ?? 'fullscreen',
            type: options.type ?? 'circle',
            size: options.size ?? 'md',
            label: options.label ?? 'Chargement...',
            hasOverlay: options.hasOverlay ?? true,
            delay: options.delay ?? 0,
            cancelable: options.cancelable ?? false,
            targetSelector: options.targetSelector,
            startTime: Date.now(),
        };

        if (loader.delay > 0) {
            delayTimeouts.set(
                id,
                () => {
                    if (!isLoadingById.value(id)) {
                        loaders.value.push(loader);
                    }
                },
                loader.delay,
            );
        } else {
            loaders.value.push(loader);
        }

        return id;
    }

    function stop(id: string): void {
        delayTimeouts.clear(id);

        const index = loaders.value.findIndex((loader) => loader.id === id);
        if (index !== -1) {
            loaders.value.splice(index, 1);
        }
    }

    function stopAll(): void {
        delayTimeouts.clearAll();
        loaders.value = [];
    }

    function stopByPosition(position: LoaderPosition): void {
        const idsToRemove = loaders.value.filter((loader) => loader.position === position).map((loader) => loader.id);
        delayTimeouts.clearByIds(idsToRemove);

        loaders.value = loaders.value.filter((loader) => loader.position !== position);
    }

    return {
        // State
        loaders,
        isLoading,
        // Getters
        isLoadingById,
        fullscreenLoaders,
        containerLoaders,
        // Actions
        start,
        stop,
        stopAll,
        stopByPosition,
    };
});
