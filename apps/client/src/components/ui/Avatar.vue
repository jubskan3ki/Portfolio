<template>
    <div :class="avatarClasses" :style="avatarStyle">
        <BaseImage
            v-if="src && !hasError"
            :src="resolvedSrc"
            :alt="alt || name"
            :width="avatarSize"
            :height="avatarSize"
            object-fit="cover"
            :show-placeholder="false"
            class="avatar__image"
            @error="handleError"
        />

        <span v-else-if="initials" class="avatar__initials" aria-hidden="true">
            {{ initials }}
        </span>

        <BaseIcon
            v-else
            name="user"
            :size="iconSize"
            class="avatar__icon"
            aria-hidden="true"
        />

        <span
            v-if="status"
            class="avatar__status"
            :class="[`avatar__status--${status}`]"
            :aria-label="statusLabel"
            role="status"
        ></span>

        <div v-if="$slots.badge" class="avatar__badge">
            <slot name="badge"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { resolveMediaUrl } from '@/services/utils/helpers';

    import type { AvatarProps, AvatarSize, AvatarStatus } from '@/types/components/base';

    type Props = AvatarProps;

    const props = withDefaults(defineProps<Props>(), {
        src: '',
        alt: '',
        name: '',
        size: 'md',
        shape: 'circle',
        status: undefined,
        color: '',
        border: false,
        customClass: '',
    });

    const hasError = ref(false);
    const resolvedSrc = computed(() => resolveMediaUrl(props.src));

    const STATUS_LABELS: Record<AvatarStatus, string> = {
        online: 'En ligne',
        offline: 'Hors ligne',
        busy: 'Occupé',
        away: 'Absent',
    };

    const SIZE_MAP: Record<AvatarSize, number> = {
        xs: 24,
        sm: 32,
        md: 40,
        lg: 48,
        xl: 64,
        '': 96,
    };

    const ICON_SIZE_MAP: Record<AvatarSize, number> = {
        xs: 12,
        sm: 16,
        md: 20,
        lg: 24,
        xl: 32,
        '': 48,
    };

    const COLORS = [
        '#6366f1',
        '#8b5cf6',
        '#ec4899',
        '#f43f5e',
        '#f97316',
        '#eab308',
        '#22c55e',
        '#14b8a6',
        '#06b6d4',
        '#3b82f6',
    ];

    const avatarSize = computed(() => SIZE_MAP[props.size]);
    const iconSize = computed(() => ICON_SIZE_MAP[props.size]);

    const initials = computed(() => {
        if (!props.name) {
            return '';
        }
        const words = props.name
            .trim()
            .split(/\s+/)
            .filter((w) => w.length > 0);
        if (words.length === 0) {
            return '';
        }
        const firstWord = words[0];
        if (words.length === 1) {
            return firstWord ? firstWord.substring(0, 2).toUpperCase() : '';
        }
        const firstChar = firstWord?.[0] ?? '';
        const lastChar = words[words.length - 1]?.[0] ?? '';
        return (firstChar + lastChar).toUpperCase();
    });

    const backgroundColor = computed(() => {
        if (props.color) {
            return props.color;
        }
        if (!props.name) {
            return undefined;
        }

        let hash = 0;
        for (let i = 0; i < props.name.length; i++) {
            hash = props.name.charCodeAt(i) + ((hash << 5) - hash);
        }

        return COLORS[Math.abs(hash) % COLORS.length];
    });

    const statusLabel = computed(() => (props.status ? STATUS_LABELS[props.status] : undefined));

    const avatarClasses = computed(() => [
        'avatar',
        `avatar--${props.size}`,
        `avatar--${props.shape}`,
        {
            'avatar--has-status': props.status,
            'avatar--border': props.border,
        },
        props.customClass,
    ]);

    const avatarStyle = computed(() => ({
        width: `${avatarSize.value}px`,
        height: `${avatarSize.value}px`,
        '--avatar-bg': !props.src || hasError.value ? backgroundColor.value : undefined,
    }));

    const handleError = () => {
        hasError.value = true;
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .avatar {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        background-color: var(--avatar-bg, vars.$gray-light);
        color: vars.$white;
        font-weight: vars.$font-weight-medium;
        overflow: hidden;
        user-select: none;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;

        &:hover {
            transform: scale(1.02);
        }

        /* Shapes */
        &--circle {
            border-radius: vars.$border-radius-full;
        }

        &--square {
            border-radius: vars.$border-radius-md;
        }

        /* Sizes handled by avatar dimensions */

        /* Border */
        &--border {
            border: 2px solid vars.$white;
            box-shadow: 0 0 0 1px func.color-alpha(vars.$black, 0.08);
        }

        /* Image */
        &__image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        &:hover &__image {
            transform: scale(1.05);
        }

        /* Initials */
        &__initials {
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        /* Icon */
        &__icon {
            color: vars.$white;
            opacity: 0.8;
        }

        /* Badge */
        &__badge {
            position: absolute;
            top: 0;
            right: 0;
            transform: translate(30%, -30%);
        }

        /* Status */
        &__status {
            position: absolute;
            bottom: 0;
            right: 0;
            width: 25%;
            height: 25%;
            min-width: 8px;
            min-height: 8px;
            max-width: 14px;
            max-height: 14px;
            border-radius: vars.$border-radius-full;
            border: 2px solid vars.$white;
            transition: transform 0.2s ease;

            &--online {
                background-color: vars.$success-color;
                animation: pulse-online 2s ease-in-out infinite;
            }

            &--offline {
                background-color: vars.$gray;
            }

            &--busy {
                background-color: vars.$danger-color;
            }

            &--away {
                background-color: vars.$warning-color;
            }
        }
    }

    @keyframes pulse-online {
        0%,
        100% {
            box-shadow: 0 0 0 0 func.color-alpha(vars.$success-color, 0.4);
        }

        50% {
            box-shadow: 0 0 0 4px func.color-alpha(vars.$success-color, 0);
        }
    }
</style>
