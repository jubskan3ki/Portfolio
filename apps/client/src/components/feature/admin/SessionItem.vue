<template>
    <div class="session-item" :class="{ 'session-item--current': session.isCurrent }">
        <div class="session-item__icon">
            <BaseIcon :name="deviceIcon" :size="20" />
        </div>

        <div class="session-item__content">
            <span class="session-item__title"> {{ browserName }} sur {{ osName }} </span>
            <span class="session-item__details">
                <template v-if="session.device?.ipAddress">
                    <span class="session-item__ip">{{ session.device.ipAddress }}</span>
                    <span class="session-item__separator">-</span>
                </template>
                <span class="session-item__time">{{ formattedTime }}</span>
            </span>
        </div>

        <span v-if="session.isCurrent" class="session-item__badge"> Actuelle </span>

        <button
            v-else
            class="session-item__revoke"
            :disabled="isRevoking"
            :title="isRevoking ? 'Revocation en cours...' : 'Revoquer cette session'"
            @click="handleRevoke"
        >
            <span v-if="isRevoking" class="session-item__spinner"></span>
            <BaseIcon v-else name="x" :size="16" />
        </button>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { Session } from '@/types/feature/admin';

    interface Props {
        session: Session;
        isRevoking?: boolean;
    }

    interface Emits {
        (e: 'revoke', sessionId: string): void;
    }

    const props = withDefaults(defineProps<Props>(), {
        isRevoking: false,
    });

    const emit = defineEmits<Emits>();

    const deviceIcon = computed(() => {
        return props.session.device?.isMobile ? 'smartphone' : 'monitor';
    });

    const browserName = computed(() => {
        return props.session.device?.browser || 'Navigateur inconnu';
    });

    const osName = computed(() => {
        return props.session.device?.os || 'Appareil inconnu';
    });

    const formattedTime = computed(() => {
        const dateStr = props.session.lastActivity;
        if (!dateStr) {
            return 'Date inconnue';
        }

        try {
            const date = new Date(dateStr);
            const now = new Date();
            const diff = now.getTime() - date.getTime();
            const minutes = Math.floor(diff / 60000);
            const hours = Math.floor(diff / 3600000);
            const days = Math.floor(diff / 86400000);

            if (minutes < 1) {
                return 'A l\'instant';
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
            return date.toLocaleDateString('fr-FR');
        } catch {
            return 'Date inconnue';
        }
    });

    const handleRevoke = () => {
        if (!props.isRevoking && props.session.id) {
            emit('revoke', props.session.id);
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .session-item {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md;
        background-color: vars.$bg-secondary;
        border-radius: vars.$border-radius-md;
        transition: background-color 0.2s ease;

        &--current {
            background-color: func.color-alpha(vars.$success-color, 0.05);
            border: 1px solid func.color-alpha(vars.$success-color, 0.15);
        }

        &__icon {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: vars.$white;
            border-radius: vars.$border-radius-md;
            color: vars.$primary-color;
            flex-shrink: 0;
            box-shadow: 0 1px 3px func.color-alpha(vars.$black, 0.05);
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__title {
            display: block;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__details {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            color: vars.$text-muted;
            margin-top: 2px;
        }

        &__ip {
            font-family: monospace;
        }

        &__separator {
            opacity: 0.5;
        }

        &__time {
            white-space: nowrap;
        }

        &__badge {
            padding: 4px 10px;
            border-radius: vars.$border-radius-full;
            font-weight: vars.$font-weight-medium;
            background-color: func.color-alpha(vars.$success-color, 0.1);
            color: vars.$success-color;
            flex-shrink: 0;
        }

        &__revoke {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: none;
            border: none;
            cursor: pointer;
            color: vars.$text-muted;
            border-radius: vars.$border-radius-sm;
            transition: all 0.2s ease;
            flex-shrink: 0;

            &:hover:not(:disabled) {
                background-color: func.color-alpha(vars.$danger-color, 0.1);
                color: vars.$danger-color;
            }

            &:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
        }

        &__spinner {
            width: 14px;
            height: 14px;
            border: 2px solid func.color-alpha(vars.$text-muted, 0.3);
            border-top-color: vars.$text-muted;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
