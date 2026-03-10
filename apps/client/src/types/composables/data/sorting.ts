import type { ComputedRef, Ref } from 'vue';

// useSorting

export interface UseSortingOptions {
    defaultSortBy?: string;
    defaultSortOrder?: 'asc' | 'desc';
    onSort?: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
}

export interface UseSortingReturn {
    sortBy: Ref<string>;
    sortOrder: Ref<'asc' | 'desc'>;
    orderingParam: ComputedRef<string>;
    setSort: (key: string, order?: 'asc' | 'desc') => void;
    toggleSort: (key: string) => void;
    reset: () => void;
}
