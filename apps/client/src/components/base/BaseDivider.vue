<template>
    <div :class="dividerClasses" :role="label ? 'separator' : undefined">
        <small v-if="label" class="divider__label">
            <slot>{{ label }}</slot>
        </small>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { DividerProps } from '@/types/components/base';

    type Props = DividerProps;

    const props = withDefaults(defineProps<Props>(), {
        orientation: 'horizontal',
        variant: 'solid',
        spacing: 'md',
        label: '',
        customClass: '',
    });

    const dividerClasses = computed(() => [
        'divider',
        `divider--${props.orientation}`,
        `divider--${props.variant}`,
        `divider--spacing-${props.spacing}`,
        {
            'divider--with-label': !!props.label,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .divider {
        display: flex;
        align-items: center;
        color: vars.$text-secondary;

        &--horizontal {
            width: 100%;
            flex-direction: row;

            &::before,
            &::after {
                content: '';
                flex: 1;
                height: 1px;
                background-color: vars.$gray-light;
            }

            &.divider--dashed::before,
            &.divider--dashed::after {
                background: repeating-linear-gradient(
                    90deg,
                    vars.$gray-light,
                    vars.$gray-light 4px,
                    transparent 4px,
                    transparent 8px
                );
            }

            &.divider--dotted::before,
            &.divider--dotted::after {
                background: repeating-linear-gradient(
                    90deg,
                    vars.$gray-light,
                    vars.$gray-light 2px,
                    transparent 2px,
                    transparent 6px
                );
            }
        }

        &--vertical {
            flex-direction: column;
            height: 100%;
            min-height: 20px;

            &::before,
            &::after {
                content: '';
                flex: 1;
                width: 1px;
                background-color: vars.$gray-light;
            }

            &.divider--dashed::before,
            &.divider--dashed::after {
                background: repeating-linear-gradient(
                    180deg,
                    vars.$gray-light,
                    vars.$gray-light 4px,
                    transparent 4px,
                    transparent 8px
                );
            }

            &.divider--dotted::before,
            &.divider--dotted::after {
                background: repeating-linear-gradient(
                    180deg,
                    vars.$gray-light,
                    vars.$gray-light 2px,
                    transparent 2px,
                    transparent 6px
                );
            }
        }

        &--spacing-none {
            margin: 0;
        }

        &--spacing-sm {
            &.divider--horizontal {
                margin: vars.$spacing-xs 0;
            }

            &.divider--vertical {
                margin: 0 vars.$spacing-xs;
            }
        }

        &--spacing-md {
            &.divider--horizontal {
                margin: vars.$spacing-md 0;
            }

            &.divider--vertical {
                margin: 0 vars.$spacing-md;
            }
        }

        &--spacing-lg {
            &.divider--horizontal {
                margin: vars.$spacing-lg 0;
            }

            &.divider--vertical {
                margin: 0 vars.$spacing-lg;
            }
        }

        &__label {
            padding: 0 vars.$spacing-md;
            font-weight: vars.$font-weight-medium;
            white-space: nowrap;
        }

        &--vertical &__label {
            padding: vars.$spacing-xs 0;
            writing-mode: vertical-rl;
            text-orientation: mixed;
        }

        &:not(.divider--with-label) {
            &::after {
                display: none;
            }
        }
    }
</style>
