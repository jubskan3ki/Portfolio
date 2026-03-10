<template>
    <div class="privacy-page">
        <Section title="Politique de confidentialité" subtitle="Protection de vos données personnelles" size="large">
            <div class="privacy-page__content">
                <article class="privacy-card">
                    <h2 class="privacy-card__title">Collecte des données</h2>
                    <p>
                        Nous collectons uniquement les données nécessaires au bon fonctionnement de nos services. Les
                        informations recueillies peuvent inclure :
                    </p>
                    <ul class="privacy-card__list">
                        <li>Nom et prénom (via le formulaire de contact)</li>
                        <li>Adresse email (via le formulaire de contact)</li>
                        <li>Message et contenu de votre demande</li>
                        <li>Données de navigation (cookies techniques)</li>
                    </ul>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Utilisation des données</h2>
                    <p>Vos données personnelles sont utilisées exclusivement pour :</p>
                    <ul class="privacy-card__list">
                        <li>Répondre à vos demandes de contact</li>
                        <li>Améliorer l'expérience utilisateur du site</li>
                        <li>Assurer le bon fonctionnement technique du site</li>
                        <li>Établir des statistiques de fréquentation anonymes</li>
                    </ul>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Conservation des données</h2>
                    <p>
                        Vos données sont conservées pour une durée n'excédant pas celle nécessaire aux finalités pour
                        lesquelles elles sont collectées. Les données du formulaire de contact sont conservées pendant
                        une durée maximale de 3 ans.
                    </p>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Vos droits (RGPD)</h2>
                    <p>
                        Conformément au Règlement Général sur la Protection des Données (RGPD), vous disposez des droits
                        suivants :
                    </p>
                    <ul class="privacy-card__list">
                        <li><strong>Droit d'accès</strong> : obtenir une copie de vos données</li>
                        <li><strong>Droit de rectification</strong> : corriger vos données</li>
                        <li><strong>Droit à l'effacement</strong> : supprimer vos données</li>
                        <li><strong>Droit à la limitation</strong> : limiter le traitement</li>
                        <li><strong>Droit à la portabilité</strong> : récupérer vos données</li>
                        <li><strong>Droit d'opposition</strong> : vous opposer au traitement</li>
                    </ul>
                    <p>
                        Pour exercer ces droits, contactez-nous via le
                        <NuxtLink to="/contact" class="privacy-card__link">formulaire de contact</NuxtLink>.
                    </p>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Cookies</h2>
                    <p>
                        Ce site utilise des cookies strictement nécessaires au fonctionnement du site. Aucun cookie de
                        tracking ou publicitaire n'est utilisé. Vous pouvez configurer votre navigateur pour refuser les
                        cookies.
                    </p>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Sécurité</h2>
                    <p>
                        Nous mettons en œuvre des mesures techniques et organisationnelles appropriées pour protéger vos
                        données contre tout accès non autorisé, modification, divulgation ou destruction.
                    </p>
                </article>

                <article class="privacy-card">
                    <h2 class="privacy-card__title">Contact</h2>
                    <p>
                        Pour toute question concernant cette politique, vous pouvez nous contacter via le
                        <NuxtLink to="/contact" class="privacy-card__link">formulaire de contact</NuxtLink>
                        ou consulter nos <NuxtLink to="/legal" class="privacy-card__link">mentions légales</NuxtLink>.
                    </p>
                </article>
            </div>
        </Section>
    </div>
</template>

<script setup lang="ts">
    import Section from '@/components/layouts/Section.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    useSeo({
        title: 'Politique de confidentialité',
        description:
            'Politique de confidentialité et protection des données personnelles du site portfolio de Juba Ait-Adda.',
        url: '/privacy',
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .privacy-page {
        position: relative;
        min-height: 100vh;

        &__content {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;
        }
    }

    .privacy-card {
        background: vars.$white;
        border-radius: vars.$border-radius-lg;
        padding: vars.$spacing-xl;
        box-shadow: vars.$box-shadow-small;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$primary-color;
            margin-bottom: vars.$spacing-md;
            padding-bottom: vars.$spacing-xs;
            border-bottom: 2px solid vars.$border-color-light;
        }

        p {
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
            margin-bottom: vars.$spacing-xs;

            &:last-child {
                margin-bottom: 0;
            }
        }

        &__list {
            margin: vars.$spacing-xs 0;
            padding-left: vars.$spacing-lg;

            li {
                color: vars.$text-secondary;
                line-height: vars.$line-height-relaxed;
                margin-bottom: vars.$spacing-xxs;
                position: relative;

                &::marker {
                    color: vars.$primary-color;
                }

                strong {
                    color: vars.$text-primary;
                }
            }
        }

        &__link {
            color: vars.$primary-color;
            text-decoration: underline;
            text-underline-offset: 2px;

            &:hover {
                color: vars.$primary-dark;
            }
        }
    }
</style>
