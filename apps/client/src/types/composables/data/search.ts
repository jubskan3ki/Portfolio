import type { ComputedRef, Ref } from 'vue';

// useSearch

export interface UseSearchOptions {
    debounceMs?: number;
    minLength?: number;
    onSearch?: (query: string) => void;
}

export interface UseSearchReturn {
    query: Ref<string>;
    debouncedQuery: Ref<string>;
    isSearching: ComputedRef<boolean>;
    setSearch: (query: string) => void;
    clear: () => void;
}
