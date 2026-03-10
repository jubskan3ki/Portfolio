import type { ComputedRef, Ref } from 'vue';

// Pagination metadata from normalized response

export interface PaginationMeta {
    page: number;
    pageSize: number;
    totalCount: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
}

// usePagination

export interface UsePaginationOptions {
    defaultPage?: number;
    defaultPerPage?: number;
    totalItems?: Ref<number> | ComputedRef<number>;
    onPageChange?: (page: number) => void;
    onPerPageChange?: (perPage: number) => void;
}

export interface UsePaginationReturn {
    currentPage: Ref<number>;
    perPage: Ref<number>;
    totalItems: Ref<number>;
    totalPages: ComputedRef<number>;
    offset: ComputedRef<number>;
    hasNextPage: ComputedRef<boolean>;
    hasPrevPage: ComputedRef<boolean>;
    setPage: (page: number) => void;
    setPerPage: (perPage: number) => void;
    nextPage: () => void;
    prevPage: () => void;
    reset: () => void;
}
