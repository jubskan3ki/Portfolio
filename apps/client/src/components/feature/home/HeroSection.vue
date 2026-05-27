<template>
    <section ref="heroRef" class="hero-section" :class="{ 'hero-section--paused': animationsPaused }">
        <!-- Background layers (SectionBackground from design system) -->
        <SectionBackground variant="light" />

        <div class="container">
            <div class="hero-wrapper">
                <div class="hero-content">
                    <h1 class="hero-title">
                        Développeur
                        <span class="hero-title__highlight hero-title__highlight--primary">Web</span>
                        &
                        <span class="hero-title__highlight hero-title__highlight--secondary">Mobile</span>
                    </h1>
                    <p v-if="bio" class="hero-subtitle">
                        {{ bio }}
                    </p>
                    <div class="hero-typing">
                        <span class="hero-typing__prefix">Expert en</span>
                        <span class="hero-typing__text">{{ currentTypingText }}</span>
                        <span class="hero-typing__cursor" :class="{ 'hero-typing__cursor--paused': isPaused }"></span>
                    </div>
                    <div class="hero-actions">
                        <BaseButton :to="ROUTES.PROJECTS" variant="primary" size="lg">
                            <BaseIcon name="code" size="sm" />
                            Voir mes projets
                        </BaseButton>
                        <BaseButton :to="ROUTES.CONTACT" variant="outline" size="lg">
                            <BaseIcon name="mail" size="sm" />
                            Me contacter
                        </BaseButton>
                    </div>
                </div>

                <div class="hero-visual">
                    <div class="hero-image-wrapper">
                        <div class="hero-image-container">
                            <NuxtImg
                                src="/images/profile.jpg"
                                alt="Portrait de Juba Aitadda"
                                class="hero-image"
                                width="280"
                                height="280"
                                sizes="xs:220px md:280px"
                                format="webp"
                                quality="70"
                                loading="eager"
                                fetchpriority="high"
                                preload
                            />
                        </div>
                        <div class="hero-background-shape"></div>

                        <div class="hero-tech-badges">
                            <StackBadge
                                v-for="(stack, index) in featuredStacks"
                                :key="stack.id"
                                :stack="stack"
                                size="small"
                                class="hero-badge"
                                :class="`hero-badge--${index + 1}`"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import StackBadge from '@/components/feature/stacks/StackBadge.vue';
    import SectionBackground from '@/components/ui/SectionBackground.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useTypingEffect } from '@/composables/ui/useTypingEffect';
    import { ROUTES } from '@/config/routes';

    import type { HeroSectionProps } from '@/types/feature/home';

    type Props = HeroSectionProps;

    withDefaults(defineProps<Props>(), {
        featuredStacks: () => [],
        bio: '',
    });

    // Accessibility - used via CSS media query prefers-reduced-motion
    const { prefersReducedMotion: _prefersReducedMotion } = useReducedMotion();

    // Pause infinite animations + typing effect when hero leaves the viewport
    const heroRef = ref<HTMLElement | null>(null);
    const animationsPaused = ref(false);
    const typingEnabled = computed(() => !animationsPaused.value);
    let observer: IntersectionObserver | null = null;

    // Typing effect (paused when hero is offscreen)
    const typingTexts = ['React.ts', 'Vue.ts', 'Nest.ts', 'Go', 'Flutter', 'Django'];
    const { currentText: currentTypingText, isPaused } = useTypingEffect(typingTexts, {
        enabled: typingEnabled,
    });

    onMounted(() => {
        if (!heroRef.value || typeof IntersectionObserver === 'undefined') {
            return;
        }
        observer = new IntersectionObserver(
            ([entry]) => {
                animationsPaused.value = !entry?.isIntersecting;
            },
            { rootMargin: '0px', threshold: 0 },
        );
        observer.observe(heroRef.value);
    });

    onBeforeUnmount(() => observer?.disconnect());
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .hero-section {
        position: relative;
        padding: calc(vars.$navbar-height + vars.$spacing-xl) 0 calc(vars.$spacing-xl + 120px);
        overflow: hidden;
        background: vars.$bg-secondary;

        &--paused,
        &--paused * {
            animation-play-state: paused !important;
        }
    }

    .hero-wrapper {
        position: relative;
        z-index: 10;
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: vars.$spacing-xxl;
        align-items: center;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
            text-align: center;
        }
    }

    .hero-content {
        @include mix.responsive(tablet) {
            order: 2;
        }
    }

    .hero-title {
        line-height: 1.1;
        font-weight: vars.$font-weight-bold;
        margin-bottom: vars.$spacing-md;
        color: vars.$text-primary;

        &__highlight {
            position: relative;
            display: inline-block;

            &--primary {
                color: vars.$primary-color;
            }

            &--secondary {
                color: vars.$secondary-color;
            }

            &::after {
                content: '';
                position: absolute;
                left: -4px;
                right: -4px;
                bottom: 4px;
                height: 12px;
                z-index: -1;
                transform: skewX(-5deg);
                border-radius: 2px;
            }

            &--primary::after {
                background: fn.color-alpha(vars.$primary-color, 0.15);
            }

            &--secondary::after {
                background: fn.color-alpha(vars.$secondary-color, 0.15);
            }
        }
    }

    .hero-subtitle {
        color: vars.$text-secondary;
        line-height: vars.$line-height-relaxed;
        margin-bottom: vars.$spacing-lg;
        max-width: 560px;

        @include mix.responsive(tablet) {
            margin-left: auto;
            margin-right: auto;
        }
    }

    .hero-typing {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        margin-bottom: vars.$spacing-xl;
        min-height: 2rem;

        @include mix.responsive(tablet) {
            justify-content: center;
        }

        &__prefix {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
        }

        &__text {
            font-weight: vars.$font-weight-bold;
            color: vars.$primary-color;
        }

        &__cursor {
            display: inline-block;
            width: 3px;
            height: 1.4em;
            background-color: vars.$primary-color;
            border-radius: 2px;
            animation: blink 0.8s step-end infinite;

            &--paused {
                animation: none;
                opacity: 1;
            }
        }
    }

    .hero-actions {
        display: flex;
        gap: vars.$spacing-md;

        @include mix.responsive(tablet) {
            justify-content: center;
        }

        @include mix.responsive(mobile) {
            flex-direction: column;
        }
    }

    .hero-visual {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;

        @include mix.responsive(tablet) {
            order: 1;
            margin-bottom: vars.$spacing-xl;
        }
    }

    .hero-image-wrapper {
        position: relative;
        width: 400px;
        height: 400px;

        @include mix.responsive(mobile) {
            width: 320px;
            height: 320px;
        }
    }

    .hero-image-container {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 280px;
        height: 280px;
        border-radius: 30% 70% 70% 30%;
        overflow: hidden;
        z-index: 2;
        will-change: transform;
        animation: hero-float 7s ease-in-out infinite alternate;

        box-shadow:
            0 20px 40px fn.color-alpha(vars.$primary-color, 0.15),
            0 0 0 4px fn.color-alpha(vars.$white, 0.9),
            inset 0 0 20px fn.color-alpha(vars.$white, 0.3);

        @include mix.responsive(mobile) {
            width: 220px;
            height: 220px;
            animation: hero-float-mobile 8s ease-in-out infinite alternate;
        }

        @media (prefers-reduced-motion: reduce) {
            animation: none;
            transform: translate(-50%, -50%);
            border-radius: 50%;
        }
    }

    .hero-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .hero-background-shape {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300px;
        height: 300px;
        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
        background: linear-gradient(135deg, vars.$primary-color 0%, vars.$primary-dark 100%);
        opacity: 0.8;
        z-index: 1;
        will-change: transform;
        animation: hero-shape-morph 14s ease-in-out infinite;

        @include mix.responsive(mobile) {
            width: 240px;
            height: 240px;
            animation: hero-shape-morph 16s ease-in-out infinite;
        }

        @media (prefers-reduced-motion: reduce) {
            animation: none;
            transform: translate(-45%, -55%);
            border-radius: 30% 70% 50% 50%;
        }
    }

    .hero-tech-badges {
        position: absolute;
        inset: 0;
        z-index: 3;
    }

    .hero-badge {
        position: absolute;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;

        &:hover {
            transform: translateY(-4px) scale(1.08);
        }

        @media (prefers-reduced-motion: no-preference) {
            animation: float 4s ease-in-out infinite;
        }

        /* Positioned around the profile image */
        &--1 {
            top: 5%;
            left: 0;
            animation-delay: 0s;
        }

        &--2 {
            top: 10%;
            right: 5%;
            animation-delay: 0.3s;
        }

        &--3 {
            bottom: 15%;
            right: 0;
            animation-delay: 0.6s;
        }

        &--4 {
            bottom: 5%;
            left: 10%;
            animation-delay: 0.9s;
        }

        &--5 {
            top: 50%;
            left: -5%;
            transform: translateY(-50%);
            animation-delay: 1.2s;
        }
    }

    /* Animations */
    @keyframes blink {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0;
        }
    }

    @keyframes float {
        0%,
        100% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-12px);
        }
    }

    @keyframes hero-float {
        0% {
            transform: translate(-50%, -50%) rotate(0deg);
        }

        50% {
            transform: translate(calc(-50% + 6px), calc(-50% - 14px)) rotate(1.2deg);
        }

        100% {
            transform: translate(calc(-50% - 7px), calc(-50% - 10px)) rotate(-1.2deg);
        }
    }

    @keyframes hero-float-mobile {
        0% {
            transform: translate(-50%, -50%) rotate(0deg);
        }

        50% {
            transform: translate(calc(-50% + 3px), calc(-50% - 7px)) rotate(0.6deg);
        }

        100% {
            transform: translate(calc(-50% - 4px), calc(-50% - 5px)) rotate(-0.6deg);
        }
    }

    @keyframes hero-shape-morph {
        0% {
            transform: translate(-45%, -55%) scale(1) rotate(0deg);
        }

        25% {
            transform: translate(-48%, -52%) scale(1.05) rotate(6deg);
        }

        50% {
            transform: translate(-42%, -58%) scale(0.97) rotate(-4deg);
        }

        75% {
            transform: translate(-47%, -53%) scale(1.03) rotate(5deg);
        }

        100% {
            transform: translate(-45%, -55%) scale(1) rotate(0deg);
        }
    }
</style>
