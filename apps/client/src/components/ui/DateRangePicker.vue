<template>
    <div class="date-range-picker">
        <DateRangeInput :display-value="displayValue" :is-open="isOpen" :disabled="disabled" @toggle="togglePicker" />

        <Transition name="dropdown">
            <div v-if="isOpen" ref="dropdownRef" class="date-range-picker__dropdown">
                <DateRangeCalendar
                    :current-month-year="currentMonthYear"
                    :week-days="weekDays"
                    :calendar-days="calendarDays"
                    :is-valid-selection="isValidSelection"
                    @previous-month="previousMonth"
                    @next-month="nextMonth"
                    @select-date="selectDate"
                    @mouse-enter-date="handleMouseEnter"
                    @cancel="cancel"
                    @apply="apply"
                />
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import DateRangeCalendar from '@/components/ui/DateRangeCalendar.vue';
    import DateRangeInput from '@/components/ui/DateRangeInput.vue';
    import { useDateRangePicker } from '@/composables/ui/useDateRangePicker';

    import type { DateRange, DateRangeSelectorProps } from '@/types/components/ui';

    const props = withDefaults(defineProps<DateRangeSelectorProps>(), {
        availableDates: () => [],
        minDays: 7,
        maxDays: 14,
        disabled: false,
    });

    const model = defineModel<DateRange>({
        default: () => ({
            startDate: '',
            endDate: '',
        }),
    });

    const dropdownRef = useTemplateRef<HTMLElement>('dropdownRef');

    const {
        isOpen,
        weekDays,
        displayValue,
        currentMonthYear,
        calendarDays,
        isValidSelection,
        togglePicker,
        previousMonth,
        nextMonth,
        selectDate,
        handleMouseEnter,
        apply,
        cancel,
    } = useDateRangePicker({
        model,
        availableDates: computed(() => props.availableDates ?? []),
        minDays: computed(() => props.minDays ?? 7),
        maxDays: computed(() => props.maxDays ?? 14),
        disabled: computed(() => props.disabled ?? false),
        dropdownRef,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/abstracts/mixins' as mix;

    .date-range-picker {
        position: relative;
        width: 100%;
        max-width: 320px;

        @include mix.responsive(mobile) {
            max-width: 100%;
        }

        &__dropdown {
            position: absolute;
            top: calc(100% + vars.$spacing-xxxs);
            left: 0;
            background: vars.$white;
            border: 1px solid func.color-alpha(vars.$black, 0.08);
            border-radius: vars.$border-radius-lg;
            box-shadow: 0 8px 24px func.color-alpha(vars.$black, 0.12);
            padding: vars.$spacing-md;
            z-index: vars.$z-index-dropdown;
            min-width: 320px;

            @include mix.responsive(mobile) {
                left: 50%;
                transform: translateX(-50%);
                min-width: 280px;
                padding: vars.$spacing-sm;
            }
        }
    }

    .dropdown-enter-active,
    .dropdown-leave-active {
        transition: all 0.2s ease;
    }

    .dropdown-enter-from,
    .dropdown-leave-to {
        opacity: 0;
        transform: translateY(-8px);
    }
</style>
