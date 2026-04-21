<template>
    <div class="article-categories">
        <h3 class="article-categories__title">
            <BaseIcon name="folder" :size="16" />
            {{ title }}
        </h3>

        <ul class="article-categories__list">
            <li v-for="category in visibleCategories" :key="category.id || category.slug">
                <button
                    class="article-categories__btn"
                    :class="{ 'article-categories__btn--active': isActive(category) }"
                    type="button"
                    @click="handleSelect(category)"
                >
                    <span class="article-categories__name">{{ category.name }}</span>
                    <span v-if="category.count !== undefined" class="article-categories__count">
                        {{ category.count }}
                    </span>
                </button>
            </li>
        </ul>

        <button v-if="canToggle" class="article-categories__toggle" type="button" @click="showAll = !showAll">
            {{ showAll ? 'Voir moins' : `Voir plus (${hiddenCount})` }}
        </button>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { ArticleCategoriesProps, ArticleCategoryItem } from '@/types/feature/blog';

    const props = withDefaults(defineProps<ArticleCategoriesProps>(), {
        title: 'Catégories',
        categories: () => [],
        modelValue: null,
        maxVisible: 0,
    });

    const emit = defineEmits<{
        'update:modelValue': [value: string | number | null];
        select: [value: string | number | null];
    }>();

    const showAll = ref(false);

    // Masque les items a count=0 ("Tous" passe si totalArticles>0 ou count=undefined).
    const filteredCategories = computed(() => props.categories.filter((c) => c.count === undefined || c.count > 0));

    const canToggle = computed(() => props.maxVisible > 0 && filteredCategories.value.length > props.maxVisible);

    const visibleCategories = computed(() => {
        if (!canToggle.value || showAll.value) {
            return filteredCategories.value;
        }
        return filteredCategories.value.slice(0, props.maxVisible);
    });

    const hiddenCount = computed(() => Math.max(0, filteredCategories.value.length - props.maxVisible));

    const isActive = (category: ArticleCategoryItem) => {
        if (!props.modelValue) {
            return !category.id && !category.slug;
        }

        const value = String(props.modelValue);
        return String(category.id) === value || String(category.slug) === value;
    };

    const handleSelect = (category: ArticleCategoryItem) => {
        if (isActive(category)) {
            return;
        }

        const value = category.slug || (category.id ? String(category.id) : null);
        emit('update:modelValue', value);
        emit('select', value);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .article-categories {
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
            gap: vars.$spacing-xxs;
            list-style: none;
            margin: 0;
            padding: 0;
        }

        &__btn {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: vars.$spacing-xs vars.$spacing-sm;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            background: transparent;
            border: 1px solid transparent;
            border-radius: vars.$border-radius-md;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover:not(&--active) {
                color: vars.$primary-color;
                background: fn.color-alpha(vars.$primary-color, 0.04);
                border-color: fn.color-alpha(vars.$primary-color, 0.1);
            }

            &--active {
                color: vars.$primary-color;
                background: fn.color-alpha(vars.$primary-color, 0.08);
                border-color: fn.color-alpha(vars.$primary-color, 0.15);
                font-weight: vars.$font-weight-semibold;

                .article-categories__count {
                    color: vars.$white;
                    background: vars.$primary-color;
                }

                &:hover {
                    color: vars.$white;
                    background: vars.$primary-color;
                    border-color: vars.$primary-color;

                    .article-categories__count {
                        color: vars.$primary-color;
                        background: vars.$white;
                    }
                }
            }
        }

        &__name {
            @include mix.truncate(1);
        }

        &__count {
            flex-shrink: 0;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-muted;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-full;
            transition: all 0.2s ease;
        }

        &__toggle {
            margin-top: vars.$spacing-sm;
            padding: vars.$spacing-xs vars.$spacing-sm;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;
            color: vars.$primary-color;
            background: transparent;
            border: none;
            border-radius: vars.$border-radius-md;
            cursor: pointer;
            transition: background 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.08);
            }
        }
    }
</style>
