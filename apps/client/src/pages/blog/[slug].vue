<template>
    <div class="article-page">
        <!-- Reading Progress Bar -->
        <div
            v-if="progressVisible"
            class="reading-progress"
            :style="{ width: `${progress}%` }"
            role="progressbar"
            :aria-valuenow="Math.round(progress)"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="Progression de lecture"
        ></div>

        <!-- Loading -->
        <LoadingState v-if="isLoading" message="Chargement de l'article..." size="lg" />

        <!-- Error -->
        <div v-else-if="error" class="article-error">
            <ErrorMessage
                :message="error?.message ?? 'Une erreur est survenue'"
                action-text="Retour au blog"
                :to="ROUTES.BLOG"
            />
        </div>

        <template v-else-if="currentArticle">
            <!-- Hero -->
            <Hero
                :title="currentArticle.title"
                :transition-key="currentArticle.slug"
                variant="secondary"
                has-meta
            >
                <template #meta>
                    <div class="hero__meta-item">
                        <BaseIcon name="folder" :size="16" />
                        <span>{{ getCategoryName(currentArticle.category) }}</span>
                    </div>
                    <div class="hero__meta-item">
                        <BaseIcon name="calendar" :size="16" />
                        <span>{{ formatDate(currentArticle.date) }}</span>
                    </div>
                    <div class="hero__meta-item">
                        <BaseIcon name="clock" :size="16" />
                        <span>{{ currentArticle.readTime }} min de lecture</span>
                    </div>
                    <div v-if="currentArticle.views" class="hero__meta-item">
                        <BaseIcon name="eye" :size="16" />
                        <span>{{ currentArticle.views }} vues</span>
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
                <!-- Article Intro -->
                <div class="article-intro">
                    <div v-if="currentArticle.image" class="article-intro__media">
                        <BaseImage
                            :src="currentArticle.image"
                            :alt="currentArticle.title"
                            object-fit="cover"
                            width="320"
                            height="240"
                            class="article-intro__img"
                        />
                        <div class="article-intro__overlay"></div>
                    </div>
                    <div class="article-intro__body">
                        <span class="article-intro__label">Introduction</span>
                        <p class="article-intro__text">{{ currentArticle.excerpt }}</p>
                    </div>
                </div>

                <DetailPageLayout>
                    <template #main>
                        <!-- Article Body -->
                        <article ref="articleRef" class="detail-card">
                            <ArticleBlockRenderer :blocks="contentBlocks" />
                        </article>
                    </template>

                    <template #sidebar>
                        <!-- Table of Contents -->
                        <nav v-if="tocHeadings.length" class="toc-card" aria-label="Table des matières">
                            <div class="toc-card__header">
                                <span class="toc-card__label">Sommaire</span>
                                <span class="toc-card__count">{{ tocHeadings.length }}</span>
                            </div>
                            <div class="toc-card__track">
                                <ul class="toc-card__list">
                                    <li
                                        v-for="(heading, index) in tocHeadings"
                                        :key="heading.id"
                                        class="toc-card__item"
                                        :class="[
                                            `toc-card__item--h${heading.level}`,
                                            { 'toc-card__item--active': activeHeadingId === heading.id },
                                        ]"
                                    >
                                        <a :href="`#${heading.id}`" class="toc-card__link">
                                            <span class="toc-card__index">{{
                                                String(index + 1).padStart(2, '0')
                                            }}</span>
                                            <span class="toc-card__text">{{ heading.text }}</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </nav>

                        <!-- Related Stacks (maillage interne) -->
                        <div v-if="resolvedStacks.length" class="sidebar-card">
                            <h3 class="sidebar-card__heading">
                                <BaseIcon name="layers" :size="16" class="sidebar-card__heading-icon" />
                                Technologies
                            </h3>
                            <div class="article-stacks">
                                <NuxtLink
                                    v-for="stack in resolvedStacks"
                                    :key="stack.slug"
                                    :to="`/stacks/${stack.slug}`"
                                    class="article-stacks__item"
                                >
                                    <img
                                        v-if="stack.logo"
                                        :src="stack.logo"
                                        :alt="stack.name"
                                        class="article-stacks__logo"
                                        width="20"
                                        height="20"
                                        loading="lazy"
                                    />
                                    <span>{{ stack.name }}</span>
                                </NuxtLink>
                            </div>
                        </div>

                        <!-- Share -->
                        <ShareCard :title="currentArticle.title" />

                        <!-- Popular Articles -->
                        <div v-if="popularArticles?.length" class="sidebar-card sidebar-card--flush">
                            <PopularArticles :articles="popularArticles" show-title />
                        </div>

                        <!-- Tags -->
                        <div v-if="currentArticle.tags?.length" class="sidebar-card sidebar-card--flush">
                            <ArticleTags :tags="currentArticle.tags" display="simple" show-title />
                        </div>
                    </template>
                </DetailPageLayout>
            </Main>

            <!-- Related Articles -->
            <Section v-if="displayedRelatedArticles?.length" variant="light" size="default">
                <template #header>
                    <h2 class="article-page__section-title">
                        <BaseIcon name="book-open" :size="22" class="article-page__section-icon" />
                        À lire ensuite
                    </h2>
                </template>
                <div class="related-grid">
                    <ArticleCard v-for="article in displayedRelatedArticles" :key="article.id" :article="article" />
                </div>
            </Section>

            <!-- CTA -->
            <CTA
                key="article-cta"
                title="Vous avez un projet ?"
                description="Discutons de vos besoins et voyons comment je peux vous aider."
                variant="secondary"
                :primary-button="{
                    label: 'Me contacter',
                    to: ROUTES.CONTACT.path,
                    icon: 'mail',
                }"
                :secondary-button="{
                    label: 'Tous les articles',
                    to: ROUTES.BLOG.path,
                }"
            />
        </template>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import ArticleBlockRenderer from '@/components/feature/blog/ArticleBlockRenderer.vue';
    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    import PopularArticles from '@/components/feature/blog/ArticlePopular.vue';
    import ArticleTags from '@/components/feature/blog/ArticleTags.vue';
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
    import { useArticleSeo } from '@/composables/seo/useSeo';
    import { useReadingProgress } from '@/composables/ui/useReadingProgress';
    import { useTableOfContents } from '@/composables/ui/useTableOfContents';
    import { ROUTES } from '@/config/routes';
    import {
        useArticle,
        usePopularArticles,
        useRelatedArticles,
        useRecordArticleView,
    } from '@/services/api/modules/articles';
    import { useFeaturedStacks } from '@/services/api/modules/stacks';
    import { normalizeContent } from '@/services/utils/contentParser';

    import type { BreadcrumbSeoItem } from '@/types/composables/seo';

    const router = useRouter();

    // Validate slug parameter
    const { slug } = useDetailSlug(ROUTES.BLOG.path);

    // API
    const { data: currentArticle, isLoading, isError, error } = useArticle(slug);
    const { data: popularArticles } = usePopularArticles(3);
    const { data: relatedArticles } = useRelatedArticles(slug);

    // Normalize content blocks (handles raw markdown, JSON string, or mixed blocks)
    const contentBlocks = computed(() => normalizeContent(currentArticle.value?.content));

    // Related articles (dedicated endpoint with popular fallback)
    const displayedRelatedArticles = computed(() => {
        if (relatedArticles.value?.length) {
            return relatedArticles.value;
        }
        return popularArticles.value?.filter((a) => a.slug !== slug.value) ?? [];
    });

    // Resolve article tags against known stacks for internal linking
    const { data: allStacks } = useFeaturedStacks(100);
    const resolvedStacks = computed(() => {
        const tags = currentArticle.value?.tags ?? [];
        const stacks = allStacks.value ?? [];
        if (!tags.length || !stacks.length) {
            return [];
        }
        return stacks.filter((s) =>
            tags.some((tag) => s.name.toLowerCase() === tag.toLowerCase()),
        );
    });

    // Record view
    const { mutate: recordView } = useRecordArticleView();
    useViewRecording(currentArticle, recordView);

    // Accessibility
    const { announceNavigation } = useAnnounce();

    // Breadcrumb
    const breadcrumbItems = ref<BreadcrumbSeoItem[]>([]);

    // SEO
    watch(
        currentArticle,
        (article) => {
            if (article) {
                useArticleSeo(article);
                const { items } = useBreadcrumbSeo({
                    meta: {
                        title: article.title,
                        category: article.category,
                    },
                });
                breadcrumbItems.value = items.value;
                announceNavigation(`Article: ${article.title}`);
            }
        },
        { immediate: true },
    );

    // Error redirect
    watch(isError, (hasError) => {
        if (hasError) {
            router.push(ROUTES.BLOG.path);
        }
    });

    // Reading progress
    const articleRef = ref<HTMLElement | null>(null);
    const { progress, isVisible: progressVisible } = useReadingProgress(articleRef);

    // Table of contents (uses normalized blocks)
    const { headings: tocHeadings, activeId: activeHeadingId } = useTableOfContents(contentBlocks);

    // Formatting
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        }).format(date);
    };

    const getCategoryName = (category: string) => category;
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .article-page {
        min-height: 100vh;

        &__section-title {
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

        &__section-icon {
            color: vars.$secondary-color;
            flex-shrink: 0;
        }
    }

    /* Reading Progress */
    .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, vars.$primary-color, vars.$secondary-color);
        z-index: vars.$z-index-fixed;
        transition: width 150ms linear;

        @media (prefers-reduced-motion: reduce) {
            transition: none;
        }
    }

    .article-error {
        min-height: 60vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: vars.$spacing-xl 0;
    }

    /* Detail Cards */
    .detail-card {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg;
        }
    }

    /* Article Intro */
    .article-intro {
        display: flex;
        align-items: stretch;
        gap: 0;
        margin-bottom: vars.$spacing-xl;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        overflow: hidden;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        @include mix.responsive(tablet) {
            flex-direction: column;
        }

        &__media {
            flex-shrink: 0;
            width: 320px;
            position: relative;

            @include mix.responsive(tablet) {
                width: 100%;
                height: 200px;
            }
        }

        &__img {
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
        }

        &__overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to right,
                transparent 30%,
                fn.color-alpha(vars.$white, 0.4) 70%,
                fn.color-alpha(vars.$white, 0.95) 100%
            );
            pointer-events: none;

            @include mix.responsive(tablet) {
                background: linear-gradient(
                    to bottom,
                    transparent 20%,
                    fn.color-alpha(vars.$white, 0.4) 65%,
                    fn.color-alpha(vars.$white, 0.95) 100%
                );
            }
        }

        &__body {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: vars.$spacing-xl;
            gap: vars.$spacing-sm;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-lg;
            }
        }

        &__label {
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: vars.$primary-color;
        }

        &__text {
            font-size: vars.$font-size-lg;
            color: vars.$text-secondary;
            line-height: 1.75;
            margin: 0;

            @include mix.responsive(mobile) {
                font-size: vars.$font-size-base;
            }
        }
    }

    /* Sidebar Cards */
    .sidebar-card {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;
        overflow: hidden;

        &--flush {
            padding: 0;
        }

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

    /* TOC Card */
    .toc-card {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        overflow: hidden;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        &__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: vars.$spacing-md vars.$spacing-lg;
            border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.12);
        }

        &__label {
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: vars.$text-muted;
        }

        &__count {
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-medium;
            color: vars.$primary-color;
            background: fn.color-alpha(vars.$primary-color, 0.08);
            padding: 2px 8px;
            border-radius: vars.$border-radius-full;
            line-height: 1.4;
        }

        &__track {
            padding: vars.$spacing-sm vars.$spacing-lg vars.$spacing-lg;
        }

        &__list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
        }

        &__item {
            &--h3 {
                padding-left: vars.$spacing-lg;
            }

            &--h4 {
                padding-left: calc(vars.$spacing-lg * 2);
            }

            &--active .toc-card__link {
                color: vars.$text-primary;

                .toc-card__index {
                    color: vars.$primary-color;
                }

                .toc-card__text {
                    font-weight: vars.$font-weight-medium;
                }
            }
        }

        &__link {
            display: flex;
            align-items: baseline;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-xs 0;
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            text-decoration: none;
            transition: color 0.2s ease;

            &:hover {
                color: vars.$text-primary;

                .toc-card__index {
                    color: vars.$primary-color;
                }
            }
        }

        &__index {
            font-size: 10px;
            font-weight: vars.$font-weight-medium;
            font-variant-numeric: tabular-nums;
            color: fn.color-alpha(vars.$text-muted, 0.4);
            flex-shrink: 0;
            transition: color 0.2s ease;
        }

        &__text {
            line-height: 1.5;
        }
    }

    /* Article Stacks (maillage interne) */
    .article-stacks {
        display: flex;
        flex-wrap: wrap;
        gap: vars.$spacing-xs;

        &__item {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: 4px 10px;
            font-size: vars.$font-size-sm;
            color: vars.$text-secondary;
            background: fn.color-alpha(vars.$primary-color, 0.06);
            border-radius: vars.$border-radius-full;
            text-decoration: none;
            transition: background 0.2s ease, color 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.14);
                color: vars.$primary-color;
            }
        }

        &__logo {
            width: 20px;
            height: 20px;
            object-fit: contain;
            flex-shrink: 0;
        }
    }

    /* Related Grid */
    .related-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: vars.$spacing-lg;
    }
</style>
