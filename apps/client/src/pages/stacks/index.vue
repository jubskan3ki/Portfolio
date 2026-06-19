<template>
    <div class="stacks-page">
        <Hero
            title="Stacks"
            description="Les outils et frameworks que je maîtrise pour créer des applications web performantes."
            badge="Stack technique"
            variant="dark"
        >
            <template #stats>
                <!-- Toujours rendre les StatCard (données SSR-préchargées, fallbacks stables dans heroStats) :
                     pas de skeleton -> StatCard, donc pas de saut de hauteur du hero qui pousse tout le main (CLS). -->
                <StatCard
                    v-for="stat in heroStats"
                    :key="stat.label"
                    :value="stat.value"
                    :label="stat.label"
                    :icon="stat.icon"
                    variant="dark"
                />
            </template>
        </Hero>

        <Main
            variant="default"
            size="large"
            with-glass-background
            glass-variant="secondary"
            show-dots
            :glass-animated="!prefersReducedMotion"
            :bubble-count="4"
        >
            <div class="stacks-nav">
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
                    <button
                        type="button"
                        class="stacks-nav__search-btn"
                        aria-label="Rechercher dans les stacks"
                        @click="toggleSearchMode"
                    >
                        <BaseIcon name="search" :size="16" />
                    </button>
                </div>

                <div v-else class="stacks-nav__search">
                    <button
                        type="button"
                        class="stacks-nav__back-btn"
                        aria-label="Quitter la recherche"
                        @click="toggleSearchMode"
                    >
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

            <div
                :id="`panel-${activeCategory}`"
                class="stacks-section"
                role="tabpanel"
                :aria-labelledby="`tab-${activeCategory}`"
            >
                <Transition name="slide-fade" mode="out-in">
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

                    <div v-else :key="contentKey" class="stacks-content">
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

                        <template v-else-if="!isSearchMode && activeCategory !== 'all'">
                            <StackCategorySlider
                                :label="activeCategoryLabel"
                                :icon="activeCategoryIcon"
                                :stacks="filteredStacks"
                                @navigate="navigateToStack"
                            />
                        </template>

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

        <CTA
            title="Besoin d'un développeur ?"
            description="Discutons de votre projet et voyons comment je peux vous aider."
            variant="dark"
            :primary-button="{ label: 'Me contacter', to: ROUTES.CONTACT.path, icon: 'mail' }"
            :secondary-button="{ label: 'Mes articles', to: ROUTES.BLOG.path }"
        />
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
    import { computed, defineAsyncComponent, ref, watch, onMounted, nextTick } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import StatCard from '@/components/feature/home/StatCard.vue';
    import StackCard from '@/components/feature/stacks/StackCard.vue';
    const StackCategorySlider = defineAsyncComponent(
        () => import('@/components/feature/stacks/StackCategorySlider.vue'),
    );
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Main from '@/components/layouts/Main.vue';
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
    import { useItemListSeo } from '@/composables/seo/useItemListSeo';
    import { useStacksSeo } from '@/composables/seo/useSeo';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import { stackKeys, stacksApi, useStacks, useStackCategories, useStackStats } from '@/services/api/modules/stacks';

    useStacksSeo();

    const router = useRouter();

    const { announceLoaded, announce } = useAnnounce();
    const { prefersReducedMotion } = useReducedMotion();

    const { filters, setFilter } = useFilters(filterPresets.stacks);

    // SSR-prefetch to kill CLS on first paint.
    const queryClient = useQueryClient();
    await useAsyncData('stacks-prefetch', async () => {
        await Promise.all([
            queryClient.prefetchQuery({
                queryKey: stackKeys.list({ limit: 100 }),
                queryFn: () => stacksApi.getAll({ limit: 100 }),
            }),
            queryClient.prefetchQuery({
                queryKey: stackKeys.categories(),
                queryFn: stacksApi.getCategories,
            }),
            queryClient.prefetchQuery({
                queryKey: stackKeys.stats(),
                queryFn: stacksApi.getStats,
            }),
        ]);
        return true;
    });

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

    const { data: statsData, refetch: refetchStats } = useStackStats();

    const isSearchMode = ref(false);
    const searchInputRef = ref<HTMLInputElement | null>(null);

    const searchQuery = computed({
        get: () => filters.value.search,
        set: (val: string) => setFilter('search', val),
    });

    const activeCategory = computed({
        get: () => filters.value.category || 'all',
        set: (val: string) => setFilter('category', val === 'all' ? '' : val),
    });

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

    // Schema.org ItemList pour rich results
    const stackListItems = computed(() =>
        (allStacks.value ?? []).map((s) => ({ name: s.name, url: `/stacks/${s.slug}`, image: s.logo })),
    );
    watch(
        stackListItems,
        (items) => {
            if (items.length) {
                useItemListSeo({ items: stackListItems });
            }
        },
        { immediate: true },
    );

    const navigateToStack = (slug: string) => {
        router.push(`${ROUTES.STACKS.path}/${slug}`);
    };

    const handleRetry = () => {
        refetchStacks();
        refetchCategories();
        refetchStats();
    };

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

    watch(activeCategory, (newCategory) => {
        const tab = availableTabs.value.find((t) => t.key === newCategory);
        if (tab) {
            const labelWithoutCount = tab.label.replace(/\s*\(\d+\)$/, '');
            announce(`Affichage: ${labelWithoutCount}`);
        }
    });

    watch(
        allStacks,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('stacks', list.length);
            }
        },
        { once: true },
    );

    onMounted(() => {
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

    .stacks-main--no-motion {
        .stacks-grid__item {
            animation: none;
            opacity: 1;
        }
    }

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

    .tabs-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
    }

    .single-category-indicator {
        @include mix.flex(column, center, center, vars.$spacing-xs);

        &__count {
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;
        }
    }

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

            content-visibility: auto;
            contain-intrinsic-size: auto 280px;
        }
    }

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
