<template>
    <section class="hero-section">
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
                                sizes="(max-width: 768px) 220px, 280px"
                                format="webp"
                                quality="75"
                                loading="eager"
                                fetchpriority="high"
                            />
                        </div>
                        <div class="hero-background-shape"></div>

                        <!-- Stack badges positioned around the image -->
                        <div class="hero-tech-badges">
                            <StackBadge
                                v-for="(stack, index) in featuredStacks"
                                :key="stack.id"
                                :stack="stack"
                                size="small"
                                class="hero-badge"
                                :class="`hero-badge--${index + 1}`"
                                :style="{ animationDelay: `${index * 0.3}s` }"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
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

    // Typing effect
    const typingTexts = ['React.ts', 'Vue.ts', 'Nest.ts', 'Go', 'Flutter', 'Django'];
    const { currentText: currentTypingText, isPaused } = useTypingEffect(typingTexts);
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
            min-width: 120px;
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
        transform: translate(-50%, -50%);
        width: 280px;
        height: 280px;
        border-radius: 30% 70% 70% 30%;
        overflow: hidden;
        z-index: 2;
        animation: morphing 15s ease-in-out infinite;
        will-change: border-radius;

        box-shadow:
            0 20px 40px fn.color-alpha(vars.$primary-color, 0.15),
            0 0 0 4px fn.color-alpha(vars.$white, 0.9),
            inset 0 0 20px fn.color-alpha(vars.$white, 0.3);

        @include mix.responsive(mobile) {
            width: 220px;
            height: 220px;
        }

        @media (prefers-reduced-motion: reduce) {
            animation: none;
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
        transform: translate(-45%, -55%);
        width: 300px;
        height: 300px;
        border-radius: 30% 70% 50% 50%;
        background: linear-gradient(135deg, vars.$primary-color 0%, vars.$primary-dark 100%);
        opacity: 0.8;
        z-index: 1;
        animation: rotate 30s linear infinite;
        animation-delay: 1s;

        @include mix.responsive(mobile) {
            width: 240px;
            height: 240px;
        }

        @media (prefers-reduced-motion: reduce) {
            animation: none;
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
        }

        &--2 {
            top: 10%;
            right: 5%;
        }

        &--3 {
            bottom: 15%;
            right: 0;
        }

        &--4 {
            bottom: 5%;
            left: 10%;
        }

        &--5 {
            top: 50%;
            left: -5%;
            transform: translateY(-50%);
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

    @keyframes rotate {
        from {
            transform: translate(-45%, -55%) rotate(0deg);
        }

        to {
            transform: translate(-45%, -55%) rotate(360deg);
        }
    }

    @keyframes morphing {
        0% {
            border-radius: 30% 70% 70% 30%;
        }

        25% {
            border-radius: 58% 42% 75% 25%;
        }

        50% {
            border-radius: 50% 50% 33% 67%;
        }

        75% {
            border-radius: 33% 67% 58% 42%;
        }

        100% {
            border-radius: 30% 70% 70% 30%;
        }
    }
</style>
