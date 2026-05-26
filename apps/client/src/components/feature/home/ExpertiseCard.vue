<template>
    <component
        :is="props.to ? NuxtLink : 'div'"
        ref="cardRef"
        :to="props.to || undefined"
        :prefetch="props.to && props.prefetch === false ? false : undefined"
        class="expertise-card"
        :class="[`expertise-card--${variant}`, { 'expertise-card--no-motion': prefersReducedMotion }]"
        tabindex="0"
        :aria-label="`Expertise en ${title}`"
        :style="cardStyle"
        @mouseenter="onMouseEnter"
        @mouseleave="onMouseLeave"
        @mousemove="onMouseMove"
    >
        <div class="expertise-card__dots"></div>

        <div v-if="variant === 'primary' || variant === 'secondary'" class="expertise-card__bubbles">
            <span class="expertise-card__bubble expertise-card__bubble--1"></span>
            <span class="expertise-card__bubble expertise-card__bubble--2"></span>
            <span class="expertise-card__bubble expertise-card__bubble--3"></span>
        </div>

        <div class="expertise-card__header">
            <div class="expertise-card__icon">
                <BaseIcon :name="icon" size="md" />
            </div>
            <h2 class="expertise-card__title">{{ title }}</h2>
        </div>
        <p class="expertise-card__description">{{ description }}</p>

        <div class="expertise-card__shine" :style="shineStyle"></div>
    </component>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';

    import type { ExpertiseCardProps } from '@/types/feature/home';
    import type { ComponentPublicInstance } from 'vue';

    type Props = ExpertiseCardProps;

    const props = withDefaults(defineProps<Props>(), {
        color: '#673c5c',
        variant: 'light',
        animateOnScroll: false,
        to: undefined,
        prefetch: undefined,
    });

    const NuxtLink = resolveComponent('NuxtLink');

    const { prefersReducedMotion } = useReducedMotion();

    const cardRef = ref<HTMLElement | ComponentPublicInstance | null>(null);
    const isHovering = ref(false);
    const mouseX = ref(0.5);
    const mouseY = ref(0.5);

    let cachedRect: DOMRect | null = null;

    const resolveEl = (): HTMLElement | null => {
        if (!cardRef.value) {
            return null;
        }
        const el = (cardRef.value as ComponentPublicInstance)?.$el ?? cardRef.value;
        return el instanceof HTMLElement ? el : null;
    };

    const onMouseEnter = () => {
        if (prefersReducedMotion.value) {
            return;
        }
        isHovering.value = true;
        const el = resolveEl();
        cachedRect = el ? el.getBoundingClientRect() : null;
    };

    const onMouseLeave = () => {
        isHovering.value = false;
        mouseX.value = 0.5;
        mouseY.value = 0.5;
        cachedRect = null;
    };

    const onMouseMove = (e: MouseEvent) => {
        if (prefersReducedMotion.value || !cachedRect) {
            return;
        }
        mouseX.value = (e.clientX - cachedRect.left) / cachedRect.width;
        mouseY.value = (e.clientY - cachedRect.top) / cachedRect.height;
    };

    const getGradientColors = computed(() => {
        const baseColor = props.color || '#673c5c';
        const lightColor = adjustColorBrightness(baseColor, 30);
        return { base: baseColor, light: lightColor };
    });

    const cardStyle = computed(() => {
        const rotateX = isHovering.value ? (mouseY.value - 0.5) * -10 : 0;
        const rotateY = isHovering.value ? (mouseX.value - 0.5) * 10 : 0;

        return {
            '--card-base-color': getGradientColors.value.base,
            '--card-light-color': getGradientColors.value.light,
            '--rotate-x': `${rotateX}deg`,
            '--rotate-y': `${rotateY}deg`,
        };
    });

    const shineStyle = computed(() => {
        if (!isHovering.value) {
            return { opacity: 0 };
        }
        return {
            opacity: 0.15,
            background: `radial-gradient(circle at ${mouseX.value * 100}% ${mouseY.value * 100}%, var(--card-light-color), transparent 50%)`,
        };
    });

    function adjustColorBrightness(color: string, percent: number): string {
        if (!color.startsWith('#')) {
            return color;
        }
        const hex = color.slice(1);
        const r = parseInt(hex.slice(0, 2), 16);
        const g = parseInt(hex.slice(2, 4), 16);
        const b = parseInt(hex.slice(4, 6), 16);

        const newR = Math.min(255, Math.max(0, r + (255 - r) * (percent / 100)));
        const newG = Math.min(255, Math.max(0, g + (255 - g) * (percent / 100)));
        const newB = Math.min(255, Math.max(0, b + (255 - b) * (percent / 100)));

        return `#${Math.round(newR).toString(16).padStart(2, '0')}${Math.round(newG).toString(16).padStart(2, '0')}${Math.round(newB).toString(16).padStart(2, '0')}`;
    }
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .expertise-card {
        position: relative;
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: vars.$spacing-lg;
        border-radius: vars.$border-radius-xl;
        cursor: pointer;
        overflow: hidden;

        transform-style: preserve-3d;
        transform: perspective(1000px) rotateX(var(--rotate-x, 0deg)) rotateY(var(--rotate-y, 0deg));
        transition:
            transform 0.15s ease-out,
            box-shadow 0.3s ease,
            border-color 0.3s ease;

        &:hover {
            transform: perspective(1000px) rotateX(var(--rotate-x, 0deg)) rotateY(var(--rotate-y, 0deg))
                translateY(-6px) scale(1.02);
        }

        &:focus-visible {
            outline: 2px solid var(--card-base-color);
            outline-offset: 2px;
        }

        &--no-motion {
            transform: none;
            transition: box-shadow 0.3s ease;

            .expertise-card__shine {
                display: none;
            }

            &:hover {
                transform: none;
            }
        }

        &__dots {
            position: absolute;
            top: 0;
            right: 0;
            width: 80px;
            height: 80px;
            mask-image: radial-gradient(circle at top right, black, transparent 70%);
            pointer-events: none;
            z-index: 1;
        }

        &__header {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            margin-bottom: vars.$spacing-md;
            position: relative;
            z-index: 1;
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: vars.$border-radius-md;
            flex-shrink: 0;
            transition: transform 0.3s ease;

            .expertise-card:hover & {
                transform: scale(1.05) translateY(-2px);
            }
        }

        &__title {
            font-size: vars.$font-size-3xl;
            font-weight: vars.$font-weight-semibold;
            margin: 0;
            position: relative;
            z-index: 1;

            @include mix.responsive(tablet) {
                font-size: vars.$font-size-xxl;
            }

            @include mix.responsive(mobile) {
                font-size: vars.$font-size-xl;
            }
        }

        &__description {
            line-height: vars.$line-height-relaxed;
            margin: 0;
            position: relative;
            z-index: 1;
            flex-grow: 1;
        }

        &__bubbles {
            position: absolute;
            inset: 0;
            overflow: hidden;
            pointer-events: none;
            z-index: 0;
            border-radius: inherit;
        }

        &__bubble {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;

            @media (prefers-reduced-motion: reduce) {
                animation: none !important;
            }

            &--1 {
                width: 20px;
                height: 20px;
                bottom: 12%;
                right: 10%;
                animation: card-bubble 6s ease-in-out infinite;
            }

            &--2 {
                width: 12px;
                height: 12px;
                top: 35%;
                right: 20%;
                animation: card-bubble 8s ease-in-out infinite 1s reverse;
            }

            &--3 {
                width: 8px;
                height: 8px;
                bottom: 25%;
                left: 15%;
                animation: card-bubble 7s ease-in-out infinite 2s;
            }
        }

        &__shine {
            position: absolute;
            inset: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            border-radius: inherit;
        }

        &--light {
            background: fn.color-alpha(vars.$white, 0.9);
            border: 1px solid fn.color-alpha(vars.$white, 0.8);
            box-shadow: 0 4px 20px fn.color-alpha(vars.$black, 0.06);

            .expertise-card__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$gray, 0.3), 2px, 12px);
            }

            .expertise-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;
            }

            .expertise-card__title {
                color: vars.$text-primary;
            }

            .expertise-card__description {
                color: vars.$text-secondary;
            }

            &:hover {
                background: fn.color-alpha(vars.$white, 0.95);
                box-shadow:
                    0 12px 40px fn.color-alpha(vars.$black, 0.14),
                    0 0 20px fn.color-alpha(vars.$primary-color, 0.08);
                border-color: fn.color-alpha(vars.$primary-color, 0.2);
            }
        }

        &--dark {
            background: vars.$black-light;
            border: 1px solid fn.color-alpha(vars.$primary-color, 0.25);
            box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.4);

            .expertise-card__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$primary-color, 0.15), 2px, 12px);
            }

            .expertise-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.2);
                border: 1px solid fn.color-alpha(vars.$primary-color, 0.3);
                color: vars.$secondary-light;
            }

            .expertise-card__title {
                color: vars.$white;
            }

            .expertise-card__description {
                color: fn.color-alpha(vars.$white, 0.75);
            }

            &:hover {
                border-color: fn.color-alpha(vars.$primary-color, 0.5);
                box-shadow:
                    0 12px 40px fn.color-alpha(vars.$black, 0.6),
                    0 0 20px fn.color-alpha(vars.$primary-color, 0.1);
            }
        }

        &--secondary {
            background: linear-gradient(135deg, vars.$primary-dark 0%, vars.$black-light 100%);
            border: 1px solid fn.color-alpha(vars.$primary-color, 0.45);
            box-shadow:
                0 4px 24px fn.color-alpha(vars.$black, 0.4),
                0 0 30px fn.color-alpha(vars.$primary-color, 0.15);

            .expertise-card__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$primary-color, 0.12), 2px, 14px);
            }

            .expertise-card__bubble {
                background: fn.color-alpha(vars.$primary-color, 0.15);
                box-shadow: 0 2px 8px fn.color-alpha(vars.$primary-color, 0.1);
            }

            .expertise-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.35);
                border: 1px solid fn.color-alpha(vars.$primary-color, 0.5);
                color: vars.$white;
            }

            .expertise-card__title {
                color: vars.$white;
            }

            .expertise-card__description {
                color: fn.color-alpha(vars.$white, 0.8);
            }

            &:hover {
                border-color: fn.color-alpha(vars.$primary-color, 0.65);
                box-shadow:
                    0 12px 40px fn.color-alpha(vars.$black, 0.55),
                    0 0 30px fn.color-alpha(vars.$primary-color, 0.2),
                    0 0 60px fn.color-alpha(vars.$primary-color, 0.08);
            }
        }

        &--primary {
            background: linear-gradient(135deg, vars.$primary-light 0%, vars.$primary-dark 100%);
            border: 1px solid fn.color-alpha(vars.$white, 0.2);
            box-shadow: 0 4px 20px fn.color-alpha(vars.$black, 0.15);

            .expertise-card__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$white, 0.08), 2px, 14px);
            }

            .expertise-card__bubble {
                background: fn.color-alpha(vars.$white, 0.12);
                box-shadow: 0 2px 8px fn.color-alpha(vars.$white, 0.06);
            }

            .expertise-card__icon {
                background: fn.color-alpha(vars.$white, 0.15);
                border: 1px solid fn.color-alpha(vars.$white, 0.2);
                color: vars.$white;
            }

            .expertise-card__title {
                color: vars.$white;
            }

            .expertise-card__description {
                color: fn.color-alpha(vars.$white, 0.85);
            }

            &:hover {
                box-shadow:
                    0 12px 40px fn.color-alpha(vars.$black, 0.3),
                    0 0 25px fn.color-alpha(vars.$primary-color, 0.15);
                border-color: fn.color-alpha(vars.$white, 0.35);
            }
        }

        @keyframes card-bubble {
            0%,
            100% {
                transform: translate(0, 0);
            }

            33% {
                transform: translate(-3px, -6px);
            }

            66% {
                transform: translate(3px, -3px);
            }
        }
    }
</style>
