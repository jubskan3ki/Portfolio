import { computed, ref, toValue, watch } from 'vue';

import { PAGINATION } from '@/config/constants';

import type { UsePaginationOptions, UsePaginationReturn } from '@/types/composables';

const DEFAULT_PAGE = 1;

export function usePagination(options: UsePaginationOptions = {}): UsePaginationReturn {
    const {
        defaultPage = DEFAULT_PAGE,
        defaultPerPage = PAGINATION.DEFAULT_PAGE_SIZE,
        totalItems: externalTotalItems,
        onPageChange,
        onPerPageChange,
    } = options;

    const currentPage = ref(defaultPage);
    const perPage = ref(defaultPerPage);
    const totalItems = ref(0);

    if (externalTotalItems) {
        watch(
            () => toValue(externalTotalItems),
            (newTotal) => {
                totalItems.value = newTotal;
                const maxPage = Math.ceil(newTotal / perPage.value) || 1;
                if (currentPage.value > maxPage) {
                    currentPage.value = maxPage;
                }
            },
            { immediate: true },
        );
    }

    const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)));
    const offset = computed(() => (currentPage.value - 1) * perPage.value);
    const hasNextPage = computed(() => currentPage.value < totalPages.value);
    const hasPrevPage = computed(() => currentPage.value > 1);

    const setPage = (page: number) => {
        const newPage = Math.max(1, Math.min(page, totalPages.value));
        if (newPage !== currentPage.value) {
            currentPage.value = newPage;
            onPageChange?.(newPage);
        }
    };

    const setPerPage = (newPerPage: number) => {
        if (newPerPage > 0 && newPerPage !== perPage.value) {
            perPage.value = newPerPage;
            currentPage.value = 1;
            onPerPageChange?.(newPerPage);
        }
    };

    const nextPage = () => {
        if (hasNextPage.value) {
            setPage(currentPage.value + 1);
        }
    };

    const prevPage = () => {
        if (hasPrevPage.value) {
            setPage(currentPage.value - 1);
        }
    };

    const reset = () => {
        currentPage.value = defaultPage;
        perPage.value = defaultPerPage;
    };

    return {
        currentPage,
        perPage,
        totalItems,
        totalPages,
        offset,
        hasNextPage,
        hasPrevPage,
        setPage,
        setPerPage,
        nextPage,
        prevPage,
        reset,
    };
}
