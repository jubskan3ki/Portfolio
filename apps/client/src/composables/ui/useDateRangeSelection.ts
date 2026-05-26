import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import { computed, ref } from 'vue';

import { dayjs } from '@/services/utils/date';

import type { UseDateRangeSelectionOptions } from '@/types/composables/ui';

dayjs.extend(isSameOrAfter);

export function useDateRangeSelection({ model, availableDates, minDays, maxDays }: UseDateRangeSelectionOptions) {
    const tempStartDate = ref('');
    const tempEndDate = ref('');
    const hoverDate = ref('');

    const availableDatesSet = computed(() => new Set(availableDates.value));

    const sortedAvailableDates = computed(() =>
        [...availableDates.value].sort((a, b) => dayjs(a).valueOf() - dayjs(b).valueOf()),
    );

    const isDateAvailable = (date: string): boolean => availableDatesSet.value.has(date);

    const isDateDisabled = (date: string): boolean => {
        if (!isDateAvailable(date)) {
            return true;
        }
        const d = dayjs(date);
        if (tempStartDate.value && !tempEndDate.value) {
            const start = dayjs(tempStartDate.value);
            return (
                d.isBefore(start.add(minDays.value, 'day'), 'day') || d.isAfter(start.add(maxDays.value, 'day'), 'day')
            );
        }
        if (tempEndDate.value && !tempStartDate.value) {
            const end = dayjs(tempEndDate.value);
            return (
                d.isAfter(end.subtract(minDays.value, 'day'), 'day') ||
                d.isBefore(end.subtract(maxDays.value, 'day'), 'day')
            );
        }
        return false;
    };

    const isValidSelection = computed(() => {
        if (!tempStartDate.value || !tempEndDate.value) {
            return false;
        }
        const diff = dayjs(tempEndDate.value).diff(dayjs(tempStartDate.value), 'day');
        return diff >= minDays.value && diff <= maxDays.value;
    });

    const displayValue = computed(() => {
        if (!model.value.startDate || !model.value.endDate) {
            return '';
        }
        return `${dayjs(model.value.startDate).format('DD/MM/YYYY')} - ${dayjs(model.value.endDate).format('DD/MM/YYYY')}`;
    });

    const selectDate = (date: string) => {
        if (!isDateAvailable(date) || isDateDisabled(date)) {
            return;
        }
        if (!tempStartDate.value) {
            tempStartDate.value = date;
            tempEndDate.value = '';
            return;
        }
        if (tempStartDate.value && !tempEndDate.value) {
            const start = dayjs(tempStartDate.value);
            const selected = dayjs(date);
            if (selected.isBefore(start, 'day')) {
                const oldStart = tempStartDate.value;
                tempStartDate.value = date;
                tempEndDate.value = oldStart;
            } else {
                const diff = selected.diff(start, 'day');
                if (diff >= minDays.value && diff <= maxDays.value) {
                    tempEndDate.value = date;
                }
            }
            return;
        }
        if (tempStartDate.value && tempEndDate.value) {
            tempStartDate.value = date;
            tempEndDate.value = '';
        }
    };

    const handleMouseEnter = (date: string) => {
        if (tempStartDate.value && !tempEndDate.value && isDateAvailable(date) && !isDateDisabled(date)) {
            hoverDate.value = date;
        }
    };

    const initializeDefaultRange = () => {
        if (sortedAvailableDates.value.length === 0) {
            return;
        }
        const lastDate = sortedAvailableDates.value[sortedAvailableDates.value.length - 1];
        const targetStartDate = dayjs(lastDate).subtract(minDays.value, 'day').format('YYYY-MM-DD');
        const startDate =
            sortedAvailableDates.value.find((date) => dayjs(date).isSameOrAfter(dayjs(targetStartDate), 'day')) ||
            sortedAvailableDates.value[0];
        const endDate = lastDate;
        if (!startDate || !endDate) {
            return;
        }
        model.value = { startDate, endDate };
    };

    const syncFromModel = () => {
        tempStartDate.value = model.value.startDate;
        tempEndDate.value = model.value.endDate;
    };

    const applyToModel = () => {
        if (!isValidSelection.value || !tempStartDate.value || !tempEndDate.value) {
            return false;
        }
        model.value = { startDate: tempStartDate.value, endDate: tempEndDate.value };
        hoverDate.value = '';
        return true;
    };

    const resetTemp = () => {
        tempStartDate.value = model.value.startDate;
        tempEndDate.value = model.value.endDate;
        hoverDate.value = '';
    };

    return {
        tempStartDate,
        tempEndDate,
        hoverDate,
        availableDatesSet,
        sortedAvailableDates,
        displayValue,
        isValidSelection,
        isDateAvailable,
        isDateDisabled,
        selectDate,
        handleMouseEnter,
        initializeDefaultRange,
        syncFromModel,
        applyToModel,
        resetTemp,
    };
}
