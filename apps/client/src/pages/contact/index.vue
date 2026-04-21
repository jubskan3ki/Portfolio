<template>
    <div class="contact-page">
        <Hero
            title="À propos & Contact"
            description="Développeur full-stack et DevOps basé à Paris, passionné par la création d'applications
                web performantes et maintenables."
            variant="light"
            show-title-underline
        />

        <Section class="about-section">
            <div class="container">
                <div class="about-section__wrapper">
                    <div class="about-section__profile animate-fade-in-up">
                        <div class="about-section__photo">
                            <NuxtImg
                                src="/images/profile.jpg"
                                :alt="`${name} - ${jobTitle}`"
                                width="280"
                                height="280"
                                loading="eager"
                                class="about-section__img"
                            />
                        </div>
                        <h2 class="about-section__name">{{ name }}</h2>
                        <p class="about-section__job">{{ jobTitle }}</p>
                        <div class="about-section__links">
                            <a
                                v-for="link in profileSocialLinks"
                                :key="link.name"
                                :href="link.url"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="about-section__link"
                                :aria-label="link.name"
                            >
                                <BaseIcon :name="link.icon" :size="20" />
                            </a>
                        </div>
                    </div>

                    <div class="about-section__bio animate-fade-in-up delay-1">
                        <h2 class="about-section__title">Qui suis-je ?</h2>
                        <p>
                            Je suis Juba Ait-Adda, développeur full-stack basé à Paris. Passionné par le
                            développement web depuis plusieurs années, je conçois des applications modernes,
                            performantes et maintenables en combinant les meilleures pratiques frontend et backend.
                        </p>
                        <p>
                            Mon expertise couvre l'ensemble du cycle de développement : de la conception d'interfaces
                            réactives avec Vue.js et React, à la mise en place d'APIs robustes avec Django et Node.js,
                            en passant par l'infrastructure et le déploiement avec Docker et Kubernetes.
                        </p>
                        <p>
                            Je suis convaincu que la qualité du code, l'accessibilité et la performance ne sont
                            pas des options mais des fondamentaux. Chaque projet est une opportunité d'apprendre
                            et de repousser les limites du possible.
                        </p>
                    </div>
                </div>
            </div>
        </Section>

        <Section class="faq-section">
            <div class="container">
                <ContactFAQ :items="faqItems" />
            </div>
        </Section>

        <Section class="contact-section" variant="light">
            <div class="container">
                <h2 class="contact-section__heading animate-fade-in">Me contacter</h2>
                <p class="contact-section__subheading animate-fade-in">
                    Vous avez un projet ou une opportunité professionnelle ? N'hésitez pas à me contacter.
                </p>
                <div class="contact-section__wrapper">
                    <div class="contact-section__form animate-fade-in-up delay-1">
                        <ContactForm form-id="contact-form-fixed" />
                    </div>

                    <div class="contact-section__info animate-fade-in-up delay-2">
                        <ContactInfos
                            title="Mes coordonnées"
                            subtitle="N'hésitez pas à me contacter par ces moyens"
                            :address="contactAddress"
                            :email="contactEmail"
                            :phone="contactPhone"
                            :social-links="socialMediaLinks"
                            custom-class="contact-page-infos"
                        />
                    </div>
                </div>
            </div>
        </Section>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import ContactFAQ from '@/components/feature/contact/ContactFAQ.vue';
    import ContactForm from '@/components/feature/contact/ContactForm.vue';
    import ContactInfos from '@/components/feature/contact/ContactInfos.vue';
    import Section from '@/components/layouts/Section.vue';
    import Hero from '@/components/ui/Hero.vue';
    import { useSiteSettings } from '@/composables/data/useSiteSettings';
    import { useContactFaqSeo } from '@/composables/seo/useContactFaqSeo';
    import { useContactSeo, SITE_CONFIG } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';

    import type { ContactSocialLink } from '@/types/feature/contact';

    useContactSeo();
    const { items: faqItems } = useContactFaqSeo();
    useScrollToTop();

    const { author } = SITE_CONFIG;
    const name = author.name;
    const jobTitle = author.jobTitle;

    const { settings } = await useSiteSettings();

    const profileSocialLinks = computed<ContactSocialLink[]>(() => {
        const links: ContactSocialLink[] = [];
        if (settings.value.socialGithub) {
            links.push({ name: 'GitHub', icon: 'github', url: settings.value.socialGithub });
        }
        if (settings.value.socialLinkedin) {
            links.push({ name: 'LinkedIn', icon: 'linkedin', url: settings.value.socialLinkedin });
        }
        return links;
    });

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
        if (settings.value.socialMedium) {
            links.push({ name: 'Medium', icon: 'medium', url: settings.value.socialMedium });
        }
        return links;
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .about-section {
        padding: vars.$spacing-xl 0;

        &__wrapper {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: vars.$spacing-xl;
            align-items: start;

            @include mix.responsive(tablet) {
                grid-template-columns: 1fr;
            }
        }

        &__profile {
            text-align: center;
            position: sticky;
            top: calc(vars.$spacing-xl + 80px);

            @include mix.responsive(tablet) {
                position: static;
            }
        }

        &__photo {
            width: 200px;
            height: 200px;
            margin: 0 auto vars.$spacing-md;
            border-radius: 50%;
            overflow: hidden;
            box-shadow: vars.$box-shadow-medium;
        }

        &__img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        &__name {
            margin: 0 0 vars.$spacing-xs;
            color: vars.$primary-color;
        }

        &__job {
            margin: 0 0 vars.$spacing-md;
            color: vars.$gray-dark;
        }

        &__links {
            display: flex;
            justify-content: center;
            gap: vars.$spacing-sm;
        }

        &__link {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: vars.$white-dark;
            color: vars.$gray-dark;
            transition: all vars.$transition-base;

            &:hover {
                background-color: vars.$primary-color;
                color: vars.$white;
            }
        }

        &__bio {
            p {
                line-height: 1.8;
                color: vars.$gray-dark;
                margin-bottom: vars.$spacing-md;
            }
        }

        &__title {
            color: vars.$primary-color;
            margin: vars.$spacing-lg 0 vars.$spacing-md;
            position: relative;

            &::after {
                content: '';
                position: absolute;
                bottom: -6px;
                left: 0;
                width: 40px;
                height: 3px;
                background-color: vars.$primary-color;
                border-radius: vars.$border-radius-full;
            }
        }

    }

    .contact-section {
        padding: vars.$spacing-xl 0;

        &__heading {
            text-align: center;
            color: vars.$primary-color;
            margin-bottom: vars.$spacing-xs;
        }

        &__subheading {
            text-align: center;
            color: vars.$gray-dark;
            margin-bottom: vars.$spacing-xl;
        }

        &__wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: vars.$spacing-xl;

            @include mix.responsive(tablet) {
                grid-template-columns: 1fr;
            }
        }

        &__form {
            background-color: vars.$white;
            border-radius: vars.$border-radius-lg;
            padding: vars.$spacing-lg;
            box-shadow: vars.$box-shadow-medium;
        }

        &__info {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;
        }
    }

    .animate-fade-in {
        animation: fadeIn vars.$transition-base forwards;
    }

    .animate-fade-in-up {
        animation: fadeInUp vars.$transition-base forwards;
    }

    .delay-1 {
        animation-delay: 0.1s;
    }

    .delay-2 {
        animation-delay: 0.2s;
    }
</style>
