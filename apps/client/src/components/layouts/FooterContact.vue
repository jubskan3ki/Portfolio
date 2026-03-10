<template>
    <section class="footer-contact" aria-labelledby="contact-heading">
        <SectionHeading :id="headingId" :title="title" />

        <address class="footer-contact__list">
            <FooterContactItem
                v-if="email"
                icon="mail"
                :text="email"
                is-link
                link-type="email"
            />
            <FooterContactItem
                v-if="phone"
                icon="phone"
                :text="phone"
                is-link
                link-type="phone"
            />
            <FooterContactItem v-if="address" icon="map-pin" :text="address" />
        </address>

        <div class="footer-contact__availability" role="status" :aria-label="availabilityText">
            <span class="footer-contact__indicator footer-contact__indicator--available" aria-hidden="true"></span>
            <small>{{ availabilityText }}</small>
        </div>
    </section>
</template>

<script setup lang="ts">
    import FooterContactItem from '@/components/layouts/FooterContactItem.vue';
    import SectionHeading from '@/components/ui/SectionHeading.vue';

    import type { FooterContactProps } from '@/types/components/layouts';

    withDefaults(defineProps<FooterContactProps>(), {
        title: 'Contact',
        email: '',
        phone: '',
        address: '',
    });

    const headingId = 'footer-contact-heading';

    const availabilityText = 'Disponible pour de nouveaux projets';
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .footer-contact {
        display: flex;
        flex-direction: column;

        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
            margin-bottom: vars.$spacing-md;
            font-style: normal;
        }

        &__availability {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin-top: vars.$spacing-xs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            border-radius: vars.$border-radius-md;

            @include mix.glass(12px, func.color-alpha(vars.$white, 0.6));

            border: 1px solid func.color-alpha(vars.$primary-color, 0.08);
            width: fit-content;
        }

        &__indicator {
            width: 8px;
            height: 8px;
            border-radius: vars.$border-radius-full;
            background-color: vars.$gray;
            flex-shrink: 0;

            &--available {
                background-color: vars.$success-color;
                animation: pulse 2s ease-in-out infinite;
            }
        }
    }

    @keyframes pulse {
        0%,
        100% {
            box-shadow: 0 0 0 0 func.color-alpha(vars.$success-color, 0.5);
        }

        50% {
            box-shadow: 0 0 0 6px func.color-alpha(vars.$success-color, 0);
        }
    }
</style>
