import { useQuery } from '@tanstack/vue-query';
import { useDebounceFn } from '@vueuse/core';
import { computed, ref, watch } from 'vue';

import { generateSearchLink, groupSearchResults, SEARCH_DEFAULTS, SEARCH_TYPE_CONFIG } from '@/config/search';
import type { UnifiedSearchItem } from '@/services/api/modules/search';
import { searchApi, searchKeys } from '@/services/api/modules/search';

import type { SearchResult, SearchResultGroup, SearchResultType, UseGlobalSearchOptions } from '@/types/config/search';

export type { SearchMode, SearchResult, SearchResultType } from '@/types/config/search';

export function useGlobalSearch(options: UseGlobalSearchOptions = {}) {
    const { mode = 'public' } = options;

    const searchQuery = ref('');
    const isOpen = ref(false);
    const selectedIndex = ref(-1);
    const debouncedQuery = ref('');

    const updateDebouncedQuery = useDebounceFn((value: string) => {
        debouncedQuery.value = value;
    }, SEARCH_DEFAULTS.DEBOUNCE_MS);

    watch(searchQuery, (value) => {
        updateDebouncedQuery(value);
        if (value.length >= SEARCH_DEFAULTS.MIN_QUERY_LENGTH) {
            isOpen.value = true;
        }
    });

    const queryParams = computed(() => ({
        q: debouncedQuery.value.trim(),
        limit: SEARCH_DEFAULTS.PAGE_SIZE * 4,
    }));

    const {
        data: searchData,
        isLoading,
        error: queryError,
    } = useQuery({
        queryKey: computed(() => searchKeys.unified(queryParams.value)),
        queryFn: async (): Promise<SearchResult[]> => {
            const params = queryParams.value;
            if (params.q.length < SEARCH_DEFAULTS.MIN_QUERY_LENGTH) {
                return [];
            }
            const response = await searchApi.query(params);
            return (response.data ?? []).map(mapToUiResult(mode));
        },
        enabled: computed(() => queryParams.value.q.length >= SEARCH_DEFAULTS.MIN_QUERY_LENGTH),
        staleTime: SEARCH_DEFAULTS.STALE_TIME_MS,
    });

    const searchError = computed<string | null>(() => (queryError.value ? 'Erreur lors de la recherche' : null));

    const searchResults = computed(() => searchData.value ?? []);
    const groupedResults = computed<SearchResultGroup[]>(() => groupSearchResults(searchResults.value));

    const flatResults = computed(() => groupedResults.value.flatMap((g) => g.results));
    const hasResults = computed(() => flatResults.value.length > 0);
    const totalResults = computed(() => flatResults.value.length);
    const hasError = computed(() => !!searchError.value || !!queryError.value);

    const clear = () => {
        searchQuery.value = '';
        debouncedQuery.value = '';
        isOpen.value = false;
        selectedIndex.value = -1;
    };

    const close = () => {
        isOpen.value = false;
        selectedIndex.value = -1;
    };

    const open = () => {
        if (searchQuery.value.length >= SEARCH_DEFAULTS.MIN_QUERY_LENGTH) {
            isOpen.value = true;
        }
    };

    const navigateUp = () => {
        if (selectedIndex.value > 0) {
            selectedIndex.value--;
        } else {
            selectedIndex.value = flatResults.value.length - 1;
        }
    };

    const navigateDown = () => {
        if (selectedIndex.value < flatResults.value.length - 1) {
            selectedIndex.value++;
        } else {
            selectedIndex.value = 0;
        }
    };

    const getSelectedResult = (): SearchResult | null => {
        if (selectedIndex.value >= 0 && selectedIndex.value < flatResults.value.length) {
            return flatResults.value[selectedIndex.value] ?? null;
        }
        return null;
    };

    return {
        searchQuery,
        isOpen,
        isLoading,
        selectedIndex,
        groupedResults,
        flatResults,
        hasResults,
        totalResults,
        hasError,
        searchError,
        clear,
        close,
        open,
        navigateUp,
        navigateDown,
        getSelectedResult,
        TYPE_CONFIG: SEARCH_TYPE_CONFIG,
    };
}

function mapToUiResult(mode: 'public' | 'admin') {
    return (item: UnifiedSearchItem): SearchResult => {
        const type = item.type as SearchResultType;
        return {
            id: item.id,
            type,
            title: item.title,
            subtitle: extractSubtitle(type, item),
            slug: item.slug,
            icon: SEARCH_TYPE_CONFIG[type].icon,
            link: generateSearchLink(type, item.id, item.slug, mode),
        };
    };
}

function extractSubtitle(type: SearchResultType, item: UnifiedSearchItem): string | undefined {
    const meta = item.metadata ?? {};
    if (type === 'experience') {
        return (meta.company as string | undefined) ?? undefined;
    }
    return (meta.category as string | undefined) ?? undefined;
}
