<template>
    <div class="blog-page">
        <Hero
            title="Blog"
            description="Articles, tutoriels et réflexions sur le développement web et les technologies modernes."
            badge="Articles"
            variant="secondary"
        >
            <template #stats>
                <StatCard
                    v-for="stat in heroStats"
                    :key="stat.label"
                    :value="stat.value"
                    :label="stat.label"
                    :icon="stat.icon"
                    variant="secondary"
                />
            </template>
        </Hero>

        <Main id="articles" variant="light" size="large">
            <div class="blog-layout">
                <div class="blog-main">
                    <div class="search-bar">
                        <div class="search-bar__input-wrapper">
                            <SearchInput
                                v-model="searchQuery"
                                placeholder="Rechercher un article..."
                                shortcut="B"
                                @clear="clearSearch"
                            />
                        </div>

                        <div class="search-bar__actions">
                            <BaseSelect
                                v-model="currentSort"
                                :options="sortOptions"
                                placeholder="Trier par"
                                aria-label="Trier les articles"
                            />
                        </div>
                    </div>

                    <div class="blog-transition">
                        <div v-if="isLoading" class="blog-loader">
                            <LazySkeletonList
                                :count="6"
                                variant="article"
                                layout="grid"
                                :columns="2"
                                show-image
                                show-description
                                show-footer
                            />
                        </div>

                        <LazyEmptyState
                            v-else-if="hasError"
                            icon="alert-circle"
                            title="Erreur de chargement"
                            description="Impossible de charger les articles. Veuillez réessayer."
                            size="lg"
                            custom-class="blog-empty-state"
                        >
                            <template #action>
                                <LazyBaseButton
                                    label="Réessayer"
                                    icon="refresh-cw"
                                    variant="primary"
                                    @click="handleRetry"
                                />
                            </template>
                        </LazyEmptyState>

                        <LazyEmptyState
                            v-else-if="!hasArticles"
                            icon="file-text"
                            :title="emptyStateTitle"
                            :description="emptyStateDescription"
                            size="lg"
                            custom-class="blog-empty-state"
                        >
                            <template v-if="hasActiveFilters" #action>
                                <LazyBaseButton
                                    label="Réinitialiser les filtres"
                                    icon="x"
                                    variant="secondary"
                                    @click="resetFilters"
                                />
                            </template>
                        </LazyEmptyState>

                        <div v-else class="blog-content">
                            <div
                                class="articles-grid"
                                :class="{ 'articles-grid--fetching': isFilterFetching }"
                                @mouseover.passive="handleCardHover"
                                @mouseout.passive="handleCardLeave"
                                @focusin="handleCardHover"
                                @focusout="handleCardLeave"
                            >
                                <ArticleCard
                                    v-for="(article, index) in articles"
                                    :key="article.id"
                                    :article="article"
                                    :eager="index < 2"
                                    class="articles-grid__item"
                                    :style="{ '--article-index': prefersReducedMotion ? 0 : index }"
                                />
                            </div>

                            <LazyPagination
                                v-if="totalPages > 1"
                                :current-page="currentPage"
                                :total-pages="totalPages"
                                class="blog-pagination"
                                @update:current-page="handlePageChange"
                            />
                        </div>
                    </div>
                </div>

                <LazyBlogSidebar
                    v-model:selected-category="selectedCategory"
                    v-model:selected-tags="selectedTags"
                    :popular-articles="popularArticles"
                    :categories="categories ?? []"
                    :tags="tags ?? []"
                    :total-articles="totalArticles"
                />
            </div>
        </Main>

        <LazyCTA
            title="Découvrez mes projets"
            description="Explorez mes réalisations et les stacks que j'utilise."
            variant="secondary"
            :primary-button="{ label: 'Voir les projets', to: ROUTES.PROJECTS.path, icon: 'briefcase' }"
            :secondary-button="{ label: 'Mon parcours', to: ROUTES.EXPERIENCE.path }"
        />
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
    import { computed, unref, watch } from 'vue';

    import BaseSelect from '@/components/base/BaseSelect.vue';
    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    import StatCard from '@/components/feature/home/StatCard.vue';
    import Main from '@/components/layouts/Main.vue';
    import Hero from '@/components/ui/Hero.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useFilters } from '@/composables/data/useFilters';
    import { useItemListSeo } from '@/composables/seo/useItemListSeo';
    import { usePaginationSeo } from '@/composables/seo/usePaginationSeo';
    import { useBlogSeo } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import {
        articleKeys,
        articlesApi,
        useArticles,
        useArticleCategories,
        useArticleTags,
        usePopularArticles,
    } from '@/services/api/modules/articles';

    import type { SelectOption } from '@/types/components/base';

    useBlogSeo();

    const { announceLoaded } = useAnnounce();
    const { prefersReducedMotion } = useReducedMotion();
    const { scrollToTop } = useScrollToTop();

    const { filters, apiFilters, currentPage, hasActiveFilters, reset, setFilter, setPage } = useFilters({
        ...filterPresets.blog,
        pagination: { ...filterPresets.blog.pagination, itemsPerPage: 6 },
    });

    // SSR-prefetch above-fold : articles + categories + tags ; `popular` est lazy (BlogSidebar) donc hors du path SSR bloquant.
    const queryClient = useQueryClient();
    await useAsyncData(
        'blog-prefetch',
        async () => {
            const initialTagsFilters = {
                category: filters.value.category || undefined,
                search: filters.value.search || undefined,
            };
            await Promise.all([
                queryClient.prefetchQuery({
                    queryKey: articleKeys.list(unref(apiFilters)),
                    queryFn: () => articlesApi.getAll(unref(apiFilters)),
                }),
                queryClient.prefetchQuery({
                    queryKey: articleKeys.categories(),
                    queryFn: articlesApi.getCategories,
                }),
                queryClient.prefetchQuery({
                    queryKey: articleKeys.tags(initialTagsFilters),
                    queryFn: () => articlesApi.getTags(initialTagsFilters),
                }),
            ]);
            return true;
        },
        {
            getCachedData: (key, nuxtApp) =>
                (nuxtApp.payload.data[key] as boolean | undefined)
                ?? (nuxtApp.static.data[key] as boolean | undefined),
        },
    );

    const searchQuery = computed({
        get: () => filters.value.search,
        set: (val: string) => setFilter('search', val),
    });
    const selectedCategory = computed({
        get: () => filters.value.category || null,
        set: (val: string | number | null) => setFilter('category', String(val ?? '')),
    });
    const selectedTags = computed({
        get: () => filters.value.tags,
        set: (val: Array<string | number>) => setFilter('tags', val.map(String)),
    });
    const currentSort = computed({
        get: () => filters.value.ordering,
        set: (val: string) => setFilter('ordering', val),
    });

    const sortOptions: SelectOption[] = [
        { value: '-date', label: 'Plus récents' },
        { value: 'date', label: 'Plus anciens' },
        { value: '-views', label: 'Plus populaires' },
        { value: 'title', label: 'A → Z' },
    ];

    // Filtré par category+search mais pas par tags : sinon on ne pourrait plus désélectionner un tag actif.
    const tagsFilters = computed(() => ({
        category: filters.value.category || undefined,
        search: filters.value.search || undefined,
    }));

    const {
        data: articlesData,
        isLoading,
        isFetching,
        isError: hasError,
        refetch: refetchArticles,
    } = useArticles(apiFilters);
    const { data: categories } = useArticleCategories();
    const { data: tags } = useArticleTags(tagsFilters);
    const { data: popularArticlesData } = usePopularArticles(5);

    const articles = computed(() => articlesData.value?.data ?? []);
    const totalArticles = computed(() => articlesData.value?.pagination?.total ?? 0);
    const totalPages = computed(() => articlesData.value?.pagination?.totalPages ?? 1);
    const popularArticles = computed(() => popularArticlesData.value ?? []);

    usePaginationSeo({ basePath: '/blog', currentPage, totalPages });

    // Schema.org ItemList (SSR-only) : pas de watch, les filtres client ne changent pas l'URL canonique.
    const articleListItems = computed(() =>
        articles.value.map((a) => ({ name: a.title, url: `/blog/${a.slug}`, image: a.image })),
    );
    useItemListSeo({ items: articleListItems });
    const hasArticles = computed(() => (articles.value?.length ?? 0) > 0);
    const isFilterFetching = computed(() => isFetching.value && hasArticles.value && !isLoading.value);

    const heroStats = computed(() => [
        { value: totalArticles.value, label: 'Articles', icon: 'file-text' },
        { value: categories.value?.length ?? 0, label: 'Catégories', icon: 'folder' },
        { value: tags.value?.length ?? 0, label: 'Tags', icon: 'hash' },
    ]);

    const emptyStateTitle = computed(() =>
        hasActiveFilters.value ? 'Aucun article trouvé' : 'Aucun article disponible',
    );

    const emptyStateDescription = computed(() =>
        hasActiveFilters.value
            ? 'Essayez de modifier vos critères de recherche.'
            : 'Les articles seront ajoutés prochainement.',
    );

    const clearSearch = () => {
        setFilter('search', '');
    };

    const resetFilters = () => {
        reset();
    };

    const handleRetry = () => {
        refetchArticles();
    };

    const handlePageChange = (page: number) => {
        setPage(page);
        scrollToTop('smooth');
    };

    // Prefetch délégué : 1 listener partagé pour les 6 cartes ; délai 120ms pour ne pas fetch en survol de traversée.
    const PREFETCH_HOVER_DELAY = 120;
    const prefetchedSlugs = new Set<string>();
    const prefetchTimers = new Map<string, ReturnType<typeof setTimeout>>();

    const handleCardHover = (event: MouseEvent | FocusEvent) => {
        const card = (event.target as HTMLElement | null)?.closest<HTMLElement>('[data-slug]');
        const slug = card?.dataset.slug;
        if (!slug || prefetchedSlugs.has(slug) || prefetchTimers.has(slug)) {
            return;
        }
        const timer = setTimeout(() => {
            prefetchTimers.delete(slug);
            prefetchedSlugs.add(slug);
            queryClient.prefetchQuery({
                queryKey: articleKeys.detail(slug),
                queryFn: () => articlesApi.getBySlug(slug),
            });
        }, PREFETCH_HOVER_DELAY);
        prefetchTimers.set(slug, timer);
    };

    const handleCardLeave = (event: MouseEvent | FocusEvent) => {
        const card = (event.target as HTMLElement | null)?.closest<HTMLElement>('[data-slug]');
        const slug = card?.dataset.slug;
        if (!slug) {
            return;
        }
        const timer = prefetchTimers.get(slug);
        if (timer) {
            clearTimeout(timer);
            prefetchTimers.delete(slug);
        }
    };

    watch(
        articles,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('articles', list.length);
            }
        },
        { once: true },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .blog-page {
        min-height: 100vh;
    }

    .blog-layout {
        display: grid;
        grid-template-columns: 1fr 380px;
        gap: vars.$spacing-xl;
        max-width: 1400px;
        margin: 0 auto;

        @include mix.responsive(desktop) {
            grid-template-columns: 1fr 340px;
            gap: vars.$spacing-lg;
        }

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }
    }

    .blog-main {
        min-width: 0;
    }

    $blog-card-row: 560px;
    $blog-card-row-mobile: 480px;

    .blog-transition {
        position: relative;
        contain: layout;
        min-height: calc(#{$blog-card-row} * 3 + #{vars.$spacing-lg} * 2);

        @include mix.responsive(mobile) {
            min-height: calc(#{$blog-card-row-mobile} * 6 + #{vars.$spacing-md} * 5);
        }
    }

    .search-bar {
        position: relative;
        z-index: vars.$z-index-dropdown;
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        margin-bottom: vars.$spacing-lg;
        padding: vars.$spacing-md;
        background: fn.color-alpha(vars.$white, 0.97);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.3);
        border-radius: vars.$border-radius-xl;
        box-shadow: 0 2px 8px fn.color-alpha(vars.$black, 0.03);

        @include mix.responsive(mobile) {
            flex-direction: column;
            align-items: stretch;
        }

        &__input-wrapper {
            flex: 1;
        }

        &__actions {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            flex-shrink: 0;

            @include mix.responsive(mobile) {
                width: 100%;
            }
        }
    }

    .blog-loader {
        max-width: 100%;
        contain: layout paint;
    }

    .blog-content {
        animation: blogFadeIn 0.3s ease-out;
    }

    :deep(.blog-empty-state) {
        max-width: 500px;
        margin: vars.$spacing-xl auto;
        padding: vars.$spacing-xxl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.06);
    }

    .articles-grid,
    .blog-loader :deep(.skeleton-list--grid) {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-lg;
        contain: layout;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
            gap: vars.$spacing-md;
        }
    }

    .articles-grid {
        &--fetching {
            opacity: 0.55;
            pointer-events: none;
        }

        &__item {
            opacity: 0;
            will-change: opacity;
            animation: blogFadeIn 0.3s ease-out forwards;
            animation-delay: calc(min(var(--article-index, 0), 2) * 40ms);
            // Pas de `paint` : sinon le hover shadow est coupé.
            contain: layout;
            // Pas de content-visibility ici : l'estimation ne matchait pas la hauteur réelle et causait du CLS.
        }
    }

    .blog-pagination {
        margin-top: vars.$spacing-xl;
        padding-top: vars.$spacing-xl;
        border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
        content-visibility: auto;
        contain-intrinsic-size: auto 80px;
    }

    @keyframes blogFadeIn {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .articles-grid__item {
            animation: none;
            opacity: 1;
        }

        .blog-content {
            animation: none;
        }
    }

    @include mix.responsive(tablet) {
        .search-bar {
            margin-bottom: vars.$spacing-md;
        }
    }
</style>
