<template>
    <div class="project-page">
        <LoadingState v-if="isLoading" message="Chargement du projet..." size="lg" />

        <div v-else-if="error" class="project-error">
            <ErrorMessage :message="errorMessage" action-text="Retour aux projets" :to="ROUTES.PROJECTS" />
        </div>

        <template v-else-if="currentProject">
            <Hero :title="currentProject.title" :transition-key="currentProject.slug" variant="primary" has-meta>
                <template v-if="breadcrumbItems.length > 1" #breadcrumb>
                    <Breadcrumb :items="breadcrumbItems" variant="hero" separator="chevron" />
                </template>
                <template #meta>
                    <div class="hero__meta-item">
                        <BaseIcon name="folder" :size="16" />
                        <span>{{ currentProject.category }}</span>
                    </div>
                    <div class="hero__meta-item">
                        <BaseIcon name="calendar" :size="16" />
                        <span>{{ formatDate(currentProject.date) }}</span>
                    </div>
                    <div v-if="currentProject.status" class="hero__meta-item">
                        <BaseIcon name="activity" :size="16" />
                        <span>{{ formatStatus(currentProject.status) }}</span>
                    </div>
                    <div v-if="currentProject.views" class="hero__meta-item">
                        <BaseIcon name="eye" :size="16" />
                        <span>{{ currentProject.views }} vues</span>
                    </div>
                </template>
            </Hero>

            <Main variant="default" size="large">
                <DetailPageLayout sidebar-width="360px">
                    <template #main>
                        <div class="project-identity">
                            <div class="project-identity__image-wrapper">
                                <BaseImage
                                    :src="currentProject.image"
                                    :alt="currentProject.title"
                                    :lazy="false"
                                    preload
                                    object-fit="cover"
                                    width="600"
                                    height="400"
                                    class="project-identity__image"
                                />
                            </div>
                            <div class="project-identity__content">
                                <h2 class="project-identity__name">{{ currentProject.title }}</h2>
                                <p class="project-identity__description">{{ currentProject.description }}</p>
                            </div>
                        </div>

                        <div v-if="currentProject.longDescription" class="detail-card">
                            <h2 class="detail-card__heading">
                                <BaseIcon name="info" :size="20" class="detail-card__heading-icon" />
                                Description du projet
                            </h2>
                            <p class="detail-card__text">{{ currentProject.longDescription }}</p>
                        </div>

                        <div v-if="currentProject.features && currentProject.features.length > 0" class="detail-card">
                            <h2 class="detail-card__heading">
                                <BaseIcon name="zap" :size="20" class="detail-card__heading-icon" />
                                Fonctionnalités principales
                            </h2>
                            <div class="features-grid">
                                <div
                                    v-for="(feature, index) in currentProject.features"
                                    :key="feature"
                                    class="feature-item"
                                >
                                    <span class="feature-item__number">{{ String(index + 1).padStart(2, '0') }}</span>
                                    <div class="feature-item__content">
                                        <span class="feature-item__text">{{ feature }}</span>
                                    </div>
                                    <BaseIcon name="check" :size="14" class="feature-item__check" />
                                </div>
                            </div>
                        </div>
                    </template>

                    <template #sidebar>
                        <div class="sidebar-card">
                            <h3 class="sidebar-card__heading">
                                <BaseIcon name="cpu" :size="16" class="sidebar-card__heading-icon" />
                                Stack technique
                            </h3>
                            <div class="tech-grid">
                                <component
                                    :is="tech.slug ? NuxtLink : 'div'"
                                    v-for="tech in resolvedTechnologies"
                                    :key="tech.name"
                                    :to="tech.slug ? `/stacks/${tech.slug}` : undefined"
                                    class="tech-item"
                                    :class="{ 'tech-item--linked': tech.slug }"
                                >
                                    <StackLogo
                                        :stack="{
                                            name: tech.name,
                                            logo: tech.logo ? resolveMediaUrl(tech.logo) : undefined,
                                        }"
                                        size="md"
                                        class="tech-item__logo"
                                    />
                                    <span class="tech-item__name">{{ tech.name }}</span>
                                    <BaseIcon
                                        v-if="tech.slug"
                                        name="arrow-right"
                                        :size="12"
                                        class="tech-item__arrow"
                                    />
                                </component>
                            </div>
                        </div>

                        <div v-if="currentProject.links" class="sidebar-card">
                            <h3 class="sidebar-card__heading">
                                <BaseIcon name="link" :size="16" class="sidebar-card__heading-icon" />
                                Liens du projet
                            </h3>
                            <div class="project-links">
                                <BaseLink
                                    v-if="currentProject.links.demo"
                                    :to="currentProject.links.demo"
                                    target="_blank"
                                    class="project-links__item"
                                >
                                    <BaseIcon name="external-link" :size="16" />
                                    <span>Voir la démo</span>
                                </BaseLink>
                                <BaseLink
                                    v-if="currentProject.links.github"
                                    :to="currentProject.links.github"
                                    target="_blank"
                                    class="project-links__item"
                                >
                                    <BaseIcon name="github" :size="16" />
                                    <span>Code source</span>
                                </BaseLink>
                                <BaseLink
                                    v-if="currentProject.links.documentation"
                                    :to="currentProject.links.documentation"
                                    target="_blank"
                                    class="project-links__item"
                                >
                                    <BaseIcon name="book" :size="16" />
                                    <span>Documentation</span>
                                </BaseLink>
                            </div>
                        </div>

                        <ShareCard :title="currentProject.title" />
                    </template>
                </DetailPageLayout>
            </Main>

            <Section v-if="relatedProjects.length > 0" variant="light" size="default">
                <template #header>
                    <h2 class="project-page__section-title">
                        <span class="project-page__section-icon">
                            <BaseIcon name="grid" :size="20" />
                        </span>
                        Projets similaires
                    </h2>
                    <p class="project-page__section-subtitle">Découvrez d'autres réalisations</p>
                </template>
                <div class="related-grid">
                    <ProjectCard v-for="project in relatedProjects" :key="project.id" :project="project" />
                </div>
            </Section>

            <CTA
                key="project-detail-cta"
                title="Vous avez un projet similaire en tête ?"
                description="Discutons de la façon dont je peux vous aider à concrétiser votre vision."
                variant="primary"
                :primary-button="{
                    label: 'Me contacter',
                    to: ROUTES.CONTACT.path,
                    icon: 'mail',
                }"
                :secondary-button="{
                    label: 'Voir tous les projets',
                    to: ROUTES.PROJECTS.path,
                }"
            />
        </template>
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
    import { computed, resolveComponent, unref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseImage from '@/components/base/BaseImage.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
    import StackLogo from '@/components/feature/stacks/StackLogo.vue';
    import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
    import DetailPageLayout from '@/components/layouts/DetailPageLayout.vue';
    import Main from '@/components/layouts/Main.vue';
    import Section from '@/components/layouts/Section.vue';
    import LoadingState from '@/components/loaders/LoadingState.vue';
    import Breadcrumb from '@/components/navigation/Breadcrumb.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import ShareCard from '@/components/ui/ShareCard.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useDetailSlug } from '@/composables/data/useDetailSlug';
    import { useViewRecording } from '@/composables/data/useViewRecording';
    import { useBreadcrumbSeo } from '@/composables/seo/useBreadcrumbSeo';
    import { useProjectSeo } from '@/composables/seo/useSeo';
    import { ROUTES } from '@/config/routes';
    import {
        projectKeys,
        projectsApi,
        useProject,
        useFeaturedProjects,
        useRecordProjectView,
    } from '@/services/api/modules/projects';
    import { useFeaturedStacks } from '@/services/api/modules/stacks';
    import { resolveMediaUrl } from '@/services/utils/helpers';

    import type { BreadcrumbSeoItem } from '@/types/composables/seo';

    const NuxtLink = resolveComponent('NuxtLink');

    const router = useRouter();

    const { slug } = useDetailSlug(ROUTES.PROJECTS.path);

    // shrink the SSR payload and unblock LCP on the text paragraph.
    const queryClient = useQueryClient();
    await useAsyncData(
        () => `project-${unref(slug)}`,
        async () => {
            const slugValue = unref(slug);
            if (!slugValue) {
                return true;
            }
            await Promise.all([
                queryClient.prefetchQuery({
                    queryKey: projectKeys.detail(slugValue),
                    queryFn: () => projectsApi.getBySlug(slugValue),
                }),
                queryClient.prefetchQuery({
                    queryKey: projectKeys.featured(),
                    queryFn: () => projectsApi.getFeatured(4),
                }),
            ]);
            return true;
        },
        { watch: [slug] },
    );

    const { data: currentProject, isLoading, isError, error } = useProject(slug);
    const { data: featuredProjects } = useFeaturedProjects(4);
    const { data: allStacks } = useFeaturedStacks(100, {
        enabled: computed(() => import.meta.client),
    });

    const { mutate: recordView } = useRecordProjectView();
    useViewRecording(currentProject, recordView);

    const { announceNavigation } = useAnnounce();

    // SEO side effects (JSON-LD schema, meta tags) are driven by the watch.
    watch(
        currentProject,
        (project) => {
            if (project) {
                useProjectSeo(project);
                useBreadcrumbSeo({
                    meta: {
                        title: project.title,
                        category: project.category || undefined,
                    },
                });
                announceNavigation(`Projet: ${project.title}`);
            }
        },
        { immediate: true },
    );

    // Template-side breadcrumb: pure computed from currentProject, avoids the
    // ref+watch roundtrip and is ready at first SSR paint (no slot flash).
    const breadcrumbItems = computed<BreadcrumbSeoItem[]>(() => {
        const project = currentProject.value;
        const crumbs: BreadcrumbSeoItem[] = [
            { label: 'Accueil', to: '/' },
            { label: 'Projets', to: '/projects' },
        ];
        if (!project) {
            return crumbs;
        }
        if (project.category) {
            crumbs.push({
                label: project.category,
                to: `/projects?category=${encodeURIComponent(project.category)}`,
            });
        }
        crumbs.push({ label: project.title, to: `/projects/${project.slug}` });
        return crumbs;
    });

    watch(isError, (hasError) => {
        if (hasError) {
            router.push(ROUTES.PROJECTS);
        }
    });

    const errorMessage = computed(() => {
        if (!error.value) {
            return 'Projet non trouvé';
        }
        return (error.value as Error).message || 'Projet non trouvé';
    });

    const relatedProjects = computed(() => {
        return featuredProjects.value?.filter((p: { slug: string }) => p.slug !== slug.value) ?? [];
    });

    // Couleur stable dérivée du nom (fallback lettre)
    const stringToColor = (str: string): string => {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const hue = Math.abs(hash) % 360;
        return `hsl(${hue}, 55%, 45%)`;
    };

    // Indexe les stacks par nom (O(1) lookup au lieu de O(N) par find).
    const stacksByName = computed(() => {
        const map = new Map<string, { logo?: string; slug?: string }>();
        (allStacks.value ?? []).forEach((s) => map.set(s.name.toLowerCase(), s));
        return map;
    });

    // Résout chaque tech en stack (logo, slug) pour maillage interne
    const resolvedTechnologies = computed(() => {
        const techs = currentProject.value?.technologies ?? [];
        const map = stacksByName.value;

        return techs.map((techName: string) => {
            const match = map.get(techName.toLowerCase());
            return {
                name: techName,
                logo: match?.logo || '',
                slug: match?.slug || '',
                color: stringToColor(techName),
            };
        });
    });

    const STATUS_LABELS: Record<string, string> = {
        in_progress: 'En cours de développement',
        completed: 'Terminé',
        maintained: 'Maintenu',
        archived: 'Archivé',
        planned: 'Planifié',
        on_hold: 'En pause',
    };

    const formatStatus = (status: string): string => {
        return STATUS_LABELS[status.toLowerCase()] ?? status;
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        }).format(date);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .project-page {
        min-height: 100vh;
    }

    .project-error {
        min-height: 60vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: vars.$spacing-xl 0;
    }

    .project-identity {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xl;
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);
        min-height: 168px;
        contain: layout paint;

        @include mix.responsive(mobile) {
            flex-direction: column;
            text-align: center;
            padding: vars.$spacing-lg;
            gap: vars.$spacing-md;
        }

        &__image-wrapper {
            flex-shrink: 0;
            width: 120px;
            height: 120px;
            border-radius: vars.$border-radius-lg;
            overflow: hidden;
            border: 1px solid fn.color-alpha(vars.$border-color, 0.1);

            @include mix.responsive(mobile) {
                width: 100px;
                height: 100px;
            }
        }

        &__image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__name {
            color: vars.$text-primary;
            font-weight: vars.$font-weight-bold;
            margin-bottom: vars.$spacing-xs;
        }

        &__description {
            line-height: 1.7;
            color: vars.$text-secondary;
        }
    }

    .detail-card {
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);
        min-height: 120px;
        contain: layout paint;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg;
        }

        &__heading {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin-bottom: vars.$spacing-md;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;
        }

        &__heading-icon {
            color: vars.$secondary-color;
            flex-shrink: 0;
        }

        &__text {
            margin-bottom: vars.$spacing-md;
            line-height: 1.7;
            color: vars.$text-secondary;

            &:last-child {
                margin-bottom: 0;
            }
        }
    }

    .features-grid {
        display: flex;
        flex-direction: column;
        gap: 0;
        animation: features-fade-in 0.35s ease-out both;
        will-change: opacity, transform;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md 0;
        border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.12);

        &:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        &:first-child {
            padding-top: 0;
        }

        &:hover {
            .feature-item__number {
                color: vars.$white;

                &::before {
                    opacity: 1;
                }
            }

            .feature-item__check {
                opacity: 1;
                transform: translateX(0);
            }

            .feature-item__text {
                color: vars.$text-primary;
            }
        }

        &__number {
            position: relative;
            isolation: isolate;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: vars.$border-radius-sm;
            background: transparent;
            border: 1.5px solid fn.color-alpha(vars.$primary-color, 0.3);
            color: vars.$primary-color;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;

            &::before {
                content: '';
                position: absolute;
                inset: -1.5px;
                border-radius: inherit;
                background: vars.$primary-color;
                opacity: 0;
                transition: opacity 0.2s ease;
                z-index: -1;
                pointer-events: none;
            }
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__text {
            line-height: 1.5;
            color: vars.$text-secondary;
        }

        &__check {
            flex-shrink: 0;
            color: vars.$primary-color;
            opacity: 0;
            transform: translateX(-4px);
            transition:
                opacity 0.2s ease,
                transform 0.2s ease;
        }
    }

    @keyframes features-fade-in {
        from {
            opacity: 0;
            transform: translateY(6px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .sidebar-card {
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);

        &__heading {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;
        }

        &__heading-icon {
            color: vars.$secondary-color;
            flex-shrink: 0;
        }
    }

    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: vars.$spacing-xs;
    }

    .tech-item {
        --tech-hover-bg: #{fn.color-alpha(vars.$border-color, 0.04)};
        --tech-hover-border: transparent;

        display: flex;
        flex-direction: column;
        align-items: center;
        gap: vars.$spacing-xs;
        padding: vars.$spacing-sm;
        background: transparent;
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-md;
        text-decoration: none;
        position: relative;
        isolation: isolate;

        &::before {
            content: '';
            position: absolute;
            inset: -1px;
            border-radius: inherit;
            background: var(--tech-hover-bg);
            border: 1px solid var(--tech-hover-border);
            opacity: 0;
            transition: opacity 0.2s ease;
            z-index: -1;
            pointer-events: none;
        }

        &:hover::before {
            opacity: 1;
        }

        &--linked {
            --tech-hover-bg: #{fn.color-alpha(vars.$primary-color, 0.04)};
            --tech-hover-border: #{fn.color-alpha(vars.$primary-color, 0.2)};

            cursor: pointer;

            &:hover {
                .tech-item__arrow {
                    opacity: 1;
                }

                .tech-item__name {
                    color: vars.$primary-color;
                }
            }
        }

        &__logo {
            // Le composant StackLogo gère dimensions/bg/letter lui-même.
            // Ce wrapper class existe pour cible override contextuelle si besoin.
        }

        &__name {
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            text-align: center;
            @include mix.truncate(1);
            max-width: 100%;
        }

        &__arrow {
            position: absolute;
            top: vars.$spacing-xxs;
            right: vars.$spacing-xxs;
            color: vars.$primary-color;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
    }

    .project-links {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxs;

        &__item {
            position: relative;
            isolation: isolate;
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-sm vars.$spacing-md;
            background: fn.color-alpha(vars.$primary-color, 0.04);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.08);
            border-radius: vars.$border-radius-md;
            color: vars.$text-secondary;
            text-decoration: none;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-medium;

            &::before {
                content: '';
                position: absolute;
                inset: -1px;
                border-radius: inherit;
                background: fn.color-alpha(vars.$primary-color, 0.08);
                border: 1px solid fn.color-alpha(vars.$primary-color, 0.15);
                opacity: 0;
                transition: opacity 0.2s ease;
                z-index: -1;
                pointer-events: none;
            }

            &:hover {
                color: vars.$primary-color;

                &::before {
                    opacity: 1;
                }
            }
        }
    }

    .project-page__section-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: vars.$spacing-sm;
        color: vars.$text-primary;
        letter-spacing: vars.$letter-spacing-tight;

        &::before,
        &::after {
            content: '';
            flex: 1;
            max-width: 80px;
            height: 1px;
            background: linear-gradient(90deg, transparent, fn.color-alpha(vars.$primary-color, 0.2));
        }

        &::after {
            background: linear-gradient(90deg, fn.color-alpha(vars.$primary-color, 0.2), transparent);
        }
    }

    .project-page__section-icon {
        color: vars.$secondary-color;
        flex-shrink: 0;
    }

    .project-page__section-subtitle {
        color: vars.$text-secondary;
        line-height: vars.$line-height-relaxed;
        max-width: 600px;
        margin: vars.$spacing-xs auto 0;
    }

    .related-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: vars.$spacing-lg;
    }
</style>
