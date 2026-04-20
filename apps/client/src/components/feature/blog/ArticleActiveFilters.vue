<!--
  ArticleActiveFilters.vue
  Composant pour afficher et gérer les filtres actifs
-->
<template>
    <Card v-if="hasActiveFilters" class="article-active-filters">
        <h3 class="article-active-filters__title">{{ title }}</h3>
        <div class="article-active-filters__chips">
            <div v-if="activeCategory" class="article-active-filters__chip">
                <span class="article-active-filters__chip-text">{{ getCategoryName(activeCategory) }}</span>
                <button class="article-active-filters__chip-remove" @click="removeCategory">
                    <BaseIcon name="close" :size="14" />
                </button>
            </div>

            <div v-for="tag in activeTags" :key="`tag-${tag}`" class="article-active-filters__chip">
                <span class="article-active-filters__chip-text">{{ getTagName(tag) }}</span>
                <button class="article-active-filters__chip-remove" @click="removeTag(tag)">
                    <BaseIcon name="close" :size="14" />
                </button>
            </div>
        </div>

        <button v-if="hasActiveFilters" class="article-active-filters__clear" @click="clearAllFilters">
            {{ clearButtonText }}
        </button>
    </Card>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Card from '@/components/ui/Card.vue';

    import type { ArticleActiveFiltersProps } from '@/types/feature/blog';

    const props = withDefaults(defineProps<ArticleActiveFiltersProps>(), {
        title: 'Filtres actifs',
        activeCategory: null,
        activeTags: () => [],
        categories: () => [],
        tags: () => [],
        clearButtonText: 'Effacer tous les filtres',
    });

    const emit = defineEmits<{
        removeCategory: [];
        removeTag: [tagId: string | number];
        clearAll: [];
    }>();

    const hasActiveFilters = computed(() => {
        return props.activeCategory || (props.activeTags && props.activeTags.length > 0);
    });

    // Type guard pour vérifier si un objet a une propriété name
    const hasName = (obj: unknown): obj is { name: string } => {
        return obj !== null && typeof obj === 'object' && 'name' in obj;
    };

    // Obtenir le nom de la catégorie à partir de son ID
    const getCategoryName = (categoryId: string | number | object): string => {
        // Si c'est déjà un objet avec une propriété name, utiliser directement
        if (hasName(categoryId)) {
            return categoryId.name;
        }

        // Sinon, chercher dans les catégories
        const category = props.categories.find(
            (c) => (c.id && c.id === categoryId) || (c.slug && c.slug === categoryId),
        );

        return category ? category.name : String(categoryId);
    };

    // Obtenir le nom du tag à partir de son ID
    const getTagName = (tagId: string | number): string => {
        const tag = props.tags.find((t) => t.id === tagId);
        return tag ? tag.name : String(tagId);
    };

    // Actions
    const removeCategory = () => {
        emit('removeCategory');
    };

    const removeTag = (tagId: string | number) => {
        emit('removeTag', tagId);
    };

    const clearAllFilters = () => {
        emit('clearAll');
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .article-active-filters {
        margin-bottom: vars.$spacing-lg;

        &__title {
            margin-bottom: vars.$spacing-md;
            padding-bottom: vars.$spacing-xs;
            border-bottom: 1px solid vars.$white-dark;
            color: vars.$primary-color;
            font-weight: 600;
        }

        &__chips {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-xxs;
            margin-bottom: vars.$spacing-xxs;
        }

        &__chip {
            display: inline-flex;
            align-items: center;
            background-color: func.color-alpha(vars.$primary-color, 0.15);
            border-radius: vars.$border-radius-full;
            padding: 6px 12px;
            color: vars.$primary-color;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: all vars.$transition-base;

            &:hover {
                background-color: func.color-alpha(vars.$primary-color, 0.2);
                transform: translateY(-2px);
            }
        }

        &__chip-text {
            margin-right: vars.$spacing-xxs;
        }

        &__chip-remove {
            display: flex;
            align-items: center;
            justify-content: center;
            background: none;
            border: none;
            padding: 2px;
            cursor: pointer;
            color: vars.$primary-color;
            border-radius: 50%;
            transition: background-color vars.$transition-base;

            &:hover {
                background-color: func.color-alpha(vars.$primary-color, 0.2);
            }
        }

        &__clear {
            display: block;
            margin-top: vars.$spacing-xs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            border: none;
            border-radius: vars.$border-radius-sm;
            background-color: vars.$white-dark;
            color: vars.$gray-dark;
            cursor: pointer;
            transition: all vars.$transition-base;

            &:hover {
                background-color: vars.$gray-light;
                color: vars.$black-light;
            }
        }
    }
</style>
