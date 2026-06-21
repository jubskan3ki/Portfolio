import { useDebounceFn } from '@vueuse/core';
import type { Ref } from 'vue';
import { computed, ref, toRaw, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { TIMEOUTS } from '@/config/constants';
import { filterPresets } from '@/config/filterPresets';

import type { FilterFieldConfig, UseFiltersOptions } from '@/types/composables/data';

// structuredClone(toRaw(...)) au lieu de JSON : plus rapide, sans conversion en string.
const snapshot = <V>(value: V): V => structuredClone(toRaw(value));

function isFilterActive(value: unknown, defaultValue: unknown): boolean {
    if (Array.isArray(value)) {
        return value.length > 0;
    }
    return value !== defaultValue && value !== '' && value !== null && value !== undefined;
}

export function useFilters<T extends Record<string, unknown>>(options: UseFiltersOptions<T>) {
    const {
        defaults,
        fieldConfig = {} as Partial<Record<keyof T, Partial<FilterFieldConfig<unknown>>>>,
        pagination = { enabled: false, pageKey: 'page', itemsPerPage: 6, limitKey: 'limit' },
        urlSync = { enabled: true, debounceMs: TIMEOUTS.SEARCH_DEBOUNCE },
        searchDebounceMs = TIMEOUTS.SEARCH_DEBOUNCE,
    } = options;

    const route = useRoute();
    const router = useRouter();

    const filters = ref({ ...defaults }) as Ref<T>;
    const debouncedFilters = ref({ ...defaults }) as Ref<T>;
    const currentPage = ref(1);

    const apiFilters = computed(() => {
        const result = { ...debouncedFilters.value };

        if (pagination.enabled) {
            (result as Record<string, unknown>)[pagination.pageKey || 'page'] = currentPage.value;
            (result as Record<string, unknown>)[pagination.limitKey || 'limit'] = pagination.itemsPerPage;
        }

        return Object.fromEntries(
            Object.entries(result).filter(([_, value]) => {
                if (Array.isArray(value)) {
                    return value.length > 0;
                }
                return value !== undefined && value !== null && value !== '';
            }),
        ) as T;
    });

    const syncFromUrl = () => {
        Object.keys(defaults).forEach((key) => {
            const urlKey = fieldConfig[key as keyof T]?.urlKey || key;
            const queryValue = route.query[urlKey];

            if (queryValue !== undefined) {
                const defaultValue = defaults[key as keyof T];

                if (Array.isArray(defaultValue)) {
                    // Supports ?tags=Vue&tags=React and ?tags=Vue,React
                    if (Array.isArray(queryValue)) {

                        (filters.value as Record<string, unknown>)[key] = queryValue.map(String);
                    } else if (typeof queryValue === 'string' && queryValue.includes(',')) {
                        (filters.value as Record<string, unknown>)[key] = queryValue
                            .split(',')
                            .map((s) => s.trim())
                            .filter(Boolean);
                    } else {
                        (filters.value as Record<string, unknown>)[key] = [String(queryValue)];
                    }
                } else if (typeof defaultValue === 'number') {
                    (filters.value as Record<string, unknown>)[key] = Number(queryValue);
                } else if (typeof defaultValue === 'boolean') {
                    (filters.value as Record<string, unknown>)[key] = queryValue === 'true';
                } else {
                    (filters.value as Record<string, unknown>)[key] = queryValue;
                }
            }
        });

        if (pagination.enabled && route.query[pagination.pageKey || 'page']) {
            currentPage.value = Number(route.query[pagination.pageKey || 'page']) || 1;
        }
    };

    const syncUrlNow = () => {
        if (!urlSync.enabled) {
            return;
        }

        const query: Record<string, string | string[]> = {};

        Object.entries(filters.value as Record<string, unknown>).forEach(([key, value]) => {
            const defaultValue = defaults[key as keyof T];
            const urlKey = fieldConfig[key as keyof T]?.urlKey || key;

            if (isFilterActive(value, defaultValue)) {
                query[urlKey] = Array.isArray(value) ? value.map(String).join(',') : String(value);
            }
        });

        if (pagination.enabled && currentPage.value > 1) {
            query[pagination.pageKey || 'page'] = String(currentPage.value);
        }

        router.replace({ query });
    };

    const syncUrlDebounced = useDebounceFn(syncUrlNow, urlSync.debounceMs);

    const syncDebouncedFiltersNow = () => {
        debouncedFilters.value = snapshot(filters.value);
    };
    const syncDebouncedFiltersDelayed = useDebounceFn(syncDebouncedFiltersNow, searchDebounceMs);

    // Snapshot précédent maintenu à la main : on ne sérialise qu'au déclenchement réel
    // du watch (et non à chaque tick réactif comme le ferait une source getter JSON).
    let previousFilters = snapshot(filters.value);

    watch(
        filters,
        (current) => {
            const newFilters = current as Record<string, unknown>;
            const oldFilters = previousFilters as Record<string, unknown>;
            const changedKeys = Object.keys(newFilters).filter((key) => {
                const oldValue = oldFilters[key];
                const newValue = newFilters[key];
                if (Array.isArray(oldValue) && Array.isArray(newValue)) {
                    return oldValue.length !== newValue.length || oldValue.some((v, i) => v !== newValue[i]);
                }
                return oldValue !== newValue;
            });

            previousFilters = snapshot(current) as T;

            if (changedKeys.length === 0) {
                return;
            }

            const shouldResetPage = changedKeys.some((key) => fieldConfig[key as keyof T]?.resetOnChange);
            if (shouldResetPage && pagination.enabled) {
                currentPage.value = 1;
            }

            const hasNonDebouncedChange = changedKeys.some((key) => !fieldConfig[key as keyof T]?.debounced);
            const hasDebouncedChange = changedKeys.some((key) => fieldConfig[key as keyof T]?.debounced);

            if (hasNonDebouncedChange) {
                syncUrlNow();
                syncDebouncedFiltersNow();
            } else if (hasDebouncedChange) {
                syncUrlDebounced();
                syncDebouncedFiltersDelayed();
            }
        },
        { deep: true },
    );

    if (pagination.enabled) {
        watch(currentPage, syncUrlNow);
    }

    syncFromUrl();
    debouncedFilters.value = snapshot(filters.value);

    const hasActiveFilters = computed(() => {
        return Object.entries(filters.value as Record<string, unknown>).some(([key, value]) =>
            isFilterActive(value, defaults[key as keyof T]),
        );
    });

    const activeFiltersCount = computed(() => {
        return Object.entries(filters.value as Record<string, unknown>).reduce((count, [key, value]) => {
            const defaultValue = defaults[key as keyof T];
            if (!isFilterActive(value, defaultValue)) {
                return count;
            }
            return count + (Array.isArray(value) ? value.length : 1);
        }, 0);
    });

    const reset = () => {
        filters.value = { ...defaults } as T;
        debouncedFilters.value = { ...defaults } as T;
        currentPage.value = 1;
    };

    const setFilter = <K extends keyof T>(key: K, value: T[K]) => {
        (filters.value as Record<string, unknown>)[key as string] = value;
    };

    const toggleArrayItem = <K extends keyof T>(key: K, item: string) => {
        const currentArray = (filters.value as Record<string, unknown>)[key as string] as string[];
        if (!Array.isArray(currentArray)) {
            return;
        }

        const index = currentArray.indexOf(item);
        if (index === -1) {
            currentArray.push(item);
        } else {
            currentArray.splice(index, 1);
        }
    };

    const removeArrayItem = <K extends keyof T>(key: K, item: string) => {
        const currentArray = (filters.value as Record<string, unknown>)[key as string] as string[];
        if (!Array.isArray(currentArray)) {
            return;
        }

        const index = currentArray.indexOf(item);
        if (index !== -1) {
            currentArray.splice(index, 1);
        }
    };

    const setPage = (page: number) => {
        currentPage.value = page;
    };

    const debouncedSetSearch = useDebounceFn((key: keyof T, value: string) => {
        setFilter(key, value as T[keyof T]);
    }, searchDebounceMs);

    return {
        filters,
        debouncedFilters,
        currentPage,
        apiFilters,
        hasActiveFilters,
        activeFiltersCount,
        reset,
        setFilter,
        toggleArrayItem,
        removeArrayItem,
        setPage,
        debouncedSetSearch,
        syncFromUrl,
    };
}

export function useBlogFilters(itemsPerPage = 6) {
    return useFilters({
        ...filterPresets.blog,
        pagination: { ...filterPresets.blog.pagination, itemsPerPage },
    });
}

export const useProjectFilters = () => useFilters(filterPresets.projects);
export const useStackFilters = () => useFilters(filterPresets.stacks);
export const useExperienceFilters = () => useFilters(filterPresets.experiences);
