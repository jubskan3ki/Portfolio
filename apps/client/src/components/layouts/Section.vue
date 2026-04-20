<template>
    <section :id="id" :class="sectionClasses" :data-animation="animationType" :aria-labelledby="titleId">
        <div :class="{ container: withContainer }">
            <header v-if="hasHeader" class="section__header">
                <slot name="header">
                    <h2 v-if="title" :id="titleId" class="section__title">{{ title }}</h2>
                    <p v-if="subtitle" class="section__subtitle">{{ subtitle }}</p>
                </slot>
            </header>

            <div class="section__content">
                <slot></slot>
            </div>

            <footer v-if="$slots.footer" class="section__footer">
                <slot name="footer"></slot>
            </footer>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { computed, useSlots } from 'vue';

    import type { SectionProps } from '@/types/components/layouts';

    const props = withDefaults(defineProps<SectionProps>(), {
        id: undefined,
        title: '',
        subtitle: '',
        size: 'default',
        variant: 'default',
        withContainer: true,
        animated: false,
        animationType: 'fade',
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
        return `section-title-${slug}`;
    });

    const slots = useSlots();

    const hasHeader = computed(() => !!slots.header || !!props.title || !!props.subtitle);

    const sectionClasses = computed(() => [
        'section',
        `section--${props.size}`,
        `section--${props.variant}`,
        {
            'section--animated': props.animated,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .section {
        padding: vars.$spacing-xl 0;
        position: relative;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg 0;
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-sm;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;

            &::before,
            &::after {
                content: '';
                flex: 1;
                max-width: 80px;
                height: 1px;
                background: linear-gradient(90deg, transparent, func.color-alpha(vars.$primary-color, 0.2));
            }

            &::after {
                background: linear-gradient(90deg, func.color-alpha(vars.$primary-color, 0.2), transparent);
            }
        }

        &__subtitle {
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
            max-width: 600px;
            margin: 0 auto;
        }

        &__content {
            width: 100%;
            position: relative;
            z-index: 5;
        }

        &__footer {
            margin-top: vars.$spacing-xl;
            text-align: center;
            position: relative;
            z-index: 5;

            @include mix.responsive(mobile) {
                margin-top: vars.$spacing-lg;
            }
        }

        // Size modifiers
        &--tight {
            padding: vars.$spacing-lg 0;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-md 0;
            }

            .section__header {
                margin-bottom: vars.$spacing-lg;

                @include mix.responsive(mobile) {
                    margin-bottom: vars.$spacing-md;
                }
            }
        }

        &--large {
            padding: vars.$spacing-xxl 0;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xl 0;
            }
        }

        // Variant modifiers - All transparent

        /* All variants transparent - dots visible through */
        &--default,
        &--light,
        &--primary,
        &--gradient,
        &--glass {
            background: transparent;
        }

        /* Dark - only variant with background */
        &--dark {
            background: vars.$gray-dark;
            color: vars.$white;

            .section__title {
                color: vars.$white;

                &::before,
                &::after {
                    background: linear-gradient(90deg, transparent, func.color-alpha(vars.$secondary-color, 0.3));
                }

                &::after {
                    background: linear-gradient(90deg, func.color-alpha(vars.$secondary-color, 0.3), transparent);
                }
            }

            .section__subtitle {
                color: func.color-alpha(vars.$white, 0.75);
            }
        }

        // Animation modifiers
        &--animated {
            .section__header {
                animation: fade-in-down 0.5s ease-out;
            }

            .section__content {
                animation: fade-in-up 0.5s ease-out 0.1s both;
            }

            .section__footer {
                animation: fade-in-up 0.5s ease-out 0.2s both;
            }

            &[data-animation='slide'] {
                .section__content {
                    animation: slide-in-right 0.5s ease-out both;
                }
            }

            &[data-animation='scale'] {
                .section__content {
                    animation: scale-in 0.5s ease-out both;
                }
            }

            &[data-animation='none'] {
                .section__header,
                .section__content,
                .section__footer {
                    animation: none;
                }
            }
        }
    }

    /* Keyframes */
    @keyframes fade-in-down {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slide-in-right {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes scale-in {
        from {
            opacity: 0;
            transform: scale(0.95);
        }

        to {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>
