<template>
    <BaseContentCard
        :to="articleLink"
        :image="article.image"
        :image-alt="article.title"
        placeholder-icon="file-text"
        :badge="article.category"
        :title="article.title"
        :description="truncatedExcerpt"
        :tags="article.tags"
        :max-tags="maxTags"
        :transition-key="article.slug"
        :eager="eager"
        :data-slug="article.slug"
        :prefetch="false"
        :show-footer="showFooter"
        :class="customClass"
    >
        <template #before-title>
            <div v-if="article.date || article.readTime" class="article-card__meta">
                <time v-if="article.date" :datetime="article.date" class="article-card__meta-item">
                    {{ formattedDate }}
                </time>
                <span v-if="article.readTime" class="article-card__meta-item"> {{ article.readTime }} min </span>
            </div>
        </template>

        <template #footer-left>
            <span v-if="showStats && article.views" class="article-card__views">
                <BaseIcon name="eye" :size="12" />
                {{ formatViews(article.views) }}
            </span>
        </template>

        <template #footer-right>
            <span class="article-card__action">
                {{ readMoreText }}
                <BaseIcon name="arrow-right" :size="14" class="article-card__arrow" />
            </span>
        </template>
    </BaseContentCard>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseContentCard from '@/components/base/BaseContentCard.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { formatDateShort } from '@/services/utils/date';
    import { formatViews, truncateText } from '@/services/utils/helpers';

    import type { ArticleCardProps } from '@/types/feature/blog';

    const props = withDefaults(defineProps<ArticleCardProps>(), {
        hoverable: true,
        flat: false,
        excerptLength: 120,
        customClass: '',
        showTags: true,
        maxTags: 3,
        eager: false,
        showFooter: true,
        showStats: true,
        readMoreText: 'Lire l\'article',
    });

    const articleLink = computed(() => (props.article.slug ? `/blog/${props.article.slug}` : ''));

    const formattedDate = computed(() => formatDateShort(props.article.date));
    const truncatedExcerpt = computed(() => truncateText(props.article.excerpt || '', props.excerptLength));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .article-card__meta {
        display: flex;
        align-items: center;
        gap: vars.$spacing-sm;
        margin-bottom: vars.$spacing-xs;
        min-height: 1.2em;
        line-height: 1.2;
    }

    .article-card__meta-item {
        font-size: vars.$font-size-xs;
        color: vars.$text-muted;
        white-space: nowrap;
    }

    .article-card__views {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxxs;
        font-size: vars.$font-size-xs;
        color: vars.$text-muted;
    }

    .article-card__action {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        font-size: vars.$font-size-sm;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-muted;
        transition: color 0.2s ease;
    }

    .article-card__arrow {
        opacity: 0.5;
        transition: all 0.2s ease;
    }

    :deep(.content-card):hover {
        .article-card__arrow {
            transform: translateX(4px);
            opacity: 1;
        }

        .article-card__action {
            color: vars.$primary-color;
        }
    }
</style>
