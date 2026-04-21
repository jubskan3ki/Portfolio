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
                        <Transition name="slide-fade">
                            <div v-if="isLoading" key="loader" class="blog-loader">
                                <SkeletonList
                                    :count="6"
                                    variant="article"
                                    layout="grid"
                                    :columns="2"
                                    show-image
                                    show-description
                                />
                            </div>

                            <LazyEmptyState
                                v-else-if="hasError"
                                key="error"
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
                                key="empty"
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
                                <div class="articles-grid" :class="{ 'articles-grid--fetching': isFilterFetching }">
                                    <ArticleCard
                                        v-for="(article, index) in articles"
                                        :key="article.id"
                                        :article="article"
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
                        </Transition>
                    </div>
                </div>

                <aside class="blog-sidebar">
                    <div class="blog-sidebar__slot blog-sidebar__slot--popular">
                        <LazyArticlePopular :articles="popularArticles" title="Articles populaires" show-title />
                    </div>

                    <div v-if="categories?.length" class="blog-sidebar__slot blog-sidebar__slot--categories">
                        <LazyArticleCategories
                            v-model="selectedCategory"
                            :categories="categoriesWithAll"
                            :max-visible="8"
                            title="Catégories"
                        />
                    </div>

                    <div v-if="tags?.length" class="blog-sidebar__slot blog-sidebar__slot--tags">
                        <LazyArticleTags
                            v-model="selectedTags"
                            :tags="tags"
                            :max-visible="10"
                            title="Tags"
                            show-title
                            display="cloud"
                            multi-select
                        />
                    </div>
                </aside>
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
    import SkeletonList from '@/components/loaders/SkeletonList.vue';
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

    // SSR-prefetch the data so the skeleton never shows on first paint (kills CLS).
    const queryClient = useQueryClient();
    await useAsyncData('blog-prefetch', async () => {
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
            queryClient.prefetchQuery({
                queryKey: articleKeys.popular(5),
                queryFn: () => articlesApi.getPopular(5),
            }),
        ]);
        return true;
    });

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

    // Tags filtres par category+search (mais pas tags!): on n'enleve jamais les
    // tags deja selectionnes, sinon l'utilisateur ne pourrait plus les deselectionner.
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

    // Schema.org ItemList pour rich results
    const articleListItems = computed(() =>
        articles.value.map((a) => ({ name: a.title, url: `/blog/${a.slug}`, image: a.image })),
    );
    watch(
        articleListItems,
        (items) => {
            if (items.length) {
                useItemListSeo({ items: articleListItems });
            }
        },
        { immediate: true },
    );
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

    const categoriesWithAll = computed(() => {
        if (!categories.value?.length) {
            return [];
        }
        return [{ id: '', slug: '', name: 'Tous', count: totalArticles.value }, ...categories.value];
    });

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
        grid-template-columns: 1fr 320px;
        gap: vars.$spacing-xl;
        max-width: 1400px;
        margin: 0 auto;

        @include mix.responsive(desktop) {
            grid-template-columns: 1fr 280px;
            gap: vars.$spacing-lg;
        }

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }
    }

    .blog-main {
        min-width: 0;
    }

    .blog-transition {
        position: relative;
        min-height: 1400px;
        contain: layout;

        @include mix.responsive(tablet) {
            min-height: 1700px;
        }

        @include mix.responsive(mobile) {
            min-height: 2600px;
        }

        > .slide-fade-leave-active {
            position: absolute;
            inset: 0;
            width: 100%;
        }
    }

    .blog-sidebar {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-lg;

        &__slot {
            background: fn.color-alpha(vars.$white, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            border-radius: vars.$border-radius-xl;
            box-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.04);
            transition: box-shadow 0.3s ease;
            contain: layout paint;

            &:hover {
                box-shadow: 0 6px 24px fn.color-alpha(vars.$black, 0.07);
            }

            &--popular {
                min-height: 420px;
            }

            &--categories {
                min-height: 260px;
            }

            &--tags {
                min-height: 220px;
            }
        }

        @include mix.responsive(tablet) {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
        }

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;

            .blog-sidebar__slot {
                &--popular {
                    min-height: 380px;
                }

                &--categories,
                &--tags {
                    min-height: 180px;
                }
            }
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
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(12px);
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
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
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

    .articles-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-lg;
        transition: opacity 0.2s ease;
        contain: layout paint;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }

        &--fetching {
            opacity: 0.55;
            pointer-events: none;
        }

        &__item {
            opacity: 0;
            will-change: opacity, transform;
            animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            animation-delay: calc(var(--article-index, 0) * 60ms);
        }
    }

    .blog-pagination {
        margin-top: vars.$spacing-xl;
        padding-top: vars.$spacing-xl;
        border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .slide-fade-enter-active,
    .slide-fade-leave-active {
        transition: opacity 0.25s ease;
    }

    .slide-fade-enter-from,
    .slide-fade-leave-to {
        opacity: 0;
    }

    @media (prefers-reduced-motion: reduce) {
        .articles-grid__item {
            animation: none;
            opacity: 1;
        }

        .blog-content {
            animation: none;
        }

        .slide-fade-enter-active,
        .slide-fade-leave-active {
            transition: none;
        }
    }

    @include mix.responsive(tablet) {
        .search-bar {
            margin-bottom: vars.$spacing-md;
        }
    }

    @include mix.responsive(mobile) {
        .articles-grid {
            gap: vars.$spacing-md;
        }
    }
</style>
