<template>
    <div class="card card--large">
        <div class="card__header">
            <div class="card__title-group">
                <BaseIcon name="trending-up" :size="18" class="card__icon" />
                <h4 class="card__title">Top contenus</h4>
            </div>
            <SegmentedTabs v-model="activeTab" :tabs="tabs" />
        </div>

        <div class="top-list">
            <template v-if="loading">
                <div v-for="i in 5" :key="i" class="top-list__skeleton"></div>
            </template>
            <template v-else-if="currentList.length">
                <NuxtLink
                    v-for="(item, index) in currentList"
                    :key="item.id"
                    :to="getItemLink(item)"
                    class="top-list__item"
                >
                    <span class="top-list__rank" :class="{ 'top-list__rank--top': index < 3 }">
                        {{ index + 1 }}
                    </span>
                    <span class="top-list__title">{{ item.title }}</span>
                    <span v-if="item.category" class="top-list__category">{{ item.category }}</span>
                    <span class="top-list__value">
                        <template v-if="item.type === 'stack'"> {{ item.level }}/5 </template>
                        <template v-else> {{ formatNumber(item.views) }} vues </template>
                    </span>
                </NuxtLink>
            </template>
            <div v-else class="top-list__empty">
                <BaseIcon name="bar-chart-2" :size="24" />
                <span>Aucune donnée</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SegmentedTabs from '@/components/ui/SegmentedTabs.vue';

    import type { DashboardTopContentProps, DashboardTopItem } from '@/types/components/admin';

    const props = withDefaults(defineProps<DashboardTopContentProps>(), {
        loading: false,
    });

    const activeTab = ref<'articles' | 'projects' | 'stacks'>('articles');

    const tabs = [
        { key: 'articles', label: 'Articles' },
        { key: 'projects', label: 'Projets' },
        { key: 'stacks', label: 'Stacks' },
    ];

    const currentList = computed(() => {
        switch (activeTab.value) {
            case 'articles':
                return props.articles;
            case 'projects':
                return props.projects;
            case 'stacks':
                return props.stacks;
            default:
                return [];
        }
    });

    const getItemLink = (item: DashboardTopItem): string => {
        const routes: Record<string, string> = {
            article: `/admin/articles/${item.id}`,
            project: `/admin/projects/${item.id}`,
            stack: `/admin/stacks/${item.id}`,
        };
        return routes[item.type] || '#';
    };

    const formatNumber = (num: number): string => {
        if (num >= 1000000) {
            return `${(num / 1000000).toFixed(1)}M`;
        }
        if (num >= 1000) {
            return `${(num / 1000).toFixed(1)}k`;
        }
        return String(num);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .card {
        background: vars.$white;
        border: 1px solid func.color-alpha(vars.$black, 0.06);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        min-width: 0;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-md;
        }

        &__header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: vars.$spacing-lg;
            gap: vars.$spacing-md;
            flex-wrap: wrap;
        }

        &__title-group {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
        }

        &__icon {
            color: vars.$text-muted;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            margin: 0;
        }
    }

    .top-list {
        display: flex;
        flex-direction: column;

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            padding: vars.$spacing-xs 0;
            text-decoration: none;
            border-bottom: 1px solid func.color-alpha(vars.$black, 0.04);
            transition: opacity 0.15s;

            &:last-child {
                border-bottom: none;
            }

            &:hover {
                opacity: 0.7;
            }
        }

        &__rank {
            width: 20px;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-muted;
            text-align: center;
            flex-shrink: 0;

            &--top {
                color: vars.$primary-color;
                font-weight: vars.$font-weight-bold;
            }
        }

        &__title {
            flex: 1;
            color: vars.$text-primary;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__category {
            color: vars.$text-muted;
            flex-shrink: 0;
            max-width: 100px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__value {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            flex-shrink: 0;
            min-width: 60px;
            text-align: right;
        }

        &__skeleton {
            height: 36px;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-sm;
            margin-bottom: vars.$spacing-xxs;
            animation: pulse 1.5s infinite;
        }

        &__empty {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: vars.$spacing-xl;
            color: vars.$text-muted;
            gap: vars.$spacing-xxs;
        }
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }
</style>
