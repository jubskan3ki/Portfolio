<template>
    <div class="session-item" :class="{ 'session-item--current': session.isCurrent }">
        <div class="session-item__icon">
            <BaseIcon :name="deviceIcon" :size="20" />
        </div>

        <div class="session-item__content">
            <span class="session-item__title">{{ deviceLabel }}</span>
            <span class="session-item__details">
                <span v-if="session.device?.ipAddress" class="session-item__ip">
                    {{ session.device.ipAddress }}
                </span>
                <span v-if="session.device?.ipAddress" class="session-item__separator">-</span>
                <span class="session-item__time" :title="absoluteTime">{{ formattedTime }}</span>
            </span>
        </div>

        <span v-if="session.isCurrent" class="session-item__badge">
            <BaseIcon name="check-circle" :size="12" />
            Session actuelle
        </span>

        <button
            v-else
            class="session-item__revoke"
            :disabled="isRevoking"
            :aria-label="'Revoquer la session ' + deviceLabel"
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

    import type { SessionItemEmits, SessionItemProps } from '@/types/components/admin';

    const props = withDefaults(defineProps<SessionItemProps>(), {
        isRevoking: false,
    });

    const emit = defineEmits<SessionItemEmits>();

    const deviceIcon = computed(() => (props.session.device?.isMobile ? 'smartphone' : 'monitor'));

    const deviceLabel = computed(() => {
        const browser = props.session.device?.browser;
        const os = props.session.device?.os;
        const hasBrowser = browser && browser !== 'Unknown';
        const hasOs = os && os !== 'Unknown';

        if (hasBrowser && hasOs) {
            return `${browser} sur ${os}`;
        }
        if (hasBrowser) {
            return browser as string;
        }
        if (hasOs) {
            return os as string;
        }
        return 'Appareil inconnu';
    });

    const parseDate = (value: string | undefined) => {
        if (!value) {
            return null;
        }
        const date = new Date(value);
        return Number.isNaN(date.getTime()) ? null : date;
    };

    const formattedTime = computed(() => {
        const date = parseDate(props.session.lastActivity);
        if (!date) {
            return 'Date inconnue';
        }

        const diff = Date.now() - date.getTime();
        if (diff < 0) {
            return 'A l\'instant';
        }

        const minutes = Math.floor(diff / 60000);
        if (minutes < 1) {
            return 'A l\'instant';
        }
        if (minutes < 60) {
            return `Il y a ${minutes} min`;
        }

        const hours = Math.floor(diff / 3600000);
        if (hours < 24) {
            return `Il y a ${hours}h`;
        }

        const days = Math.floor(diff / 86400000);
        if (days < 7) {
            return `Il y a ${days}j`;
        }
        return date.toLocaleDateString('fr-FR');
    });

    const absoluteTime = computed(() => {
        const date = parseDate(props.session.lastActivity);
        return date ? date.toLocaleString('fr-FR') : '';
    });

    const handleRevoke = () => {
        if (!props.isRevoking && props.session.id && !props.session.isCurrent) {
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
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: vars.$border-radius-full;
            font-weight: vars.$font-weight-medium;
            background-color: func.color-alpha(vars.$success-color, 0.1);
            color: vars.$success-color;
            flex-shrink: 0;
            white-space: nowrap;
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
