<!--
  StackTags.vue
  Composant pour afficher les tags associés à la technologie
-->
<template>
    <div v-if="tags && tags.length > 0" class="stack-tags">
        <h3 class="stack-tags__heading">
            <BaseIcon name="hash" :size="16" />
            Tags associés
        </h3>
        <div class="stack-tags__list">
            <div v-for="tag in tags" :key="tag as string" class="stack-tags__item">
                <BaseIcon name="code" :size="14" />
                <span>{{ tag }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    interface Props {
        tags?: string[];
    }

    withDefaults(defineProps<Props>(), {
        tags: () => [],
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stack-tags {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        &__heading {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;
        }

        &__list {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-xs;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xxs vars.$spacing-sm;
            background: fn.color-alpha(vars.$primary-color, 0.06);
            border-radius: vars.$border-radius-full;
            color: vars.$primary-color;
            font-weight: vars.$font-weight-medium;
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.12);
            }
        }
    }
</style>
