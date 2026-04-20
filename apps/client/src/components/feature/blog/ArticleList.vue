<template>
    <div class="article-list" :class="[`article-list--${layout}`, customClass]">
        <div v-if="title || $slots.header" class="article-list__header">
            <slot name="header">
                <h2 v-if="title" class="article-list__title">{{ title }}</h2>
                <p v-if="description" class="article-list__description">{{ description }}</p>
            </slot>
        </div>

        <QueryStateHandler
            :loading="loading"
            :error="error"
            :empty="!articles || articles.length === 0"
            :loading-message="loadingText"
            :empty-title="emptyTitle"
            :empty-description="emptyDescription"
            empty-icon="info"
            :retryable="retryable"
            :retry-text="retryText"
            @retry="$emit('retry')"
        >
            <template v-if="$slots['empty-action']" #empty-action>
                <slot name="empty-action"></slot>
            </template>

            <div
                class="article-list__grid"
                :class="[`article-list__grid--${layout}`, { 'article-list__grid--animated': !prefersReducedMotion }]"
            >
                <div
                    v-for="(article, index) in articles"
                    :key="article.id ?? index"
                    class="article-list__item"
                    :style="!prefersReducedMotion ? { '--index': index } : undefined"
                >
                    <slot name="article" :article="article" :index="index">
                        <ArticleCard
                            :article="article"
                            :hoverable="cardHoverable"
                            :flat="cardFlat"
                            :bordered="cardBordered"
                            :excerpt-length="excerptLength"
                            :show-footer="showFooter"
                            :show-stats="showStats"
                            :read-more-text="readMoreText"
                        />
                    </slot>
                </div>
            </div>
        </QueryStateHandler>

        <div v-if="showPagination && totalPages > 1" class="article-list__pagination">
            <Pagination
                :current-page="currentPage"
                :total-pages="totalPages"
                @update:current-page="$emit('update:currentPage', $event)"
                @page-change="$emit('pageChange', $event)"
            />
        </div>

        <div v-if="$slots.footer" class="article-list__footer">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    import QueryStateHandler from '@/components/feedback/QueryStateHandler.vue';
    import Pagination from '@/components/navigation/Pagination.vue';

    import type { ArticleListProps } from '@/types/feature/blog';

    type Props = ArticleListProps;

    withDefaults(defineProps<Props>(), {
        articles: () => [],
        title: '',
        description: '',
        layout: 'grid',
        loading: false,
        error: '',
        retryable: false,
        retryText: 'Réessayer',
        loadingText: 'Chargement des articles...',
        emptyTitle: 'Aucun article trouvé',
        emptyDescription: 'Il n\'y a pas d\'articles disponibles pour le moment.',
        currentPage: 1,
        totalPages: 1,
        showPagination: true,
        cardHoverable: true,
        cardFlat: false,
        cardBordered: false,
        excerptLength: 150,
        showFooter: true,
        showStats: true,
        readMoreText: 'Lire la suite',
        customClass: '',
        prefersReducedMotion: false,
    });

    defineEmits<{
        'update:currentPage': [page: number];
        pageChange: [page: number];
        retry: [];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .article-list {
        width: 100%;

        &__header {
            margin-bottom: vars.$spacing-lg;
            text-align: center;
        }

        &__title {
            margin-bottom: vars.$spacing-xs;
            position: relative;
            display: inline-block;

            &::after {
                content: '';
                display: block;
                width: 50px;
                height: 3px;
                background-color: vars.$primary-color;
                margin: vars.$spacing-xs auto 0;
            }
        }

        &__description {
            max-width: 700px;
            margin: 0 auto;
            color: vars.$gray-dark;
        }

        &__grid {
            display: grid;
            grid-gap: vars.$spacing-lg;

            &--grid {
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));

                @include mix.responsive(mobile) {
                    grid-template-columns: 1fr;
                }
            }

            &--list {
                grid-template-columns: 1fr;
            }

            &--compact {
                grid-template-columns: 1fr;
                grid-gap: vars.$spacing-md;
            }

            // Animations staggered
            &--animated {
                .article-list__item {
                    opacity: 0;
                    animation: fadeInUp 0.5s ease forwards;
                    animation-delay: calc(var(--index, 0) * 60ms);
                }
            }
        }

        &__item {
            height: 100%;
        }

        &__pagination {
            margin-top: vars.$spacing-xl;
            display: flex;
            justify-content: center;
        }

        &__footer {
            margin-top: vars.$spacing-lg;
        }

        /* Variante liste */
        &--list {
            .article-list__grid {
                grid-template-columns: 1fr;
            }
        }
    }

    // Animation keyframes
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
</style>
