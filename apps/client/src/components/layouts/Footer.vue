<template>
    <footer class="footer" role="contentinfo">
        <!-- Background decoration -->
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
                        :title="footerData.contactTitle"
                        :email="footerData.email"
                        :phone="footerData.phone"
                        :address="footerData.address"
                        :is-available="footerData.isAvailable"
                    />

                    <FooterSocial title="Suivez-moi" :links="footerData.socialLinks" />
                </aside>
            </div>

            <div class="footer__bottom">
                <p class="footer__copyright">
                    <small>&copy; {{ currentYear }} {{ footerData.companyName }}. {{ footerData.copyrightText }}</small>
                </p>

                <nav v-if="footerData.legalLinks?.length" class="footer__legal" aria-label="Liens légaux">
                    <NuxtLink
                        v-for="link in footerData.legalLinks"
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
    import { footerConfig } from '@/config/footer';
    import { ROUTES } from '@/config/routes';
    import { useContactInfo } from '@/services/api/modules/contact';
    import { useExperienceStats } from '@/services/api/modules/experiences';
    import { useProjectStats } from '@/services/api/modules/projects';
    import { useStackStats } from '@/services/api/modules/stacks';

    import type { CtaLinks } from '@/config/footer';
    import type { SocialLink, StatItem } from '@/types/config/footer';

    const summaryTitle = 'Donnez vie à vos idées avec des solutions digitales innovantes';
    const summaryDescription = computed(
        () =>
            contactInfo.value?.bio
            ?? 'Développeur Web & Mobile passionné par la création d\'expériences digitales modernes et performantes.',
    );

    // API Queries
    const { data: contactInfo } = useContactInfo();
    const { data: projectStats } = useProjectStats();
    const { data: stackStats } = useStackStats();
    const { data: experienceStats } = useExperienceStats();

    const currentYear = computed(() => new Date().getFullYear());

    // Contact info from API with fallbacks
    const footerData = computed(() => {
        const info = contactInfo.value;

        const address = info?.address
            ? [info.address.city, info.address.country].filter(Boolean).join(', ')
            : footerConfig.address;

        const socialLinks: SocialLink[] = [];
        if (info?.socialMedia) {
            const social = info.socialMedia;
            if (social.github) {
                socialLinks.push({ name: 'GitHub', icon: 'github', url: social.github });
            }
            if (social.linkedin) {
                socialLinks.push({ name: 'LinkedIn', icon: 'linkedin', url: social.linkedin });
            }
            if (social.twitter) {
                socialLinks.push({ name: 'Twitter', icon: 'twitter', url: social.twitter });
            }
            if (social.medium) {
                socialLinks.push({ name: 'Medium', icon: 'medium', url: social.medium });
            }
        }

        const isAvailable = info?.availability?.status === 'available';

        return {
            contactTitle: footerConfig.contactTitle,
            email: info?.email ?? footerConfig.email,
            phone: info?.phone ?? footerConfig.phone,
            address,
            companyName: footerConfig.companyName,
            copyrightText: footerConfig.copyrightText,
            isAvailable: info ? isAvailable : footerConfig.isAvailable,
            socialLinks: socialLinks.length > 0 ? socialLinks : footerConfig.socialLinks,
            legalLinks: footerConfig.legalLinks,
            ctaLinks: footerConfig.ctaLinks,
        };
    });

    const ctaLinks = computed<CtaLinks>(() => ({
        primary: footerData.value.ctaLinks?.primary || { label: 'Parlons de votre projet', url: ROUTES.CONTACT },
        secondary: footerData.value.ctaLinks?.secondary || {
            label: 'Découvrir mes réalisations',
            url: ROUTES.PROJECTS,
        },
    }));

    const stats = computed<StatItem[]>(() => [
        { value: projectStats.value?.totalProjects ?? footerConfig.projectsCount, label: 'Projets réalisés' },
        { value: experienceStats.value?.totalYears ?? footerConfig.yearsExperience, label: 'Années d\'expérience' },
        { value: stackStats.value?.totalStacks ?? footerConfig.techCount, label: 'Technologies maîtrisées' },
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
