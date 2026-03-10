<template>
    <div class="experience-page">
        <!-- Hero with Stats -->
        <Hero
            title="Expérience & Formation"
            description="Mon parcours professionnel et académique dans le développement web et logiciel."
            badge="Parcours"
            variant="light"
        >
            <template #stats>
                <StatCard
                    v-for="stat in heroStats"
                    :key="stat.label"
                    :value="stat.value"
                    :label="stat.label"
                    :icon="stat.icon"
                    :suffix="stat.suffix"
                    variant="light"
                />
            </template>
        </Hero>

        <!-- Content Section -->
        <Main variant="default" size="large" :custom-class="prefersReducedMotion ? 'content--no-motion' : ''">
            <!-- Tabs Navigation -->
            <div v-if="availableTabs.length > 1" class="tabs-wrapper">
                <NavigationTabs v-model="activeType" :tabs="availableTabs" variant="glass" />
            </div>

            <!-- Single type indicator -->
            <div v-else-if="availableTabs.length === 1 && availableTabs[0]" class="single-type-indicator">
                <Badge :text="availableTabs[0].label" variant="primary" size="lg" />
                <span class="single-type-indicator__count">
                    {{ totalExperiences }} expérience{{ totalExperiences > 1 ? 's' : '' }}
                </span>
            </div>

            <!-- Timeline Section -->
            <div
                :id="`panel-${activeType}`"
                class="timeline-section"
                role="tabpanel"
                :aria-labelledby="`tab-${activeType}`"
            >
                <Transition name="slide-fade" mode="out-in">
                    <!-- Loading State -->
                    <div v-if="isLoading" key="loader" class="timeline-loader">
                        <SkeletonList
                            :count="3"
                            variant="default"
                            layout="list"
                            show-image
                            show-description
                            show-tags
                        />
                    </div>

                    <!-- Error State -->
                    <EmptyState
                        v-else-if="hasError"
                        key="error"
                        icon="alert-circle"
                        title="Erreur de chargement"
                        description="Impossible de charger les expériences. Veuillez réessayer."
                        size="lg"
                        custom-class="timeline-empty-state"
                    >
                        <template #action>
                            <BaseButton label="Réessayer" icon="refresh-cw" variant="primary" @click="handleRetry" />
                        </template>
                    </EmptyState>

                    <!-- Empty State -->
                    <EmptyState
                        v-else-if="!hasAnyData"
                        key="empty-all"
                        icon="briefcase"
                        title="Aucune expérience disponible"
                        description="Les expériences seront ajoutées prochainement."
                        size="lg"
                        custom-class="timeline-empty-state"
                    />

                    <!-- Timeline Content -->
                    <div v-else :key="activeType" class="timeline-content">
                        <ExperienceTimeline
                            :experiences="experiences"
                            :show-header="false"
                            custom-class="timeline--enhanced"
                        />
                    </div>
                </Transition>
            </div>

            <!-- Skills Summary -->
            <Transition name="fade-up">
                <div v-if="topSkills.length > 0 && !isLoading" class="skills-section">
                    <SectionHeading
                        title="Compétences clés"
                        icon="zap"
                        size="md"
                        no-separator
                        custom-class="skills-section__heading"
                    />
                    <div class="skills-section__list">
                        <Badge
                            v-for="(skill, index) in topSkills"
                            :key="skill.skill"
                            :text="skill.skill"
                            variant="primary"
                            size="md"
                            class="skills-section__badge"
                            :style="{ '--badge-delay': `${index * 50}ms` }"
                        />
                    </div>
                    <p v-if="stats?.totalYears" class="skills-section__summary">
                        <BaseIcon name="trending-up" :size="16" />
                        <span>{{ stats.totalYears }}+ années d'expérience cumulée</span>
                    </p>
                </div>
            </Transition>
        </Main>

        <!-- CTA -->
        <CTA
            title="Intéressé par mon profil ?"
            description="Discutons de vos projets ou opportunités de collaboration."
            variant="light"
            :primary-button="{ label: 'Me contacter', to: ROUTES.CONTACT.path, icon: 'mail' }"
            :secondary-button="{ label: 'Voir mes projets', to: ROUTES.PROJECTS.path }"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed, watch, onMounted } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import ExperienceTimeline from '@/components/feature/experience/ExperienceTimeline.vue';
    import StatCard from '@/components/feature/home/StatCard.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Main from '@/components/layouts/Main.vue';
    import SkeletonList from '@/components/loaders/SkeletonList.vue';
    import NavigationTabs from '@/components/navigation/NavigationTabs.vue';
    import Badge from '@/components/ui/Badge.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import SectionHeading from '@/components/ui/SectionHeading.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useFilters } from '@/composables/data/useFilters';
    import { useExperienceSeo } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';
    import { filterPresets } from '@/config/filterPresets';
    import { ROUTES } from '@/config/routes';
    import {
        useExperiences,
        useExperiencesByType,
        useExperienceTypes,
        useExperienceStats,
    } from '@/services/api/modules/experiences';

    import type { ExperienceType } from '@/types/feature/experience';

    // SEO
    useExperienceSeo();

    // Composables
    const { announceLoaded, announce } = useAnnounce();
    const { scrollToTop } = useScrollToTop();
    const { prefersReducedMotion } = useReducedMotion();

    // URL-synced filters
    const { filters, setFilter } = useFilters(filterPresets.experiences);

    // API Queries — fetch all experiences (limit=100 to bypass pagination for client-side filtering)
    const { data: allExperiencesResponse, isLoading: allExperiencesLoading } = useExperiences({ limit: 100 });
    const allExperiences = computed(() => allExperiencesResponse.value?.data ?? []);

    const {
        data: experienceTypes,
        isLoading: typesLoading,
        isError: typesError,
        refetch: refetchTypes,
    } = useExperienceTypes();

    const { data: stats, refetch: refetchStats } = useExperienceStats();

    // Type mappings
    const typeIconMap: Record<string, string> = {
        professional: 'briefcase',
        professionnel: 'briefcase',
        education: 'graduation-cap',
        formation: 'graduation-cap',
        certification: 'award',
        volunteer: 'heart',
        benevolat: 'heart',
        internship: 'book-open',
        stage: 'book-open',
    };

    const typeLabelMap: Record<string, string> = {
        professional: 'Professionnel',
        professionnel: 'Professionnel',
        education: 'Formation',
        formation: 'Formation',
        certification: 'Certification',
        volunteer: 'Bénévolat',
        benevolat: 'Bénévolat',
        internship: 'Stage',
        stage: 'Stage',
    };

    // Get count for a specific tab type
    const getTypeCount = (typeKey: string): number => {
        return (allExperiences.value ?? []).filter((exp) => exp.type?.toLowerCase() === typeKey).length;
    };

    // Build tabs dynamically based on types that have actual data
    const availableTabs = computed(() => {
        const allExp = allExperiences.value ?? [];
        const typesWithData = new Set(allExp.map((exp) => exp.type?.toLowerCase()));

        if (typesWithData.size === 0 && !allExperiencesLoading.value) {
            return [];
        }

        // Use API types if available, filtered by those with data
        if (experienceTypes.value && experienceTypes.value.length > 0) {
            return experienceTypes.value
                .filter((type: ExperienceType) => typesWithData.has(type.name.toLowerCase()))
                .map((type: ExperienceType) => {
                    const key = type.name.toLowerCase();
                    const count = getTypeCount(key);
                    const label = typeLabelMap[key] || type.name.charAt(0).toUpperCase() + type.name.slice(1);
                    return {
                        key,
                        label: `${label} (${count})`,
                        icon: type.icon || typeIconMap[key] || 'folder',
                    };
                });
        }

        // Fallback: build tabs from experience types directly
        return Array.from(typesWithData).map((type) => {
            const count = getTypeCount(type);
            const label = typeLabelMap[type] || type.charAt(0).toUpperCase() + type.slice(1);
            return {
                key: type,
                label: `${label} (${count})`,
                icon: typeIconMap[type] || 'folder',
            };
        });
    });

    // Active type from URL-synced filters
    const activeType = computed({
        get: () => {
            const urlType = filters.value.type;
            const tabs = availableTabs.value;

            // If URL type exists and is valid, use it
            if (urlType && tabs.some((t) => t.key === urlType)) {
                return urlType;
            }

            // Fallback to first tab
            return tabs[0]?.key ?? '';
        },
        set: (val: string) => setFilter('type', val),
    });

    // Set initial tab from URL or default to first available
    // Only run when tabs are loaded and no valid type is set
    watch(
        availableTabs,
        (tabs) => {
            if (tabs.length === 0) {
                return;
            }

            const currentType = filters.value.type;
            const isValidType = tabs.some((t) => t.key === currentType);

            // Only set default if no type or invalid type
            const firstTab = tabs[0];
            if ((!currentType || !isValidType) && firstTab) {
                setFilter('type', firstTab.key);
            }
        },
        { immediate: true },
    );

    // Fetch experiences by type (server-side filtering)
    const {
        data: experiences,
        isLoading: experiencesLoading,
        isError: experiencesError,
        refetch: refetchExperiences,
    } = useExperiencesByType(activeType);

    // Total experiences count
    const totalExperiences = computed(() => experiences.value?.length ?? 0);

    // Loading & Error states
    const isLoading = computed(() => experiencesLoading.value || typesLoading.value || allExperiencesLoading.value);
    const hasError = computed(() => experiencesError.value || typesError.value);
    const hasAnyData = computed(() => (experiences.value?.length ?? 0) > 0);

    // Top skills from stats (all skills, no limit)
    const topSkills = computed(() => stats.value?.topSkills ?? []);

    // Hero stats
    const heroStats = computed(() => [
        {
            value: stats.value?.totalYears ?? 0,
            label: 'Années d\'expérience',
            suffix: '+',
            icon: 'calendar',
        },
        {
            value: stats.value?.companiesCount ?? 0,
            label: 'Entreprises',
            suffix: '',
            icon: 'building-2',
        },
        {
            value: topSkills.value.length,
            label: 'Stacks',
            suffix: '+',
            icon: 'code',
        },
    ]);

    // Retry handler
    const handleRetry = () => {
        refetchExperiences();
        refetchTypes();
        refetchStats();
    };

    // Announce tab changes for accessibility
    watch(activeType, (newType) => {
        const tab = availableTabs.value.find((t) => t.key === newType);
        if (tab) {
            const labelWithoutCount = tab.label.replace(/\s*\(\d+\)$/, '');
            announce(`Affichage: ${labelWithoutCount}`);
            scrollToTop('smooth');
        }
    });

    // Announce loaded data
    watch(
        experiences,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('expériences', list.length);
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

    .experience-page {
        min-height: 100vh;
    }

    // Tabs wrapper
    .tabs-wrapper {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: center;
        margin-bottom: vars.$spacing-xl;
    }

    // Single type indicator
    .single-type-indicator {
        @include mix.flex(column, center, center, vars.$spacing-xs);

        margin-bottom: vars.$spacing-xl;

        &__count {
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;
        }
    }

    // Timeline section
    .timeline-section {
        position: relative;
        z-index: 5;
        min-height: 400px;
    }

    .timeline-loader {
        max-width: 800px;
        margin: 0 auto;
    }

    .timeline-content {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    // Empty state styling
    :deep(.timeline-empty-state) {
        max-width: 500px;
        margin: vars.$spacing-xl auto;
        padding: vars.$spacing-xxl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.06);
    }

    // Skills section
    .skills-section {
        position: relative;
        z-index: 5;
        max-width: 900px;
        margin: vars.$spacing-xxl auto 0;
        padding: vars.$spacing-xl vars.$spacing-xxl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        &__heading {
            justify-content: center;
            margin-bottom: vars.$spacing-lg;
        }

        &__list {
            @include mix.flex(row, center, center, vars.$spacing-xs);

            flex-wrap: wrap;
        }

        &__badge {
            animation: badgeFadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            animation-delay: var(--badge-delay, 0ms);
            opacity: 0;

            &:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.2);
            }
        }

        &__summary {
            @include mix.flex(row, center, center, vars.$spacing-xxs);

            margin: vars.$spacing-lg 0 0;
            padding-top: vars.$spacing-md;
            border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;

            :deep(svg) {
                color: vars.$success-color;
            }
        }
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

    @keyframes badgeFadeIn {
        from {
            opacity: 0;
            transform: translateY(10px) scale(0.95);
        }

        to {
            opacity: 1;
            transform: translateY(0) scale(1);
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

    .fade-up-enter-active {
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-up-leave-active {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-up-enter-from {
        opacity: 0;
        transform: translateY(30px);
    }

    .fade-up-leave-to {
        opacity: 0;
        transform: translateY(-20px);
    }

    // Reduced motion support
    .content--no-motion {
        .timeline-content,
        .skills-section__badge {
            animation: none;
            opacity: 1;
        }

        .slide-fade-enter-active,
        .slide-fade-leave-active,
        .fade-up-enter-active,
        .fade-up-leave-active {
            transition: none;
        }
    }

    // Responsive - Tablet
    @include mix.responsive(tablet) {
        .skills-section {
            padding: vars.$spacing-lg;
            margin-left: vars.$spacing-md;
            margin-right: vars.$spacing-md;
        }
    }

    // Responsive - Mobile
    @include mix.responsive(mobile) {
        .content {
            padding: vars.$spacing-xl 0;
        }

        .tabs-wrapper {
            padding: 0 vars.$spacing-md;
        }

        .skills-section {
            padding: vars.$spacing-md;
            margin-left: vars.$spacing-sm;
            margin-right: vars.$spacing-sm;

            &__list {
                gap: vars.$spacing-xxs;
            }

            &__summary {
                font-size: vars.$font-size-sm;
            }
        }
    }
</style>
