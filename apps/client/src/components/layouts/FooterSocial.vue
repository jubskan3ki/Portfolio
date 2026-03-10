<template>
    <section class="footer-social" aria-labelledby="social-heading">
        <SectionHeading :id="headingId" :title="title" />

        <ul class="footer-social__list" role="list">
            <li v-for="social in links" :key="social.name" class="footer-social__item">
                <NuxtLink
                    :to="social.url"
                    external
                    target="_blank"
                    class="footer-social__link"
                    :aria-label="`Suivre sur ${social.name}`"
                >
                    <BaseIcon :name="social.icon" :size="20" aria-hidden="true" />
                    <span class="footer-social__name">{{ social.name }}</span>
                </NuxtLink>
            </li>
        </ul>
    </section>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SectionHeading from '@/components/ui/SectionHeading.vue';

    import type { FooterSocialProps } from '@/types/components/layouts';

    withDefaults(defineProps<FooterSocialProps>(), {
        title: 'Suivez-moi',
    });

    const headingId = 'footer-social-heading';
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .footer-social {
        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
            list-style: none;
            padding: 0;
            margin: 0;
        }

        &__item {
            margin: 0;
        }

        &__link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            color: vars.$text-secondary;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-md;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            @include mix.glass(12px, func.color-alpha(vars.$white, 0.7));

            border: 1px solid func.color-alpha(vars.$primary-color, 0.06);

            &:hover {
                background: vars.$primary-color;
                border-color: vars.$primary-color;
                color: vars.$white;
                transform: translateY(-3px);
                box-shadow: 0 8px 24px func.color-alpha(vars.$primary-color, 0.25);

                :deep(svg) {
                    transform: scale(1.1);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 3px;
            }

            &:active {
                transform: translateY(-1px) scale(0.98);
            }

            :deep(svg) {
                transition: transform 0.3s ease;
            }
        }

        &__name {
            font-weight: vars.$font-weight-medium;
        }
    }
</style>
