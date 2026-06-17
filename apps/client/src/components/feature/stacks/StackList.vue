<template>
    <div class="stack-list" :class="[customClass]">
        <div v-if="title || $slots.header" class="stack-list__header">
            <slot name="header">
                <h2 v-if="title" class="stack-list__title">{{ title }}</h2>
                <p v-if="description" class="stack-list__description">{{ description }}</p>
            </slot>
        </div>

        <div v-if="showFilters && categoryFilters.length > 0" class="stack-list__filters">
            <div class="stack-list__filter-label">{{ filterLabel }}:</div>
            <div class="stack-list__filter-options">
                <button
                    class="stack-list__filter-btn"
                    :class="{ 'stack-list__filter-btn--active': activeFilter === 'all' }"
                    @click="setFilter('all')"
                >
                    {{ allFilterLabel }}
                </button>
                <button
                    v-for="filter in categoryFilters"
                    :key="filter.value"
                    class="stack-list__filter-btn"
                    :class="{ 'stack-list__filter-btn--active': activeFilter === filter.value }"
                    @click="setFilter(filter.value)"
                >
                    {{ filter.label }}
                </button>
            </div>
        </div>

        <QueryStateHandler
            :loading="loading"
            :error="error"
            :empty="!filteredStacks || filteredStacks.length === 0"
            :loading-message="loadingText"
            :empty-title="emptyTitle"
            :empty-description="emptyDescription"
            empty-icon="folder"
            :retryable="retryable"
            :retry-text="retryText"
            @retry="$emit('retry')"
        >
            <template v-if="$slots['empty-action']" #empty-action>
                <slot name="empty-action"></slot>
            </template>

            <div v-if="displayMode === 'badges'" class="stack-list__badges">
                <StackBadge
                    v-for="stack in filteredStacks"
                    :key="stack.id"
                    :stack="stack"
                    :size="badgeSize"
                    :show-name="showStackName"
                    :show-level="showStackLevel"
                    :clickable="clickableItems"
                    @click="handleStackClick(stack)"
                />
            </div>

            <div v-else class="stack-list__grid" :class="[`stack-list__grid--${displayMode}`]">
                <template v-for="(stack, index) in filteredStacks" :key="stack.id ?? index">
                    <slot name="stack" :stack="stack" :index="index">
                        <StackCard
                            :stack="stack"
                            :hoverable="cardHoverable"
                            :flat="cardFlat"
                            :bordered="cardBordered"
                            :show-level="showStackLevel"
                            :description-length="descriptionLength"
                            @click="handleStackClick(stack)"
                        />
                    </slot>
                </template>
            </div>
        </QueryStateHandler>

        <div v-if="$slots.footer" class="stack-list__footer">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import QueryStateHandler from '@/components/feedback/QueryStateHandler.vue';

    import StackBadge from './StackBadge.vue';
    import StackCard from './StackCard.vue';

    import type { Stack, StackListProps } from '@/types/feature/stacks';

    type Props = StackListProps;

    const props = withDefaults(defineProps<Props>(), {
        stacks: () => [],
        title: 'Compétences Techniques',
        description: '',
        displayMode: 'grid',
        showFilters: true,
        categoryFilters: () => [],
        filterLabel: 'Filtrer par',
        allFilterLabel: 'Toutes les technologies',
        loading: false,
        error: '',
        retryable: false,
        retryText: 'Réessayer',
        loadingText: 'Chargement des technologies...',
        emptyTitle: 'Aucune technologie',
        emptyDescription: 'Aucune technologie ne correspond à votre recherche.',
        badgeSize: 'medium',
        showStackName: true,
        showStackLevel: true,
        clickableItems: false,
        cardHoverable: true,
        cardFlat: false,
        cardBordered: false,
        descriptionLength: 200,
        customClass: '',
    });

    const emit = defineEmits<{
        filterChange: [filter: string];
        stackClick: [stack: Stack];
        retry: [];
    }>();

    const activeFilter = ref('all');

    const setFilter = (filter: string) => {
        activeFilter.value = filter;
        emit('filterChange', filter);
    };

    // Filtré par catégorie puis trié par niveau décroissant (les stacks sans niveau en dernier, par nom).
    const filteredStacks = computed(() => {
        let filtered = [...props.stacks];

        if (activeFilter.value !== 'all') {
            filtered = filtered.filter((stack) => stack.category === activeFilter.value);
        }

        return filtered.sort((a, b) => {
            if (a.level !== undefined && b.level !== undefined) {
                return b.level - a.level;
            }
            if (a.level !== undefined) {
                return -1;
            }
            if (b.level !== undefined) {
                return 1;
            }
            return a.name.localeCompare(b.name);
        });
    });

    const handleStackClick = (stack: Stack) => {
        emit('stackClick', stack);
    };
</script>

<style lang="scss" scoped>
    @use '../../../styles/abstracts/variables' as vars;
    @use '../../../styles/abstracts/mixins' as mix;
    @use '../../../styles/abstracts/functions' as func;

    .stack-list {
        width: 100%;

        &__header {
            text-align: center;
            margin-bottom: vars.$spacing-xl;
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

        &__filters {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: vars.$spacing-xs;
            margin-bottom: vars.$spacing-lg;
            padding: vars.$spacing-md 0;
            border-bottom: 1px solid vars.$gray-light;
        }

        &__filter-label {
            font-weight: 600;
            margin-right: vars.$spacing-xs;
        }

        &__filter-options {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-xxs;
        }

        &__filter-btn {
            padding: vars.$spacing-xxs vars.$spacing-xs;
            background-color: vars.$white-dark;
            border: 1px solid vars.$gray-light;
            border-radius: vars.$border-radius-sm;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover {
                background-color: func.adjust-color-brightness(vars.$primary-color, 35%);
            }

            &--active {
                background-color: vars.$primary-color;
                color: white;
                border-color: vars.$primary-color;

                &:hover {
                    background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
                }
            }
        }

        &__loading {
            display: flex;
            justify-content: center;
            padding: vars.$spacing-xl 0;
        }

        &__error {
            text-align: center;
            padding: vars.$spacing-xl 0;
        }

        &__retry {
            margin-top: vars.$spacing-md;
        }

        &__badges {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-md;
            margin: vars.$spacing-lg 0;
            justify-content: center;
        }

        &__grid {
            width: 100%;
            display: grid;
            gap: vars.$spacing-lg;

            &--grid {
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));

                @include mix.responsive(mobile) {
                    grid-template-columns: 1fr;
                }
            }

            &--list {
                grid-template-columns: 1fr;
            }
        }

        &__footer {
            margin-top: vars.$spacing-xl;
            text-align: center;
        }
    }

    .filter-enter-active,
    .filter-leave-active {
        transition:
            opacity 0.3s,
            transform 0.3s;
    }

    .filter-enter-from,
    .filter-leave-to {
        opacity: 0;
        transform: translateY(10px);
    }

    .stack-enter-active,
    .stack-leave-active {
        transition:
            opacity 0.4s,
            transform 0.4s;
    }

    .stack-enter-from {
        opacity: 0;
        transform: translateY(20px);
    }

    .stack-leave-to {
        opacity: 0;
        transform: scale(0.9);
    }

    @include mix.responsive(tablet) {
        .stack-list {
            &__filters {
                flex-direction: column;
                align-items: flex-start;
            }

            &__filter-label {
                margin-bottom: vars.$spacing-xxs;
            }
        }
    }
</style>
