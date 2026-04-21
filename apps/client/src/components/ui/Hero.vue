<template>
    <section
        ref="heroRef"
        class="hero"
        :class="[`hero--${variant}`, { 'hero--compact': size === 'compact', 'hero--has-stats': hasStats }]"
    >
        <SectionBackground :variant="variant" />

        <div class="container">
            <div class="hero__wrapper" :style="parallaxStyle">
                <div class="hero__card">
                    <div class="hero__card-inner">
                        <div v-if="$slots.breadcrumb" class="hero__breadcrumb">
                            <slot name="breadcrumb"></slot>
                        </div>

                        <span v-if="badge" class="hero__badge">{{ badge }}</span>

                        <div v-if="logo" class="hero__logo" :style="logoTransitionStyle">
                            <BaseImage
                                :src="resolvedLogo"
                                :alt="logoAlt || title"
                                :width="64"
                                :height="64"
                                :lazy="false"
                                :show-placeholder="false"
                            />
                        </div>

                        <h1 class="hero__title" :style="titleTransitionStyle">
                            <slot name="title">{{ title }}</slot>
                        </h1>

                        <p v-if="description || $slots.description" class="hero__description">
                            <slot name="description">{{ description }}</slot>
                        </p>

                        <div v-if="hasMeta || $slots.meta" class="hero__meta">
                            <slot name="meta"></slot>
                        </div>

                        <div v-if="$slots.links" class="hero__links">
                            <slot name="links"></slot>
                        </div>

                        <slot></slot>
                    </div>

                    <span class="hero__float hero__float--1"></span>
                    <span class="hero__float hero__float--2"></span>
                    <span class="hero__float hero__float--3"></span>
                </div>

                <div v-if="$slots.stats" class="hero__stats">
                    <slot name="stats"></slot>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted, useSlots } from 'vue';

    import SectionBackground from '@/components/ui/SectionBackground.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { resolveMediaUrl } from '@/services/utils/helpers';

    import type { HeroProps } from '@/types/components/ui';

    const props = withDefaults(defineProps<HeroProps>(), {
        description: '',
        variant: 'primary',
        showTitleUnderline: false,
        logo: '',
        logoAlt: '',
        hasMeta: false,
        badge: '',
        centered: true,
        size: 'default',
        showDots: true,
        showOrbs: true,
        showBottomFade: false,
        animateDots: false,
        parallaxIntensity: 0.02,
    });

    const slots = useSlots();
    const hasStats = computed(() => !!slots.stats);
    const resolvedLogo = computed(() => resolveMediaUrl(props.logo));

    const titleTransitionStyle = computed(() =>
        props.transitionKey ? { viewTransitionName: `hero-title-${props.transitionKey}` } : undefined,
    );
    const logoTransitionStyle = computed(() =>
        props.transitionKey ? { viewTransitionName: `hero-media-${props.transitionKey}` } : undefined,
    );

    const heroRef = ref<HTMLElement | null>(null);
    const scrollY = ref(0);
    const isHeroVisible = ref(true);
    const { prefersReducedMotion } = useReducedMotion();

    const parallaxStyle = computed(() => {
        if (prefersReducedMotion.value || props.parallaxIntensity === 0) {
            return {};
        }
        return { transform: `translateY(${scrollY.value * props.parallaxIntensity}px)` };
    });

    let rafId = 0;
    const updateScrollY = () => {
        rafId = 0;
        scrollY.value = window.scrollY;
    };
    const handleScroll = () => {
        if (!isHeroVisible.value || rafId !== 0) {
            return;
        }
        rafId = requestAnimationFrame(updateScrollY);
    };

    let observer: IntersectionObserver | null = null;

    onMounted(() => {
        if (prefersReducedMotion.value || props.parallaxIntensity === 0 || !heroRef.value) {
            return;
        }

        observer = new IntersectionObserver(
            (entries) => {
                for (const entry of entries) {
                    isHeroVisible.value = entry.isIntersecting;
                }
            },
            { rootMargin: '0px' },
        );
        observer.observe(heroRef.value);

        window.addEventListener('scroll', handleScroll, { passive: true });
    });

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll);
        if (rafId !== 0) {
            cancelAnimationFrame(rafId);
        }
        observer?.disconnect();
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/functions' as fn;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/components/hero-variants' as hero;

    .hero {
        position: relative;
        padding: calc(vars.$navbar-height + vars.$spacing-xxl) 0 vars.$spacing-xxl;
        overflow: hidden;

        &--has-stats {
            padding-bottom: calc(vars.$spacing-xxl + 40px);

            @include mix.responsive(mobile) {
                padding-bottom: vars.$spacing-xl;
            }
        }

        &__wrapper {
            position: relative;
            z-index: 1;
            will-change: transform;
        }

        &__card {
            position: relative;
            max-width: 800px;
            margin: 0 auto;
            padding: vars.$spacing-xxl vars.$spacing-xl;
            backdrop-filter: blur(16px);
            border-radius: vars.$border-radius-xl;
            text-align: center;
            transition: transform 0.4s ease;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xl vars.$spacing-lg;
            }

            &:hover {
                transform: translateY(-4px);

                .hero__float {
                    transform: translateY(-8px);
                }
            }
        }

        &__card-inner {
            position: relative;
            z-index: 2;
        }

        &__breadcrumb {
            display: flex;
            justify-content: center;
            margin-bottom: vars.$spacing-md;
        }

        &__float {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);

            @media (prefers-reduced-motion: reduce) {
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

        &__badge {
            display: inline-block;
            margin-bottom: vars.$spacing-lg;
            padding: vars.$spacing-xxs vars.$spacing-md;
            font-weight: vars.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            border-radius: vars.$border-radius-full;
        }

        &__logo {
            margin-bottom: vars.$spacing-lg;

            img {
                width: 64px;
                height: 64px;
                object-fit: contain;
                border-radius: vars.$border-radius-lg;
                padding: vars.$spacing-sm;
            }
        }

        &__title {
            margin: 0 0 vars.$spacing-sm;
            font-weight: vars.$font-weight-bold;
            line-height: vars.$line-height-tight;
        }

        &__description {
            margin: 0 0 vars.$spacing-lg;
            line-height: vars.$line-height-relaxed;
            max-width: 500px;
            margin-inline: auto;
        }

        &__meta {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: vars.$spacing-md;
            margin-top: vars.$spacing-lg;
        }

        &__links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: vars.$spacing-sm;
            margin-top: vars.$spacing-lg;
        }

        &__stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: vars.$spacing-sm;
            max-width: 750px;
            margin: 0 auto;
            margin-top: calc(-1 * vars.$spacing-lg);
            transform: translateY(50%);

            @include mix.responsive(mobile) {
                grid-template-columns: 1fr;
                gap: vars.$spacing-sm;
                max-width: 300px;
                margin-top: vars.$spacing-md;
                transform: none;
            }
        }

        &--compact {
            padding: calc(vars.$navbar-height + vars.$spacing-xl) 0 vars.$spacing-xl;

            &.hero--has-stats {
                padding-bottom: calc(vars.$spacing-xl + 30px);

                @include mix.responsive(mobile) {
                    padding-bottom: vars.$spacing-lg;
                }
            }

            .hero__card {
                padding: vars.$spacing-xl vars.$spacing-lg;
            }
        }

        &--light {
            @include hero.hero-variant(
                $background: vars.$bg-secondary,
                $card-bg: fn.color-alpha(vars.$white, 0.8),
                $card-border: fn.color-alpha(vars.$white, 0.9),
                $card-shadow: (
                    0 8px 32px fn.color-alpha(vars.$black, 0.06),
                    0 1px 2px fn.color-alpha(vars.$black, 0.04),
                    inset 0 1px 0 vars.$white,
                ),
                $badge-color: vars.$primary-color,
                $badge-bg: fn.color-alpha(vars.$primary-color, 0.08),
                $badge-border: fn.color-alpha(vars.$primary-color, 0.12),
                $title-color: vars.$text-primary,
                $desc-color: vars.$text-secondary,
                $meta-color: vars.$text-secondary,
                $logo-bg: fn.color-alpha(vars.$primary-color, 0.08)
            );
        }

        &--dark {
            @include hero.hero-variant(
                $background: vars.$black-light,
                $card-bg: fn.color-alpha(vars.$primary-dark, 0.3),
                $card-border: fn.color-alpha(vars.$primary-color, 0.2),
                $card-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.3),
                $badge-color: vars.$secondary-light,
                $badge-bg: fn.color-alpha(vars.$primary-color, 0.15),
                $badge-border: fn.color-alpha(vars.$primary-color, 0.25),
                $title-color: vars.$white,
                $desc-color: fn.color-alpha(vars.$white, 0.75),
                $meta-color: fn.color-alpha(vars.$white, 0.65),
                $logo-bg: fn.color-alpha(vars.$primary-color, 0.15)
            );
        }

        &--primary {
            @include hero.hero-variant(
                $background: linear-gradient(180deg, vars.$primary-light 0%, vars.$primary-dark 100%),
                $card-bg: fn.color-alpha(vars.$white, 0.1),
                $card-border: fn.color-alpha(vars.$white, 0.2),
                $card-shadow: (
                    0 8px 32px fn.color-alpha(vars.$black, 0.1),
                    inset 0 1px 0 fn.color-alpha(vars.$white, 0.2),
                ),
                $badge-color: vars.$white,
                $badge-bg: fn.color-alpha(vars.$white, 0.1),
                $badge-border: fn.color-alpha(vars.$white, 0.15),
                $title-color: vars.$white,
                $desc-color: fn.color-alpha(vars.$white, 0.85),
                $meta-color: fn.color-alpha(vars.$white, 0.7),
                $logo-bg: fn.color-alpha(vars.$white, 0.1)
            );
        }

        &--secondary {
            @include hero.hero-variant(
                $background: linear-gradient(180deg, vars.$primary-dark 0%, vars.$black-light 100%),
                $card-bg: fn.color-alpha(vars.$white, 0.05),
                $card-border: fn.color-alpha(vars.$primary-color, 0.3),
                $card-shadow: (
                    0 8px 32px fn.color-alpha(vars.$black, 0.4),
                    0 0 60px fn.color-alpha(vars.$primary-color, 0.15),
                    inset 0 1px 0 fn.color-alpha(vars.$white, 0.08),
                ),
                $badge-color: vars.$white,
                $badge-bg: fn.color-alpha(vars.$primary-color, 0.2),
                $badge-border: fn.color-alpha(vars.$primary-color, 0.4),
                $title-color: vars.$white,
                $desc-color: fn.color-alpha(vars.$white, 0.8),
                $meta-color: fn.color-alpha(vars.$white, 0.65),
                $logo-bg: fn.color-alpha(vars.$primary-color, 0.15),
                $logo-border: fn.color-alpha(vars.$primary-color, 0.3)
            );
        }
    }

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
</style>
