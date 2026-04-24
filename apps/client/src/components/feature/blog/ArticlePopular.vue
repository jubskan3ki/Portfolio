<template>
    <div class="popular-articles">
        <h3 v-if="showTitle" class="popular-articles__title">
            <BaseIcon name="trending-up" :size="16" />
            {{ title }}
        </h3>

        <div class="popular-articles__list">
            <BaseLink
                v-for="article in articles"
                :key="article.id"
                :to="`/blog/${article.slug}`"
                class="popular-articles__item"
            >
                <div class="popular-articles__image">
                    <BaseImage
                        v-if="article.image"
                        :src="article.image"
                        :alt="article.title"
                        :width="56"
                        :height="56"
                        object-fit="cover"
                        :show-placeholder="false"
                        class="popular-articles__img"
                    />
                    <BaseIcon v-else name="file-text" :size="20" />
                </div>

                <div class="popular-articles__info">
                    <h4 class="popular-articles__name">{{ article.title }}</h4>
                    <div class="popular-articles__meta">
                        <span>{{ formatRelative(article.date) }}</span>
                        <span v-if="article.readTime" class="popular-articles__dot"></span>
                        <span v-if="article.readTime">{{ article.readTime }} min</span>
                        <span v-if="article.views" class="popular-articles__dot"></span>
                        <span v-if="article.views" class="popular-articles__views">
                            <BaseIcon name="eye" :size="11" />
                            {{ formatViews(article.views) }}
                        </span>
                    </div>
                </div>
            </BaseLink>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import { formatRelativeDate } from '@/services/utils/date';
    import { formatViews } from '@/services/utils/helpers';

    import type { ArticlePopularProps } from '@/types/feature/blog';

    withDefaults(defineProps<ArticlePopularProps>(), {
        articles: () => [],
        title: 'Articles populaires',
        showTitle: true,
    });

    const formatRelative = (date: string | Date) => formatRelativeDate(date);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .popular-articles {
        padding: vars.$spacing-lg;

        &__title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            padding-bottom: vars.$spacing-sm;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        }

        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxxs;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-xs;
            text-decoration: none;
            border: 1px solid transparent;
            border-radius: vars.$border-radius-md;
            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.06);
                border-color: fn.color-alpha(vars.$primary-color, 0.18);
                text-decoration: none;
                transform: translateY(-1px);
                box-shadow: 0 2px 6px fn.color-alpha(vars.$primary-color, 0.06);

                .popular-articles__name {
                    color: vars.$primary-color;
                }

                .popular-articles__img {
                    transform: scale(1.05);
                }
            }

            &:active {
                transform: translateY(0);
            }

            &:focus {
                outline: none;
            }

            &:focus-visible {
                outline: 2px solid fn.color-alpha(vars.$primary-color, 0.5);
                outline-offset: 2px;
            }

            @media (prefers-reduced-motion: reduce) {
                transition: none;

                &:hover,
                &:active {
                    transform: none;

                    .popular-articles__img {
                        transform: none;
                    }
                }
            }
        }

        &__image {
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 56px;
            height: 56px;
            overflow: hidden;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-md;
            color: vars.$text-muted;
        }

        &__img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        &__info {
            flex: 1;
            min-width: 0;
        }

        &__name {
            margin: 0 0 vars.$spacing-xxxs;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            line-height: 1.4;
            transition: color 0.2s ease;

            @include mix.truncate(2);
        }

        &__meta {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            font-size: 11px;
            color: vars.$text-muted;
        }

        &__dot {
            width: 3px;
            height: 3px;
            background: vars.$text-muted;
            border-radius: 50%;
            opacity: 0.4;
        }

        &__views {
            display: inline-flex;
            align-items: center;
            gap: 2px;
        }
    }

    // Reduced motion
    @media (prefers-reduced-motion: reduce) {
        .popular-articles__img {
            transition: none;
        }
    }
</style>
