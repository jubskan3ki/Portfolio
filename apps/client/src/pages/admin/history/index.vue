<template>
    <div class="history">
        <header class="history__header">
            <div>
                <h1 class="history__title">Historique</h1>
                <p class="history__subtitle">Toutes les actions et activités récentes</p>
            </div>
            <div class="history__actions">
                <BaseButton variant="outline" :loading="isRefreshing" @click="refresh">
                    <template #icon-left>
                        <BaseIcon name="refresh-cw" :size="16" />
                    </template>
                    Actualiser
                </BaseButton>
            </div>
        </header>

        <div class="history__filters">
            <div class="filter-group filter-group--search">
                <SearchInput
                    v-model="searchQuery"
                    placeholder="Rechercher une activité..."
                    aria-label="Rechercher dans l'historique"
                />
            </div>

            <div class="filter-group">
                <BaseSelect
                    v-model="filterType"
                    placeholder="Type"
                    :options="typeOptions"
                    aria-label="Filtrer par type"
                />
            </div>
            <div class="filter-group">
                <BaseSelect
                    v-model="filterPeriod"
                    placeholder="Période"
                    :options="periodOptions"
                    aria-label="Filtrer par période"
                />
            </div>
        </div>

        <div class="history__content">
            <template v-if="isLoading">
                <div v-for="i in 10" :key="i" class="activity-skeleton">
                    <Skeleton type="avatar" :width="40" :height="40" />
                    <div class="activity-skeleton__content">
                        <Skeleton type="text" width="70%" height="16px" />
                        <Skeleton type="text" width="40%" height="12px" />
                    </div>
                </div>
            </template>
            <template v-else-if="filteredActivities.length">
                <div
                    v-for="activity in filteredActivities"
                    :key="activity.id"
                    class="activity-card"
                    :class="`activity-card--${activity.type}`"
                >
                    <div class="activity-card__icon">
                        <BaseIcon :name="getIcon(activity.type)" :size="18" />
                    </div>
                    <div class="activity-card__content">
                        <p class="activity-card__title">{{ activity.title }}</p>
                        <div class="activity-card__meta">
                            <span class="activity-card__type">{{ getTypeLabel(activity.type) }}</span>
                            <span class="activity-card__dot"></span>
                            <span class="activity-card__date">{{ formatRelativeDate(activity.timestamp) }}</span>
                        </div>
                    </div>
                    <BaseButton
                        v-if="activity.link"
                        :to="activity.link"
                        variant="ghost"
                        size="icon"
                        aria-label="Voir le détail"
                    >
                        <template #icon-left>
                            <BaseIcon name="external-link" :size="16" />
                        </template>
                    </BaseButton>
                </div>
            </template>
            <EmptyState
                v-else
                icon="inbox"
                title="Aucune activité"
                description="Il n'y a pas encore d'activité à afficher"
                size="md"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useQuery, useQueryClient } from '@tanstack/vue-query';
    import { computed, ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Skeleton from '@/components/loaders/Skeleton.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';
    import { useSearch } from '@/composables/data/useSearch';
    import { useSeo } from '@/composables/seo/useSeo';
    import {
        ACTIVITY_TYPE_ICONS,
        ACTIVITY_TYPE_LABELS,
        ACTIVITY_TYPE_OPTIONS,
        ACTIVITY_PERIOD_OPTIONS,
    } from '@/config/constants';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { statsApi, statsKeys } from '@/services/api/modules/stats';
    import { formatRelativeDate } from '@/services/utils/date';

    import type { HistoryActivityResponse } from '@/types/pages/admin';

    definePageMeta({
        layout: 'admin',
        title: 'Historique',
    });

    useSeo({
        title: 'Historique - Admin',
        description: 'Historique des actions',
        noindex: true,
        url: '/admin/history',
    });

    const HISTORY_LIMIT = 200;

    const queryClient = useQueryClient();
    const { query: searchQuery, debouncedQuery } = useSearch({ debounceMs: 300 });
    const filterType = ref('');
    const filterPeriod = ref('');

    const routeMap: Record<string, string> = {
        article: ADMIN_ROUTES.ARTICLES.path,
        project: ADMIN_ROUTES.PROJECTS.path,
        stack: ADMIN_ROUTES.STACKS.path,
        experience: ADMIN_ROUTES.EXPERIENCES.path,
        message: ADMIN_ROUTES.MESSAGES.path,
    };

    const {
        data: activitiesData,
        isLoading,
        isFetching: isRefreshing,
    } = useQuery({
        queryKey: statsKeys.history(HISTORY_LIMIT),
        queryFn: async () => {
            const data = await statsApi.getActivity<HistoryActivityResponse>(HISTORY_LIMIT);
            return (data?.activities || []).map((a) => ({
                ...a,
                link: routeMap[a.type],
            }));
        },
        staleTime: 1000 * 60 * 2,
    });

    const activities = computed(() => activitiesData.value || []);

    const filteredActivities = computed(() => {
        let result = [...activities.value];

        if (debouncedQuery.value.trim()) {
            const q = debouncedQuery.value.toLowerCase().trim();
            result = result.filter(
                (a) =>
                    a.title.toLowerCase().includes(q)
                    || a.type.toLowerCase().includes(q)
                    || getTypeLabel(a.type).toLowerCase().includes(q),
            );
        }

        if (filterType.value) {
            result = result.filter((a) => a.type === filterType.value);
        }

        if (filterPeriod.value && filterPeriod.value !== 'all') {
            const filterDate = new Date();
            switch (filterPeriod.value) {
                case 'today':
                    filterDate.setHours(0, 0, 0, 0);
                    break;
                case 'week':
                    filterDate.setDate(filterDate.getDate() - 7);
                    break;
                case 'month':
                    filterDate.setMonth(filterDate.getMonth() - 1);
                    break;
            }
            result = result.filter((a) => new Date(a.timestamp) >= filterDate);
        }

        return result;
    });

    const getIcon = (type: string): string => ACTIVITY_TYPE_ICONS[type] || 'activity';
    const getTypeLabel = (type: string): string => ACTIVITY_TYPE_LABELS[type] || type;

    const typeOptions = [...ACTIVITY_TYPE_OPTIONS];
    const periodOptions = [...ACTIVITY_PERIOD_OPTIONS];

    const refresh = () => {
        queryClient.invalidateQueries({ queryKey: ['stats', 'history', 'activities'] });
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .history {
        animation: fade-in 0.3s ease-out;
    }

    // Header
    .history__header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: vars.$spacing-xl;
        gap: vars.$spacing-lg;
        flex-wrap: wrap;
    }

    .history__title {
        font-weight: vars.$font-weight-bold;
        color: vars.$text-primary;
        margin: 0;
    }

    .history__subtitle {
        color: vars.$text-secondary;
        margin: vars.$spacing-xxs 0 0;
    }

    // Filters
    .history__filters {
        display: flex;
        gap: vars.$spacing-md;
        margin-bottom: vars.$spacing-xl;
        flex-wrap: wrap;
    }

    .filter-group {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxs;

        &--search {
            flex: 1;
            max-width: 320px;

            :deep(.input) {
                margin-bottom: 0;
            }
        }

        :deep(.select) {
            margin-bottom: 0;
            min-width: 160px;
        }
    }

    // Content
    .history__content {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xs;
    }

    .activity-card {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md vars.$spacing-lg;
        background: vars.$white;
        border: 1px solid func.color-alpha(vars.$black, 0.06);
        border-radius: vars.$border-radius-lg;
        transition: all 0.2s ease;

        &:hover {
            border-color: func.color-alpha(vars.$black, 0.1);
            box-shadow: 0 2px 8px func.color-alpha(vars.$black, 0.04);
        }

        &__icon {
            width: 40px;
            height: 40px;
            border-radius: vars.$border-radius-md;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            background: vars.$bg-secondary;
            color: vars.$text-muted;
        }

        &--message &__icon {
            background: func.color-alpha(#f59e0b, 0.1);
            color: #f59e0b;
        }

        &--article &__icon {
            background: func.color-alpha(#3b82f6, 0.1);
            color: #3b82f6;
        }

        &--project &__icon {
            background: func.color-alpha(#10b981, 0.1);
            color: #10b981;
        }

        &--stack &__icon {
            background: func.color-alpha(#8b5cf6, 0.1);
            color: #8b5cf6;
        }

        &--experience &__icon {
            background: func.color-alpha(#ec4899, 0.1);
            color: #ec4899;
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__title {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__meta {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin-top: 4px;
        }

        &__type {
            color: vars.$text-secondary;
        }

        &__dot {
            width: 3px;
            height: 3px;
            border-radius: 50%;
            background: vars.$text-muted;
        }

        &__date {
            color: vars.$text-muted;
        }
    }

    // Skeleton
    .activity-skeleton {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md vars.$spacing-lg;
        background: vars.$white;
        border: 1px solid func.color-alpha(vars.$black, 0.06);
        border-radius: vars.$border-radius-lg;

        &__content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxs;
        }
    }

    // Animations
    @keyframes fade-in {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }
</style>
