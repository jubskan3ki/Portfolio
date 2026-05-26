import { useDebounceFn } from '@vueuse/core';
import { computed, ref, watch } from 'vue';

import type { UseSearchOptions, UseSearchReturn } from '@/types/composables';

const DEFAULT_DEBOUNCE_MS = 300;
const DEFAULT_MIN_LENGTH = 0;

export function useSearch(options: UseSearchOptions = {}): UseSearchReturn {
    const { debounceMs = DEFAULT_DEBOUNCE_MS, minLength = DEFAULT_MIN_LENGTH, onSearch } = options;

    const query = ref('');
    const debouncedQuery = ref('');

    const isSearching = computed(() => {
        return query.value.length >= minLength && query.value !== debouncedQuery.value;
    });

    const updateDebouncedQuery = useDebounceFn((value: string) => {
        debouncedQuery.value = value;
        onSearch?.(value);
    }, debounceMs);

    watch(query, (newQuery) => {
        if (newQuery.length >= minLength || newQuery === '') {
            updateDebouncedQuery(newQuery);
        }
    });

    const setSearch = (newQuery: string) => {
        query.value = newQuery;
    };

    const clear = () => {
        query.value = '';
        debouncedQuery.value = '';
        onSearch?.('');
    };

    return {
        query,
        debouncedQuery,
        isSearching,
        setSearch,
        clear,
    };
}
