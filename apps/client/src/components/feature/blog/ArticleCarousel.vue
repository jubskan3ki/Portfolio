<template>
    <ContentCarousel
        :items="displayedArticles"
        :is-loading="isLoading"
        :is-error="!!error"
        loading-label="Chargement des articles..."
        :error-message="error ?? 'Une erreur est survenue lors du chargement des articles.'"
        empty-title="Aucun article"
        empty-description="Aucun article n'est disponible pour le moment."
        :slides-desktop="3"
        :autoplay="autoplay"
        :autoplay-interval="autoplaySpeed"
        :show-dots="showDots"
        @change="emit('change', $event)"
    >
        <template v-if="title || subtitle" #header>
            <div class="article-carousel__header">
                <h2 v-if="title" class="article-carousel__title">{{ title }}</h2>
                <p v-if="subtitle" class="article-carousel__subtitle">{{ subtitle }}</p>
            </div>
        </template>

        <template #slide="{ item }">
            <ArticleCard
                :article="item as Article"
                hoverable
                :show-footer="showFooter"
                :show-stats="showStats"
                :excerpt-length="excerptLength"
                custom-class="article-carousel__card"
            />
        </template>
    </ContentCarousel>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
    import ContentCarousel from '@/components/ui/ContentCarousel.vue';

    import type { Article, ArticleCarouselProps } from '@/types/feature/blog';

    type Props = ArticleCarouselProps;

    const props = withDefaults(defineProps<Props>(), {
        limit: 5,
        showFooter: true,
        showStats: true,
        showDots: true,
        showViewAllButton: true,
        viewAllLink: '/blog',
        autoplay: false,
        autoplaySpeed: 5000,
        excerptLength: 100,
        isLoading: false,
        error: null,
    });

    const emit = defineEmits<{ change: [index: number] }>();

    const displayedArticles = computed(() => {
        let filteredArticles = [...props.articles];

        if (props.category) {
            filteredArticles = filteredArticles.filter(
                (article) => article.category?.toLowerCase() === props.category?.toLowerCase(),
            );
        }

        return filteredArticles.slice(0, props.limit);
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .article-carousel {
        &__header {
            text-align: center;
            margin-bottom: vars.$spacing-xl;
        }

        &__title {
            font-weight: 700;
            margin-bottom: vars.$spacing-xs;
            color: vars.$black-light;
        }

        &__subtitle {
            color: vars.$gray-dark;
            max-width: 800px;
            margin: 0 auto;
        }

        &__card {
            height: 100%;
        }
    }
</style>
