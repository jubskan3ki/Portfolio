<template>
    <div class="projects-page">
        <!-- Hero -->
        <Hero
            title="Mes Projets"
            description="Explorez mes réalisations, des applications web innovantes aux solutions DevOps robustes."
            badge="Portfolio"
            variant="primary"
        >
            <template #stats>
                <StatCard
                    v-for="stat in statsCards"
                    :key="stat.label"
                    :value="stat.value"
                    :label="stat.label"
                    :icon="stat.icon"
                    variant="primary"
                />
            </template>
        </Hero>

        <!-- Main -->
        <Main variant="default" size="large">
            <!-- Filters -->
            <div class="projects-filters">
                <!-- Search -->
                <div class="projects-filters__search">
                    <SearchInput
                        v-model="searchQuery"
                        placeholder="Rechercher un projet..."
                        shortcut="P"
                        @clear="searchQuery = ''"
                    />
                </div>

                <!-- Category Select -->
                <BaseSelect
                    v-model="selectedCategory"
                    :options="categoryOptions"
                    placeholder="Catégorie"
                    class="projects-filters__select"
                />

                <!-- Technologies MultiSelect -->
                <BaseMultiSelect
                    v-model="selectedTechs"
                    :options="techOptions"
                    placeholder="Technologies..."
                    class="projects-filters__multiselect"
                />

                <!-- Reset -->
                <button v-if="hasActiveFilters" type="button" class="projects-filters__reset" @click="resetFilters">
                    <BaseIcon name="x" :size="14" />
                    Réinitialiser
                </button>
            </div>

            <!-- Content -->
            <ClientOnly>
                <!-- Loading -->
                <div v-if="isLoading && !hasProjects" class="projects-grid">
                    <div v-for="i in 6" :key="i" class="project-skeleton">
                        <div class="project-skeleton__image"></div>
                        <div class="project-skeleton__body">
                            <div class="project-skeleton__title"></div>
                            <div class="project-skeleton__text"></div>
                            <div class="project-skeleton__tags">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <div class="project-skeleton__footer"></div>
                        </div>
                    </div>
                </div>

                <!-- Empty -->
                <EmptyState
                    v-else-if="!hasProjects"
                    icon="folder-open"
                    :title="hasActiveFilters ? 'Aucun projet trouvé' : 'Aucun projet disponible'"
                    :description="
                        hasActiveFilters ? 'Essayez de modifier vos filtres' : 'Les projets seront bientôt disponibles.'
                    "
                    :action-text="hasActiveFilters ? 'Réinitialiser' : undefined"
                    @action="resetFilters"
                />

                <!-- Grid -->
                <div v-else class="projects-grid">
                    <ProjectCard
                        v-for="(project, index) in allProjects"
                        :key="project.id"
                        :project="project"
                        :style="{ '--i': index }"
                        class="projects-grid__item"
                    />
                </div>

                <!-- Load More -->
                <div v-if="hasProjects && hasNextPage" ref="targetRef" class="projects-more">
                    <button v-if="!isFetchingNextPage" type="button" class="projects-more__btn" @click="loadMore">
                        Voir plus
                        <BaseIcon name="chevron-down" :size="16" />
                    </button>
                    <Spinner v-else size="sm" />
                </div>

                <template #fallback>
                    <div class="projects-grid">
                        <div v-for="i in 6" :key="i" class="project-skeleton">
                            <div class="project-skeleton__image"></div>
                            <div class="project-skeleton__body">
                                <div class="project-skeleton__title"></div>
                                <div class="project-skeleton__text"></div>
                                <div class="project-skeleton__tags">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                                <div class="project-skeleton__footer"></div>
                            </div>
                        </div>
                    </div>
                </template>
            </ClientOnly>
        </Main>

        <!-- CTA -->
        <CTA
            title="Un projet en tête ?"
            description="Discutons de vos idées et voyons comment transformer votre vision en réalité."
            variant="primary"
            :primary-button="{
                label: 'Me contacter',
                to: ROUTES.CONTACT.path,
                icon: 'mail',
            }"
            :secondary-button="{
                label: 'Mes compétences',
                to: ROUTES.STACKS.path,
            }"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseMultiSelect from '@/components/base/BaseMultiSelect.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import StatCard from '@/components/feature/home/StatCard.vue';
    import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Main from '@/components/layouts/Main.vue';
    import Spinner from '@/components/loaders/Spinner.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';
    import { useFilters } from '@/composables/data/useFilters';
    import { useInfiniteScroll } from '@/composables/data/useInfiniteScroll';
    import { useItemListSeo } from '@/composables/seo/useItemListSeo';
    import { useProjectsSeo } from '@/composables/seo/useSeo';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import { useInfiniteProjects, useProjectCategories, useProjectStats } from '@/services/api/modules/projects';

    import type { SelectOption } from '@/types/components/base';
    import type { Project, ProjectCategory } from '@/types/feature/project';

    // SEO
    useProjectsSeo();

    // Filters with URL sync
    const { filters, hasActiveFilters, reset, setFilter } = useFilters(filterPresets.projects);

    // Computed aliases for template compatibility
    const searchQuery = computed({
        get: () => filters.value.search,
        set: (val: string) => setFilter('search', val),
    });

    const selectedCategory = computed({
        get: () => filters.value.category,
        set: (val: string) => setFilter('category', val),
    });

    const selectedTechs = computed({
        get: () => filters.value.technologies,
        set: (val: string[]) => setFilter('technologies', val),
    });

    // API filters (adapt technologies array to comma-separated string)
    const apiFilters = computed(() => ({
        category: filters.value.category || undefined,
        search: filters.value.search || undefined,
        technologies: filters.value.technologies.length ? filters.value.technologies.join(',') : undefined,
        ordering: filters.value.ordering,
    }));

    // Data fetching
    const {
        data: projectsData,
        isLoading,
        isFetchingNextPage,
        hasNextPage,
        fetchNextPage,
    } = useInfiniteProjects(apiFilters, 9);

    const { data: categoriesData } = useProjectCategories();
    const { data: statsData } = useProjectStats();

    // Computed
    const allProjects = computed(() => {
        if (!projectsData.value?.pages) {
            return [];
        }
        return projectsData.value.pages.flatMap((page) => page?.data ?? []).filter((p): p is Project => p != null);
    });

    const hasProjects = computed(() => allProjects.value.length > 0);

    // ItemList Schema.org pour resultats enrichis
    const projectListItems = computed(() =>
        allProjects.value.map((p) => ({ name: p.title, url: `/projects/${p.slug}`, image: p.image })),
    );
    watch(projectListItems, (items) => {
        if (items.length) {
            useItemListSeo({ items: projectListItems });
        }
    }, { immediate: true });

    // Category options
    const categoryOptions = computed<SelectOption[]>(() => {
        const cats = (categoriesData.value?.data ?? []) as ProjectCategory[];
        return [
            { value: '', label: 'Toutes les catégories' },
            ...cats.filter((c) => c.count > 0).map((c) => ({ value: String(c.id), label: c.name })),
        ];
    });

    // Technology options (extracted from all projects)
    const techOptions = computed(() => {
        const techSet = new Set<string>();
        for (const project of allProjects.value) {
            for (const tech of project.technologies ?? []) {
                techSet.add(tech);
            }
        }
        return Array.from(techSet)
            .sort()
            .map((tech) => ({ value: tech, label: tech }));
    });

    // Stats
    const statsCards = computed(() => {
        const stats = statsData.value;
        return [
            { value: stats?.totalProjects ?? 0, label: 'Projets', icon: 'folder' },
            { value: stats?.projectsByCategory?.length ?? 0, label: 'Catégories', icon: 'layers' },
            { value: stats?.totalViews ?? 0, label: 'Vues', icon: 'eye' },
        ];
    });

    // Methods
    const resetFilters = () => reset();

    const loadMore = () => {
        if (hasNextPage.value && !isFetchingNextPage.value) {
            fetchNextPage();
        }
    };

    const canAutoLoad = computed(() => hasNextPage.value && !isFetchingNextPage.value);
    const { targetRef } = useInfiniteScroll(loadMore, { enabled: canAutoLoad });
    void targetRef; // Used as template ref
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .projects-page {
        min-height: 100vh;
    }

    /* Filters */
    .projects-filters {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: vars.$spacing-md;
        margin-bottom: vars.$spacing-xl;
        padding: vars.$spacing-md;
        background: vars.$white;
        border: 1px solid vars.$border-color;
        border-radius: vars.$border-radius-lg;

        @include mix.responsive(tablet) {
            flex-direction: column;
            align-items: stretch;
        }

        &__search {
            flex: 1;
            min-width: 200px;

            @include mix.responsive(tablet) {
                width: 100%;
            }
        }

        &__select {
            width: 250px;
            margin-bottom: 0;

            @include mix.responsive(tablet) {
                width: 100%;
            }
        }

        &__multiselect {
            width: 250px;
            margin-bottom: 0;

            @include mix.responsive(tablet) {
                width: 100%;
            }
        }

        &__reset {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xs vars.$spacing-md;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$danger-color;
            background: fn.color-alpha(vars.$danger-color, 0.08);
            border: 1px solid fn.color-alpha(vars.$danger-color, 0.2);
            border-radius: vars.$border-radius-md;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$danger-color, 0.15);
            }

            @include mix.responsive(tablet) {
                width: 100%;
                justify-content: center;
            }
        }
    }

    /* Grid */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: vars.$spacing-lg;

        @include mix.responsive(tablet) {
            grid-template-columns: repeat(2, 1fr);
        }

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }

        &__item {
            animation: fadeUp 0.4s ease forwards;
            animation-delay: calc(var(--i, 0) * 50ms);
            opacity: 0;
        }
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Skeleton */
    .project-skeleton {
        background: vars.$white;
        border: 1px solid vars.$border-color;
        border-radius: vars.$border-radius-lg;
        overflow: hidden;

        &__image {
            aspect-ratio: 16 / 10;
            background: linear-gradient(90deg, vars.$gray-light 25%, vars.$white-dark 50%, vars.$gray-light 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }

        &__body {
            padding: vars.$spacing-md;
        }

        &__title {
            width: 75%;
            height: 18px;
            margin-bottom: vars.$spacing-xs;
            background: vars.$gray-light;
            border-radius: vars.$border-radius-sm;
        }

        &__text {
            width: 100%;
            height: 14px;
            margin-bottom: vars.$spacing-sm;
            background: vars.$gray-light;
            border-radius: vars.$border-radius-sm;
        }

        &__tags {
            display: flex;
            gap: vars.$spacing-xxs;
            margin-bottom: vars.$spacing-sm;

            span {
                width: 48px;
                height: 20px;
                background: vars.$bg-secondary;
                border-radius: vars.$border-radius-sm;
            }
        }

        &__footer {
            height: 16px;
            width: 60px;
            margin-top: vars.$spacing-sm;
            padding-top: vars.$spacing-sm;
            border-top: 1px solid vars.$border-color;
            background: vars.$gray-light;
            border-radius: vars.$border-radius-sm;
        }
    }

    @keyframes shimmer {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }

    /* Load More */
    .projects-more {
        display: flex;
        justify-content: center;
        margin-top: vars.$spacing-xl;

        &__btn {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-sm vars.$spacing-xl;
            font-weight: vars.$font-weight-medium;
            color: vars.$primary-color;
            background: vars.$white;
            border: 1px solid vars.$border-color;
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover {
                border-color: vars.$primary-color;
                box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.15);
            }
        }
    }
</style>
