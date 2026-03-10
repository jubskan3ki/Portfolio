<template>
    <div>
        <!-- En-tête de contact avec le composant Hero -->
        <Hero
            title="Contact"
            description="Vous avez un projet ou une opportunité professionnelle ? N'hésitez pas à me contacter."
            variant="light"
            show-title-underline
        />

        <!-- Contenu principal avec formulaire et infos -->
        <Section class="contact-content">
            <div class="container">
                <div class="contact-content__wrapper">
                    <!-- Formulaire de contact -->
                    <div class="contact-content__form animate-fade-in-up">
                        <ContactForm form-id="contact-form-fixed" />
                    </div>

                    <!-- Informations de contact -->
                    <div class="contact-content__info animate-fade-in-up delay-2">
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

        <!-- FAQ - Questions fréquentes (désactivé temporairement)
        <Section class="contact-faq" variant="light">
            <div class="container">
                <h2 class="contact-faq__title animate-fade-in">Questions fréquentes</h2>

                <SkeletonList
                    v-if="faqsLoading"
                    :count="4"
                    variant="default"
                    layout="list"
                    :show-image="false"
                    show-description
                    :show-tags="false"
                    custom-class="faq-skeleton"
                />

                <div v-else class="faq-list animate-fade-in delay-1">
                    <div v-for="(faq, index) in faqs" :key="faq.id" class="faq-item">
                        <button
                            class="faq-item__question"
                            :class="{ 'faq-item__question--active': expandedFaq === index }"
                            :aria-expanded="expandedFaq === index"
                            :aria-controls="`faq-answer-${faq.id}`"
                            @click="toggleFaq(index)"
                        >
                            <h3>{{ faq.question }}</h3>
                            <BaseIcon :name="expandedFaq === index ? 'chevron-up' : 'chevron-down'" :size="16" />
                        </button>
                        <div
                            :id="`faq-answer-${faq.id}`"
                            role="region"
                            :aria-labelledby="`faq-question-${faq.id}`"
                            class="faq-item__answer"
                            :class="{ 'faq-item__answer--active': expandedFaq === index }"
                        >
                            <p>{{ faq.answer }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </Section>
        -->
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    // import BaseIcon from '@/components/base/BaseIcon.vue';
    import ContactForm from '@/components/feature/contact/ContactForm.vue';
    import ContactInfos from '@/components/feature/contact/ContactInfos.vue';
    import Section from '@/components/layouts/Section.vue';
    // import SkeletonList from '@/components/loaders/SkeletonList.vue';
    import Hero from '@/components/ui/Hero.vue';
    // import { useAnnounce } from '@/composables/accessibility/useAnnounce';
    import { useContactSeo } from '@/composables/seo/useSeo';
    import { useScrollToTop } from '@/composables/ui/useScrollToTop';
    import { /* useFaqs, */ useContactInfo } from '@/services/api/modules/contact';

    // SEO with Schema.org
    useContactSeo();

    // Accessibility & UX
    // const { announce } = useAnnounce();
    useScrollToTop();

    // API Queries
    // const { data: faqsData, isLoading: faqsLoading } = useFaqs();
    const { data: contactInfo } = useContactInfo();

    // FAQs (filter published only) — désactivé temporairement
    // const faqs = computed(() => {
    //     return faqsData.value?.filter((faq) => faq.isPublished) ?? [];
    // });

    // Contact info with fallbacks
    const contactAddress = computed(() => contactInfo.value?.address?.city ?? 'Paris, France');
    const contactEmail = computed(() => contactInfo.value?.email ?? 'contact@aitaddajuba.fr');
    const contactPhone = computed(() => contactInfo.value?.phone ?? '+33 6 95 21 71 97');

    // État — désactivé temporairement
    // const expandedFaq = ref<number | null>(null);

    // Configuration des liens sociaux
    const socialMediaLinks = computed(() => {
        if (contactInfo.value?.socialMedia) {
            const social = contactInfo.value.socialMedia;
            const links = [];
            if (social.linkedin) {
                links.push({ name: 'LinkedIn', icon: 'linkedin', url: social.linkedin });
            }
            if (social.github) {
                links.push({ name: 'GitHub', icon: 'github', url: social.github });
            }
            if (social.twitter) {
                links.push({ name: 'Twitter', icon: 'twitter', url: social.twitter });
            }
            if (social.medium) {
                links.push({ name: 'Medium', icon: 'medium', url: social.medium });
            }
            return links;
        }
        // Fallback
        return [
            { name: 'LinkedIn', icon: 'linkedin', url: 'https://www.linkedin.com/in/juba-aitadda/' },
            { name: 'GitHub', icon: 'github', url: 'https://github.com/jubskan3ki' },
        ];
    });

    // Méthodes — désactivé temporairement
    // const toggleFaq = (index: number) => {
    //     const isExpanding = expandedFaq.value !== index;
    //     expandedFaq.value = isExpanding ? index : null;
    //
    //     // Accessibilité: annoncer l'état de la FAQ
    //     if (isExpanding && faqs.value[index]) {
    //         announce(`Question ouverte: ${faqs.value[index].question}`);
    //     } else {
    //         announce('Question fermée');
    //     }
    // };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    // Contenu principal
    .contact-content {
        padding: vars.$spacing-xl 0;

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

    /* FAQ - Questions fréquentes */
    .contact-faq {
        padding: vars.$spacing-xl 0;

        &__title {
            text-align: center;
            margin-bottom: vars.$spacing-xl;
            position: relative;
            color: vars.$primary-color;

            &::after {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 3px;
                background-color: vars.$primary-color;
                border-radius: vars.$border-radius-full;
            }
        }
    }

    .faq-skeleton {
        max-width: 800px;
        margin: 0 auto;
    }

    .faq-list {
        max-width: 800px;
        margin: 0 auto;
    }

    .faq-item {
        margin-bottom: vars.$spacing-md;
        border-radius: vars.$border-radius-md;
        overflow: hidden;
        box-shadow: vars.$box-shadow;
        background-color: vars.$white;

        &__question {
            width: 100%;
            border: none;
            font: inherit;
            text-align: left;
            padding: vars.$spacing-md;
            background-color: vars.$white;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.3s ease;

            &:hover {
                background-color: vars.$white-dark;
            }

            &--active {
                background-color: func.color-alpha(vars.$primary-color, 0.1);

                h3 {
                    color: vars.$primary-color;
                }
            }

            h3 {
                margin: 0;
                transition: color 0.3s ease;
            }
        }

        &__answer {
            max-height: 0;
            overflow: hidden;
            transition:
                max-height 0.3s ease,
                padding 0.3s ease;

            &--active {
                max-height: 500px;
                padding: vars.$spacing-md;
                border-top: 1px solid vars.$white-dark;
            }

            p {
                margin: 0;
                color: vars.$gray-dark;
                line-height: 1.6;
            }
        }
    }

    /* Animation */
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
