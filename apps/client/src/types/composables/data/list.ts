import type { PaginationMeta, UsePaginationReturn } from './pagination';
import type { UseSearchReturn } from './search';
import type {
    BulkDeleteResult,
    UseBulkDeleteConfirmationReturn,
    UseDeleteConfirmationReturn,
    UseSelectionReturn,
} from './selection';
import type { UseSortingReturn } from './sorting';
import type { DjangoPaginatedResponse as PaginatedResponse } from '@/types/api/common';
import type { ComputedRef, Ref } from 'vue';

// useDataList

export interface ListParams<TFilters = Record<string, unknown>> {
    page: number;
    pageSize: number;
    ordering: string;
    search?: string;
    filters?: TFilters;
}

export interface UseDataListOptions<T, TFilters extends Record<string, unknown> = Record<string, unknown>> {
    // Vue Query configuration
    queryKey: string[];
    queryFn: (params: ListParams<TFilters>) => Promise<PaginatedResponse<T>>;

    // Configuration
    defaultSort?: string;
    defaultSortOrder?: 'asc' | 'desc';
    defaultPerPage?: number;
    searchDebounceMs?: number;
    staleTime?: number;

    // Map frontend sort keys to backend field names (e.g. { views: 'view_count' })
    sortFieldMap?: Record<string, string>;

    // Filtres additionnels (optionnel)
    filters?: Ref<TFilters> | ComputedRef<TFilters>;

    // Delete mutation (optionnel)
    deleteFn?: (item: T) => Promise<void>;
    onDeleteSuccess?: () => void;
    onDeleteError?: (error: Error) => void;

    // Bulk delete (optionnel - utilise deleteFn par défaut)
    onBulkDeleteSuccess?: (result: BulkDeleteResult) => void;
    onBulkDeleteError?: (error: Error) => void;
}

export interface UseDataListReturn<T extends { id: number | string }> {
    // Vue Query state
    items: ComputedRef<T[]>;
    isLoading: Ref<boolean>;
    isError: Ref<boolean>;
    error: Ref<Error | null>;
    isEmpty: ComputedRef<boolean>;
    isFetching: Ref<boolean>;

    // Pagination normalisée
    paginationMeta: ComputedRef<PaginationMeta>;

    // Pagination controls
    pagination: UsePaginationReturn;

    // Sorting
    sorting: UseSortingReturn;

    // Search
    search: UseSearchReturn;

    // Selection (pour actions bulk)
    selection: UseSelectionReturn<T>;

    // Actions
    refresh: () => void;
    refetch: () => Promise<unknown>;

    // Event handlers (ready to bind to DataTable or similar list components)
    handlers: DataListHandlers;

    // Delete (si deleteFn fourni)
    deletion?: UseDeleteConfirmationReturn<T>;

    // Bulk delete (si deleteFn fourni)
    bulkDeletion?: UseBulkDeleteConfirmationReturn<T>;
}

export interface DataListHandlers {
    sort: (key: string, order: 'asc' | 'desc') => void;
    queryChange: (payload: { search?: string; filters?: Record<string, string> }) => void;
    paginationChange: (payload: { page?: number; perPage?: number }) => void;
}

// useInfiniteScroll

export interface UseInfiniteScrollOptions {
    threshold?: number;
    rootMargin?: string;
    enabled?: Ref<boolean>;
}

// useDeferredMatch | resolves raw values against async-loaded items

export interface UseDeferredMatchOptions<TItem, TRaw = unknown> {
    /** Reactive source of loaded items (e.g. categories, tags from API) */
    source: Ref<TItem[]> | ComputedRef<TItem[]>;

    /** Getter for the raw value stored before items were loaded */
    getRawValue: () => TRaw | undefined;

    /** Returns true when the form field has not been matched yet */
    isUnmatched: () => boolean;

    /** Match raw value against loaded items, return the resolved value or undefined if no match */
    match: (items: TItem[], rawValue: TRaw) => unknown;

    /** Set the matched value on the form field */
    setFieldValue: (value: unknown) => void;
}
