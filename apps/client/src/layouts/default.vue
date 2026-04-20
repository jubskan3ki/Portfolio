<template>
    <div class="layout">
        <a href="#main-content" class="skip-link">Aller au contenu principal</a>

        <div class="layout__bg" :class="{ 'layout__bg--active': bgReady }" aria-hidden="true">
            <div class="layout__dots"></div>
            <div class="layout__glow layout__glow--primary"></div>
            <div class="layout__glow layout__glow--secondary"></div>
        </div>

        <Header id="navigation" />

        <main id="main-content" class="layout__main">
            <ErrorBoundary
                title="Une erreur est survenue"
                fallback-message="Veuillez recharger la page ou revenir a l'accueil."
                show-home-button
                :show-details="false"
            >
                <slot></slot>
            </ErrorBoundary>
        </main>

        <LazyFooter />

        <!-- ClientOnly: évite render-blocking CSS des composants globaux -->
        <ClientOnly>
            <LazyAlertList position="top-right" />
            <LazyModal />
            <LazyLoader />
            <LazyOfflineBadge />

            <Transition name="scroll-btn">
                <button
                    v-if="showScrollTop"
                    class="layout__scroll-top"
                    aria-label="Retour en haut de page"
                    @click="scrollToTop"
                >
                    <BaseIcon name="arrow-up" :size="20" />
                </button>
            </Transition>
        </ClientOnly>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, onUnmounted } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import ErrorBoundary from '@/components/feedback/ErrorBoundary.vue';
    import Header from '@/components/layouts/Header.vue';
    import { usePrefetch } from '@/composables/performance/usePrefetch';
    import { useUiStore } from '@/stores/ui';

    usePrefetch({ strategy: 'idle' });

    const uiStore = useUiStore();
    const showScrollTop = ref(false);
    const bgReady = ref(false);
    let ticking = false;

    const handleScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                showScrollTop.value = window.scrollY > 400;
                uiStore.updateScroll(window.scrollY);
                ticking = false;
            });
            ticking = true;
        }
    };

    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    onMounted(() => {
        window.addEventListener('scroll', handleScroll, { passive: true });

        // Anime le background après le first paint
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                bgReady.value = true;
            });
        } else {
            setTimeout(() => {
                bgReady.value = true;
            }, 200);
        }
    });

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll);
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .skip-link {
        position: absolute;
        top: -100%;
        left: vars.$spacing-md;
        z-index: vars.$z-index-modal;
        padding: vars.$spacing-xs vars.$spacing-md;
        background: vars.$primary-color;
        color: vars.$white;
        border-radius: vars.$border-radius-md;
        text-decoration: none;
        font-weight: vars.$font-weight-bold;
        transition: top 0.2s ease;

        &:focus {
            top: vars.$spacing-md;
        }
    }

    .layout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
        background-color: vars.$bg-primary;

        /* Background différé pour améliorer le FCP */
        &__bg {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
            content-visibility: auto;
        }

        &__dots {
            position: absolute;
            inset: -10%;
            contain: layout style paint;
            content-visibility: auto;

            @include mix.dots-pattern(func.color-alpha(vars.$gray, 0.15), 1.5px, 28px);
            animation: dots-drift 120s linear infinite;
            animation-play-state: paused;

            .layout__bg--active & {
                animation-play-state: running;
            }

            @media (prefers-reduced-motion: reduce) {
                animation: none !important;
            }
        }

        &__glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.4;
            contain: layout style paint;
            animation-play-state: paused;

            .layout__bg--active & {
                animation-play-state: running;
            }

            &--primary {
                top: -20%;
                right: -15%;
                width: 50%;
                height: 50%;
                background: radial-gradient(circle, func.color-alpha(vars.$primary-color, 0.1) 0%, transparent 70%);
                animation: glow-float 30s ease-in-out infinite;
            }

            &--secondary {
                bottom: -25%;
                left: -15%;
                width: 45%;
                height: 45%;
                background: radial-gradient(circle, func.color-alpha(vars.$secondary-color, 0.06) 0%, transparent 70%);
                animation: glow-float 35s ease-in-out infinite reverse;
            }
        }

        &__main {
            flex: 1;
            position: relative;
            z-index: 1;
            padding-top: 75px;
            width: 100%;
        }

        &__scroll-top {
            position: fixed;
            bottom: vars.$spacing-xl;
            right: vars.$spacing-xl;
            width: 48px;
            height: 48px;
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            z-index: vars.$z-index-fixed;
            border: none;

            @include mix.flex-center;

            background: func.color-alpha(vars.$white, 0.75);
            backdrop-filter: blur(16px) saturate(1.2);
            color: vars.$primary-color;
            box-shadow: 0 4px 24px func.color-alpha(vars.$black, 0.08);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                transform: translateY(-4px);
                background: func.color-alpha(vars.$white, 0.9);
                color: vars.$primary-dark;
                box-shadow:
                    0 8px 32px func.color-alpha(vars.$primary-color, 0.25),
                    0 0 0 1px func.color-alpha(vars.$primary-color, 0.1),
                    inset 0 0 0 1px func.color-alpha(vars.$white, 0.5);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 3px;
            }

            &:active {
                transform: translateY(-2px) scale(0.96);
            }

            @include mix.responsive(mobile) {
                width: 44px;
                height: 44px;
                bottom: vars.$spacing-lg;
                right: vars.$spacing-lg;
            }
        }
    }

    @keyframes dots-drift {
        0% {
            transform: translate(0, 0);
        }

        100% {
            transform: translate(32px, 32px);
        }
    }

    @keyframes glow-float {
        0%,
        100% {
            transform: translate(0, 0) scale(1);
        }

        50% {
            transform: translate(25px, -20px) scale(1.05);
        }
    }

    .scroll-btn-enter-active {
        transition:
            opacity 0.3s ease,
            transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .scroll-btn-leave-active {
        transition:
            opacity 0.2s ease,
            transform 0.2s ease;
    }

    .scroll-btn-enter-from {
        opacity: 0;
        transform: translateY(20px) scale(0.8);
    }

    .scroll-btn-leave-to {
        opacity: 0;
        transform: translateY(10px) scale(0.9);
    }
</style>
