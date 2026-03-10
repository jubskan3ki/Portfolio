<template>
    <span
        :class="badgeClasses"
        :role="clickable ? 'button' : undefined"
        :tabindex="clickable ? 0 : undefined"
        @click="handleClick"
        @keydown.enter="handleClick"
        @keydown.space.prevent="handleClick"
    >
        <span v-if="dot" class="badge__dot" aria-hidden="true"></span>

        <BaseIcon
            v-if="icon && !dot"
            :name="icon"
            :size="iconSize"
            class="badge__icon"
            aria-hidden="true"
        />

        <slot>{{ text }}</slot>

        <button
            v-if="removable"
            type="button"
            class="badge__remove"
            aria-label="Supprimer"
            @click.stop="handleRemove"
        >
            <BaseIcon name="x" :size="12" aria-hidden="true" />
        </button>
    </span>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { BadgeProps } from '@/types/components/base';

    type Props = BadgeProps;

    const props = withDefaults(defineProps<Props>(), {
        text: '',
        variant: 'primary',
        size: 'md',
        rounded: false,
        removable: false,
        dot: false,
        clickable: false,
        icon: '',
        iconSize: 12,
        customClass: '',
    });

    const emit = defineEmits<{
        click: [event: MouseEvent | KeyboardEvent];
        remove: [];
    }>();

    const badgeClasses = computed(() => [
        'badge',
        `badge--${props.variant}`,
        `badge--${props.size}`,
        {
            'badge--rounded': props.rounded,
            'badge--removable': props.removable,
            'badge--dot': props.dot,
            'badge--clickable': props.clickable,
        },
        props.customClass,
    ]);

    const handleClick = (event: MouseEvent | KeyboardEvent) => {
        if (props.clickable) {
            emit('click', event);
        }
    };

    const handleRemove = () => {
        emit('remove');
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .badge {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        font-weight: vars.$font-weight-medium;
        white-space: nowrap;
        transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        line-height: 1;

        // Sizes
        &--sm {
            padding: 2px vars.$spacing-xxs;
            border-radius: vars.$border-radius-sm;
        }

        &--md {
            padding: vars.$spacing-xxs vars.$spacing-xs;
            border-radius: vars.$border-radius-md;
        }

        &--lg {
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-md;
        }

        // Variants
        &--primary {
            background-color: func.color-alpha(vars.$primary-color, 0.12);
            color: vars.$primary-color;

            &:hover {
                background-color: func.color-alpha(vars.$primary-color, 0.18);
            }
        }

        &--secondary {
            background-color: func.color-alpha(vars.$secondary-color, 0.12);
            color: vars.$secondary-color;

            &:hover {
                background-color: func.color-alpha(vars.$secondary-color, 0.18);
            }
        }

        &--success {
            background-color: func.color-alpha(vars.$success-color, 0.12);
            color: vars.$success-color;

            &:hover {
                background-color: func.color-alpha(vars.$success-color, 0.18);
            }
        }

        &--warning {
            background-color: func.color-alpha(vars.$warning-color, 0.15);
            color: vars.$warning-dark;

            &:hover {
                background-color: func.color-alpha(vars.$warning-color, 0.22);
            }
        }

        &--danger {
            background-color: func.color-alpha(vars.$danger-color, 0.12);
            color: vars.$danger-color;

            &:hover {
                background-color: func.color-alpha(vars.$danger-color, 0.18);
            }
        }

        &--info {
            background-color: func.color-alpha(vars.$info-color, 0.12);
            color: vars.$info-color;

            &:hover {
                background-color: func.color-alpha(vars.$info-color, 0.18);
            }
        }

        &--outline {
            background-color: transparent;
            border: 1px solid vars.$gray-light;
            color: vars.$text-secondary;

            &:hover {
                border-color: vars.$gray;
                background-color: func.color-alpha(vars.$gray-light, 0.3);
            }
        }

        // Rounded
        &--rounded {
            border-radius: vars.$border-radius-full;
        }

        // Clickable
        &--clickable {
            cursor: pointer;

            &:hover {
                transform: translateY(-1px);
            }

            &:active {
                transform: translateY(0);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }

        // Icon
        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        // Dot
        &__dot {
            width: 6px;
            height: 6px;
            border-radius: vars.$border-radius-full;
            background-color: currentcolor;
            animation: dot-pulse 2s ease-in-out infinite;
        }

        // Remove button
        &__remove {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            margin-left: 2px;
            background: none;
            border: none;
            color: currentcolor;
            opacity: 0.6;
            cursor: pointer;
            border-radius: vars.$border-radius-full;
            transition: all 0.15s ease;

            &:hover {
                opacity: 1;
                background-color: func.color-alpha(vars.$black, 0.1);
            }

            &:focus-visible {
                outline: 2px solid currentcolor;
                outline-offset: 1px;
            }
        }
    }

    @keyframes dot-pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: 0.5;
            transform: scale(0.9);
        }
    }
</style>
