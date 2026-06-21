<template>
    <div class="card card--small">
        <div class="card__header">
            <div class="card__title-group">
                <BaseIcon name="activity" :size="18" class="card__icon" />
                <h4 class="card__title">Activité récente</h4>
            </div>
            <NuxtLink :to="historyPath" class="card__link">Tout voir</NuxtLink>
        </div>
        <div class="activity-list">
            <template v-if="loading">
                <div v-for="i in 5" :key="i" class="activity-skeleton"></div>
            </template>
            <template v-else-if="activities.length">
                <div v-for="activity in activities" :key="activity.id" class="activity-item">
                    <div class="activity-item__icon" :class="`activity-item__icon--${activity.type}`">
                        <BaseIcon :name="getActivityIcon(activity.type)" :size="14" />
                    </div>
                    <div class="activity-item__content">
                        <p class="activity-item__text">{{ activity.text }}</p>
                        <small class="activity-item__date">{{ formatRelativeDate(activity.date) }}</small>
                    </div>
                </div>
            </template>
            <div v-else class="activity-empty">
                <BaseIcon name="inbox" :size="28" />
                <span>Aucune activité</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { onMounted, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { ADMIN_ROUTES } from '@/config/routes';

    import type { DashboardActivityFeedProps } from '@/types/components/admin';

    withDefaults(defineProps<DashboardActivityFeedProps>(), {
        loading: false,
    });

    const historyPath = ADMIN_ROUTES.HISTORY.path;

    const ACTIVITY_ICONS: Record<string, string> = {
        message: 'mail',
        article: 'file-text',
        project: 'folder',
        stack: 'layers',
        experience: 'briefcase',
    };

    const getActivityIcon = (type: string): string => {
        return ACTIVITY_ICONS[type] || 'activity';
    };

    // "now" n'est posé qu'au montage client : SSR et première hydratation rendent la date
    // absolue déterministe (zéro mismatch), puis on bascule en relatif après mount.
    const now = ref<number | null>(null);
    onMounted(() => {
        now.value = Date.now();
    });

    const absoluteDate = (date: Date): string =>
        date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', timeZone: 'Europe/Paris' });

    const formatRelativeDate = (date: Date): string => {
        if (now.value === null) {
            return absoluteDate(date);
        }

        const diff = now.value - date.getTime();
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) {
            return 'À l\'instant';
        }
        if (minutes < 60) {
            return `Il y a ${minutes} min`;
        }
        if (hours < 24) {
            return `Il y a ${hours}h`;
        }
        if (days < 7) {
            return `Il y a ${days}j`;
        }

        return absoluteDate(date);
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

        &__link {
            color: vars.$primary-color;
            text-decoration: none;
            font-weight: vars.$font-weight-medium;

            &:hover {
                text-decoration: underline;
            }
        }
    }

    .activity-list {
        display: flex;
        flex-direction: column;
    }

    .activity-item {
        display: flex;
        gap: vars.$spacing-xs;
        padding: vars.$spacing-xs 0;
        border-bottom: 1px solid func.color-alpha(vars.$black, 0.04);

        &:last-child {
            border-bottom: none;
        }

        &__icon {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            background: vars.$bg-secondary;
            color: vars.$text-muted;

            &--message {
                background: func.color-alpha(#f59e0b, 0.1);
                color: #f59e0b;
            }

            &--article {
                background: func.color-alpha(#3b82f6, 0.1);
                color: #3b82f6;
            }

            &--project {
                background: func.color-alpha(#10b981, 0.1);
                color: #10b981;
            }

            &--stack {
                background: func.color-alpha(#8b5cf6, 0.1);
                color: #8b5cf6;
            }
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__text {
            color: vars.$text-primary;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__date {
            color: vars.$text-muted;
        }
    }

    .activity-skeleton {
        height: 44px;
        background: vars.$bg-secondary;
        border-radius: vars.$border-radius-md;
        margin-bottom: vars.$spacing-xxs;
        animation: pulse 1.5s infinite;
    }

    .activity-empty {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xl;
        color: vars.$text-muted;
        gap: vars.$spacing-xs;
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
