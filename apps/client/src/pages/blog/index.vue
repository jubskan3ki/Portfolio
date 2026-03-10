<template>
    <div class="blog-page">
        <!-- Hero -->
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

        <!-- Content -->
        <Main id="articles" variant="light" size="large">
            <div class="blog-layout">
                <!-- Main Content -->
                <div class="blog-main">
                    <!-- Search Bar -->
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
                            <BaseSelect v-model="currentSort" :options="sortOptions" placeholder="Trier par" />
                        </div>
                    </div>

                    <!-- Content States -->
                    <Transition name="slide-fade" mode="out-in">
                        <!-- Loading State -->
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

                        <!-- Error State -->
                        <EmptyState
                            v-else-if="hasError"
                            key="error"
                            icon="alert-circle"
                            title="Erreur de chargement"
                            description="Impossible de charger les articles. Veuillez réessayer."
                            size="lg"
                            custom-class="blog-empty-state"
                        >
                            <template #action>
                                <BaseButton
                                    label="Réessayer"
                                    icon="refresh-cw"
                                    variant="primary"
                                    @click="handleRetry"
                                />
                            </template>
                        </EmptyState>

                        <!-- Empty State -->
                        <EmptyState
                            v-else-if="!hasArticles"
                            key="empty"
                            icon="file-text"
                            :title="emptyStateTitle"
                            :description="emptyStateDescription"
                            size="lg"
                            custom-class="blog-empty-state"
                        >
                            <template v-if="hasActiveFilters" #action>
                                <BaseButton
                                    label="Réinitialiser les filtres"
                                    icon="x"
                                    variant="secondary"
                                    @click="resetFilters"
                                />
                            </template>
                        </EmptyState>

                        <!-- Articles Grid -->
                        <div v-else :key="contentKey" class="blog-content">
                            <div class="articles-grid">
                                <ArticleCard
                                    v-for="(article, index) in articles"
                                    :key="article.id"
                                    :article="article"
                                    class="articles-grid__item"
                                    :style="{ '--article-index': prefersReducedMotion ? 0 : index }"
                                />
                            </div>

                            <!-- Pagination -->
                            <Pagination
                                v-if="totalPages > 1"
                                :current-page="currentPage"
                                :total-pages="totalPages"
                                class="blog-pagination"
                                @update:current-page="handlePageChange"
                            />
                        </div>
                    </Transition>
                </div>

                <!-- Sidebar -->
                <aside class="blog-sidebar">
                    <LazyArticlePopular :articles="popularArticles" title="Articles populaires" show-title />

                    <LazyArticleCategories
                        v-if="categories?.length"
                        v-model="selectedCategory"
                        :categories="categoriesWithAll"
                        title="Catégories"
                    />

                    <LazyArticleTags
                        v-if="tags?.length"
                        v-model="selectedTags"
                        :tags="tags"
                        title="Tags"
                        show-title
                        display="cloud"
                        multi-select
                    />
                </aside>
            </div>
        </Main>

        <!-- CTA -->
        <CTA
            title="Découvrez mes projets"
            description="Explorez mes réalisations et les stacks que j'utilise."
            variant="secondary"
            :primary-button="{ label: 'Voir les projets', to: ROUTES.PROJECTS.path, icon: 'briefcase' }"
            :secondary-button="{ label: 'Mon parcours', to: ROUTES.EXPERIENCE.path }"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed, watch, onMounted } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    // ArticlePopular, ArticleCategories, ArticleTags are lazy-loaded via Lazy prefix in template
    import StatCard from '@/components/feature/home/StatCard.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Main from '@/components/layouts/Main.vue';
    import SkeletonList from '@/components/loaders/SkeletonList.vue';
    import Pagination from '@/components/navigation/Pagination.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useFilters } from '@/composables/data/useFilters';
    import { useBlogSeo } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import {
        useArticles,
        useArticleCategories,
        useArticleTags,
        usePopularArticles,
    } from '@/services/api/modules/articles';

    import type { SelectOption } from '@/types/components/base';

    // SEO
    useBlogSeo();

    // Accessibility
    const { announceLoaded } = useAnnounce();
    const { prefersReducedMotion } = useReducedMotion();
    const { scrollToTop } = useScrollToTop();

    const { filters, apiFilters, currentPage, hasActiveFilters, reset, setFilter, setPage } = useFilters({
        ...filterPresets.blog,
        pagination: { ...filterPresets.blog.pagination, itemsPerPage: 6 },
    });

    // Aliases
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

    // Sort options
    const sortOptions: SelectOption[] = [
        { value: '-date', label: 'Plus récents' },
        { value: 'date', label: 'Plus anciens' },
        { value: '-views', label: 'Plus populaires' },
        { value: 'title', label: 'A → Z' },
    ];

    // Queries
    const { data: articlesData, isLoading, isError: hasError, refetch: refetchArticles } = useArticles(apiFilters);
    const { data: categories } = useArticleCategories();
    const { data: tags } = useArticleTags();
    const { data: popularArticlesData } = usePopularArticles(5);

    // Computed
    const articles = computed(() => articlesData.value?.data ?? []);
    const totalArticles = computed(() => articlesData.value?.pagination?.total ?? 0);
    const totalPages = computed(() => articlesData.value?.pagination?.totalPages ?? 1);
    const popularArticles = computed(() => popularArticlesData.value ?? []);
    const hasArticles = computed(() => (articles.value?.length ?? 0) > 0);

    const contentKey = computed(() => `${selectedCategory.value ?? 'all'}-${currentPage.value}-${searchQuery.value}`);

    // Hero stats
    const heroStats = computed(() => [
        { value: totalArticles.value, label: 'Articles', icon: 'file-text' },
        { value: categories.value?.length ?? 0, label: 'Catégories', icon: 'folder' },
        { value: tags.value?.length ?? 0, label: 'Tags', icon: 'hash' },
    ]);

    // Empty state messages
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

    // Handlers
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

    // Announce loaded data
    watch(
        articles,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('articles', list.length);
            }
        },
        { once: true },
    );

    // Scroll to top on mount
    onMounted(() => {
        scrollToTop('instant');
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .blog-page {
        min-height: 100vh;
    }

    // Layout
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

    // Sidebar
    .blog-sidebar {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-lg;

        > :deep(*) {
            background: fn.color-alpha(vars.$white, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            border-radius: vars.$border-radius-xl;
            box-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.04);
            transition: box-shadow 0.3s ease;

            &:hover {
                box-shadow: 0 6px 24px fn.color-alpha(vars.$black, 0.07);
            }
        }

        @include mix.responsive(tablet) {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
        }

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }
    }

    // Search Bar
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

    // Content
    .blog-loader {
        max-width: 100%;
    }

    .blog-content {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    // Empty state
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

    // Articles Grid
    .articles-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-lg;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }

        &__item {
            opacity: 0;
            animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            animation-delay: calc(var(--article-index, 0) * 60ms);
        }
    }

    // Pagination
    .blog-pagination {
        margin-top: vars.$spacing-xl;
        padding-top: vars.$spacing-xl;
        border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
    }

    // Animations
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

    // Transitions
    .slide-fade-enter-active {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .slide-fade-leave-active {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .slide-fade-enter-from {
        opacity: 0;
        transform: translateY(20px);
    }

    .slide-fade-leave-to {
        opacity: 0;
        transform: translateY(-10px);
    }

    // Reduced motion
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

    // Responsive
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
