<template>
    <nav class="search-filters" aria-label="Filtrer par type">
        <button
            v-for="group in groups"
            :key="group.type"
            type="button"
            class="search-filters__btn"
            :class="[`search-filters__btn--${group.type}`, { 'is-active': activeFilter === group.type }]"
            @click="$emit('toggle', group.type)"
        >
            <BaseIcon :name="group.icon" :size="14" />
            <span>{{ group.label }}</span>
            <small>{{ group.count }}</small>
        </button>
    </nav>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    interface FilterGroup {
        type: string;
        label: string;
        icon: string;
        count: number;
    }

    interface Props {
        groups: FilterGroup[];
        activeFilter: string | null;
    }

    defineProps<Props>();

    defineEmits<{
        toggle: [type: string];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/mixins' as m;
    @use '@/styles/abstracts/functions' as fn;

    $type-colors: (
        article: v.$info-color,
        project: v.$success-color,
        stack: v.$secondary-color,
        experience: v.$warning-color,
    );

    .search-filters {
        display: flex;
        align-items: center;
        gap: v.$spacing-xxs;
        padding: v.$spacing-xs;
        background: v.$bg-secondary;
        border-bottom: 1px solid v.$border-color;

        @include m.hide-scrollbar;

        &__btn {
            display: flex;
            align-items: center;
            gap: v.$spacing-xxxs;
            padding: v.$spacing-xxxs v.$spacing-xxs;
            border: none;
            border-radius: v.$border-radius-md;
            background: transparent;
            color: v.$text-secondary;
            font-weight: v.$font-weight-medium;
            font-family: inherit;
            white-space: nowrap;
            cursor: pointer;
            transition: all v.$transition-fast;

            small {
                display: flex;
                align-items: center;
                justify-content: center;
                min-width: 18px;
                height: 18px;
                padding: 0 v.$spacing-xxs;
                border-radius: v.$border-radius-full;
                background: fn.color-alpha(v.$black, 0.06);
                font-weight: v.$font-weight-semibold;
            }

            &:hover {
                background: v.$white;
                color: v.$text-primary;
            }

            &.is-active {
                background: v.$white;
                color: v.$primary-color;
                box-shadow: v.$box-shadow-xs;

                small {
                    background: fn.color-alpha(v.$primary-color, 0.12);
                    color: v.$primary-color;
                }
            }

            @each $type, $color in $type-colors {
                &--#{$type}.is-active {
                    color: $color;

                    small {
                        background: fn.color-alpha($color, 0.12);
                        color: $color;
                    }
                }
            }
        }
    }
</style>
