import { useQuery, useQueryClient } from '@tanstack/vue-query';
import { computed, watch, toValue } from 'vue';

import { PAGINATION, TIMEOUTS } from '@/config/constants';
import { CACHE_TIMES } from '@/services/api/core/cache';
import { normalizePaginatedResponse } from '@/services/utils/responseNormalizer';

import { useBulkDelete } from './useBulkDelete';
import { usePagination } from './usePagination';
import { useSearch } from './useSearch';
import { useSelection } from './useSelection';
import { useSorting } from './useSorting';

import type { UseDataListOptions, UseDataListReturn, ListParams } from '@/types/composables';

export function useDataList<
    T extends { id: number | string },
    TFilters extends Record<string, unknown> = Record<string, unknown>,
>(options: UseDataListOptions<T, TFilters>): UseDataListReturn<T> {
    const {
        queryKey,
        queryFn,
        defaultSort = 'created_at',
        defaultSortOrder = 'desc',
        defaultPerPage = PAGINATION.DEFAULT_PAGE_SIZE,
        searchDebounceMs = TIMEOUTS.SEARCH_DEBOUNCE,
        staleTime = CACHE_TIMES.DETAIL,
        sortFieldMap,
        filters: externalFilters,
        deleteFn,
        onDeleteSuccess,
        onDeleteError,
        onBulkDeleteSuccess,
        onBulkDeleteError,
    } = options;

    const queryClient = useQueryClient();

    const pagination = usePagination({ defaultPerPage });
    const sorting = useSorting({ defaultSortBy: defaultSort, defaultSortOrder });
    const search = useSearch({ debounceMs: searchDebounceMs });

    const queryParams = computed<ListParams<TFilters>>(() => ({
        page: pagination.currentPage.value,
        pageSize: pagination.perPage.value,
        ordering: sorting.orderingParam.value,
        search: search.debouncedQuery.value || undefined,
        filters: externalFilters ? toValue(externalFilters) : undefined,
    }));

    const reactiveQueryKey = computed(
        () =>
            [
                ...queryKey,
                pagination.currentPage.value,
                pagination.perPage.value,
                sorting.orderingParam.value,
                search.debouncedQuery.value,
            ] as const,
    );

    const query = useQuery({
        queryKey: reactiveQueryKey,
        queryFn: () => queryFn(queryParams.value),
        placeholderData: (previousData) => previousData,
        staleTime,
    });

    const normalizedData = computed(() => {
        const response = query.data.value;
        return normalizePaginatedResponse<T>(response, pagination.perPage.value);
    });

    const items = computed<T[]>(() => normalizedData.value.data);

    watch(
        () => normalizedData.value.pagination.totalCount,
        (count) => {
            pagination.totalItems.value = count;
        },
        { immediate: true },
    );

    const selection = useSelection<T>({ items });

    watch(
        () => search.debouncedQuery.value,
        () => {
            pagination.setPage(1);
        },
    );

    watch([() => sorting.sortBy.value, () => sorting.sortOrder.value], () => {
        pagination.setPage(1);
    });

    const { isLoading, isFetching, isError, error } = query;
    const isEmpty = computed(() => !isLoading.value && items.value.length === 0);

    const refresh = () => {
        queryClient.invalidateQueries({ queryKey });
    };

    const refetch = () => query.refetch();

    const { deletion, bulkDeletion } = deleteFn
        ? useBulkDelete<T>({
            deleteFn,
            onRefresh: refresh,
            onDeleteSuccess,
            onDeleteError,
            onBulkDeleteSuccess,
            onBulkDeleteError,
        })
        : { deletion: undefined, bulkDeletion: undefined };

    watch(items, () => {
        selection.deselectAll();
    });

    const handlers = {
        sort(key: string, order: 'asc' | 'desc') {
            const backendField = sortFieldMap?.[key] ?? key;
            sorting.setSort(backendField, order);
        },
        queryChange(payload: { search?: string; filters?: Record<string, string> }) {
            if (payload.search !== undefined) {
                search.setSearch(payload.search);
            }
        },
        paginationChange(payload: { page?: number; perPage?: number }) {
            if (payload.page !== undefined) {
                pagination.setPage(payload.page);
            }
            if (payload.perPage !== undefined) {
                pagination.setPerPage(payload.perPage);
            }
        },
    };

    return {
        items,
        isLoading,
        isFetching,
        isError,
        error,
        isEmpty,
        paginationMeta: computed(() => normalizedData.value.pagination),
        pagination,
        sorting,
        search,
        selection,
        refresh,
        refetch,
        handlers,
        deletion,
        bulkDeletion,
    };
}
