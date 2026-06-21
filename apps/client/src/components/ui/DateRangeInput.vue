<template>
    <div
        class="date-range-picker__trigger"
        role="button"
        tabindex="0"
        aria-haspopup="dialog"
        :aria-expanded="isOpen"
        @click="$emit('toggle')"
        @keydown.enter="$emit('toggle')"
        @keydown.space.prevent="$emit('toggle')"
    >
        <BaseIcon name="calendar" :size="16" class="date-range-picker__icon" />
        <span v-if="displayValue" class="date-range-picker__value">{{ displayValue }}</span>
        <span v-else class="date-range-picker__placeholder">Sélectionner une période</span>
        <BaseIcon name="chevron-down" :size="14" class="date-range-picker__arrow" :class="{ active: isOpen }" />
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { DateRangeInputProps } from '@/types/components/ui';

    defineProps<DateRangeInputProps>();

    defineEmits<{
        toggle: [];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/abstracts/mixins' as mix;

    .date-range-picker {
        &__trigger {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-sm;
            background: vars.$white;
            border: 1px solid func.color-alpha(vars.$black, 0.08);
            border-radius: vars.$border-radius-md;
            cursor: pointer;
            transition:
                border-color vars.$transition-fast,
                box-shadow vars.$transition-fast,
                background-color vars.$transition-fast;

            &:hover {
                border-color: func.color-alpha(vars.$black, 0.12);
                background-color: vars.$bg-secondary;
            }

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xxs vars.$spacing-xs;
            }
        }

        &__icon {
            color: vars.$text-muted;
            flex-shrink: 0;
        }

        &__value {
            flex: 1;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__placeholder {
            flex: 1;
            color: vars.$text-muted;
        }

        &__arrow {
            color: vars.$text-muted;
            transition: transform vars.$transition-fast;

            &.active {
                transform: rotate(180deg);
            }
        }
    }
</style>
