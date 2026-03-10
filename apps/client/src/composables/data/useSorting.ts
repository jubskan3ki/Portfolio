import { ref, computed } from 'vue';

import type { UseSortingOptions, UseSortingReturn } from '@/types/composables';

const DEFAULT_SORT_BY = 'created_at';
const DEFAULT_SORT_ORDER = 'desc' as const;

export function useSorting(options: UseSortingOptions = {}): UseSortingReturn {
    const { defaultSortBy = DEFAULT_SORT_BY, defaultSortOrder = DEFAULT_SORT_ORDER, onSort } = options;

    const sortBy = ref(defaultSortBy);
    const sortOrder = ref<'asc' | 'desc'>(defaultSortOrder);

    const orderingParam = computed(() => {
        return sortOrder.value === 'desc' ? `-${sortBy.value}` : sortBy.value;
    });

    const setSort = (key: string, order?: 'asc' | 'desc') => {
        sortBy.value = key;
        if (order) {
            sortOrder.value = order;
        }
        onSort?.(sortBy.value, sortOrder.value);
    };

    const toggleSort = (key: string) => {
        if (sortBy.value === key) {
            sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
        } else {
            sortBy.value = key;
            sortOrder.value = 'desc';
        }
        onSort?.(sortBy.value, sortOrder.value);
    };

    const reset = () => {
        sortBy.value = defaultSortBy;
        sortOrder.value = defaultSortOrder;
    };

    return {
        sortBy,
        sortOrder,
        orderingParam,
        setSort,
        toggleSort,
        reset,
    };
}
