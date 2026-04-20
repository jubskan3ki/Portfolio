<template>
    <footer class="footer" role="contentinfo">
        <div class="footer__bg" aria-hidden="true">
            <div class="footer__dots"></div>
            <div class="footer__glow"></div>
        </div>

        <div class="container footer__container">
            <div class="footer__main">
                <PortfolioSummary
                    :title="summaryTitle"
                    :description="summaryDescription"
                    :cta-links="ctaLinks"
                    :stats="stats"
                />

                <aside class="footer__contact">
                    <FooterContact
                        :title="footerConfig.contactTitle"
                        :email="settings.email"
                        :phone="settings.phone"
                        :address="address"
                        :is-available="settings.isAvailable"
                        :availability-label="settings.availabilityMessage"
                    />

                    <FooterSocial title="Suivez-moi" :links="socialLinks" />
                </aside>
            </div>

            <div class="footer__bottom">
                <p class="footer__copyright">
                    <small>
                        &copy; {{ currentYear }} {{ footerConfig.companyName }}.
                        {{ footerConfig.copyrightText }}
                    </small>
                </p>

                <nav v-if="footerConfig.legalLinks?.length" class="footer__legal" aria-label="Liens légaux">
                    <NuxtLink
                        v-for="link in footerConfig.legalLinks"
                        :key="link.label"
                        :to="link.url"
                        class="footer__legal-link"
                    >
                        <small>{{ link.label }}</small>
                    </NuxtLink>
                </nav>
            </div>
        </div>
    </footer>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import FooterContact from '@/components/layouts/FooterContact.vue';
    import FooterSocial from '@/components/layouts/FooterSocial.vue';
    import PortfolioSummary from '@/components/ui/PortfolioSummary.vue';
    import { useSiteSettings } from '@/composables/data/useSiteSettings';
    import { footerConfig } from '@/config/footer';
    import { ROUTES } from '@/config/routes';
    import { useExperienceStats } from '@/services/api/modules/experiences';
    import { useProjectStats } from '@/services/api/modules/projects';
    import { useStackStats } from '@/services/api/modules/stacks';

    import type { CtaLinks } from '@/config/footer';
    import type { SocialLink, StatItem } from '@/types/config/footer';

    const summaryTitle = 'Donnez vie à vos idées avec des solutions digitales innovantes';

    // Dynamic site settings (SSR — hydrated in initial HTML)
    const { settings } = await useSiteSettings();

    // Client-only stats
    const { data: projectStats } = useProjectStats();
    const { data: stackStats } = useStackStats();
    const { data: experienceStats } = useExperienceStats();

    const currentYear = computed(() => new Date().getFullYear());

    const summaryDescription = computed(() => settings.value.bio);

    const address = computed(() =>
        [settings.value.addressCity, settings.value.addressCountry].filter(Boolean).join(', '),
    );

    const socialLinks = computed<SocialLink[]>(() => {
        const links: SocialLink[] = [];
        if (settings.value.socialGithub) {
            links.push({ name: 'GitHub', icon: 'github', url: settings.value.socialGithub });
        }
        if (settings.value.socialLinkedin) {
            links.push({ name: 'LinkedIn', icon: 'linkedin', url: settings.value.socialLinkedin });
        }
        if (settings.value.socialTwitter) {
            links.push({ name: 'Twitter', icon: 'twitter', url: settings.value.socialTwitter });
        }
        if (settings.value.socialMedium) {
            links.push({ name: 'Medium', icon: 'medium', url: settings.value.socialMedium });
        }
        return links;
    });

    const ctaLinks = computed<CtaLinks>(() => ({
        primary: footerConfig.ctaLinks?.primary || { label: 'Parlons de votre projet', url: ROUTES.CONTACT },
        secondary: footerConfig.ctaLinks?.secondary || {
            label: 'Découvrir mes réalisations',
            url: ROUTES.PROJECTS,
        },
    }));

    const stats = computed<StatItem[]>(() => [
        { value: projectStats.value?.totalProjects ?? 0, label: 'Projets réalisés' },
        { value: experienceStats.value?.totalYears ?? 0, label: 'Années d\'expérience' },
        { value: stackStats.value?.totalStacks ?? 0, label: 'Technologies maîtrisées' },
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .footer {
        position: relative;
        padding: vars.$spacing-xxxl 0 vars.$spacing-lg;
        overflow: hidden;
        margin-top: auto;

        /* Background layer */
        &__bg {
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }

        &__dots {
            position: absolute;
            inset: -10%;

            @include mix.dots-pattern(func.color-alpha(vars.$primary-color, 0.02), 1px, 28px);
        }

        &__glow {
            position: absolute;
            top: -40%;
            left: 50%;
            transform: translateX(-50%);
            width: 70%;
            height: 50%;
            background: radial-gradient(ellipse, func.color-alpha(vars.$primary-color, 0.04) 0%, transparent 65%);
            filter: blur(80px);
        }

        &__container {
            position: relative;
            z-index: 1;
        }

        &__main {
            display: grid;
            grid-template-columns: 3fr 1fr;
            gap: vars.$spacing-lg;
            margin-bottom: vars.$spacing-lg;

            @include mix.responsive(tablet) {
                grid-template-columns: 1fr;
                gap: vars.$spacing-md;
            }
        }

        &__contact {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;

            @include mix.responsive(tablet) {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: vars.$spacing-md;
            }

            @include mix.responsive(mobile) {
                grid-template-columns: 1fr;
            }
        }

        /* Bottom bar */
        &__bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: vars.$spacing-md;
            border-top: 1px solid func.color-alpha(vars.$primary-color, 0.06);

            @include mix.responsive(mobile) {
                flex-direction: column;
                gap: vars.$spacing-xs;
                align-items: flex-start;
            }
        }

        &__copyright {
            color: vars.$text-muted;
            margin: 0;
        }

        &__legal {
            display: flex;
            gap: vars.$spacing-md;

            @include mix.responsive(mobile) {
                flex-wrap: wrap;
                gap: vars.$spacing-xxs;
            }
        }

        &__legal-link {
            color: vars.$text-muted;
            text-decoration: none;
            transition: color 0.2s ease;
            position: relative;

            &::after {
                content: '';
                position: absolute;
                bottom: -2px;
                left: 0;
                width: 0;
                height: 1px;
                background: vars.$primary-color;
                transition: width 0.2s ease;
            }

            &:hover {
                color: vars.$primary-color;

                &::after {
                    width: 100%;
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }
    }
</style>
