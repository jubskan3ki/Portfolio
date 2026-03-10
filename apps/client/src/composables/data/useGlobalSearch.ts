import { useQuery } from '@tanstack/vue-query';
import { useDebounceFn } from '@vueuse/core';
import { ref, computed, watch } from 'vue';

import {
    SEARCH_TYPE_CONFIG,
    SEARCH_DEFAULTS,
    SEARCH_SOURCES,
    generateSearchLink,
    groupSearchResults,
} from '@/config/search';
import { articlesApi } from '@/services/api/modules/articles';
import { experiencesApi } from '@/services/api/modules/experiences';
import { projectsApi } from '@/services/api/modules/projects';
import { stacksApi } from '@/services/api/modules/stacks';
import { extractPaginatedData } from '@/services/utils/pagination';

import type { SearchResult, SearchResultGroup, UseGlobalSearchOptions } from '@/types/config/search';

const searchFetchers: Record<string, (params: Record<string, unknown>) => Promise<unknown>> = {
    articles: (params) => articlesApi.getAdminList(params),
    projects: (params) => projectsApi.getAdminList(params),
    stacks: (params) => stacksApi.getAdminList(params),
    experiences: (params) => experiencesApi.getAdminList(params),
};

export type { SearchResult, SearchMode, SearchResultType } from '@/types/config/search';

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

    interface SearchQueryResult {
        results: SearchResult[];
        failedSources: string[];
    }

    const {
        data: searchData,
        isLoading,
        error: queryError,
    } = useQuery({
        queryKey: computed(() => ['global-search', debouncedQuery.value]),
        queryFn: async (): Promise<SearchQueryResult> => {
            const query = debouncedQuery.value.trim();
            if (query.length < SEARCH_DEFAULTS.MIN_QUERY_LENGTH) {
                return { results: [], failedSources: [] };
            }

            const searchParams = { search: query, page_size: SEARCH_DEFAULTS.PAGE_SIZE };

            const settled = await Promise.allSettled(
                SEARCH_SOURCES.map((source) => {
                    const fetcher = searchFetchers[source.key];
                    return fetcher ? fetcher(searchParams) : Promise.reject(new Error(`No fetcher for ${source.key}`));
                }),
            );

            const failedSources: string[] = [];
            const results: SearchResult[] = [];

            settled.forEach((result, index) => {
                const source = SEARCH_SOURCES[index];
                if (!source) {
                    return;
                }
                if (result.status === 'rejected') {
                    failedSources.push(source.key);
                    return;
                }

                const items = extractPaginatedData<Record<string, unknown>>(result.value);
                for (const item of items) {
                    const mapped = source.mapItem(item);
                    results.push({
                        id: item.id as number,
                        type: source.type,
                        icon: SEARCH_TYPE_CONFIG[source.type].icon,
                        link: generateSearchLink(source.type, item.id as number, mapped.slug, mode),
                        ...mapped,
                    });
                }
            });

            return { results, failedSources };
        },
        enabled: computed(() => debouncedQuery.value.length >= SEARCH_DEFAULTS.MIN_QUERY_LENGTH),
        staleTime: SEARCH_DEFAULTS.STALE_TIME_MS,
    });

    const searchError = computed<string | null>(() => {
        const failed = searchData.value?.failedSources ?? [];
        if (failed.length === 0) {
            return null;
        }
        if (failed.length === 4) {
            return 'Erreur lors de la recherche';
        }
        return `Recherche partielle (${failed.join(', ')} indisponible)`;
    });

    const searchResults = computed(() => searchData.value?.results ?? []);
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
