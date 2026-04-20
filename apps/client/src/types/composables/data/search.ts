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

// useSearchHistory

// Minimal shape stored for history items — keeps localStorage footprint low
// and decouples persistence from API schema drift.
export interface HistoryItem {
    id: number | string;
    type: string;
    title: string;
    subtitle?: string;
    icon: string;
    link: string;
}

export type RecordableItem = HistoryItem;

// useSearchActions

export interface SearchAction {
    id: string;
    title: string;
    subtitle?: string;
    icon: string;
    // Either a navigation target or an imperative action — never both
    link?: string;
    external?: boolean;
    run?: () => void | Promise<void>;
}
