<template>
    <div class="home-page" :class="{ 'home-page--ready': pageReady }">
        <ClientOnly>
            <div class="home-page__orb home-page__orb--primary" aria-hidden="true"></div>
            <div class="home-page__orb home-page__orb--secondary" aria-hidden="true"></div>

            <div v-if="enableShapes" class="home-page__shapes" aria-hidden="true">
                <span
                    v-for="shape in shapes"
                    :key="shape.id"
                    :ref="(el) => setShapeRef(el as HTMLElement, shape.id)"
                    class="home-page__shape"
                    :class="`home-page__shape--${shape.type}`"
                    :style="{
                        left: shape.x + '%',
                        top: shape.y + '%',
                        width: shape.size + 'px',
                        height: shape.size + 'px',
                        opacity: shape.opacity,
                    }"
                ></span>
            </div>
        </ClientOnly>

        <HeroSection :featured-stacks="featuredStacks" :bio="heroBio" />

        <section class="expertise-section">
            <div class="container">
                <div class="expertise-grid">
                    <ExpertiseCard
                        title="Front-end"
                        description="Interfaces modernes et accessibles avec React, Vue, Svelte et CSS/SASS."
                        icon="layout"
                        color="#673c5c"
                        variant="light"
                        to="/stacks?category=Frontend"
                        :prefetch="false"
                    />
                    <ExpertiseCard
                        title="DevOps"
                        description="Infrastructures cloud scalables avec Docker, Kubernetes et Terraform."
                        icon="cloud"
                        color="#ff2453"
                        variant="primary"
                        to="/stacks?category=DevOps"
                        :prefetch="false"
                    />
                    <ExpertiseCard
                        title="Back-end"
                        description="APIs robustes avec Go, Node.js et Django, bases de données SQL/NoSQL."
                        icon="server"
                        color="#43889d"
                        variant="dark"
                        to="/stacks?category=Backend"
                        :prefetch="false"
                    />
                    <ExpertiseCard
                        title="Mobile"
                        description="Applications natives et cross-platform avec React Native et Flutter."
                        icon="smartphone"
                        color="#ac72a0"
                        variant="secondary"
                        to="/stacks?category=Mobile"
                        :prefetch="false"
                    />
                </div>
            </div>
        </section>

        <Section
            id="Experiences"
            title="Expériences récentes"
            subtitle="Parcours professionnel et réalisations marquantes"
            animation-type="scale"
            :animated="!shouldDisableParallax"
            variant="glass"
        >
            <div ref="experiencesTargetRef" class="container">
                <div class="project-timeline">
                    <ClientOnly>
                        <LazyExperienceTimeline
                            :hydrate-on-visible="{ rootMargin: '300px' }"
                            :experiences="professionalExperiences"
                            :limit="3"
                            compact
                        />
                        <template #fallback>
                            <div class="home-section-placeholder" :style="{ minHeight: '420px' }" />
                        </template>
                    </ClientOnly>

                    <div class="section-actions">
                        <BaseButton :to="ROUTES.EXPERIENCE" variant="outline" :prefetch="false">
                            <BaseIcon name="grid" size="sm" class="mr-xs" />
                            Voir mon parcours complet
                        </BaseButton>
                    </div>
                </div>
            </div>
        </Section>

        <Section
            id="projects"
            title="Projets récents"
            subtitle="Solutions digitales innovantes et impactantes"
            animation-type="fade"
            :animated="!shouldDisableParallax"
            variant="light"
        >
            <div class="container">
                <ClientOnly>
                    <LazyProjectCarousel
                        :hydrate-on-visible="{ rootMargin: '300px' }"
                        :limit="5"
                        autoplay
                    />
                    <template #fallback>
                        <div class="home-section-placeholder" :style="{ minHeight: '420px' }" />
                    </template>
                </ClientOnly>

                <div class="section-actions">
                    <BaseButton :to="ROUTES.PROJECTS" variant="primary" :prefetch="false">
                        <BaseIcon name="grid" size="sm" class="mr-xs" />
                        Explorer tous mes projets
                    </BaseButton>
                </div>
            </div>
        </Section>

        <Section
            id="stacks"
            title="Stacks"
            subtitle="Mon expertise technique polyvalente"
            animation-type="slide"
            :animated="!shouldDisableParallax"
        >
            <div class="container">
                <ClientOnly>
                    <LazyStackCarousel
                        :hydrate-on-visible="{ rootMargin: '300px' }"
                        :limit="10"
                        autoplay
                        :slides-per-view="6"
                        show-level
                    />
                    <template #fallback>
                        <div class="home-section-placeholder" :style="{ minHeight: '280px' }" />
                    </template>
                </ClientOnly>

                <div class="section-actions">
                    <BaseButton :to="ROUTES.STACKS" variant="outline" :prefetch="false">
                        <BaseIcon name="layers" size="sm" class="mr-xs" />
                        Découvrir tous mes stacks
                    </BaseButton>
                </div>
            </div>
        </Section>

        <Section
            id="blog"
            title="Articles récents"
            subtitle="Partage de connaissances et veille technologique"
            animation-type="scale"
            :animated="!shouldDisableParallax"
            variant="light"
        >
            <div ref="articlesTargetRef" class="container">
                <ClientOnly>
                    <LazyArticleCarousel
                        :hydrate-on-visible="{ rootMargin: '300px' }"
                        :articles="articles"
                        :limit="4"
                        autoplay
                        :autoplay-speed="6000"
                        show-stats
                        show-dots
                    />
                    <template #fallback>
                        <div class="home-section-placeholder" :style="{ minHeight: '420px' }" />
                    </template>
                </ClientOnly>

                <div class="section-actions">
                    <BaseButton :to="ROUTES.BLOG" variant="primary" :prefetch="false">
                        <BaseIcon name="book-open" size="sm" class="mr-xs" />
                        Lire tous mes articles
                    </BaseButton>
                </div>
            </div>
        </Section>

        <section class="contact-section">
            <div class="container">
                <div class="contact-section__header">
                    <h2 class="contact-section__title">Travaillons ensemble</h2>
                    <p class="contact-section__subtitle">Transformons vos idées en solutions digitales</p>
                </div>
                <div class="contact-wrapper">
                    <div class="contact-wrapper__form">
                        <ClientOnly>
                            <LazyContactForm
                                :hydrate-on-visible="{ rootMargin: '200px' }"
                                form-id="contact-form-home"
                            />
                            <template #fallback>
                                <div class="home-section-placeholder" :style="{ minHeight: '580px' }" />
                            </template>
                        </ClientOnly>
                    </div>
                    <div class="contact-wrapper__info">
                        <ClientOnly>
                            <LazyContactInfos
                                :hydrate-on-visible="{ rootMargin: '200px' }"
                                title="Mes coordonnées"
                                subtitle="Discutons de vos besoins et objectifs"
                                :address="contactAddress"
                                :email="contactEmail"
                                :phone="contactPhone"
                                :social-links="socialMediaLinks"
                            />
                            <template #fallback>
                                <div class="home-section-placeholder" :style="{ minHeight: '480px' }" />
                            </template>
                        </ClientOnly>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
    import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import ExpertiseCard from '@/components/feature/home/ExpertiseCard.vue';
    import HeroSection from '@/components/feature/home/HeroSection.vue';
    import Section from '@/components/layouts/Section.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useSiteSettings } from '@/composables/data/useSiteSettings';
    import { useViewportTrigger } from '@/composables/performance/useViewportTrigger';
    import { useHomeSeo } from '@/composables/seo/useSeo';
    import { useResponsive } from '@/composables/ui/useResponsive';
    import { ROUTES } from '@/config/routes';
    import { useRecentArticles } from '@/services/api/modules/articles';
    import { useProfessionalExperiences } from '@/services/api/modules/experiences';
    import { stacksApi } from '@/services/api/modules/stacks';

    import type { ContactSocialLink } from '@/types/feature/contact';
    import type { HeroStack } from '@/types/feature/home';
    import type { Stack } from '@/types/feature/stacks';

    useHomeSeo();
    // Le preload de l'image LCP est émis par NuxtImg (prop preload sur HeroSection) avec le bon imagesrcset ; un <link preload> manuel re-téléchargeait la variante 560px.

    const { prefersReducedMotion } = useReducedMotion();
    const { isMobile } = useResponsive();

    const shouldDisableParallax = computed(() => prefersReducedMotion.value || isMobile.value);
    const enableShapes = computed(() => !shouldDisableParallax.value);

    const pageReady = ref(false);

    const shapeRefs = ref<Map<number, HTMLElement>>(new Map());

    const shapes = [
        { id: 1, type: 'blob-1', size: 120, x: 3, y: 8, depth: 25, opacity: 0.12 },
        { id: 2, type: 'blob-3', size: 150, x: 88, y: 45, depth: 30, opacity: 0.08 },
        { id: 3, type: 'blob-2', size: 70, x: 15, y: 85, depth: 45, opacity: 0.12 },
    ];

    interface ShapeRender { el: HTMLElement; depth: number }
    let shapeRender: ShapeRender[] = [];

    const setShapeRef = (el: HTMLElement | null, id: number) => {
        if (el) {
            shapeRefs.value.set(id, el);
        }
    };

    const rebuildShapeRender = () => {
        shapeRender = shapes
            .map((s) => {
                const el = shapeRefs.value.get(s.id);
                return el ? { el, depth: s.depth } : null;
            })
            .filter((v): v is ShapeRender => v !== null);
    };

    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let animationId = 0;
    let viewportW = 0;
    let viewportH = 0;

    const updateViewport = () => {
        viewportW = window.innerWidth;
        viewportH = window.innerHeight;
    };

    const onMouseMove = (e: MouseEvent) => {
        if (viewportW === 0) {
            return;
        }
        targetX = (e.clientX / viewportW - 0.5) * 2;
        targetY = (e.clientY / viewportH - 0.5) * 2;
    };

    const animate = () => {
        const dx = targetX - currentX;
        const dy = targetY - currentY;

        if (Math.abs(dx) > 0.0005 || Math.abs(dy) > 0.0005) {
            currentX += dx * 0.05;
            currentY += dy * 0.05;
            for (const { el, depth } of shapeRender) {
                el.style.transform = `translate3d(${currentX * depth}px, ${currentY * depth}px, 0)`;
            }
        }

        animationId = requestAnimationFrame(animate);
    };

    const startParallax = () => {
        if (shouldDisableParallax.value) {
            return;
        }
        rebuildShapeRender();
        if (!shapeRender.length) {
            return;
        }
        updateViewport();
        window.addEventListener('mousemove', onMouseMove, { passive: true });
        window.addEventListener('resize', updateViewport, { passive: true });
        animationId = requestAnimationFrame(animate);
    };

    const stopParallax = () => {
        window.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('resize', updateViewport);
        if (animationId) {
            cancelAnimationFrame(animationId);
            animationId = 0;
        }
    };

    const handleVisibilityChange = () => {
        if (document.hidden) {
            stopParallax();
        } else {
            startParallax();
        }
    };

    onMounted(() => {
        const boot = () => {
            pageReady.value = true;
            startParallax();
        };
        if ('requestIdleCallback' in window) {
            requestIdleCallback(boot, { timeout: 1500 });
        } else {
            setTimeout(boot, 300);
        }
        document.addEventListener('visibilitychange', handleVisibilityChange);
    });

    onBeforeUnmount(() => {
        stopParallax();
        document.removeEventListener('visibilitychange', handleVisibilityChange);
    });

    const defaultStacks: HeroStack[] = [
        { id: 1, name: 'Vue.js', logo: '', level: 90, slug: 'vue-js' },
        { id: 2, name: 'React', logo: '', level: 85, slug: 'react' },
        { id: 3, name: 'TypeScript', logo: '', level: 90, slug: 'typescript' },
        { id: 4, name: 'Node.js', logo: '', level: 80, slug: 'node-js' },
        { id: 5, name: 'Go', logo: '', level: 70, slug: 'golang' },
    ];

    const { data: heroStacks } = useAsyncData(
        'hero-stacks',
        () => stacksApi.getFeatured(10),
        {
            lazy: true,
            default: () => [] as HeroStack[],
            transform: (stacks: Stack[]) =>
                stacks
                    .sort((a, b) => b.level - a.level)
                    .slice(0, 5)
                    .map(({ id, name, logo, level, slug }) => ({ id, name, logo, level, slug })),
        },
    );

    const { settings } = await useSiteSettings({ lazy: true });

    const {
        targetRef: experiencesTargetRef,
        enabled: experiencesEnabled,
    } = useViewportTrigger({ rootMargin: '300px', ssrEager: true });
    void experiencesTargetRef;
    const { data: experiencesData } = useProfessionalExperiences({ enabled: experiencesEnabled });

    const {
        targetRef: articlesTargetRef,
        enabled: articlesEnabled,
    } = useViewportTrigger({ rootMargin: '300px', ssrEager: true });
    void articlesTargetRef;
    const { data: articlesData } = useRecentArticles(4, { enabled: articlesEnabled });

    const featuredStacks = computed(() =>
        heroStacks.value?.length ? heroStacks.value : defaultStacks,
    );

    const professionalExperiences = computed(() => {
        const data = experiencesData.value;
        return Array.isArray(data) ? data : [];
    });

    const articles = computed(() => articlesData.value ?? []);

    const heroBio = computed(() => settings.value.bio);

    const contactAddress = computed(() =>
        [settings.value.addressCity, settings.value.addressCountry].filter(Boolean).join(', '),
    );
    const contactEmail = computed(() => settings.value.email);
    const contactPhone = computed(() => settings.value.phone);

    const socialMediaLinks = computed<ContactSocialLink[]>(() => {
        const links: ContactSocialLink[] = [];
        if (settings.value.socialLinkedin) {
            links.push({ name: 'LinkedIn', icon: 'linkedin', url: settings.value.socialLinkedin });
        }
        if (settings.value.socialGithub) {
            links.push({ name: 'GitHub', icon: 'github', url: settings.value.socialGithub });
        }
        return links;
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .home-page {
        position: relative;
        min-height: 100vh;
        overflow-x: hidden;

        &__orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
            opacity: 0.5;
            contain: layout style paint;
            animation-play-state: paused;

            @media (prefers-reduced-motion: reduce) {
                animation: none !important;
            }

            &--primary {
                width: 45%;
                height: 55%;
                top: -15%;
                right: -10%;
                background: radial-gradient(circle, fn.color-alpha(vars.$primary-color, 0.12) 0%, transparent 70%);
                animation: glow-drift 25s ease-in-out infinite;
                animation-play-state: paused;
            }

            &--secondary {
                width: 40%;
                height: 50%;
                bottom: -20%;
                left: -10%;
                background: radial-gradient(circle, fn.color-alpha(vars.$secondary-color, 0.08) 0%, transparent 70%);
                animation: glow-drift 30s ease-in-out infinite reverse;
                animation-play-state: paused;
            }
        }

        &__shapes {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 1;
            contain: layout style paint;
            content-visibility: auto;
        }

        &__shape {
            position: absolute;
            will-change: transform;
            transition: transform 0.15s ease-out;
            filter: blur(40px);
            contain: layout style paint;

            @media (prefers-reduced-motion: reduce) {
                animation: none !important;
            }

            &--blob-1 {
                background: fn.color-alpha(vars.$primary-color, 0.6);
                border-radius: 60% 40% 30% 70%;
                animation: blob-float-1 22s ease-in-out infinite;
                animation-play-state: paused;
            }

            &--blob-2 {
                background: fn.color-alpha(vars.$secondary-color, 0.5);
                border-radius: 40% 60% 70% 30%;
                animation: blob-float-2 28s ease-in-out infinite;
                animation-play-state: paused;
            }

            &--blob-3 {
                background: fn.color-alpha(vars.$primary-light, 0.4);
                border-radius: 50% 50% 40% 60%;
                animation: blob-float-3 20s ease-in-out infinite;
                animation-play-state: paused;
            }
        }

        &--ready &__orb,
        &--ready &__shape {
            animation-play-state: running;
        }
    }

    @keyframes glow-drift {
        0%,
        100% {
            transform: translate(0, 0) scale(1);
        }

        50% {
            transform: translate(20px, -15px) scale(1.03);
        }
    }

    @keyframes blob-float-1 {
        0%,
        100% {
            border-radius: 60% 40% 30% 70%;
            transform: translateY(0) rotate(0deg);
        }

        33% {
            border-radius: 30% 60% 70% 40%;
            transform: translateY(-8px) rotate(3deg);
        }

        66% {
            border-radius: 50% 60% 30% 65%;
            transform: translateY(5px) rotate(-2deg);
        }
    }

    @keyframes blob-float-2 {
        0%,
        100% {
            border-radius: 40% 60% 70% 30%;
            transform: translateX(0) rotate(0deg);
        }

        50% {
            border-radius: 70% 30% 50% 50%;
            transform: translateX(-12px) rotate(-4deg);
        }
    }

    @keyframes blob-float-3 {
        0%,
        100% {
            border-radius: 50% 50% 40% 60%;
            transform: scale(1) rotate(0deg);
        }

        50% {
            border-radius: 40% 60% 60% 40%;
            transform: scale(1.04) rotate(2deg);
        }
    }

    .expertise-section {
        position: relative;
        z-index: 10;
        margin-top: -100px;
        padding-bottom: vars.$spacing-xxl;

        @include mix.responsive(mobile) {
            margin-top: -60px;
        }
    }

    .expertise-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: vars.$spacing-lg;

        @include mix.responsive(tablet) {
            grid-template-columns: repeat(2, 1fr);
        }

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
            gap: vars.$spacing-md;
        }
    }

    .contact-section {
        position: relative;
        z-index: 10;
        padding: vars.$spacing-xxl 0;
        background: linear-gradient(135deg, vars.$primary-color 0%, vars.$primary-dark 100%);
        overflow: hidden;

        &::before {
            content: '';
            position: absolute;
            inset: -20%;

            @include mix.dots-pattern(fn.color-alpha(vars.$white, 0.04), 1.5px, 24px);

            pointer-events: none;
        }

        &::after {
            content: '';
            position: absolute;
            top: -30%;
            right: -15%;
            width: 50%;
            height: 70%;
            background: radial-gradient(circle, fn.color-alpha(vars.$white, 0.06) 0%, transparent 60%);
            filter: blur(60px);
            pointer-events: none;
        }

        &__header {
            position: relative;
            z-index: 2;
            text-align: center;
            margin-bottom: vars.$spacing-xl;
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            color: vars.$white;
            margin-bottom: vars.$spacing-xs;
            letter-spacing: -0.02em;
        }

        &__subtitle {
            color: fn.color-alpha(vars.$white, 0.8);
            max-width: 500px;
            margin: 0 auto;
            line-height: 1.6;
        }
    }

    .contact-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: vars.$spacing-xl;
        position: relative;
        z-index: 2;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }

        &__form {
            padding: vars.$spacing-xl;
            background: fn.color-alpha(vars.$white, 0.95);
            backdrop-filter: blur(16px) saturate(1.2);
            border-radius: vars.$border-radius-xl;
            border: 1px solid fn.color-alpha(vars.$white, 0.3);
            box-shadow:
                0 8px 32px fn.color-alpha(vars.$black, 0.12),
                0 0 0 1px fn.color-alpha(vars.$white, 0.1) inset;
            transition:
                transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
                box-shadow 0.3s ease;

            &:hover {
                transform: translateY(-4px);
                box-shadow:
                    0 16px 48px fn.color-alpha(vars.$black, 0.15),
                    0 0 0 1px fn.color-alpha(vars.$white, 0.2) inset;
            }

            @include mix.responsive(mobile) {
                padding: vars.$spacing-lg;
            }
        }

        &__info {
            height: 100%;
            display: flex;
            align-items: center;
        }
    }

    .section-actions {
        display: flex;
        justify-content: center;
        margin-top: vars.$spacing-xl;
        gap: vars.$spacing-md;
    }

    .project-timeline {
        position: relative;
        z-index: 1;
    }
</style>
