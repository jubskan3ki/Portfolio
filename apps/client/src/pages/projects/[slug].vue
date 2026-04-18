<template>
    <div class="project-page">
        <!-- Loading -->
        <LoadingState v-if="isLoading" message="Chargement du projet..." size="lg" />

        <!-- Error -->
        <div v-else-if="error" class="project-error">
            <ErrorMessage :message="errorMessage" action-text="Retour aux projets" :to="ROUTES.PROJECTS" />
        </div>

        <template v-else-if="currentProject">
            <!-- Hero -->
            <Hero
                :title="currentProject.title"
                :transition-key="currentProject.slug"
                variant="primary"
                has-meta
            >
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

            <!-- Breadcrumb -->
            <Breadcrumb
                v-if="breadcrumbItems.length > 1"
                :items="breadcrumbItems"
                separator="chevron"
            />

            <!-- Content -->
            <Main variant="default" size="large">
                <DetailPageLayout sidebar-width="360px">
                    <template #main>
                        <!-- Project Identity (image + title + short desc) -->
                        <div class="project-identity">
                            <div class="project-identity__image-wrapper">
                                <BaseImage
                                    :src="currentProject.image"
                                    :alt="currentProject.title"
                                    :lazy="false"
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

                        <!-- Long Description -->
                        <div v-if="currentProject.longDescription" class="detail-card">
                            <h2 class="detail-card__heading">
                                <BaseIcon name="info" :size="20" class="detail-card__heading-icon" />
                                Description du projet
                            </h2>
                            <p class="detail-card__text">{{ currentProject.longDescription }}</p>
                        </div>

                        <!-- Features -->
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
                                    :style="{ animationDelay: `${index * 0.05}s` }"
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
                        <!-- Technologies -->
                        <div class="sidebar-card">
                            <h3 class="sidebar-card__heading">
                                <BaseIcon name="cpu" :size="16" class="sidebar-card__heading-icon" />
                                Stack technique
                            </h3>
                            <div class="tech-grid">
                                <template v-for="tech in resolvedTechnologies" :key="tech.name">
                                    <NuxtLink
                                        v-if="tech.slug"
                                        :to="`/stacks/${tech.slug}`"
                                        class="tech-item tech-item--linked"
                                    >
                                        <div class="tech-item__logo">
                                            <BaseImage
                                                v-if="tech.logo"
                                                :src="tech.logo"
                                                :alt="tech.name"
                                                :width="36"
                                                :height="36"
                                                :show-placeholder="false"
                                                class="tech-item__img"
                                            />
                                            <span
                                                v-else
                                                class="tech-item__letter"
                                                :style="{ backgroundColor: tech.color }"
                                            >
                                                {{ tech.name.charAt(0).toUpperCase() }}
                                            </span>
                                        </div>
                                        <span class="tech-item__name">{{ tech.name }}</span>
                                        <BaseIcon name="arrow-right" :size="12" class="tech-item__arrow" />
                                    </NuxtLink>
                                    <div v-else class="tech-item">
                                        <div class="tech-item__logo">
                                            <BaseImage
                                                v-if="tech.logo"
                                                :src="tech.logo"
                                                :alt="tech.name"
                                                :width="36"
                                                :height="36"
                                                :show-placeholder="false"
                                                class="tech-item__img"
                                            />
                                            <span
                                                v-else
                                                class="tech-item__letter"
                                                :style="{ backgroundColor: tech.color }"
                                            >
                                                {{ tech.name.charAt(0).toUpperCase() }}
                                            </span>
                                        </div>
                                        <span class="tech-item__name">{{ tech.name }}</span>
                                    </div>
                                </template>
                            </div>
                        </div>

                        <!-- Links -->
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

                        <!-- Share -->
                        <ShareCard :title="currentProject.title" />
                    </template>
                </DetailPageLayout>
            </Main>

            <!-- Related Projects -->
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

            <!-- CTA -->
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
    import { computed, ref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
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
    import { useProject, useFeaturedProjects, useRecordProjectView } from '@/services/api/modules/projects';
    import { useFeaturedStacks } from '@/services/api/modules/stacks';

    import type { BreadcrumbSeoItem } from '@/types/composables/seo';

    const router = useRouter();

    // Validate slug parameter
    const { slug } = useDetailSlug(ROUTES.PROJECTS.path);

    // API Queries
    const { data: currentProject, isLoading, isError, error } = useProject(slug);
    const { data: featuredProjects } = useFeaturedProjects(4);
    const { data: allStacks } = useFeaturedStacks(100);

    // Record view
    const { mutate: recordView } = useRecordProjectView();
    useViewRecording(currentProject, recordView);

    // Accessibility
    const { announceNavigation } = useAnnounce();

    // Breadcrumb
    const breadcrumbItems = ref<BreadcrumbSeoItem[]>([]);

    // SEO and accessibility
    watch(
        currentProject,
        (project) => {
            if (project) {
                useProjectSeo(project);
                const { items } = useBreadcrumbSeo({
                    meta: { title: project.title },
                });
                breadcrumbItems.value = items.value;
                announceNavigation(`Projet: ${project.title}`);
            }
        },
        { immediate: true },
    );

    // Redirect on error
    watch(isError, (hasError) => {
        if (hasError) {
            router.push(ROUTES.PROJECTS);
        }
    });

    // Error message
    const errorMessage = computed(() => {
        if (!error.value) {
            return 'Projet non trouvé';
        }
        return (error.value as Error).message || 'Projet non trouvé';
    });

    // Related projects (excluding current)
    const relatedProjects = computed(() => {
        return featuredProjects.value?.filter((p: { slug: string }) => p.slug !== slug.value) ?? [];
    });

    // Stable color from string (for fallback tech letters)
    const stringToColor = (str: string): string => {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const hue = Math.abs(hash) % 360;
        return `hsl(${hue}, 55%, 45%)`;
    };

    // Resolve tech names to stack objects (logos, slugs)
    const resolvedTechnologies = computed(() => {
        const techs = currentProject.value?.technologies ?? [];
        const stacks = allStacks.value ?? [];

        return techs.map((techName: string) => {
            const match = stacks.find((s) => s.name.toLowerCase() === techName.toLowerCase());
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

    /* ========================
       Project Identity
       ======================== */
    .project-identity {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xl;
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);

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

    /* ========================
       Detail Cards
       ======================== */
    .detail-card {
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);

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

    /* ========================
       Features
       ======================== */
    .features-grid {
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md 0;
        border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.12);
        transition: all vars.$transition-base;
        animation: feature-fade-in 0.35s ease-out both;

        &:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        &:first-child {
            padding-top: 0;
        }

        &:hover {
            .feature-item__number {
                background: vars.$primary-color;
                color: vars.$white;
                border-color: vars.$primary-color;
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
            transition: all vars.$transition-base;
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
            transition: all vars.$transition-base;
        }
    }

    @keyframes feature-fade-in {
        from {
            opacity: 0;
            transform: translateY(4px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ========================
       Sidebar Cards
       ======================== */
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

    /* ========================
       Tech Grid
       ======================== */
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: vars.$spacing-xs;
    }

    .tech-item {
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
        transition: all 0.2s ease;

        &--linked {
            cursor: pointer;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.04);
                border-color: fn.color-alpha(vars.$primary-color, 0.2);

                .tech-item__arrow {
                    opacity: 1;
                }

                .tech-item__name {
                    color: vars.$primary-color;
                }
            }
        }

        &:not(&--linked):hover {
            background: fn.color-alpha(vars.$border-color, 0.04);
        }

        &__logo {
            width: 40px;
            height: 40px;
            border-radius: vars.$border-radius-sm;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            background: fn.color-alpha(vars.$border-color, 0.06);
        }

        &__img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 5px;
        }

        &__letter {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: vars.$font-weight-semibold;
            font-size: vars.$font-size-sm;
            color: vars.$white;
            border-radius: vars.$border-radius-sm;
        }

        &__name {
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            text-align: center;
            @include mix.truncate(1);
            max-width: 100%;
            transition: color 0.2s ease;
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

    /* ========================
       Project Links
       ======================== */
    .project-links {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxs;

        &__item {
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
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.08);
                border-color: fn.color-alpha(vars.$primary-color, 0.15);
                color: vars.$primary-color;
            }
        }
    }

    /* ========================
       Section Title
       ======================== */
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

    /* ========================
       Related Grid
       ======================== */
    .related-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: vars.$spacing-lg;
    }
</style>
