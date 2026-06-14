<template>
    <section ref="heroRef" class="hero-section" :class="{ 'hero-section--paused': animationsPaused }">
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
                            />
                        </div>
                        <div class="hero-background-shape"></div>

                        <div class="hero-tech-badges">
                            <StackBadge
                                v-for="(stack, index) in featuredStacks"
                                :key="stack.id"
                                :stack="stack"
                                size="small"
                                :clickable="Boolean(stack.slug)"
                                class="hero-badge"
                                :class="`hero-badge--${index + 1}`"
                                @click="onStackClick"
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
    import { useRouter } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import StackBadge from '@/components/feature/stacks/StackBadge.vue';
    import SectionBackground from '@/components/ui/SectionBackground.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useTypingEffect } from '@/composables/ui/useTypingEffect';
    import { ROUTES } from '@/config/routes';

    import type { HeroSectionProps, HeroStack } from '@/types/feature/home';

    type Props = HeroSectionProps;

    withDefaults(defineProps<Props>(), {
        featuredStacks: () => [],
        bio: '',
    });

    const router = useRouter();
    const onStackClick = (stack: HeroStack) => {
        if (stack.slug) {
            router.push(`${ROUTES.STACKS.path}/${stack.slug}`);
        }
    };

    const { prefersReducedMotion: _prefersReducedMotion } = useReducedMotion();

    // Démarré paused : pas d'animations décoratives pendant l'hydratation (fenêtre TBT), libérées à l'idle.
    const heroRef = ref<HTMLElement | null>(null);
    const animationsPaused = ref(true);
    const typingEnabled = computed(() => !animationsPaused.value);
    let observer: IntersectionObserver | null = null;

    const typingTexts = ['React.ts', 'Vue.ts', 'Nest.ts', 'Go', 'Flutter', 'Django'];
    const { currentText: currentTypingText, isPaused } = useTypingEffect(typingTexts, {
        enabled: typingEnabled,
    });

    const startHeroAnimations = () => {
        if (!heroRef.value || typeof IntersectionObserver === 'undefined') {
            animationsPaused.value = false;
            return;
        }
        observer = new IntersectionObserver(
            ([entry]) => {
                animationsPaused.value = !entry?.isIntersecting;
            },
            { rootMargin: '0px', threshold: 0 },
        );
        observer.observe(heroRef.value);
    };

    onMounted(() => {
        // Différé à l'idle : laisse l'hydratation et le first paint finir avant les animations infinies (gain TBT).
        if ('requestIdleCallback' in window) {
            requestIdleCallback(startHeroAnimations, { timeout: 1500 });
        } else {
            setTimeout(startHeroAnimations, 300);
        }
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
        border-radius: 40% 60% 65% 35% / 65% 35% 65% 40%;
        overflow: hidden;
        z-index: 2;
        // Position figée : seul le border-radius est animé.
        transform: translate(-50%, -50%);
        animation: hero-blob-morph 9s ease-in-out infinite;

        box-shadow:
            0 18px 44px fn.color-alpha(vars.$primary-color, 0.3),
            0 0 0 5px fn.color-alpha(vars.$white, 0.95),
            0 0 0 11px fn.color-alpha(vars.$primary-color, 0.08),
            inset 0 0 24px fn.color-alpha(vars.$white, 0.35);

        @include mix.responsive(mobile) {
            width: 220px;
            height: 220px;
            animation-duration: 11s;
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
        width: 330px;
        height: 330px;
        border-radius: 65% 35% 50% 50% / 40% 65% 35% 60%;
        background: linear-gradient(135deg, vars.$primary-color 0%, vars.$primary-dark 100%);
        opacity: 0.85;
        z-index: 1;
        // Translate constant dans chaque keyframe : seuls border-radius, rotation et scale sont animés.
        transform: translate(-45%, -55%);
        will-change: transform;
        animation: hero-shape-morph 18s linear infinite;

        @include mix.responsive(mobile) {
            width: 260px;
            height: 260px;
            animation-duration: 22s;
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

    /* Photo : seul le border-radius ondule, le transform n'est pas animé (centrage préservé). */
    @keyframes hero-blob-morph {
        0%,
        100% {
            border-radius: 40% 60% 65% 35% / 65% 35% 65% 40%;
        }

        20% {
            border-radius: 72% 28% 45% 55% / 55% 70% 30% 45%;
        }

        40% {
            border-radius: 50% 50% 25% 75% / 35% 60% 40% 65%;
        }

        60% {
            border-radius: 60% 40% 70% 30% / 70% 30% 60% 40%;
        }

        80% {
            border-radius: 30% 70% 50% 50% / 45% 50% 50% 55%;
        }
    }

    /* Forme de fond : border-radius identique à 0% et 100% + rotation 360deg pour une boucle continue. */
    @keyframes hero-shape-morph {
        0% {
            border-radius: 65% 35% 50% 50% / 40% 65% 35% 60%;
            transform: translate(-45%, -55%) rotate(0deg) scale(1);
        }

        25% {
            border-radius: 35% 65% 70% 30% / 60% 45% 55% 40%;
            transform: translate(-45%, -55%) rotate(90deg) scale(1.07);
        }

        50% {
            border-radius: 55% 45% 30% 70% / 50% 35% 65% 50%;
            transform: translate(-45%, -55%) rotate(180deg) scale(0.94);
        }

        75% {
            border-radius: 70% 30% 60% 40% / 35% 60% 40% 65%;
            transform: translate(-45%, -55%) rotate(270deg) scale(1.05);
        }

        100% {
            border-radius: 65% 35% 50% 50% / 40% 65% 35% 60%;
            transform: translate(-45%, -55%) rotate(360deg) scale(1);
        }
    }
</style>
