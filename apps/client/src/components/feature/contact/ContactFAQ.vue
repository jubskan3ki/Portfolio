<template>
    <section class="contact-faq" aria-labelledby="contact-faq-title">
        <div class="contact-faq__head">
            <span class="contact-faq__eyebrow">FAQ</span>
            <h2 id="contact-faq-title" class="contact-faq__title">Les réponses rapides</h2>
            <p class="contact-faq__subtitle">
                Les questions qui reviennent souvent avant nos échanges.
            </p>
        </div>

        <div class="contact-faq__list">
            <details
                v-for="(item, idx) in items"
                :key="idx"
                class="contact-faq__item"
                :name="group ? 'contact-faq' : undefined"
            >
                <summary class="contact-faq__question">
                    <span class="contact-faq__question-text">{{ item.question }}</span>
                    <span class="contact-faq__chevron" aria-hidden="true">
                        <BaseIcon name="chevron-down" :size="18" />
                    </span>
                </summary>
                <div class="contact-faq__answer">
                    <p>{{ item.answer }}</p>
                </div>
            </details>
        </div>
    </section>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { FaqItem } from '@/types/feature/contact';

    withDefaults(
        defineProps<{
            items: FaqItem[];
            // When true, only one item stays open at a time (exclusive accordion via `name` attr)
            group?: boolean;
        }>(),
        {
            group: true,
        },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .contact-faq {
        &__head {
            text-align: center;
            margin-bottom: vars.$spacing-xl;
        }

        &__eyebrow {
            display: inline-block;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: vars.$primary-color;
            margin-bottom: vars.$spacing-xs;
        }

        &__title {
            margin: 0 0 vars.$spacing-xs;
            color: vars.$text-primary;
        }

        &__subtitle {
            margin: 0;
            color: vars.$gray-dark;
        }

        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-sm;
            max-width: 760px;
            margin: 0 auto;
        }

        &__item {
            background: fn.color-alpha(vars.$white, 0.95);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.4);
            border-radius: vars.$border-radius-lg;
            overflow: hidden;
            transition: border-color vars.$transition-base, box-shadow vars.$transition-base;

            &[open] {
                border-color: fn.color-alpha(vars.$primary-color, 0.35);
                box-shadow: 0 4px 18px fn.color-alpha(vars.$primary-color, 0.08);
            }

            &[open] .contact-faq__chevron {
                transform: rotate(180deg);
            }
        }

        &__question {
            list-style: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-md vars.$spacing-lg;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;

            &::-webkit-details-marker {
                display: none;
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: -2px;
                border-radius: vars.$border-radius-lg;
            }
        }

        &__question-text {
            flex: 1;
        }

        &__chevron {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: vars.$primary-color;
            transition: transform vars.$transition-base;

            @media (prefers-reduced-motion: reduce) {
                transition: none;
            }
        }

        &__answer {
            padding: 0 vars.$spacing-lg vars.$spacing-lg;

            p {
                margin: 0;
                color: vars.$gray-dark;
                line-height: 1.75;
            }
        }
    }
</style>
