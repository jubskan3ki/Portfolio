<template>
    <div class="stack-page">
        <LoadingState v-if="isLoading" message="Chargement du stack..." size="lg" />

        <div v-else-if="error" class="stack-error">
            <ErrorMessage :message="errorMessage" action-text="Retour aux stacks" :to="ROUTES.STACKS" />
        </div>

        <template v-else-if="currentStack">
            <Hero :title="currentStack.name" :transition-key="currentStack.slug" variant="dark" has-meta>
                <template v-if="breadcrumbItems.length > 1" #breadcrumb>
                    <Breadcrumb :items="breadcrumbItems" variant="hero" separator="chevron" />
                </template>
                <template #meta>
                    <div class="hero__meta-item">
                        <BaseIcon name="folder" :size="16" />
                        <span>{{ currentStack.category }}</span>
                    </div>
                    <div v-if="currentStack.firstRelease" class="hero__meta-item">
                        <BaseIcon name="calendar" :size="16" />
                        <span>Première version : {{ currentStack.firstRelease }}</span>
                    </div>
                    <div v-if="currentStack.license" class="hero__meta-item">
                        <BaseIcon name="code" :size="16" />
                        <span>Licence : {{ currentStack.license }}</span>
                    </div>
                </template>

                <template #links>
                    <BaseLink
                        v-if="currentStack.website"
                        variant="white"
                        :to="currentStack.website"
                        target="_blank"
                        class="hero__link"
                    >
                        <BaseIcon name="external-link" :size="16" />
                        <span>{{ currentStack.websiteLabel || 'Site officiel' }}</span>
                    </BaseLink>

                    <BaseLink
                        v-if="currentStack.github"
                        variant="white"
                        :to="currentStack.github"
                        target="_blank"
                        class="hero__link"
                    >
                        <BaseIcon name="github" :size="16" />
                        <span>{{ currentStack.githubLabel || 'GitHub' }}</span>
                    </BaseLink>
                </template>
            </Hero>

            <Main variant="default" size="large">
                <DetailPageLayout>
                    <template #main>
                        <div class="stack-identity">
                            <StackLogo
                                :stack="currentStack"
                                size="xl"
                                :transition-name="`hero-media-${currentStack.slug}`"
                                class="stack-identity__logo-wrapper"
                            />
                            <div class="stack-identity__content">
                                <h2 class="stack-identity__name">{{ currentStack.name }}</h2>
                                <p class="stack-identity__description">{{ currentStack.description }}</p>
                            </div>
                        </div>

                        <div v-if="currentStack.content" class="detail-card">
                            <h2 class="detail-card__heading">
                                <BaseIcon name="cpu" :size="20" class="detail-card__icon" />
                                Détails techniques
                            </h2>
                            <p class="detail-card__text">{{ currentStack.content }}</p>
                        </div>

                        <div v-if="relatedStacks.length" class="detail-card">
                            <h2 class="detail-card__heading">
                                <BaseIcon name="layers" :size="20" class="detail-card__icon" />
                                Stacks similaires
                            </h2>
                            <div class="related-grid">
                                <NuxtLink
                                    v-for="stack in relatedStacks"
                                    :key="stack.slug"
                                    :to="`/stacks/${stack.slug}`"
                                    class="related-grid__card"
                                >
                                    <div class="related-grid__logo">
                                        <BaseImage
                                            v-if="stack.logo"
                                            :src="stack.logo"
                                            :alt="stack.name"
                                            :width="40"
                                            :height="40"
                                            :show-placeholder="false"
                                            class="related-grid__img"
                                        />
                                        <div v-else class="related-grid__letter">
                                            {{ stack.name.charAt(0).toUpperCase() }}
                                        </div>
                                    </div>
                                    <span class="related-grid__name">{{ stack.name }}</span>
                                    <span class="related-grid__category">{{ stack.category }}</span>
                                    <BaseIcon name="arrow-right" :size="14" class="related-grid__arrow" />
                                </NuxtLink>
                            </div>
                        </div>
                    </template>

                    <template #sidebar>
                        <div class="sidebar-card">
                            <h3 class="sidebar-card__heading">
                                <BaseIcon name="award" :size="16" />
                                Mon expérience
                            </h3>
                            <div class="experience-info">
                                <div class="experience-info__item">
                                    <BaseIcon name="clock" :size="18" class="experience-info__icon" />
                                    <div>
                                        <span class="experience-info__value">{{ experienceDisplay }}</span>
                                        <span class="experience-info__label">d'expérience</span>
                                    </div>
                                </div>
                            </div>
                            <div class="skill-level">
                                <ProgressBar
                                    :value="currentStack.level"
                                    :max="5"
                                    :label="`Niveau : ${skillLabel}`"
                                    variant="primary"
                                    size="md"
                                    :steps="5"
                                    striped
                                />
                            </div>
                        </div>

                        <StackTags :tags="currentStack.tags" />

                        <ShareCard :title="currentStack.name" />
                    </template>
                </DetailPageLayout>
            </Main>

            <Section v-if="currentStack.resources?.length" variant="light" size="default">
                <template #header>
                    <h2 class="stack-page__section-title">
                        <BaseIcon name="book-open" :size="22" class="stack-page__section-icon" />
                        Ressources utiles
                    </h2>
                    <p class="stack-page__section-subtitle">
                        Documentation, tutoriels et guides pour {{ currentStack.name }}
                    </p>
                </template>
                <div class="stack-page__resources-grid">
                    <BaseLink
                        v-for="resource in currentStack.resources"
                        :key="resource.url"
                        :to="resource.url"
                        target="_blank"
                        class="resource-card"
                    >
                        <div class="resource-card__icon-wrapper">
                            <BaseIcon :name="resourceIcon(resource.type)" :size="22" />
                        </div>
                        <div class="resource-card__content">
                            <h3 class="resource-card__title">{{ resource.title }}</h3>
                            <p class="resource-card__description">{{ resource.description }}</p>
                        </div>
                        <BaseIcon name="arrow-right" :size="16" class="resource-card__arrow" />
                    </BaseLink>
                </div>
            </Section>

            <Section v-if="stackArticles?.length" variant="default" size="default">
                <template #header>
                    <h2 class="stack-page__section-title">
                        <BaseIcon name="file-text" :size="22" class="stack-page__section-icon" />
                        Articles liés à {{ currentStack.name }}
                    </h2>
                </template>
                <div class="stack-page__articles-grid">
                    <ArticleCard v-for="article in stackArticles" :key="article.id" :article="article" />
                </div>
            </Section>

            <Section v-if="stackProjects?.length" variant="light" size="default">
                <template #header>
                    <h2 class="stack-page__section-title">
                        <BaseIcon name="grid" :size="22" class="stack-page__section-icon" />
                        Projets réalisés avec {{ currentStack.name }}
                    </h2>
                    <p class="stack-page__section-subtitle">Découvrez les projets utilisant ce stack</p>
                </template>
                <div class="stack-page__projects-grid">
                    <ProjectCard v-for="project in stackProjects" :key="project.id" :project="project" />
                </div>
            </Section>

            <CTA
                key="stack-detail-cta"
                :title="`Besoin d'un développeur ${currentStack.name} ?`"
                :description="ctaDescription"
                variant="dark"
                :primary-button="{
                    label: 'Me contacter',
                    to: ROUTES.CONTACT.path,
                    icon: 'mail',
                }"
                :secondary-button="{
                    label: 'Voir tous les stacks',
                    to: ROUTES.STACKS.path,
                }"
            />
        </template>
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
    import { computed, ref, unref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
    import StackLogo from '@/components/feature/stacks/StackLogo.vue';
    import StackTags from '@/components/feature/stacks/StackTags.vue';
    import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
    import DetailPageLayout from '@/components/layouts/DetailPageLayout.vue';
    import Main from '@/components/layouts/Main.vue';
    import Section from '@/components/layouts/Section.vue';
    import LoadingState from '@/components/loaders/LoadingState.vue';
    import Breadcrumb from '@/components/navigation/Breadcrumb.vue';
    import CTA from '@/components/ui/CTA.vue';
    import Hero from '@/components/ui/Hero.vue';
    import ProgressBar from '@/components/ui/ProgressBar.vue';
    import ShareCard from '@/components/ui/ShareCard.vue';
    import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useDetailSlug } from '@/composables/data/useDetailSlug';
    import { useBreadcrumbSeo } from '@/composables/seo/useBreadcrumbSeo';
    import { useStackSeo } from '@/composables/seo/useSeo';
    import { ROUTES } from '@/config/routes';
    import {
        stackKeys,
        stacksApi,
        useStack,
        useFeaturedStacks,
        useStackProjects,
        useStackArticles,
    } from '@/services/api/modules/stacks';
    import { extractErrorStatus } from '@/services/utils/errors';

    import type { BreadcrumbSeoItem } from '@/types/composables/seo';
    import type { StackResourceType } from '@/types/feature/stacks';

    const { slug } = useDetailSlug(ROUTES.STACKS.path);

    // SSR-prefetch detail + sidebars (kills CLS on first paint).
    const queryClient = useQueryClient();
    const { error: detailError } = await useAsyncData(
        () => `stack-${unref(slug)}`,
        async () => {
            const slugValue = unref(slug);
            if (!slugValue) {
                return null;
            }
            let stack;
            try {
                stack = await stacksApi.getBySlug(slugValue);
                queryClient.setQueryData(stackKeys.detail(slugValue), stack);
            } catch (err) {
                const status = extractErrorStatus(err);
                throw createError({
                    statusCode: status === 404 ? 404 : 500,
                    statusMessage: status === 404 ? 'Stack introuvable' : 'Erreur de chargement',
                    fatal: true,
                });
            }
            await Promise.allSettled([
                queryClient.prefetchQuery({
                    queryKey: stackKeys.featured(5),
                    queryFn: () => stacksApi.getFeatured(5),
                }),
                queryClient.prefetchQuery({
                    queryKey: stackKeys.projects(slugValue),
                    queryFn: () => stacksApi.getProjects(slugValue),
                }),
                queryClient.prefetchQuery({
                    queryKey: stackKeys.articles(slugValue),
                    queryFn: () => stacksApi.getArticles(slugValue),
                }),
            ]);
            return stack;
        },
        { watch: [slug] },
    );

    if (detailError.value) {
        // Re-throw at setup level so Nuxt renders error.vue with the correct
        // status code. useAsyncData stores the error but does not propagate it.
        throw detailError.value;
    }

    const { data: currentStack, isLoading, error } = useStack(slug);
    const { data: featuredStacks } = useFeaturedStacks(5);
    const { data: stackProjects } = useStackProjects(slug);
    const { data: stackArticles } = useStackArticles(slug);

    const { announceNavigation } = useAnnounce();

    const breadcrumbItems = ref<BreadcrumbSeoItem[]>([]);

    watch(
        currentStack,
        (stack) => {
            if (stack) {
                useStackSeo(stack);
                const { items } = useBreadcrumbSeo({
                    meta: {
                        title: stack.name,
                        category: stack.category || undefined,
                    },
                });
                breadcrumbItems.value = items.value;
                announceNavigation(`Stack: ${stack.name}`);
            }
        },
        { immediate: true },
    );

    const errorMessage = computed(() => {
        if (!error.value) {
            return 'Stack non trouvé';
        }
        return (error.value as Error).message || 'Stack non trouvé';
    });

    const resourceIcon = (type: StackResourceType): string => {
        const icons: Record<StackResourceType, string> = {
            documentation: 'book',
            tutorial: 'play-circle',
            article: 'file-text',
            video: 'video',
            other: 'link',
        };
        return icons[type] || 'link';
    };

    const experienceDisplay = computed(() => {
        const months = currentStack.value?.experience ?? 0;
        const years = Math.floor(months / 12);
        const remainingMonths = months % 12;

        if (years === 0) {
            return `${months} mois`;
        }
        if (remainingMonths === 0) {
            return `${years} an${years > 1 ? 's' : ''}`;
        }
        return `${years} an${years > 1 ? 's' : ''} et ${remainingMonths} mois`;
    });

    const skillLabel = computed(() => {
        const level = currentStack.value?.level ?? 0;
        if (level >= 4.5) {
            return 'Expert';
        }
        if (level >= 3.5) {
            return 'Avancé';
        }
        if (level >= 2.5) {
            return 'Intermédiaire';
        }
        if (level >= 1.5) {
            return 'Junior';
        }
        return 'Débutant';
    });

    const ctaDescription = computed(() => {
        const name = currentStack.value?.name ?? '';
        return `Avec ${experienceDisplay.value} d'expérience en ${name}, je peux vous aider à réaliser votre projet.`;
    });

    const relatedStacks = computed(() => {
        if (currentStack.value?.relatedStacks?.length) {
            return currentStack.value.relatedStacks;
        }
        return featuredStacks.value?.filter((s) => s.slug !== slug.value) ?? [];
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stack-page {
        min-height: 100vh;
    }

    .stack-error {
        min-height: 60vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: vars.$spacing-xl 0;
    }

    .stack-identity {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(vars.$glass-blur);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        @include mix.responsive(mobile) {
            flex-direction: column;
            text-align: center;
            padding: vars.$spacing-lg;
            gap: vars.$spacing-md;
        }

        &__logo-wrapper {
            flex-shrink: 0;

            @include mix.responsive(mobile) {
                width: 80px;
                height: 80px;
                font-size: vars.$font-size-3xl;
            }
        }

        &__content {
            flex: 1;
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
        backdrop-filter: blur(vars.$glass-blur);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

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

        &__icon {
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

    .related-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: vars.$spacing-md;

        @include mix.responsive(mobile) {
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: vars.$spacing-sm;
        }

        &__card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-lg vars.$spacing-md;
            background: transparent;
            border: 1px solid fn.color-alpha(vars.$border-color, 0.15);
            border-radius: vars.$border-radius-lg;
            box-shadow: none;
            text-decoration: none;
            position: relative;
            cursor: pointer;
            transition: all vars.$transition-base;

            &:hover {
                transform: translateY(-4px);
                box-shadow: vars.$box-shadow;
                background: fn.color-alpha(vars.$white, 0.5);
                border-color: fn.color-alpha(vars.$primary-color, 0.25);

                .related-grid__arrow {
                    opacity: 1;
                    transform: translateX(4px);
                }

                .related-grid__logo {
                    transform: scale(1.08);
                }
            }
        }

        &__logo {
            width: 52px;
            height: 52px;
            border-radius: vars.$border-radius-md;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            background: vars.$bg-secondary;
            transition: transform vars.$transition-base;
        }

        &__img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 6px;
        }

        &__letter {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: vars.$font-weight-semibold;
            color: vars.$primary-color;
            background: fn.color-alpha(vars.$primary-color, 0.08);
            border-radius: vars.$border-radius-md;
        }

        &__name {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            text-align: center;
            @include mix.truncate(1);
            max-width: 100%;
        }

        &__category {
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
        }

        &__arrow {
            position: absolute;
            top: vars.$spacing-xs;
            right: vars.$spacing-xs;
            color: vars.$primary-color;
            opacity: 0;
            transition: all vars.$transition-base;
        }
    }

    .sidebar-card {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(vars.$glass-blur);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        &__heading {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;
        }
    }

    .skill-level {
        margin-top: vars.$spacing-md;
    }

    .stack-page__section-title {
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

    .stack-page__section-icon {
        color: vars.$secondary-color;
        flex-shrink: 0;
    }

    .stack-page__section-subtitle {
        color: vars.$text-secondary;
        line-height: vars.$line-height-relaxed;
        max-width: 600px;
        margin: vars.$spacing-xs auto 0;
    }

    .stack-page__resources-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: vars.$spacing-md;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }
    }

    .resource-card {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-lg;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(vars.$glass-blur);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-lg;
        box-shadow: vars.$box-shadow-xs;
        text-decoration: none;
        transition: all vars.$transition-base;

        &:hover {
            transform: translateY(-4px);
            box-shadow: vars.$box-shadow-medium;
            border-color: fn.color-alpha(vars.$primary-color, 0.25);

            .resource-card__arrow {
                opacity: 1;
                transform: translateX(4px);
            }

            .resource-card__icon-wrapper {
                background: vars.$primary-color;
                color: vars.$white;
            }
        }

        &__icon-wrapper {
            flex-shrink: 0;
            width: 48px;
            height: 48px;
            border-radius: vars.$border-radius-md;
            background: fn.color-alpha(vars.$primary-color, 0.08);
            color: vars.$primary-color;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all vars.$transition-base;
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            margin-bottom: vars.$spacing-xxxs;
        }

        &__description {
            font-size: vars.$font-size-sm;
            color: vars.$text-secondary;
            line-height: 1.5;
            @include mix.truncate(2);
        }

        &__arrow {
            flex-shrink: 0;
            color: vars.$primary-color;
            opacity: 0;
            transition: all vars.$transition-base;
        }
    }

    .stack-page__articles-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: vars.$spacing-lg;
    }

    .stack-page__projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: vars.$spacing-lg;
    }

    .experience-info {
        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
        }

        &__icon {
            color: vars.$primary-color;
            flex-shrink: 0;
        }

        &__value {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            margin-right: vars.$spacing-xxs;
        }

        &__label {
            color: vars.$text-secondary;
        }
    }
</style>
