<template>
    <main :id="id" :class="mainClasses" :aria-labelledby="titleId">
        <GlassBackground
            v-if="withGlassBackground"
            :variant="glassVariant"
            :show-dots="showDots"
            :animated="glassAnimated"
            :bubble-count="bubbleCount"
        />

        <div :class="{ container: withContainer }">
            <header v-if="hasHeader" class="main__header">
                <slot name="header">
                    <h1 v-if="title" :id="titleId" class="main__title">{{ title }}</h1>
                    <p v-if="subtitle" class="main__subtitle">{{ subtitle }}</p>
                </slot>
            </header>

            <div class="main__content">
                <slot></slot>
            </div>

            <footer v-if="$slots.footer" class="main__footer">
                <slot name="footer"></slot>
            </footer>
        </div>
    </main>
</template>

<script setup lang="ts">
    import { computed, useSlots } from 'vue';

    import GlassBackground from '@/components/ui/GlassBackground.vue';

    import type { MainLayoutProps } from '@/types/components/layouts';

    const props = withDefaults(defineProps<MainLayoutProps>(), {
        id: undefined,
        title: '',
        subtitle: '',
        size: 'large',
        variant: 'default',
        withContainer: true,
        withGlassBackground: false,
        glassVariant: 'secondary',
        showDots: false,
        glassAnimated: true,
        bubbleCount: 4,
        customClass: '',
    });

    const titleId = computed(() => {
        if (!props.title) {
            return undefined;
        }
        // Generate a stable ID based on the title
        const slug = props.title
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '');
        return `main-title-${slug}`;
    });

    const slots = useSlots();

    const hasHeader = computed(() => !!slots.header || !!props.title || !!props.subtitle);

    const mainClasses = computed(() => ['main', `main--${props.size}`, `main--${props.variant}`, props.customClass]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .main {
        position: relative;
        padding: vars.$spacing-xxl 0;
        background: transparent;
        overflow: clip;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-xl 0;
        }

        /* Elements */
        &__header {
            text-align: center;
            max-width: 800px;
            margin: 0 auto vars.$spacing-xl;
            position: relative;
            z-index: 5;

            @include mix.responsive(mobile) {
                margin-bottom: vars.$spacing-lg;
            }
        }

        &__title {
            margin-bottom: vars.$spacing-md;
            position: relative;
            display: inline-block;
            color: vars.$text-primary;

            &::after {
                content: '';
                display: block;
                width: 60px;
                height: 4px;
                background: linear-gradient(90deg, vars.$primary-color, vars.$secondary-color);
                margin: vars.$spacing-sm auto 0;
                border-radius: 2px;
            }
        }

        &__subtitle {
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
            max-width: 700px;
            margin: 0 auto;
        }

        &__content {
            width: 100%;
            position: relative;
            z-index: 5;
        }

        &__footer {
            margin-top: vars.$spacing-xxl;
            text-align: center;
            position: relative;
            z-index: 5;

            @include mix.responsive(mobile) {
                margin-top: vars.$spacing-xl;
            }
        }

        // Size modifiers
        &--tight {
            padding: vars.$spacing-lg 0;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-md 0;
            }

            .main__header {
                margin-bottom: vars.$spacing-lg;

                @include mix.responsive(mobile) {
                    margin-bottom: vars.$spacing-md;
                }
            }
        }

        &--default,
        &--large {
            padding: vars.$spacing-xxl 0;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xl 0;
            }
        }

        // All variants are transparent - background managed by parent or GlassBackground
        &--default,
        &--light,
        &--primary,
        &--gradient,
        &--glass,
        &--dark,
        &--transparent {
            background: transparent;
        }
    }
</style>
