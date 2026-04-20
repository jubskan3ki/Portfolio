<!--
  StackRelated.vue
  Composant pour afficher les technologies similaires
-->
<template>
    <div v-if="stacks && stacks.length > 0" class="stack-related">
        <h3 class="stack-related__heading">Stacks similaires</h3>
        <div class="stack-related__list">
            <BaseLink
                v-for="stack in stacks"
                :key="stack.slug"
                :to="`/stacks/${stack.slug}`"
                class="stack-related__item"
            >
                <BaseImage
                    :src="stack.logo"
                    :alt="stack.name"
                    :width="40"
                    :height="40"
                    :show-placeholder="false"
                    class="stack-related__logo"
                />
                <div class="stack-related__info">
                    <span class="stack-related__name">{{ stack.name }}</span>
                    <small class="stack-related__category">{{ stack.category }}</small>
                </div>
            </BaseLink>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseLink from '@/components/base/BaseLink.vue';

    import type { StackRelatedProps } from '@/types/feature/stacks';

    withDefaults(defineProps<StackRelatedProps>(), {
        stacks: () => [],
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stack-related {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        &__heading {
            margin-bottom: vars.$spacing-md;
            color: vars.$primary-color;
            font-weight: vars.$font-weight-semibold;
            padding-bottom: vars.$spacing-xxs;
            border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.3);
        }

        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxs;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-xs;
            text-decoration: none;
            border-radius: vars.$border-radius-md;
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.06);
                transform: translateX(4px);

                .stack-related__name {
                    color: vars.$primary-color;
                }
            }
        }

        &__logo {
            width: 40px;
            height: 40px;
            object-fit: contain;
            flex-shrink: 0;
        }

        &__info {
            display: flex;
            flex-direction: column;
        }

        &__name {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            transition: color 0.2s ease;
        }

        &__category {
            color: vars.$text-muted;
            font-size: vars.$font-size-sm;
        }
    }
</style>
