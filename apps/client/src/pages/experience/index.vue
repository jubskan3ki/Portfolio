<template>
    <div class="experience-page">
        <Hero
            title="Expérience & Formation"
            description="Mon parcours professionnel et académique dans le développement web et logiciel."
            badge="Parcours"
            variant="light"
        >
            <template #stats>
                <ClientOnly>
                    <StatCard
                        v-for="stat in heroStats"
                        :key="stat.label"
                        :value="stat.value"
                        :label="stat.label"
                        :icon="stat.icon"
                        :suffix="stat.suffix"
                        variant="light"
                    />
                </ClientOnly>
            </template>
        </Hero>

        <Main variant="default" size="large" :custom-class="prefersReducedMotion ? 'content--no-motion' : ''">
            <ClientOnly>
                <template #fallback>
                    <div class="page-content-placeholder" style="min-height: 1100px" />
                </template>
            <div v-if="availableTabs.length > 1" class="tabs-wrapper">
                <NavigationTabs v-model="activeType" :tabs="availableTabs" variant="glass" />
            </div>

            <div v-else-if="availableTabs.length === 1 && availableTabs[0]" class="single-type-indicator">
                <Badge :text="availableTabs[0].label" variant="primary" size="lg" />
                <span class="single-type-indicator__count">
                    {{ totalExperiences }} expérience{{ totalExperiences > 1 ? 's' : '' }}
                </span>
            </div>

            <div
                :id="`panel-${activeType}`"
                class="timeline-section"
                role="tabpanel"
                :aria-labelledby="`tab-${activeType}`"
            >
                <h2 class="sr-only">{{ activeTypeHeading }}</h2>
                <Transition name="slide-fade" mode="out-in">
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

                    <EmptyState
                        v-else-if="!hasAnyData"
                        key="empty-all"
                        icon="briefcase"
                        title="Aucune expérience disponible"
                        description="Les expériences seront ajoutées prochainement."
                        size="lg"
                        custom-class="timeline-empty-state"
                    />

                    <div v-else :key="activeType" class="timeline-content">
                        <ExperienceTimeline
                            :experiences="experiences"
                            :show-header="false"
                            custom-class="timeline--enhanced"
                        />
                    </div>
                </Transition>
            </div>

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
                        <component
                            :is="getSkillLink(skill.skill) ? 'NuxtLink' : 'span'"
                            v-for="(skill, index) in topSkills"
                            :key="skill.skill"
                            :to="getSkillLink(skill.skill) ? `/stacks/${getSkillLink(skill.skill)}` : undefined"
                            class="skills-section__badge-link"
                        >
                            <Badge
                                :text="skill.skill"
                                variant="primary"
                                size="md"
                                class="skills-section__badge"
                                :style="{ '--badge-delay': `${index * 50}ms` }"
                            />
                        </component>
                    </div>
                    <p v-if="stats?.totalYears" class="skills-section__summary">
                        <BaseIcon name="trending-up" :size="16" />
                        <span>{{ stats.totalYears }}+ années d'expérience cumulée</span>
                    </p>
                </div>
            </Transition>
            </ClientOnly>
        </Main>

        <ClientOnly>
            <CTA
                title="Intéressé par mon profil ?"
                description="Discutons de vos projets ou opportunités de collaboration."
                variant="light"
                :primary-button="{ label: 'Me contacter', to: ROUTES.CONTACT.path, icon: 'mail' }"
                :secondary-button="{ label: 'Voir mes projets', to: ROUTES.PROJECTS.path }"
            />
            <template #fallback>
                <div class="page-content-placeholder" style="min-height: 280px" />
            </template>
        </ClientOnly>
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
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
        experienceKeys,
        experiencesApi,
        useExperiences,
        useExperiencesByType,
        useExperienceTypes,
        useExperienceStats,
    } from '@/services/api/modules/experiences';
    import { stackKeys, stacksApi, useFeaturedStacks } from '@/services/api/modules/stacks';

    import type { ExperienceType } from '@/types/feature/experience';

    useExperienceSeo();

    const { announceLoaded, announce } = useAnnounce();
    const { scrollToTop } = useScrollToTop();
    const { prefersReducedMotion } = useReducedMotion();

    const { filters, setFilter } = useFilters(filterPresets.experiences);

    // SSR-prefetch to kill CLS on first paint.
    const queryClient = useQueryClient();
    await useAsyncData('experience-prefetch', async () => {
        await Promise.all([
            queryClient.prefetchQuery({
                queryKey: experienceKeys.list({ limit: 100 }),
                queryFn: () => experiencesApi.getAll({ limit: 100 }),
            }),
            queryClient.prefetchQuery({
                queryKey: experienceKeys.types(),
                queryFn: experiencesApi.getTypes,
            }),
            queryClient.prefetchQuery({
                queryKey: experienceKeys.stats(),
                queryFn: experiencesApi.getStats,
            }),
            queryClient.prefetchQuery({
                queryKey: stackKeys.featured(100),
                queryFn: () => stacksApi.getFeatured(100),
            }),
        ]);
        return true;
    });

    // limit=100 contourne la pagination pour filtrer côté client
    const { data: allExperiencesResponse, isLoading: allExperiencesLoading } = useExperiences({ limit: 100 });
    const allExperiences = computed(() => allExperiencesResponse.value?.data ?? []);

    const {
        data: experienceTypes,
        isLoading: typesLoading,
        isError: typesError,
        refetch: refetchTypes,
    } = useExperienceTypes();

    const { data: stats, refetch: refetchStats } = useExperienceStats();

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

    const getTypeCount = (typeKey: string): number => {
        return (allExperiences.value ?? []).filter((exp) => exp.type?.toLowerCase() === typeKey).length;
    };

    const availableTabs = computed(() => {
        const allExp = allExperiences.value ?? [];
        const typesWithData = new Set(allExp.map((exp) => exp.type?.toLowerCase()));

        if (typesWithData.size === 0 && !allExperiencesLoading.value) {
            return [];
        }

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

    const activeType = computed({
        get: () => {
            const urlType = filters.value.type;
            const tabs = availableTabs.value;

            if (urlType && tabs.some((t) => t.key === urlType)) {
                return urlType;
            }

            return tabs[0]?.key ?? '';
        },
        set: (val: string) => setFilter('type', val),
    });

    watch(
        availableTabs,
        (tabs) => {
            if (tabs.length === 0) {
                return;
            }

            const currentType = filters.value.type;
            const isValidType = tabs.some((t) => t.key === currentType);

            const firstTab = tabs[0];
            if ((!currentType || !isValidType) && firstTab) {
                setFilter('type', firstTab.key);
            }
        },
        { immediate: true },
    );

    const {
        data: experiences,
        isLoading: experiencesLoading,
        isError: experiencesError,
        refetch: refetchExperiences,
    } = useExperiencesByType(activeType);

    const totalExperiences = computed(() => experiences.value?.length ?? 0);

    const activeTypeHeading = computed(() => {
        const tab = availableTabs.value.find((t) => t.key === activeType.value);
        const label = tab?.label.replace(/\s*\(\d+\)$/, '') ?? 'Expériences';
        return label;
    });

    const isLoading = computed(() => experiencesLoading.value || typesLoading.value || allExperiencesLoading.value);
    const hasError = computed(() => experiencesError.value || typesError.value);
    const hasAnyData = computed(() => (experiences.value?.length ?? 0) > 0);

    const topSkills = computed(() => stats.value?.topSkills ?? []);

    const { data: allStacksData } = useFeaturedStacks(100);
    const skillStackMap = computed(() => {
        const stacks = allStacksData.value ?? [];
        const map = new Map<string, string>();
        for (const stack of stacks) {
            map.set(stack.name.toLowerCase(), stack.slug);
        }
        return map;
    });
    const getSkillLink = (skillName: string): string | undefined => {
        return skillStackMap.value.get(skillName.toLowerCase());
    };

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

    const handleRetry = () => {
        refetchExperiences();
        refetchTypes();
        refetchStats();
    };

    watch(activeType, (newType) => {
        const tab = availableTabs.value.find((t) => t.key === newType);
        if (tab) {
            const labelWithoutCount = tab.label.replace(/\s*\(\d+\)$/, '');
            announce(`Affichage: ${labelWithoutCount}`);
            scrollToTop('smooth');
        }
    });

    watch(
        experiences,
        (list) => {
            if (list && list.length > 0) {
                announceLoaded('expériences', list.length);
            }
        },
        { once: true },
    );

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

    .tabs-wrapper {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: center;
        margin-bottom: vars.$spacing-xl;
    }

    .single-type-indicator {
        @include mix.flex(column, center, center, vars.$spacing-xs);

        margin-bottom: vars.$spacing-xl;

        &__count {
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;
        }
    }

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

        &__badge-link {
            text-decoration: none;
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

    .slide-fade-enter-active {
        transition:
            opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1),
            transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .slide-fade-leave-active {
        transition:
            opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
            transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
        transition:
            opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1),
            transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-up-leave-active {
        transition:
            opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
            transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-up-enter-from {
        opacity: 0;
        transform: translateY(30px);
    }

    .fade-up-leave-to {
        opacity: 0;
        transform: translateY(-20px);
    }

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

    @include mix.responsive(tablet) {
        .skills-section {
            padding: vars.$spacing-lg;
            margin-left: vars.$spacing-md;
            margin-right: vars.$spacing-md;
        }
    }

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
