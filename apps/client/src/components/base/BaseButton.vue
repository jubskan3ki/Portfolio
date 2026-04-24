<template>
    <NuxtLink v-if="isInternalLink" v-bind="componentProps" :class="buttonClasses" @click="handleClick">
        <span v-if="loading" class="button__loader">
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
        </span>
        <span v-else class="button__content">
            <slot name="icon-left">
                <BaseIcon v-if="icon && iconPosition !== 'right'" :name="icon" :size="iconSize" />
            </slot>
            <slot>{{ displayText }}</slot>
            <slot name="icon-right">
                <BaseIcon v-if="icon && iconPosition === 'right'" :name="icon" :size="iconSize" />
            </slot>
        </span>
    </NuxtLink>

    <a
        v-else-if="isExternalLink"
        v-bind="componentProps"
        :class="buttonClasses"
        @click="handleClick"
        @keydown.enter="handleClick"
    >
        <span v-if="loading" class="button__loader">
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
        </span>
        <span v-else class="button__content">
            <slot name="icon-left">
                <BaseIcon v-if="icon && iconPosition !== 'right'" :name="icon" :size="iconSize" />
            </slot>
            <slot>{{ displayText }}</slot>
            <slot name="icon-right">
                <BaseIcon v-if="icon && iconPosition === 'right'" :name="icon" :size="iconSize" />
            </slot>
        </span>
    </a>

    <button
        v-else
        v-bind="componentProps"
        :class="buttonClasses"
        :disabled="disabled || loading"
        @click="handleClick"
    >
        <span v-if="loading" class="button__loader">
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
            <span class="button__loader-dot"></span>
        </span>
        <span v-else class="button__content">
            <slot name="icon-left">
                <BaseIcon v-if="icon && iconPosition !== 'right'" :name="icon" :size="iconSize" />
            </slot>
            <slot>{{ displayText }}</slot>
            <slot name="icon-right">
                <BaseIcon v-if="icon && iconPosition === 'right'" :name="icon" :size="iconSize" />
            </slot>
        </span>
    </button>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useLinkResolver } from '@/composables/ui/useLinkResolver';

    import type { ButtonVariant, ButtonSize, LinkTarget, ButtonProps } from '@/types/components/base';

    type Props = Omit<ButtonProps, 'variant' | 'size' | 'target'> & {
        variant?: ButtonVariant | '';
        size?: ButtonSize | '';
        target?: LinkTarget | '';
        label?: string;
        icon?: string;
        iconPosition?: 'left' | 'right';
        iconSize?: number;
    };

    const props = withDefaults(defineProps<Props>(), {
        text: '',
        type: 'button',
        variant: '',
        size: '',
        disabled: false,
        loading: false,
        fullWidth: false,
        customClass: '',
        to: '',
        params: () => ({}),
        target: '',
        ariaLabel: '',
        label: '',
        icon: '',
        iconPosition: 'left',
        iconSize: 16,
    });

    const emit = defineEmits<{
        click: [event: MouseEvent];
    }>();

    const displayText = computed(() => props.label || props.text);

    const { isInternalLink, isExternalLink, linkProps } = useLinkResolver(() => ({
        to: props.to,
        params: props.params,
        target: props.target,
    }));

    const effectiveAriaLabel = computed(() => {
        if (props.ariaLabel) {
            return props.ariaLabel;
        }
        if (props.loading) {
            return 'Chargement en cours';
        }
        return undefined;
    });

    const componentProps = computed(() => {
        if (isInternalLink.value) {
            return {
                ...linkProps.value,
                'aria-label': effectiveAriaLabel.value,
                ...(props.prefetch === false ? { prefetch: false } : {}),
            };
        }
        if (isExternalLink.value) {
            return {
                ...linkProps.value,
                'aria-label': effectiveAriaLabel.value,
            };
        }
        return {
            type: props.type,
            'aria-label': effectiveAriaLabel.value,
            'aria-busy': props.loading || undefined,
        };
    });

    const buttonClasses = computed(() => [
        'button',
        props.variant && `button--${props.variant}`,
        props.size && `button--${props.size}`,
        {
            'button--disabled': props.disabled,
            'button--loading': props.loading,
            'button--full-width': props.fullWidth,
        },
        props.customClass,
    ]);

    const handleClick = (event: MouseEvent | KeyboardEvent) => {
        if (props.disabled || props.loading) {
            event.preventDefault();
            return;
        }
        if (event instanceof MouseEvent) {
            emit('click', event);
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: vars.$spacing-xxs;
        padding: vars.$spacing-xs vars.$spacing-md;
        border: none;
        border-radius: vars.$border-radius-md;
        background-color: vars.$primary-color;
        color: vars.$white;
        font-family: vars.$font-family;
        font-weight: vars.$font-weight-medium;
        text-decoration: none;
        cursor: pointer;
        transition: all vars.$transition-base;

        @include mix.focus-outline;

        &:hover:not(:disabled) {
            background-color: vars.$primary-dark;
        }

        &__content {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
        }

        &--primary {
            background-color: vars.$primary-color;
            color: vars.$white;

            &:hover:not(:disabled) {
                background-color: vars.$primary-dark;
            }
        }

        &--secondary {
            background-color: vars.$secondary-color;
            color: vars.$white;

            &:hover:not(:disabled) {
                background-color: vars.$secondary-dark;
            }
        }

        &--outline {
            background-color: transparent;
            border: 2px solid vars.$primary-color;
            color: vars.$primary-color;

            &:hover:not(:disabled) {
                background-color: vars.$primary-color;
                color: vars.$white;
            }
        }

        &--danger {
            background-color: vars.$danger-color;
            color: vars.$white;

            &:hover:not(:disabled) {
                background-color: vars.$danger-dark;
            }
        }

        &--ghost {
            background-color: transparent;
            color: vars.$text-primary;

            &:hover:not(:disabled) {
                background-color: vars.$bg-secondary;
            }
        }

        &--xs {
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
        }

        &--sm {
            padding: vars.$spacing-xxs vars.$spacing-xs;
            font-size: 0.875rem;
        }

        &--lg {
            padding: vars.$spacing-md vars.$spacing-lg;
            font-size: 1.125rem;
        }

        &--xl {
            padding: vars.$spacing-lg vars.$spacing-xl;
            font-size: 1.25rem;
        }

        &--icon {
            padding: vars.$spacing-xs;
            width: 36px;
            height: 36px;
            min-width: 36px;
        }

        &--small {
            padding: vars.$spacing-xxs vars.$spacing-xs;
            font-size: 0.875rem;
        }

        &--large {
            padding: vars.$spacing-md vars.$spacing-lg;
            font-size: 1.125rem;
        }

        &--full-width {
            width: 100%;
        }

        &--disabled,
        &:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            pointer-events: none;
        }

        &--loading {
            cursor: wait;
        }

        &__loader {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xxs;

            &-dot {
                width: 6px;
                height: 6px;
                background-color: currentcolor;
                border-radius: vars.$border-radius-full;
                animation: button-loading 1.2s infinite ease-in-out;

                &:nth-child(1) {
                    animation-delay: 0s;
                }

                &:nth-child(2) {
                    animation-delay: 0.2s;
                }

                &:nth-child(3) {
                    animation-delay: 0.4s;
                }
            }
        }
    }

    @keyframes button-loading {
        0%,
        80%,
        100% {
            transform: scale(0);
            opacity: 0.6;
        }

        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>
