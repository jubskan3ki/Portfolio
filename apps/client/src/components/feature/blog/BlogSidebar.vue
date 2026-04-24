<template>
    <aside ref="targetRef" class="blog-sidebar">
        <template v-if="shouldRender">
            <div class="blog-sidebar__slot blog-sidebar__slot--popular">
                <LazyArticlePopular :articles="popularArticles" title="Articles populaires" show-title />
            </div>

            <div v-if="categories?.length" class="blog-sidebar__slot blog-sidebar__slot--categories">
                <LazyArticleCategories
                    :model-value="selectedCategory"
                    :categories="categoriesWithAll"
                    :max-visible="8"
                    title="Catégories"
                    @update:model-value="(val) => emit('update:selectedCategory', val)"
                />
            </div>

            <div v-if="tags?.length" class="blog-sidebar__slot blog-sidebar__slot--tags">
                <LazyArticleTags
                    :model-value="selectedTags"
                    :tags="tags"
                    :max-visible="10"
                    title="Tags"
                    show-title
                    display="cloud"
                    multi-select
                    @update:model-value="(val) => emit('update:selectedTags', val)"
                />
            </div>
        </template>

        <template v-else>
            <div class="blog-sidebar__slot blog-sidebar__slot--popular blog-sidebar__placeholder"></div>
            <div class="blog-sidebar__slot blog-sidebar__slot--categories blog-sidebar__placeholder"></div>
            <div class="blog-sidebar__slot blog-sidebar__slot--tags blog-sidebar__placeholder"></div>
        </template>
    </aside>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import { useViewportTrigger } from '@/composables/performance/useViewportTrigger';

    import type {
        ArticleCategoryItem,
        PopularArticle,
        Tag,
    } from '@/types/feature/blog';

    interface Props {
        popularArticles: PopularArticle[];
        categories?: ArticleCategoryItem[];
        tags?: Tag[];
        selectedCategory: string | number | null;
        selectedTags: Array<string | number>;
        totalArticles: number;
    }

    const props = withDefaults(defineProps<Props>(), {
        categories: () => [],
        tags: () => [],
    });

    const emit = defineEmits<{
        'update:selectedCategory': [value: string | number | null];
        'update:selectedTags': [value: Array<string | number>];
    }>();

    const trigger = useViewportTrigger({ rootMargin: '400px', once: true });
    const targetRef = trigger.targetRef;
    const shouldRender = computed(() => trigger.isVisible.value);
    defineExpose({ targetRef });

    const categoriesWithAll = computed<ArticleCategoryItem[]>(() => {
        if (!props.categories?.length) {
            return [];
        }
        return [
            { id: '', slug: '', name: 'Tous', count: props.totalArticles } as ArticleCategoryItem,
            ...props.categories,
        ];
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .blog-sidebar {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-lg;

        &__slot {
            background: fn.color-alpha(vars.$white, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            border-radius: vars.$border-radius-xl;
            box-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.04);
            transition: box-shadow 0.3s ease;
            contain: layout paint;

            &:hover {
                box-shadow: 0 6px 24px fn.color-alpha(vars.$black, 0.07);
            }

            &--popular {
                min-height: 420px;
            }

            &--categories {
                min-height: 260px;
            }

            &--tags {
                min-height: 220px;
            }
        }

        &__placeholder {
            background: fn.color-alpha(vars.$white, 0.6);
        }

        @include mix.responsive(tablet) {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
        }

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;

            .blog-sidebar__slot {
                &--popular {
                    min-height: 380px;
                }

                &--categories,
                &--tags {
                    min-height: 180px;
                }
            }
        }
    }
</style>
