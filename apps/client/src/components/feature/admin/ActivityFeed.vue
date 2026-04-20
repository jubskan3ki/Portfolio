<template>
    <div class="activity-feed">
        <template v-if="loading">
            <div v-for="i in 4" :key="i" class="activity-feed__item activity-feed__item--skeleton">
                <div class="activity-feed__icon-skeleton"></div>
                <div class="activity-feed__content-skeleton">
                    <div class="activity-feed__text-skeleton"></div>
                    <div class="activity-feed__date-skeleton"></div>
                </div>
            </div>
        </template>

        <EmptyState v-else-if="!activities.length" title="Aucune activité récente" icon="inbox" size="sm" />

        <template v-else>
            <div v-for="activity in activities" :key="activity.id" class="activity-feed__item">
                <div class="activity-feed__icon" :class="`activity-feed__icon--${activity.type}`">
                    <BaseIcon :name="getActivityIcon(activity.type)" :size="16" />
                </div>
                <div class="activity-feed__content">
                    <p class="activity-feed__text">{{ activity.text }}</p>
                    <small class="activity-feed__date">{{ formatDate(activity.date) }}</small>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';

    import type { ActivityFeedProps } from '@/types/components/admin';

    defineProps<ActivityFeedProps>();

    const getActivityIcon = (type: string): string => {
        const icons: Record<string, string> = {
            message: 'mail',
            article: 'file-text',
            project: 'folder',
            stack: 'layers',
            experience: 'briefcase',
            user: 'user',
        };
        return icons[type] || 'activity';
    };

    const formatDate = (date: Date): string => {
        const now = new Date();
        const diff = now.getTime() - new Date(date).getTime();
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

        return new Date(date).toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'short',
        });
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .activity-feed {
        &__item {
            display: flex;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs 0;
            border-bottom: 1px solid rgba(vars.$border-color, 0.5);

            &:last-child {
                border-bottom: none;
            }

            &--skeleton {
                .activity-feed__icon-skeleton {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: vars.$bg-secondary;
                    animation: skeleton-pulse 1.5s infinite;
                }

                .activity-feed__content-skeleton {
                    flex: 1;
                }

                .activity-feed__text-skeleton {
                    height: 14px;
                    width: 80%;
                    background: vars.$bg-secondary;
                    animation: skeleton-pulse 1.5s infinite;
                    border-radius: vars.$border-radius-sm;
                    margin-bottom: vars.$spacing-xxs;
                }

                .activity-feed__date-skeleton {
                    height: 12px;
                    width: 40%;
                    background: vars.$bg-secondary;
                    animation: skeleton-pulse 1.5s infinite;
                    border-radius: vars.$border-radius-sm;
                }
            }
        }

        &__icon {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            background-color: vars.$bg-secondary;
            color: vars.$text-secondary;

            &--message {
                background-color: rgba(vars.$warning-color, 0.1);
                color: vars.$warning-color;
            }

            &--article {
                background-color: rgba(vars.$info-color, 0.1);
                color: vars.$info-color;
            }

            &--project {
                background-color: rgba(vars.$success-color, 0.1);
                color: vars.$success-color;
            }

            &--stack {
                background-color: rgba(vars.$secondary-color, 0.1);
                color: vars.$secondary-color;
            }

            &--experience {
                background-color: rgba(vars.$primary-color, 0.1);
                color: vars.$primary-color;
            }
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__text {
            color: vars.$text-primary;
            margin: 0 0 vars.$spacing-xxxs;
            line-height: 1.4;
        }

        &__date {
            color: vars.$text-muted;
        }
    }

    @keyframes skeleton-pulse {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }
</style>
