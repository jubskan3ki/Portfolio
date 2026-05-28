<template>
    <div class="portfolio-summary">
        <div class="portfolio-summary__bg" aria-hidden="true">
            <div class="portfolio-summary__dots"></div>
            <div class="portfolio-summary__glow portfolio-summary__glow--1"></div>
            <div class="portfolio-summary__glow portfolio-summary__glow--2"></div>
        </div>

        <div class="portfolio-summary__content">
            <h3 class="portfolio-summary__title">{{ title }}</h3>
            <p class="portfolio-summary__description">{{ description }}</p>
            <div class="portfolio-summary__cta">
                <BaseButton :to="ctaLinks.primary.url" :text="ctaLinks.primary.label" variant="primary" />
                <BaseButton
                    :to="ctaLinks.secondary.url"
                    :text="ctaLinks.secondary.label"
                    variant="primary"
                    custom-class="portfolio-summary__btn-outline"
                />
            </div>
        </div>

        <div class="portfolio-summary__stats">
            <div v-for="stat in stats" :key="stat.label" class="portfolio-summary__stat">
                <span class="portfolio-summary__stat-value">{{ stat.value }}+</span>
                <span class="portfolio-summary__stat-label">{{ stat.label }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import { ROUTES } from '@/config/routes';

    import type { PortfolioSummaryProps } from '@/types/components/ui';

    withDefaults(defineProps<PortfolioSummaryProps>(), {
        title: 'Transformez vos idées en réalité numérique',
        description:
            'Diplômé d\'un Bachelor en Développement Web et actuellement en Mastère CTO & Tech Lead à HETIC, j\'allie expertise technique et vision stratégique pour créer des solutions digitales modernes, performantes et innovantes.',
        ctaLinks: () => ({
            primary: { label: 'Discutons de votre projet', url: ROUTES.CONTACT },
            secondary: { label: 'Voir mes réalisations', url: ROUTES.PROJECTS },
        }),
        stats: () => [
            { value: 25, label: 'Projets réalisés' },
            { value: 5, label: 'Années d\'expérience' },
            { value: 18, label: 'Clients satisfaits' },
        ],
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .portfolio-summary {
        position: relative;
        background: linear-gradient(135deg, vars.$primary-color 0%, vars.$primary-dark 100%);
        border-radius: vars.$border-radius-xl;
        color: vars.$white;
        padding: vars.$spacing-xl;
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: vars.$spacing-xl;
        overflow: hidden;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
            padding: vars.$spacing-lg;
        }

        /* Background layer */
        &__bg {
            position: absolute;
            inset: 0;
            pointer-events: none;
            overflow: hidden;
        }

        &__dots {
            position: absolute;
            inset: -20%;

            @include mix.dots-pattern(func.color-alpha(vars.$white, 0.04), 1.5px, 20px);
        }

        &__glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);

            &--1 {
                top: -20%;
                right: -10%;
                width: 40%;
                height: 60%;
                background: func.color-alpha(vars.$white, 0.08);
            }

            &--2 {
                bottom: -30%;
                left: -10%;
                width: 35%;
                height: 50%;
                background: func.color-alpha(vars.$secondary-color, 0.1);
            }
        }

        /* Content */
        &__content {
            position: relative;
            z-index: 1;
        }

        &__title {
            margin-bottom: vars.$spacing-md;
            color: vars.$white;
            font-weight: 600;
            line-height: 1.3;
        }

        &__description {
            margin-bottom: vars.$spacing-lg;
            max-width: 550px;
            line-height: 1.7;
            color: func.color-alpha(vars.$white, 0.85);
        }

        &__cta {
            display: flex;
            gap: vars.$spacing-md;

            @include mix.responsive(mobile) {
                flex-direction: column;
            }
        }

        /* Stats */
        &__stats {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-md;

            @include mix.responsive(tablet) {
                flex-direction: row;
                flex-wrap: wrap;
            }
        }

        &__stat {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: vars.$spacing-md vars.$spacing-lg;
            background: func.color-alpha(vars.$white, 0.08);
            border: 1px solid func.color-alpha(vars.$white, 0.1);
            border-radius: vars.$border-radius-lg;
            text-align: center;
            backdrop-filter: blur(8px);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            @include mix.responsive(tablet) {
                flex: 1;
                min-width: 120px;
            }

            &:hover {
                transform: translateY(-4px);
                background: func.color-alpha(vars.$white, 0.12);
                border-color: func.color-alpha(vars.$white, 0.2);
            }

            &--skeleton {
                animation: stat-pulse 1.5s ease-in-out infinite;
            }
        }

        @keyframes stat-pulse {
            0%,
            100% {
                opacity: 0.4;
            }

            50% {
                opacity: 0.7;
            }
        }

        &__stat-value {
            font-weight: 700;
            color: vars.$white;
            line-height: 1.2;
        }

        &__stat-label {
            color: func.color-alpha(vars.$white, 0.7);
            margin-top: vars.$spacing-md;
        }
    }

    /* Outline button on dark background - increased specificity without !important */
    :deep(.portfolio-summary__btn-outline.btn.btn--outline) {
        --btn-bg: transparent;
        --btn-border-color: #{func.color-alpha(vars.$white, 0.4)};
        --btn-text-color: #{vars.$white};

        background: var(--btn-bg);
        border-color: var(--btn-border-color);
        color: var(--btn-text-color);

        &:hover,
        &:focus-visible {
            --btn-bg: #{func.color-alpha(vars.$white, 0.1)};
            --btn-border-color: #{func.color-alpha(vars.$white, 0.6)};
        }
    }
</style>
