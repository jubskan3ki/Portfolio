import { computed, ref } from 'vue';

import { dayjs } from '@/services/utils/date';

import type { CalendarDay } from '@/types/components/ui';
import type { Ref } from 'vue';

interface UseCalendarGridOptions {
    tempStartDate: Ref<string>;
    tempEndDate: Ref<string>;
    hoverDate: Ref<string>;
    isDateAvailable: (date: string) => boolean;
    isDateDisabled: (date: string) => boolean;
}

export function useCalendarGrid(options: UseCalendarGridOptions) {
    const { tempStartDate, tempEndDate, hoverDate, isDateAvailable, isDateDisabled } = options;

    const currentMonth = ref(dayjs());
    const weekDays = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

    const currentMonthYear = computed(() => currentMonth.value.format('MMMM YYYY'));

    const calendarDays = computed((): CalendarDay[] => {
        const days: CalendarDay[] = [];
        const startOfMonth = currentMonth.value.startOf('month');
        const endOfMonth = currentMonth.value.endOf('month');
        const startDay = startOfMonth.day() === 0 ? 6 : startOfMonth.day() - 1;
        const today = dayjs().format('YYYY-MM-DD');

        // Previous month padding
        for (let i = startDay - 1; i >= 0; i--) {
            const date = startOfMonth.subtract(i + 1, 'day');
            const dateStr = date.format('YYYY-MM-DD');
            days.push({
                day: date.date(),
                date: dateStr,
                isCurrentMonth: false,
                isAvailable: false,
                isDisabled: true,
                isSelected: false,
                isInRange: false,
                isRangeStart: false,
                isRangeEnd: false,
                isToday: false,
            });
        }

        // Current month days
        const daysInMonth = endOfMonth.date();
        for (let i = 1; i <= daysInMonth; i++) {
            const date = startOfMonth.date(i);
            const dateStr = date.format('YYYY-MM-DD');
            const available = isDateAvailable(dateStr);
            const disabledDay = isDateDisabled(dateStr);
            const start = tempStartDate.value ? dayjs(tempStartDate.value) : null;
            let end = tempEndDate.value ? dayjs(tempEndDate.value) : null;
            if (!end && hoverDate.value && tempStartDate.value) {
                end = dayjs(hoverDate.value);
            }

            let isInRange = false;
            let isRangeStart = false;
            let isRangeEnd = false;
            if (start && end && end.isAfter(start)) {
                isInRange = date.isAfter(start, 'day') && date.isBefore(end, 'day');
                isRangeStart = date.isSame(start, 'day');
                isRangeEnd = date.isSame(end, 'day');
            }

            days.push({
                day: i,
                date: dateStr,
                isCurrentMonth: true,
                isAvailable: available,
                isDisabled: disabledDay,
                isSelected: dateStr === tempStartDate.value || dateStr === tempEndDate.value,
                isInRange,
                isRangeStart,
                isRangeEnd,
                isToday: dateStr === today,
            });
        }

        // Next month padding (fill to 42 = 6 rows)
        const remainingDays = 42 - days.length;
        for (let i = 1; i <= remainingDays; i++) {
            const date = endOfMonth.add(i, 'day');
            const dateStr = date.format('YYYY-MM-DD');
            days.push({
                day: date.date(),
                date: dateStr,
                isCurrentMonth: false,
                isAvailable: false,
                isDisabled: true,
                isSelected: false,
                isInRange: false,
                isRangeStart: false,
                isRangeEnd: false,
                isToday: false,
            });
        }

        return days;
    });

    const previousMonth = () => {
        currentMonth.value = currentMonth.value.subtract(1, 'month');
    };

    const nextMonth = () => {
        currentMonth.value = currentMonth.value.add(1, 'month');
    };

    return {
        currentMonth,
        weekDays,
        currentMonthYear,
        calendarDays,
        previousMonth,
        nextMonth,
    };
}
