<template>
    <component :is="clickable ? 'button' : 'article'" :class="cardClasses" :style="cardStyle" @click="handleClick">
        <div v-if="accentColor" class="card__accent" aria-hidden="true"></div>

        <figure v-if="$slots.image" class="card__image">
            <slot name="image"></slot>
        </figure>

        <header v-if="$slots.header || title" class="card__header">
            <slot name="header">
                <div class="card__header-content">
                    <h5 v-if="title" class="card__title">{{ title }}</h5>
                    <small v-if="subtitle" class="card__subtitle">{{ subtitle }}</small>
                </div>
            </slot>
            <div v-if="$slots.actions" class="card__actions">
                <slot name="actions"></slot>
            </div>
        </header>

        <div v-if="$slots.default" class="card__body">
            <slot></slot>
        </div>

        <footer v-if="$slots.footer" class="card__footer">
            <slot name="footer"></slot>
        </footer>
    </component>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { CardProps } from '@/types/components/base';

    type Props = CardProps;

    const props = withDefaults(defineProps<Props>(), {
        title: '',
        subtitle: '',
        variant: 'default',
        padding: 'md',
        hoverable: false,
        clickable: false,
        accentColor: '',
        fullHeight: false,
        customClass: '',
    });

    const emit = defineEmits<{
        click: [event: MouseEvent];
    }>();

    const cardClasses = computed(() => [
        'card',
        `card--${props.variant}`,
        `card--padding-${props.padding}`,
        {
            'card--hoverable': props.hoverable,
            'card--clickable': props.clickable,
            'card--has-accent': props.accentColor,
            'card--full-height': props.fullHeight,
        },
        props.customClass,
    ]);

    const cardStyle = computed(() => ({
        '--card-accent-color': props.accentColor || undefined,
    }));

    const handleClick = (event: MouseEvent) => {
        if (props.clickable) {
            emit('click', event);
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .card {
        position: relative;
        display: flex;
        flex-direction: column;
        background-color: vars.$white;
        border-radius: vars.$border-radius-xl;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        overflow: hidden;

        // Reset button styles when clickable
        &--clickable {
            border: none;
            text-align: left;
            width: 100%;
            font-family: inherit;
            font-size: inherit;
            cursor: pointer;
        }

        // Variants
        &--default {
            border: 1px solid func.color-alpha(vars.$gray-light, 0.6);
        }

        &--elevated {
            border: none;
            box-shadow: vars.$box-shadow-medium;
        }

        &--outlined {
            border: 2px solid vars.$gray-light;
            background-color: transparent;
        }

        &--glass {
            background: func.color-alpha(vars.$white, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid func.color-alpha(vars.$white, 0.3);
        }

        // Padding
        &--padding-none {
            .card__header,
            .card__body,
            .card__footer {
                padding: 0;
            }
        }

        &--padding-sm {
            .card__header,
            .card__body,
            .card__footer {
                padding: vars.$spacing-xs;
            }
        }

        &--padding-md {
            .card__header,
            .card__body,
            .card__footer {
                padding: vars.$spacing-md;
            }
        }

        &--padding-lg {
            .card__header,
            .card__body,
            .card__footer {
                padding: vars.$spacing-lg;
            }
        }

        // States
        &--hoverable,
        &--clickable {
            &:hover {
                transform: translateY(-4px);
                box-shadow: vars.$box-shadow-medium;
                border-color: transparent;
            }

            &:active {
                transform: translateY(-2px);
            }
        }

        &--clickable:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }

        &--full-height {
            height: 100%;
        }

        // Accent
        &__accent {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background-color: var(--card-accent-color);
        }

        &--has-accent {
            padding-top: 3px;
        }

        // Image
        &__image {
            width: 100%;
            margin: 0;
            position: relative;
            overflow: hidden;

            :deep(img) {
                width: 100%;
                height: auto;
                display: block;
                object-fit: cover;
                transition: transform 0.4s ease;
            }
        }

        &--hoverable &__image :deep(img),
        &--clickable &__image :deep(img) {
            &:hover {
                transform: scale(1.03);
            }
        }

        // Header
        &__header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: vars.$spacing-md;

            &:not(:last-child) {
                border-bottom: 1px solid func.color-alpha(vars.$gray-light, 0.5);
            }
        }

        &__header-content {
            flex: 1;
            min-width: 0;
        }

        &__title {
            margin: 0;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            line-height: vars.$line-height-tight;
        }

        &__subtitle {
            margin: vars.$spacing-xxs 0 0;
            color: vars.$text-secondary;
        }

        &__actions {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            flex-shrink: 0;
        }

        // Body
        &__body {
            flex: 1;
        }

        // Footer
        &__footer {
            margin-top: auto;

            &:not(:first-child) {
                border-top: 1px solid func.color-alpha(vars.$gray-light, 0.5);
            }
        }

        @include mix.focus-outline;
    }
</style>
