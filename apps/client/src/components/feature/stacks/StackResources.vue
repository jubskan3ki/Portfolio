<template>
    <div v-if="resources && resources.length > 0" class="stack-resources">
        <h2 class="stack-resources__heading">Ressources utiles</h2>
        <div class="stack-resources__list">
            <div v-for="resource in resources" :key="resource.url" class="stack-resources__item">
                <h3 class="stack-resources__item-title">
                    {{ resource.title }}
                </h3>
                <p class="stack-resources__item-description">
                    {{ resource.description }}
                </p>
                <BaseLink :to="resource.url" target="_blank" class="stack-resources__item-link">
                    <BaseIcon name="external-link" :size="14" />
                    <span>Consulter</span>
                </BaseLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';

    interface Resource {
        title: string;
        description: string;
        url: string;
    }

    interface Props {
        resources?: Resource[];
    }

    withDefaults(defineProps<Props>(), {
        resources: () => [],
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stack-resources {
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid fn.color-alpha(vars.$white, 0.8);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-xl;
        box-shadow:
            0 8px 32px fn.color-alpha(vars.$black, 0.06),
            0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-lg;
        }

        &__heading {
            position: relative;
            padding-bottom: vars.$spacing-xs;
            margin-bottom: vars.$spacing-md;
            color: vars.$primary-color;

            &::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 60px;
                height: 3px;
                background: linear-gradient(90deg, vars.$primary-color, vars.$secondary-color);
                border-radius: vars.$border-radius-full;
            }
        }

        &__list {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-md;
        }

        &__item {
            padding: vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            background: fn.color-alpha(vars.$primary-color, 0.04);
            border-left: 3px solid vars.$primary-color;
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.08);
            }
        }

        &__item-title {
            color: vars.$text-primary;
            font-weight: vars.$font-weight-semibold;
            margin-bottom: vars.$spacing-xxs;
        }

        &__item-description {
            margin-bottom: vars.$spacing-xs;
            color: vars.$text-secondary;
            line-height: 1.6;
        }

        &__item-link {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            color: vars.$primary-color;
            font-weight: vars.$font-weight-medium;
            text-decoration: none;
            transition: all 0.2s ease;

            &:hover {
                text-decoration: underline;
            }
        }
    }
</style>
