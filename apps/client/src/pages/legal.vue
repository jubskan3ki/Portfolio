<template>
    <div class="legal-page">
        <Section title="Mentions légales" subtitle="Informations légales obligatoires" size="large">
            <div class="legal-page__content">
                <article class="legal-card">
                    <h2 class="legal-card__title">Éditeur du site</h2>
                    <div class="legal-card__info">
                        <p><strong>Nom :</strong> [Votre nom complet]</p>
                        <p><strong>Adresse :</strong> [Votre adresse]</p>
                        <p><strong>Email :</strong> [Votre email]</p>
                        <p><strong>Téléphone :</strong> [Votre téléphone]</p>
                        <p><strong>Statut :</strong> [Auto-entrepreneur / SARL / etc.]</p>
                        <p><strong>SIRET :</strong> [Numéro SIRET]</p>
                    </div>
                </article>

                <article class="legal-card">
                    <h2 class="legal-card__title">Hébergement</h2>
                    <div class="legal-card__info">
                        <p><strong>Hébergeur :</strong> [Nom de l'hébergeur]</p>
                        <p><strong>Adresse :</strong> [Adresse de l'hébergeur]</p>
                        <p><strong>Site web :</strong> [URL de l'hébergeur]</p>
                    </div>
                </article>

                <article class="legal-card">
                    <h2 class="legal-card__title">Propriété intellectuelle</h2>
                    <p>
                        L'ensemble du contenu de ce site (textes, images, graphiques, logos, icônes, sons, logiciels,
                        etc.) est la propriété exclusive de l'éditeur ou de ses partenaires et est protégé par les lois
                        françaises et internationales relatives à la propriété intellectuelle.
                    </p>
                    <p>
                        Toute reproduction, représentation, modification, publication, adaptation de tout ou partie des
                        éléments du site, quel que soit le moyen ou le procédé utilisé, est interdite, sauf autorisation
                        écrite préalable.
                    </p>
                </article>

                <article class="legal-card">
                    <h2 class="legal-card__title">Crédits</h2>
                    <p>
                        Ce site a été conçu et développé par [Votre nom]. Les photographies et illustrations utilisées
                        sont soit notre propriété, soit utilisées avec l'autorisation de leurs auteurs respectifs.
                    </p>
                </article>

                <article class="legal-card">
                    <h2 class="legal-card__title">Données personnelles</h2>
                    <p>
                        Pour toute information concernant le traitement de vos données personnelles, veuillez consulter
                        notre <NuxtLink to="/privacy" class="legal-card__link">Politique de confidentialité</NuxtLink>.
                    </p>
                </article>

                <article class="legal-card">
                    <h2 class="legal-card__title">Droit applicable</h2>
                    <p>
                        Les présentes mentions légales sont soumises au droit français. En cas de litige, les tribunaux
                        français seront seuls compétents.
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
        title: 'Mentions légales',
        description:
            'Mentions légales et informations obligatoires du site portfolio de Juba Ait-Adda, développeur full-stack.',
        url: '/legal',
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .legal-page {
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

    .legal-card {
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

        &__info {
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-md;
            padding: vars.$spacing-md;

            p {
                margin-bottom: vars.$spacing-xxs;
                color: vars.$text-secondary;

                &:last-child {
                    margin-bottom: 0;
                }

                strong {
                    color: vars.$text-primary;
                }
            }
        }

        p {
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
            margin-bottom: vars.$spacing-xs;

            &:last-child {
                margin-bottom: 0;
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
