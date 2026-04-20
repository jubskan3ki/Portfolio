<template>
    <div class="colophon-page">
        <Hero
            title="Colophon"
            :description="heroDescription"
            variant="secondary"
            badge="meta"
        />

        <Main variant="default" size="large">
            <section class="colophon-section" aria-labelledby="stack-title">
                <h2 id="stack-title" class="colophon-section__title">Stack</h2>
                <div class="colophon-grid">
                    <article v-for="group in stackGroups" :key="group.label" class="colophon-card">
                        <header class="colophon-card__head">
                            <BaseIcon :name="group.icon" :size="18" />
                            <h3 class="colophon-card__title">{{ group.label }}</h3>
                        </header>
                        <ul class="colophon-card__list">
                            <li v-for="item in group.items" :key="item.name" class="colophon-card__item">
                                <span class="colophon-card__item-name">{{ item.name }}</span>
                                <small v-if="item.detail" class="colophon-card__item-detail">{{ item.detail }}</small>
                            </li>
                        </ul>
                    </article>
                </div>
            </section>

            <section class="colophon-section" aria-labelledby="metrics-title">
                <h2 id="metrics-title" class="colophon-section__title">Métriques en temps réel</h2>
                <p class="colophon-section__intro">
                    Extraits agrégés depuis l'endpoint interne Web Vitals (p75 sur 30 jours). Les seuils
                    <abbr title="Core Web Vitals">CWV</abbr> Google sont appliqués tel quel.
                </p>
                <div v-if="vitalsError" class="colophon-empty" role="status">
                    Les métriques en direct ne sont pas disponibles pour l'instant.
                </div>
                <div v-else-if="!vitalsReady" class="colophon-empty" role="status" aria-live="polite">
                    Chargement des métriques…
                </div>
                <div v-else class="colophon-grid">
                    <article
                        v-for="metric in vitalsRows"
                        :key="metric.name"
                        class="colophon-metric"
                        :class="`colophon-metric--${metric.rating}`"
                    >
                        <header class="colophon-metric__head">
                            <span class="colophon-metric__name">{{ metric.name }}</span>
                            <span class="colophon-metric__rating">{{ metric.ratingLabel }}</span>
                        </header>
                        <p class="colophon-metric__value">{{ metric.formatted }}</p>
                        <small class="colophon-metric__desc">{{ metric.desc }}</small>
                    </article>
                </div>
            </section>

            <section class="colophon-section" aria-labelledby="build-title">
                <h2 id="build-title" class="colophon-section__title">Build &amp; budget</h2>
                <dl class="colophon-kv">
                    <div class="colophon-kv__row">
                        <dt>Objectif Lighthouse</dt>
                        <dd>Performance ≥ 90, A11y ≥ 95, Best Practices ≥ 95, SEO ≥ 95</dd>
                    </div>
                    <div class="colophon-kv__row">
                        <dt>Budget bundle client</dt>
                        <dd>Core Vendor &lt; 120 kB gzip · Route-specifique &lt; 30 kB gzip</dd>
                    </div>
                    <div class="colophon-kv__row">
                        <dt>Mode offline</dt>
                        <dd>Articles en stale-while-revalidate (24 h) via service worker</dd>
                    </div>
                    <div class="colophon-kv__row">
                        <dt>Tests</dt>
                        <dd>Vitest (unit + a11y via axe-core) dans la CI GitLab à chaque MR</dd>
                    </div>
                </dl>
            </section>
        </Main>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, onMounted } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Main from '@/components/layouts/Main.vue';
    import Hero from '@/components/ui/Hero.vue';
    import { useSeo } from '@/composables/seo/useSeo';
    import { getBaseUrl } from '@/config/api';

    import type { StackGroup } from '@/types/pages/colophon';

    const heroDescription
        = 'La stack, les choix techniques et les métriques de ce portfolio — '
            + 'pour que vous puissiez juger le code avant de juger le CV.';

    useSeo({
        title: 'Colophon',
        description: 'Stack, choix techniques et métriques en direct du portfolio.',
        url: '/colophon',
        keywords: ['colophon', 'stack', 'web vitals', 'portfolio', 'observabilite'],
    });

    const stackGroups: StackGroup[] = [
        {
            label: 'Frontend',
            icon: 'layout',
            items: [
                { name: 'Nuxt 4 (SSR)', detail: 'Vue 3 + TS strict' },
                { name: 'Pinia', detail: 'État global' },
                { name: '@tanstack/vue-query', detail: 'Cache API + prefetch' },
                { name: '@vueuse/core', detail: 'Composables utilitaires' },
            ],
        },
        {
            label: 'Styles',
            icon: 'palette',
            items: [
                { name: 'SCSS modulaire', detail: 'Variables + mixins' },
                { name: 'Lato + Fira Code', detail: 'via @nuxt/fonts' },
                { name: '@nuxt/image (IPX)', detail: 'AVIF / WebP / PNG' },
            ],
        },
        {
            label: 'SEO & sharing',
            icon: 'search',
            items: [
                { name: '@nuxtjs/seo', detail: 'Sitemap + robots + schema.org' },
                { name: 'OG images dynamiques', detail: 'Satori par slug' },
                { name: 'Atom + JSON Feed', detail: '/feed.xml, /feed.json' },
                { name: 'View Transitions API', detail: 'Morph hero + titre' },
            ],
        },
        {
            label: 'Observabilité',
            icon: 'chart',
            items: [
                { name: 'Web Vitals', detail: 'Sample 20 % en prod' },
                { name: 'Lighthouse CI', detail: 'Seuils par route' },
                { name: 'Grafana + Loki + Prometheus', detail: 'Stack monitoring Docker' },
            ],
        },
        {
            label: 'Qualité',
            icon: 'shield',
            items: [
                { name: 'Vitest + vitest-axe', detail: 'Unit + a11y smoke' },
                { name: 'ESLint + Stylelint', detail: 'Rules a11y incluses' },
                { name: 'GitLab CI', detail: 'validate / test / security / build / deploy' },
            ],
        },
        {
            label: 'Backend',
            icon: 'server',
            items: [
                { name: 'Django 5 + DRF', detail: 'Python 3.13' },
                { name: 'PostgreSQL 17', detail: 'SearchVector full-text' },
                { name: 'Celery + Redis', detail: 'Jobs asynchrones' },
            ],
        },
    ];

    // Web Vitals thresholds (Google Core Web Vitals)
    const VITAL_DEFS: Record<string, { desc: string; goodMs: number; poorMs: number; unit: 'ms' | 's' | 'ratio' }> = {
        LCP: { desc: 'Largest Contentful Paint', goodMs: 2500, poorMs: 4000, unit: 'ms' },
        INP: { desc: 'Interaction to Next Paint', goodMs: 200, poorMs: 500, unit: 'ms' },
        CLS: { desc: 'Cumulative Layout Shift', goodMs: 0.1, poorMs: 0.25, unit: 'ratio' },
        FCP: { desc: 'First Contentful Paint', goodMs: 1800, poorMs: 3000, unit: 'ms' },
        TTFB: { desc: 'Time to First Byte', goodMs: 800, poorMs: 1800, unit: 'ms' },
    };

    interface VitalSummary { name: string; p75: number }
    const vitals = ref<VitalSummary[] | null>(null);
    const vitalsError = ref(false);
    const vitalsReady = computed(() => vitals.value !== null);

    onMounted(async () => {
        try {
            const base = getBaseUrl();
            const res = await fetch(`${base}/api/stats/web-vitals/summary/`, { credentials: 'omit' });
            if (!res.ok) {
                throw new Error(`status ${res.status}`);
            }
            const data = await res.json() as { metrics?: VitalSummary[] };
            vitals.value = data.metrics ?? [];
        } catch {
            vitalsError.value = true;
        }
    });

    function formatValue(name: string, value: number): string {
        const def = VITAL_DEFS[name];
        if (!def) {
            return String(value);
        }
        if (def.unit === 'ms') {
            return value >= 1000 ? `${(value / 1000).toFixed(2)} s` : `${Math.round(value)} ms`;
        }
        if (def.unit === 's') {
            return `${value.toFixed(2)} s`;
        }
        return value.toFixed(3);
    }

    function ratingOf(name: string, value: number): 'good' | 'ni' | 'poor' {
        const def = VITAL_DEFS[name];
        if (!def) {
            return 'good';
        }
        if (value <= def.goodMs) {
            return 'good';
        }
        if (value <= def.poorMs) {
            return 'ni';
        }
        return 'poor';
    }
    const ratingLabel: Record<'good' | 'ni' | 'poor', string> = {
        good: 'Bon',
        ni: 'À améliorer',
        poor: 'Mauvais',
    };

    const vitalsRows = computed(() => {
        const list = vitals.value ?? [];
        return list
            .filter((m) => m.name in VITAL_DEFS)
            .map((m) => {
                const rating = ratingOf(m.name, m.p75);
                return {
                    name: m.name,
                    p75: m.p75,
                    formatted: formatValue(m.name, m.p75),
                    desc: VITAL_DEFS[m.name]?.desc ?? '',
                    rating,
                    ratingLabel: ratingLabel[rating],
                };
            });
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .colophon-section {
        margin-bottom: vars.$spacing-xxl;

        &__title {
            margin: 0 0 vars.$spacing-sm;
            color: vars.$text-primary;
        }

        &__intro {
            margin: 0 0 vars.$spacing-lg;
            color: vars.$text-secondary;
            max-width: 720px;
        }
    }

    .colophon-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: vars.$spacing-md;
    }

    .colophon-card {
        padding: vars.$spacing-lg;
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.4);
        border-radius: vars.$border-radius-lg;

        &__head {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin-bottom: vars.$spacing-md;
            color: vars.$primary-color;
        }

        &__title {
            margin: 0;
            font-size: vars.$font-size-lg;
            color: vars.$text-primary;
        }

        &__list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
        }

        &__item {
            display: flex;
            flex-direction: column;
        }

        &__item-name {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
        }

        &__item-detail {
            color: vars.$text-muted;
            font-size: vars.$font-size-sm;
        }
    }

    .colophon-empty {
        padding: vars.$spacing-lg;
        border: 1px dashed fn.color-alpha(vars.$border-color, 0.5);
        border-radius: vars.$border-radius-md;
        color: vars.$text-muted;
        text-align: center;
    }

    .colophon-metric {
        padding: vars.$spacing-lg;
        border-radius: vars.$border-radius-lg;
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.4);

        &--good { border-left: 4px solid vars.$success-color; }
        &--ni   { border-left: 4px solid vars.$warning-color; }
        &--poor { border-left: 4px solid vars.$danger-color; }

        &__head {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: vars.$spacing-xs;
        }

        &__name {
            font-weight: vars.$font-weight-bold;
            letter-spacing: 0.05em;
            color: vars.$text-primary;
        }

        &__rating {
            font-size: vars.$font-size-xs;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: vars.$text-muted;
        }

        &__value {
            margin: 0;
            font-size: 1.75rem;
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
        }

        &__desc {
            color: vars.$text-muted;
        }
    }

    .colophon-kv {
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-md;

        &__row {
            display: grid;
            grid-template-columns: 220px 1fr;
            gap: vars.$spacing-md;

            @media (max-width: 640px) {
                grid-template-columns: 1fr;
            }
        }

        dt {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
        }

        dd {
            margin: 0;
            color: vars.$text-secondary;
        }
    }
</style>
