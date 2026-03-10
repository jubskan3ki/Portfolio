<template>
    <div class="stacks-page">
        <!-- Hero Section -->
        <Hero
            title="Stacks"
            description="Les outils et frameworks que je maîtrise pour créer des applications web performantes."
            badge="Stack technique"
            variant="dark"
        >
            <template #stats>
                <template v-if="statsLoading">
                    <div v-for="i in 3" :key="i" class="stat-skeleton">
                        <Skeleton width="50px" height="28px" />
                        <Skeleton width="80px" height="14px" />
                    </div>
                </template>
                <template v-else>
                    <StatCard
                        v-for="stat in heroStats"
                        :key="stat.label"
                        :value="stat.value"
                        :label="stat.label"
                        :icon="stat.icon"
                        variant="dark"
                    />
                </template>
            </template>
        </Hero>

        <!-- Main Content -->
        <Main
            variant="default"
            size="large"
            with-glass-background
            glass-variant="secondary"
            show-dots
            :glass-animated="!prefersReducedMotion"
            :bubble-count="4"
        >
            <!-- Navigation Bar: Tabs + Search -->
            <div class="stacks-nav">
                <!-- Tabs -->
                <div v-if="!isSearchMode" class="stacks-nav__tabs">
                    <NavigationTabs
                        v-if="availableTabs.length > 1"
                        v-model="activeCategory"
                        :tabs="availableTabs"
                        variant="glass"
                    />
                    <Badge
                        v-else-if="availableTabs.length === 1 && availableTabs[0]"
                        :text="availableTabs[0]?.label || ''"
                        variant="primary"
                        size="lg"
                    />
                    <button class="stacks-nav__search-btn" @click="toggleSearchMode">
                        <BaseIcon name="search" :size="16" />
                    </button>
                </div>

                <!-- Search -->
                <div v-else class="stacks-nav__search">
                    <button class="stacks-nav__back-btn" @click="toggleSearchMode">
                        <BaseIcon name="arrow-left" :size="16" />
                    </button>
                    <SearchInput
                        ref="searchInputRef"
                        v-model="searchQuery"
                        placeholder="Rechercher..."
                        shortcut="S"
                        @clear="clearSearch"
                    />
                    <span v-if="searchQuery" class="stacks-nav__results">
                        {{ filteredStacks.length }}
                    </span>
                </div>
            </div>

            <!-- Content Section -->
            <div
                :id="`panel-${activeCategory}`"
                class="stacks-section"
                role="tabpanel"
                :aria-labelledby="`tab-${activeCategory}`"
            >
                <Transition name="slide-fade" mode="out-in">
                    <!-- Loading State -->
                    <div v-if="isLoading" key="loader" class="stacks-loader">
                        <SkeletonList
                            :count="6"
                            variant="stack"
                            layout="grid"
                            :columns="3"
                            show-image
                            show-tags
                        />
                    </div>

                    <!-- Error State -->
                    <EmptyState
                        v-else-if="hasError"
                        key="error"
                        icon="alert-circle"
                        title="Erreur de chargement"
                        description="Impossible de charger les stacks. Veuillez réessayer."
                        size="lg"
                        custom-class="stacks-empty-state"
                    >
                        <template #action>
                            <BaseButton label="Réessayer" icon="refresh-cw" variant="primary" @click="handleRetry" />
                        </template>
                    </EmptyState>

                    <!-- Empty State -->
                    <EmptyState
                        v-else-if="!hasAnyData"
                        key="empty-all"
                        icon="code"
                        :title="emptyStateTitle"
                        :description="emptyStateDescription"
                        size="lg"
                        custom-class="stacks-empty-state"
                    >
                        <template v-if="isSearchMode" #action>
                            <BaseButton
                                label="Effacer la recherche"
                                icon="x"
                                variant="secondary"
                                @click="clearSearch"
                            />
                        </template>
                    </EmptyState>

                    <!-- Content: Sections by Category or Grid -->
                    <div v-else :key="contentKey" class="stacks-content">
                        <!-- Netflix Mode: Carousel sections when "All" is selected -->
                        <template v-if="showSections">
                            <StackCategorySlider
                                v-for="section in stackSections"
                                :key="section.key"
                                :label="section.label"
                                :icon="section.icon"
                                :stacks="section.stacks"
                                @navigate="navigateToStack"
                            />
                        </template>

                        <!-- Single Category Mode: Carousel for selected category -->
                        <template v-else-if="!isSearchMode && activeCategory !== 'all'">
                            <StackCategorySlider
                                :label="activeCategoryLabel"
                                :icon="activeCategoryIcon"
                                :stacks="filteredStacks"
                                @navigate="navigateToStack"
                            />
                        </template>

                        <!-- Search Mode: Grid for search results -->
                        <template v-else>
                            <div class="stacks-grid">
                                <StackCard
                                    v-for="(stack, index) in filteredStacks"
                                    :key="stack.id"
                                    :stack="stack"
                                    :style="{ '--stack-index': prefersReducedMotion ? 0 : index }"
                                    class="stacks-grid__item"
                                    @click="navigateToStack(stack.slug)"
                                />
                            </div>
                        </template>
                    </div>
                </Transition>
            </div>
        </Main>

        <!-- CTA -->
        <CTA
            title="Besoin d'un développeur ?"
            description="Discutons de votre projet et voyons comment je peux vous aider."
            variant="light"
            :primary-button="{ label: 'Me contacter', to: ROUTES.CONTACT.path, icon: 'mail' }"
            :secondary-button="{ label: 'Mes articles', to: ROUTES.BLOG.path }"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, watch, onMounted, nextTick } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import StatCard from '@/components/feature/home/StatCard.vue';
    import StackCard from '@/components/feature/stacks/StackCard.vue';
    import StackCategorySlider from '@/components/feature/stacks/StackCategorySlider.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Main from '@/components/layouts/Main.vue';
    import Skeleton from '@/components/loaders/Skeleton.vue';
    import SkeletonList from '@/components/loaders/SkeletonList.vue';
    import NavigationTabs from '@/components/navigation/NavigationTabs.vue';
    import Badge from '@/components/ui/Badge.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useFilters } from '@/composables/data/useFilters';
    import { useStacksPage } from '@/composables/data/useStacksPage';
    import { useStacksSeo } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import { useStacks, useStackCategories, useStackStats } from '@/services/api/modules/stacks';

    // SEO
    useStacksSeo();

    // Router
    const router = useRouter();

    // Composables
    const { announceLoaded, announce } = useAnnounce();
    const { scrollToTop } = useScrollToTop();
    const { prefersReducedMotion } = useReducedMotion();

    // Filters with URL sync
    const { filters, setFilter } = useFilters(filterPresets.stacks);

    // API Queries
    const {
        data: stacksData,
        isLoading: stacksLoading,
        isError: stacksError,
        refetch: refetchStacks,
    } = useStacks({ limit: 100 });

    const {
        data: categoriesData,
        isLoading: categoriesLoading,
        isError: categoriesError,
        refetch: refetchCategories,
    } = useStackCategories();

    const { data: statsData, isLoading: statsLoading, refetch: refetchStats } = useStackStats();

    // Search mode state (local, not URL-synced)
    const isSearchMode = ref(false);
    const searchInputRef = ref<HTMLInputElement | null>(null);

    // Computed aliases for template compatibility with URL sync
    const searchQuery = computed({
        get: () => filters.value.search,
        set: (val: string) => setFilter('search', val),
    });

    const activeCategory = computed({
        get: () => filters.value.category || 'all',
        set: (val: string) => setFilter('category', val === 'all' ? '' : val),
    });

    // Data transformation via composable
    const {
        isLoading,
        hasError,
        allStacks,
        availableTabs,
        filteredStacks,
        showSections,
        activeCategoryLabel,
        activeCategoryIcon,
        stackSections,
        hasAnyData,
        emptyStateTitle,
        emptyStateDescription,
        contentKey,
        heroStats,
    } = useStacksPage({
        stacksData,
        categoriesData,
        statsData,
        stacksLoading,
        categoriesLoading,
        stacksError,
        categoriesError,
        activeCategory,
        searchQuery,
        isSearchMode,
    });

    // Navigation
    const navigateToStack = (slug: string) => {
        router.push(`${ROUTES.STACKS.path}/${slug}`);
    };

    // Retry handler
    const handleRetry = () => {
        refetchStacks();
        refetchCategories();
        refetchStats();
    };

    // Search handlers
    const toggleSearchMode = () => {
        isSearchMode.value = !isSearchMode.value;
        if (isSearchMode.value) {
            nextTick(() => {
                searchInputRef.value?.focus();
            });
            announce('Mode recherche activé');
        } else {
            setFilter('search', '');
            announce('Retour aux catégories');
        }
    };

    const clearSearch = () => {
        setFilter('search', '');
        searchInputRef.value?.focus();
    };

    // Announce tab changes
    watch(activeCategory, (newCategory) => {
        const tab = availableTabs.value.find((t) => t.key === newCategory);
        if (tab) {
            const labelWithoutCount = tab.label.replace(/\s*\(\d+\)$/, '');
            announce(`Affichage: ${labelWithoutCount}`);
            scrollToTop('smooth');
        }
    });

    // Announce loaded data
    watch(
        allStacks,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('stacks', list.length);
            }
        },
        { once: true },
    );

    // Scroll to top on mount and check for search in URL
    onMounted(() => {
        scrollToTop('instant');
        if (filters.value.search) {
            isSearchMode.value = true;
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stacks-page {
        min-height: 100vh;
    }

    // Hero skeleton
    .stat-skeleton {
        @include mix.flex(column, center, center, vars.$spacing-xs);
        padding: vars.$spacing-sm;
    }

    // Main Content - No motion modifier
    .stacks-main--no-motion {
        .stacks-grid__item {
            animation: none;
            opacity: 1;
        }
    }

    // Navigation Bar
    .stacks-nav {
        margin-bottom: vars.$spacing-xl;

        &__tabs {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-md;
        }

        &__search {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-sm;
        }

        &__back-btn,
        &__search-btn {
            height: 48px;
            width: 48px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: vars.$white;
            border: 1px solid fn.color-alpha(vars.$border-color, 0.4);
            color: vars.$text-secondary;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover {
                border-color: vars.$primary-color;
                color: vars.$white;
            }
        }

        &__results {
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 32px;
            height: 32px;
            padding: 0 vars.$spacing-xs;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-secondary;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-sm;
        }
    }

    // Tabs wrapper
    .tabs-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
    }

    // Single category indicator
    .single-category-indicator {
        @include mix.flex(column, center, center, vars.$spacing-xs);

        &__count {
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;
        }
    }

    // Stacks section
    .stacks-section {
        position: relative;
        z-index: 5;
        min-height: 400px;
    }

    .stacks-loader {
        max-width: 100%;
    }

    .stacks-content {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    // Grid (for search results)
    .stacks-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: vars.$spacing-lg;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }

        &__item {
            opacity: 0;
            animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            animation-delay: calc(var(--stack-index, 0) * 50ms);
        }
    }

    // Empty State
    :deep(.stacks-empty-state) {
        max-width: 500px;
        margin: vars.$spacing-xl auto;
        padding: vars.$spacing-xxl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.06);
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

    // Responsive - Tablet
    // Responsive - Mobile
    @include mix.responsive(mobile) {
        .stacks-nav {
            padding: 0 vars.$spacing-md;

            &__search {
                width: 100%;
            }
        }

        .stacks-grid {
            gap: vars.$spacing-md;
        }
    }
</style>
