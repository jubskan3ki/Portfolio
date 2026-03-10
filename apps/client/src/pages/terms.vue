<template>
    <div class="terms-page">
        <Section title="Conditions d'utilisation" subtitle="Règles d'usage du site" size="large">
            <div class="terms-page__content">
                <article class="terms-card">
                    <h2 class="terms-card__title">Acceptation des conditions</h2>
                    <p>
                        En accédant et en utilisant ce site, vous acceptez d'être lié par les présentes conditions
                        d'utilisation. Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser ce site.
                    </p>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Utilisation du site</h2>
                    <p>Ce site est destiné à un usage personnel et non commercial. Vous vous engagez à :</p>
                    <ul class="terms-card__list">
                        <li>Ne pas utiliser le site à des fins illégales ou non autorisées</li>
                        <li>Ne pas tenter de perturber le fonctionnement du site</li>
                        <li>Ne pas collecter d'informations sur les autres utilisateurs</li>
                        <li>Respecter les droits de propriété intellectuelle</li>
                    </ul>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Propriété intellectuelle</h2>
                    <p>
                        L'ensemble du contenu présent sur ce site (textes, images, graphiques, logos, icônes, code
                        source) est protégé par les lois sur la propriété intellectuelle et reste la propriété exclusive
                        de l'éditeur.
                    </p>
                    <p>
                        Toute reproduction, distribution, modification ou utilisation du contenu sans autorisation
                        préalable écrite est strictement interdite.
                    </p>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Limitation de responsabilité</h2>
                    <p>
                        Les informations fournies sur ce site le sont à titre indicatif. L'éditeur s'efforce de
                        maintenir des informations exactes et à jour, mais ne peut garantir l'exactitude, l'exhaustivité
                        ou la pertinence des informations.
                    </p>
                    <p>
                        L'éditeur ne saurait être tenu responsable des dommages directs ou indirects résultant de
                        l'utilisation de ce site ou de l'impossibilité d'y accéder.
                    </p>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Liens externes</h2>
                    <p>
                        Ce site peut contenir des liens vers des sites externes. Ces liens sont fournis uniquement pour
                        votre commodité. L'éditeur n'a aucun contrôle sur le contenu de ces sites et décline toute
                        responsabilité quant à leur contenu.
                    </p>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Modification des conditions</h2>
                    <p>
                        L'éditeur se réserve le droit de modifier ces conditions d'utilisation à tout moment. Les
                        modifications prennent effet dès leur publication sur le site. Il est conseillé de consulter
                        régulièrement cette page.
                    </p>
                </article>

                <article class="terms-card">
                    <h2 class="terms-card__title">Contact</h2>
                    <p>
                        Pour toute question concernant ces conditions, vous pouvez nous contacter via le
                        <NuxtLink to="/contact" class="terms-card__link">formulaire de contact</NuxtLink>
                        ou consulter nos <NuxtLink to="/legal" class="terms-card__link">mentions légales</NuxtLink>.
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
        title: 'Conditions d\'utilisation',
        description: 'Conditions générales d\'utilisation du site portfolio de Juba Ait-Adda, développeur full-stack.',
        url: '/terms',
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .terms-page {
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

    .terms-card {
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
