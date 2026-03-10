import { useEventListener } from '@vueuse/core';
import { ref, watch, onMounted } from 'vue';

import { dayjs } from '@/services/utils/date';

import { useCalendarGrid } from './useCalendarGrid';
import { useDateRangeSelection } from './useDateRangeSelection';

import type { DateRange } from '@/types/components/ui';
import type { Ref } from 'vue';

interface UseDateRangePickerOptions {
    model: Ref<DateRange>;
    availableDates: Ref<string[]>;
    minDays: Ref<number>;
    maxDays: Ref<number>;
    disabled: Ref<boolean>;
}

export function useDateRangePicker({ model, availableDates, minDays, maxDays, disabled }: UseDateRangePickerOptions) {
    const isOpen = ref(false);
    const dropdownRef = ref<HTMLElement | null>(null);

    const selection = useDateRangeSelection({ model, availableDates, minDays, maxDays });

    const grid = useCalendarGrid({
        tempStartDate: selection.tempStartDate,
        tempEndDate: selection.tempEndDate,
        hoverDate: selection.hoverDate,
        isDateAvailable: selection.isDateAvailable,
        isDateDisabled: selection.isDateDisabled,
    });

    const togglePicker = () => {
        if (disabled.value) {
            return;
        }
        isOpen.value = !isOpen.value;
        if (isOpen.value) {
            selection.syncFromModel();
            if (model.value.startDate) {
                grid.currentMonth.value = dayjs(model.value.startDate);
            } else if (selection.sortedAvailableDates.value.length > 0) {
                grid.currentMonth.value = dayjs(selection.sortedAvailableDates.value[0]);
            }
        }
    };

    const apply = () => {
        if (selection.applyToModel()) {
            isOpen.value = false;
        }
    };

    const cancel = () => {
        selection.resetTemp();
        isOpen.value = false;
    };

    const handleClickOutside = (event: MouseEvent) => {
        if (!isOpen.value) {
            return;
        }
        const target = event.target as HTMLElement;
        const triggerEl = target.closest('.date-range-picker__trigger');
        const dropdownEl = dropdownRef.value;
        if (!triggerEl && dropdownEl && !dropdownEl.contains(target)) {
            cancel();
        }
    };

    useEventListener(document, 'click', handleClickOutside);

    onMounted(() => {
        selection.initializeDefaultRange();
        if (model.value.startDate) {
            grid.currentMonth.value = dayjs(model.value.startDate);
        }
    });

    watch(
        () => availableDates.value,
        (newDates) => {
            if (newDates.length > 0) {
                selection.initializeDefaultRange();
            }
        },
        { immediate: true },
    );

    return {
        isOpen,
        dropdownRef,
        weekDays: grid.weekDays,
        displayValue: selection.displayValue,
        currentMonthYear: grid.currentMonthYear,
        calendarDays: grid.calendarDays,
        isValidSelection: selection.isValidSelection,
        togglePicker,
        previousMonth: grid.previousMonth,
        nextMonth: grid.nextMonth,
        selectDate: selection.selectDate,
        handleMouseEnter: selection.handleMouseEnter,
        apply,
        cancel,
    };
}
