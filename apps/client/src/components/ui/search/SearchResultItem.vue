<template>
    <li
        class="search-result"
        :class="[`search-result--${type}`, { 'is-selected': isSelected }]"
        role="option"
        tabindex="-1"
        :aria-selected="isSelected"
        @mouseenter="$emit('hover')"
    >
        <NuxtLink :to="link" class="search-result__link" @click="$emit('select')">
            <span class="search-result__icon">
                <BaseIcon :name="icon" :size="18" />
            </span>
            <span class="search-result__content">
                <strong>{{ title }}</strong>
                <small v-if="subtitle">{{ subtitle }}</small>
            </span>
            <small class="search-result__badge">{{ badgeLabel }}</small>
            <BaseIcon name="arrow-right" :size="14" class="search-result__arrow" />
        </NuxtLink>
    </li>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    interface Props {
        link: string;
        icon: string;
        title: string;
        subtitle?: string;
        type: string;
        badgeLabel: string;
        isSelected?: boolean;
    }

    withDefaults(defineProps<Props>(), {
        subtitle: '',
        isSelected: false,
    });

    defineEmits<{
        hover: [];
        select: [];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/functions' as fn;

    $type-colors: (
        article: v.$info-color,
        project: v.$success-color,
        stack: v.$secondary-color,
        experience: v.$warning-color,
    );

    .search-result {
        border-radius: v.$border-radius-md;
        transition: background-color v.$transition-fast;

        &:hover,
        &.is-selected {
            .search-result__arrow {
                opacity: 1;
                transform: translateX(0);
            }
        }

        &.is-selected {
            background: fn.color-alpha(v.$primary-color, 0.06);
        }

        @each $type, $color in $type-colors {
            &--#{$type} {
                .search-result__icon {
                    background: fn.color-alpha($color, 0.1);
                    color: $color;
                }

                .search-result__badge {
                    background: fn.color-alpha($color, 0.1);
                    color: $color;
                }

                &:hover,
                &.is-selected {
                    background: fn.color-alpha($color, 0.06);
                }
            }
        }

        &__link {
            display: flex;
            align-items: center;
            gap: v.$spacing-sm;
            padding: v.$spacing-xs v.$spacing-sm;
            text-decoration: none;
            color: inherit;
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: v.$border-radius-md;
            flex-shrink: 0;
        }

        &__content {
            display: flex;
            flex-direction: column;
            gap: 2px;
            flex: 1;
            min-width: 0;

            strong {
                font-weight: v.$font-weight-medium;
                color: v.$text-primary;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            small {
                color: v.$text-muted;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        }

        &__badge {
            padding: v.$spacing-xxxs v.$spacing-xs;
            border-radius: v.$border-radius-full;
            font-weight: v.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: v.$letter-spacing-base;
            flex-shrink: 0;
        }

        &__arrow {
            color: v.$text-muted;
            opacity: 0;
            transform: translateX(-4px);
            transition: all v.$transition-fast;
        }
    }
</style>
