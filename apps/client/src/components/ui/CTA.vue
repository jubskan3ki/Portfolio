<template>
    <section class="cta" :class="[`cta--${variant}`]">
        <SectionBackground :variant="variant" />

        <div class="container">
            <div class="cta__card">
                <div class="cta__card-inner">
                    <h2 class="cta__title">{{ title }}</h2>
                    <p v-if="description" class="cta__description">{{ description }}</p>

                    <div class="cta__actions">
                        <NuxtLink
                            v-if="primaryButtonConfig.show"
                            :to="primaryButtonConfig.to"
                            class="cta__btn cta__btn--primary"
                        >
                            {{ primaryButtonConfig.label }}
                            <BaseIcon v-if="primaryButtonConfig.icon" :name="primaryButtonConfig.icon" :size="18" />
                        </NuxtLink>

                        <NuxtLink
                            v-if="secondaryButtonConfig.show"
                            :to="secondaryButtonConfig.to"
                            class="cta__btn cta__btn--secondary"
                        >
                            {{ secondaryButtonConfig.label }}
                            <BaseIcon name="arrow-right" :size="16" />
                        </NuxtLink>
                    </div>
                </div>

                <span class="cta__float cta__float--1"></span>
                <span class="cta__float cta__float--2"></span>
                <span class="cta__float cta__float--3"></span>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SectionBackground from '@/components/ui/SectionBackground.vue';

    import type { CTAProps } from '@/types/components/ui';

    const props = withDefaults(defineProps<CTAProps>(), {
        title: 'Vous avez un projet ?',
        description: '',
        variant: 'primary',
        primaryButton: () => ({
            show: true,
            label: 'Me contacter',
            to: '/contact',
            icon: 'arrow-right',
        }),
        secondaryButton: () => ({
            show: false,
            label: 'En savoir plus',
            to: '/projects',
        }),
    });

    const primaryButtonConfig = computed(() => ({
        show: props.primaryButton?.show !== false,
        label: props.primaryButton?.label || 'Me contacter',
        to: props.primaryButton?.to || '/contact',
        icon: props.primaryButton?.icon || 'arrow-right',
    }));

    const secondaryButtonConfig = computed(() => ({
        show: props.secondaryButton ? props.secondaryButton.show !== false : false,
        label: props.secondaryButton?.label || 'En savoir plus',
        to: props.secondaryButton?.to || '/projects',
    }));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;
    @use '@/styles/components/cta-variants' as cta;

    .cta {
        position: relative;
        padding: vars.$spacing-xxl 0;
        overflow: hidden;
        // Skip layout/paint + pause infinite float/bubble animations when offscreen.
        content-visibility: auto;
        contain-intrinsic-size: auto 600px;

        // Background
        &__bg {
            position: absolute;
            inset: 0;
            pointer-events: none;
        }

        &__dots {
            position: absolute;
            inset: 0;
            opacity: 0.4;

            @include mix.dots-pattern(currentColor, 1px, 32px);
        }

        &__gradient {
            position: absolute;
            inset: 0;
            background: radial-gradient(
                ellipse 80% 50% at 50% -20%,
                fn.color-alpha(vars.$primary-color, 0.15),
                transparent
            );
        }

        // Glass card
        &__card {
            position: relative;
            max-width: 800px;
            margin: 0 auto;
            padding: vars.$spacing-xxl;
            text-align: center;
            border-radius: vars.$border-radius-xl;
            backdrop-filter: blur(16px);
            transition: transform 0.4s ease;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xl vars.$spacing-lg;
            }

            &:hover {
                transform: translateY(-4px);

                .cta__float {
                    transform: translateY(-8px);
                }
            }
        }

        &__card-inner {
            position: relative;
            z-index: 2;
        }

        // Floating decorative elements
        &__float {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);

            @media (prefers-reduced-motion: reduce),
                (hover: none) and (pointer: coarse) {
                animation: none !important;
            }

            &--1 {
                top: -20px;
                right: 10%;
                width: 40px;
                height: 40px;
                animation: float-1 8s ease-in-out infinite;
            }

            &--2 {
                bottom: -15px;
                left: 15%;
                width: 24px;
                height: 24px;
                animation: float-2 6s ease-in-out infinite;
            }

            &--3 {
                top: 30%;
                right: -10px;
                width: 16px;
                height: 16px;
                animation: float-3 7s ease-in-out infinite;

                @include mix.responsive(mobile) {
                    display: none;
                }
            }
        }

        // Title
        &__title {
            margin: 0 0 vars.$spacing-sm;
            font-weight: vars.$font-weight-bold;
            line-height: vars.$line-height-tight;
        }

        // Description
        &__description {
            margin: 0 0 vars.$spacing-lg;
            line-height: vars.$line-height-relaxed;
            max-width: 500px;
            margin-inline: auto;
        }

        // Actions
        &__actions {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-md;
            flex-wrap: wrap;

            @include mix.responsive(mobile) {
                flex-direction: column;
                width: 100%;
            }
        }

        // Buttons
        &__btn {
            position: relative;
            isolation: isolate;
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-sm vars.$spacing-xl;
            font-weight: vars.$font-weight-semibold;
            text-decoration: none;
            border-radius: vars.$border-radius-lg;
            transition: transform 0.3s ease;

            @include mix.responsive(mobile) {
                width: 100%;
                justify-content: center;
            }

            svg {
                transition: transform 0.3s ease;
            }

            &:hover {
                transform: translateY(-1px);

                svg {
                    transform: translateX(3px);
                }
            }

            &--secondary {
                background: transparent;
            }
        }

        // Bubbles container
        &__bubbles {
            position: absolute;
            inset: 0;
            overflow: hidden;
        }

        &__bubble {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;

            @media (prefers-reduced-motion: reduce),
                (hover: none) and (pointer: coarse) {
                animation: none !important;
            }

            &--1 {
                width: 60px;
                height: 60px;
                top: 10%;
                right: 15%;
                animation: float-bubble 8s ease-in-out infinite;
            }

            &--2 {
                width: 35px;
                height: 35px;
                bottom: 20%;
                left: 10%;
                animation: float-bubble 6s ease-in-out infinite reverse;
            }

            &--3 {
                width: 25px;
                height: 25px;
                top: 50%;
                left: 25%;
                animation: float-bubble 7s ease-in-out infinite 1s;

                @include mix.responsive(mobile) {
                    display: none;
                }
            }

            &--4 {
                width: 45px;
                height: 45px;
                bottom: 15%;
                right: 25%;
                animation: float-bubble 9s ease-in-out infinite 0.5s;

                @include mix.responsive(mobile) {
                    width: 30px;
                    height: 30px;
                }
            }

            &--5 {
                width: 18px;
                height: 18px;
                top: 20%;
                left: 5%;
                animation: float-bubble 5s ease-in-out infinite 2s reverse;
            }
        }

        // Primary variant
        &--primary {
            @include cta.cta-variant(
                (
                    bg: linear-gradient(180deg, vars.$primary-light 0%, vars.$primary-dark 100%),
                    dots-hidden: true,
                    card-bg: fn.color-alpha(vars.$white, 0.1),
                    card-border: fn.color-alpha(vars.$white, 0.2),
                    card-shadow: (
                        0 8px 32px fn.color-alpha(vars.$black, 0.1),
                        inset 0 1px 0 fn.color-alpha(vars.$white, 0.2),
                    ),
                    bubble-base: fn.color-alpha(vars.$white, 0.15),
                    bubble-shadow: 0 4px 16px fn.color-alpha(vars.$white, 0.1),
                    bubble-alphas: (
                        1: 0.22,
                        2: 0.14,
                        3: 0.18,
                        4: 0.16,
                        5: 0.12,
                    ),
                    title-color: vars.$white,
                    desc-color: fn.color-alpha(vars.$white, 0.85),
                    btn-primary-color: vars.$primary-color,
                    btn-primary-bg: vars.$white,
                    btn-primary-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.15),
                    btn-primary-hover-shadow: 0 8px 24px fn.color-alpha(vars.$black, 0.2),
                    btn-secondary-color: vars.$white,
                    btn-secondary-border: fn.color-alpha(vars.$white, 0.3),
                    btn-secondary-hover-bg: fn.color-alpha(vars.$white, 0.1),
                    btn-secondary-hover-border: fn.color-alpha(vars.$white, 0.5),
                )
            );
        }

        // Dark variant
        &--dark {
            @include cta.cta-variant(
                (
                    bg: vars.$black-light,
                    dots-color: fn.color-alpha(vars.$primary-color, 0.65),
                    gradient: radial-gradient(
                            ellipse 80% 50% at 50% -20%,
                            fn.color-alpha(vars.$primary-dark, 0.4),
                            transparent
                        ),
                    card-bg: fn.color-alpha(vars.$primary-dark, 0.3),
                    card-border: fn.color-alpha(vars.$primary-color, 0.2),
                    card-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.3),
                    title-color: vars.$white,
                    desc-color: fn.color-alpha(vars.$white, 0.75),
                    btn-primary-color: vars.$primary-dark,
                    btn-primary-bg: vars.$white,
                    btn-primary-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.2),
                    btn-primary-hover-shadow: 0 8px 24px fn.color-alpha(vars.$black, 0.3),
                    btn-secondary-color: vars.$secondary-light,
                    btn-secondary-border: fn.color-alpha(vars.$primary-color, 0.3),
                    btn-secondary-hover-bg: fn.color-alpha(vars.$primary-color, 0.15),
                    btn-secondary-hover-border: fn.color-alpha(vars.$primary-color, 0.5),
                    btn-secondary-hover-color: vars.$white,
                )
            );
        }

        // Light variant
        &--light {
            @include cta.cta-variant(
                (
                    bg: vars.$bg-secondary,
                    dots-pattern: fn.color-alpha(vars.$gray, 0.4),
                    gradient: radial-gradient(
                            ellipse 80% 50% at 50% -20%,
                            fn.color-alpha(vars.$primary-color, 0.08),
                            transparent
                        ),
                    card-bg: fn.color-alpha(vars.$white, 0.8),
                    card-border: fn.color-alpha(vars.$white, 0.9),
                    card-shadow: (
                        0 8px 32px fn.color-alpha(vars.$black, 0.06),
                        0 1px 2px fn.color-alpha(vars.$black, 0.04),
                        inset 0 1px 0 vars.$white,
                    ),
                    title-color: vars.$text-primary,
                    desc-color: vars.$text-secondary,
                    btn-primary-color: vars.$white,
                    btn-primary-bg: vars.$primary-color,
                    btn-primary-shadow: 0 4px 16px fn.color-alpha(vars.$primary-color, 0.3),
                    btn-primary-hover-shadow: 0 8px 24px fn.color-alpha(vars.$primary-color, 0.4),
                    btn-secondary-color: vars.$text-secondary,
                    btn-secondary-border: vars.$border-color,
                    btn-secondary-hover-color: vars.$primary-color,
                    btn-secondary-hover-border: vars.$primary-color,
                    btn-secondary-hover-bg: fn.color-alpha(vars.$primary-color, 0.05),
                )
            );
        }

        // Secondary variant
        &--secondary {
            @include cta.cta-variant(
                (
                    bg: linear-gradient(180deg, vars.$primary-dark 0%, vars.$black-light 100%),
                    dots-hidden: true,
                    gradient: radial-gradient(
                            ellipse 80% 50% at 50% -20%,
                            fn.color-alpha(vars.$primary-color, 0.25),
                            transparent
                        ),
                    card-bg: fn.color-alpha(vars.$white, 0.05),
                    card-border: fn.color-alpha(vars.$primary-color, 0.3),
                    card-shadow: (
                        0 8px 32px fn.color-alpha(vars.$black, 0.4),
                        0 0 60px fn.color-alpha(vars.$primary-color, 0.15),
                        inset 0 1px 0 fn.color-alpha(vars.$white, 0.08),
                    ),
                    bubble-base: fn.color-alpha(vars.$white, 0.12),
                    bubble-shadow: 0 4px 24px fn.color-alpha(vars.$primary-color, 0.4),
                    bubble-alphas: (
                        1: 0.18,
                        2: 0.14,
                        3: 0.16,
                        4: 0.12,
                        5: 0.1,
                    ),
                    title-color: vars.$white,
                    desc-color: fn.color-alpha(vars.$white, 0.8),
                    btn-primary-color: vars.$primary-color,
                    btn-primary-bg: vars.$white,
                    btn-primary-shadow: 0 4px 16px fn.color-alpha(vars.$black, 0.25),
                    btn-primary-hover-shadow: 0 8px 24px fn.color-alpha(vars.$black, 0.35),
                    btn-secondary-color: vars.$white,
                    btn-secondary-border: fn.color-alpha(vars.$primary-color, 0.4),
                    btn-secondary-hover-bg: fn.color-alpha(vars.$primary-color, 0.15),
                    btn-secondary-hover-border: fn.color-alpha(vars.$primary-color, 0.6),
                )
            );
        }
    }

    // Floating animations
    @keyframes float-1 {
        0%,
        100% {
            transform: translate(0, 0) rotate(0deg);
        }

        25% {
            transform: translate(-5px, -10px) rotate(5deg);
        }

        50% {
            transform: translate(5px, -5px) rotate(-3deg);
        }

        75% {
            transform: translate(-3px, -12px) rotate(2deg);
        }
    }

    @keyframes float-2 {
        0%,
        100% {
            transform: translate(0, 0);
        }

        33% {
            transform: translate(8px, -8px);
        }

        66% {
            transform: translate(-4px, -12px);
        }
    }

    @keyframes float-3 {
        0%,
        100% {
            transform: translate(0, 0) scale(1);
        }

        50% {
            transform: translate(-6px, -10px) scale(1.1);
        }
    }

    // Bubble animations (for bubble variants)
    @keyframes float-bubble {
        0%,
        100% {
            transform: translate(0, 0) rotate(0deg);
        }

        25% {
            transform: translate(-5px, -10px) rotate(5deg);
        }

        50% {
            transform: translate(5px, -5px) rotate(-3deg);
        }

        75% {
            transform: translate(-3px, -12px) rotate(2deg);
        }
    }
</style>
