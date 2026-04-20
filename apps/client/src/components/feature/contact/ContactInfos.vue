<template>
    <div class="contact-infos">
        <div class="contact-infos__decoration">
            <div class="contact-infos__orb contact-infos__orb--1"></div>
            <div class="contact-infos__orb contact-infos__orb--2"></div>
        </div>

        <div class="contact-infos__content">
            <div class="contact-infos__header">
                <h2 class="contact-infos__title">{{ title }}</h2>
                <p v-if="subtitle" class="contact-infos__subtitle">{{ subtitle }}</p>
            </div>

            <div class="contact-infos__items">
                <div v-if="address" class="contact-infos__item">
                    <div class="contact-infos__icon">
                        <BaseIcon name="map-pin" :size="20" />
                    </div>
                    <div class="contact-infos__details">
                        <span class="contact-infos__label">{{ addressTitle }}</span>
                        <span class="contact-infos__value">{{ address }}</span>
                    </div>
                </div>

                <div v-if="email" class="contact-infos__item">
                    <div class="contact-infos__icon">
                        <BaseIcon name="mail" :size="20" />
                    </div>
                    <div class="contact-infos__details">
                        <span class="contact-infos__label">{{ emailTitle }}</span>
                        <BaseLink :to="`mailto:${email}`" class="contact-infos__value contact-infos__value--link">
                            {{ email }}
                        </BaseLink>
                    </div>
                </div>

                <div v-if="phone" class="contact-infos__item">
                    <div class="contact-infos__icon">
                        <BaseIcon name="phone" :size="20" />
                    </div>
                    <div class="contact-infos__details">
                        <span class="contact-infos__label">{{ phoneTitle }}</span>
                        <BaseLink
                            :to="`tel:${phone.replace(/\s+/g, '')}`"
                            class="contact-infos__value contact-infos__value--link"
                        >
                            {{ phone }}
                        </BaseLink>
                    </div>
                </div>
            </div>

            <div v-if="socialLinks && socialLinks.length > 0" class="contact-infos__social">
                <h3 class="contact-infos__social-title">{{ socialTitle }}</h3>
                <div class="contact-infos__social-links">
                    <BaseLink
                        v-for="social in socialLinks"
                        :key="social.url"
                        :to="social.url"
                        :aria-label="social.name"
                        class="contact-infos__social-btn"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <BaseIcon :name="social.icon" :size="18" />
                        <span>{{ social.name }}</span>
                    </BaseLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';

    import type { ContactInfosProps } from '@/types/feature/contact';

    withDefaults(defineProps<ContactInfosProps>(), {
        title: 'Contactez-moi',
        subtitle: '',
        addressTitle: 'Localisation',
        emailTitle: 'Email',
        phoneTitle: 'Téléphone',
        socialTitle: 'Réseaux sociaux',
        address: 'Paris, France',
        email: 'contact@aitaddajuba.fr',
        phone: '+33 6 95 21 71 97',
        socialLinks: () => [
            {
                name: 'LinkedIn',
                icon: 'linkedin',
                url: 'https://www.linkedin.com/in/juba-aitadda/',
            },
            {
                name: 'GitHub',
                icon: 'github',
                url: 'https://github.com/jubskan3ki',
            },
        ],
    });
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .contact-infos {
        position: relative;
        height: 100%;
        width: 100%;
        padding: vars.$spacing-xl;
        border-radius: vars.$border-radius-xl;
        overflow: hidden;

        // Dark glassmorphism
        background: linear-gradient(
            135deg,
            vars.$primary-dark 0%,
            color.adjust(vars.$primary-dark, $lightness: -8%) 100%
        );
        box-shadow:
            0 20px 40px fn.color-alpha(vars.$black, 0.2),
            inset 0 1px 0 fn.color-alpha(vars.$white, 0.1);

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg;
        }

        // Decoration container
        &__decoration {
            position: absolute;
            inset: 0;
            overflow: hidden;
            pointer-events: none;
        }

        // Floating orbs
        &__orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);

            &--1 {
                width: 200px;
                height: 200px;
                background: vars.$primary-color;
                opacity: 0.15;
                top: -50px;
                right: -50px;
            }

            &--2 {
                width: 150px;
                height: 150px;
                background: vars.$secondary-color;
                opacity: 0.1;
                bottom: -30px;
                left: -30px;
            }
        }

        &__content {
            position: relative;
            z-index: 1;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        &__header {
            margin-bottom: vars.$spacing-xl;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$white;
            margin-bottom: vars.$spacing-xxs;
        }

        &__subtitle {
            color: fn.color-alpha(vars.$white, 0.7);
            margin: 0;
        }

        &__items {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-md;
            flex-grow: 1;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            padding: vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            background: fn.color-alpha(vars.$white, 0.05);
            border: 1px solid fn.color-alpha(vars.$white, 0.08);
            transition:
                background 0.3s ease,
                transform 0.3s ease,
                border-color 0.3s ease;

            &:hover {
                background: fn.color-alpha(vars.$white, 0.1);
                border-color: fn.color-alpha(vars.$white, 0.15);
                transform: translateX(4px);
            }
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: vars.$border-radius-md;
            background: fn.color-alpha(vars.$white, 0.1);
            color: vars.$white;
            flex-shrink: 0;
        }

        &__details {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        &__label {
            font-weight: vars.$font-weight-medium;
            color: fn.color-alpha(vars.$white, 0.5);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        &__value {
            color: vars.$white;

            &--link {
                text-decoration: none;
                transition: color 0.2s ease;

                &:hover {
                    color: vars.$secondary-color;
                }
            }
        }

        &__social {
            margin-top: vars.$spacing-xl;
            padding-top: vars.$spacing-lg;
            border-top: 1px solid fn.color-alpha(vars.$white, 0.1);
        }

        &__social-title {
            font-weight: vars.$font-weight-medium;
            color: fn.color-alpha(vars.$white, 0.6);
            margin-bottom: vars.$spacing-md;
        }

        &__social-links {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
        }

        &__social-btn {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-md;
            background: fn.color-alpha(vars.$white, 0.08);
            border: 1px solid fn.color-alpha(vars.$white, 0.1);
            color: vars.$white;
            font-weight: vars.$font-weight-medium;
            text-decoration: none;
            transition:
                background 0.3s ease,
                transform 0.3s ease,
                border-color 0.3s ease;

            &:hover {
                background: vars.$primary-color;
                border-color: vars.$primary-color;
                color: vars.$white;
                transform: translateY(-2px);
            }
        }
    }
</style>
