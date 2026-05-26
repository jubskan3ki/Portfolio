import dayjs from 'dayjs';
import 'dayjs/locale/fr';
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);
dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);
dayjs.locale('fr');

type DateInput = string | Date | null | undefined;

export function formatDate(date: DateInput, format = 'DD/MM/YYYY'): string {
    if (!date) {
        return '';
    }
    return dayjs(date).format(format);
}

export function formatDateShort(date: DateInput): string {
    if (!date) {
        return '';
    }
    return dayjs(date).format('DD/MM/YYYY');
}

export function formatRelativeDate(date: DateInput): string {
    if (!date) {
        return '';
    }

    const now = dayjs();
    const d = dayjs(date);
    const diffMinutes = now.diff(d, 'minute');
    const diffHours = now.diff(d, 'hour');
    const diffDays = now.diff(d, 'day');

    if (diffMinutes < 1) {
        return "À l'instant";
    }
    if (diffMinutes < 60) {
        return `Il y a ${diffMinutes} min`;
    }
    if (diffHours < 24) {
        return `Il y a ${diffHours}h`;
    }
    if (diffDays < 7) {
        return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
    }

    const format = d.year() !== now.year() ? 'D MMM YYYY' : 'D MMM';
    return d.format(format);
}

export function formatDateRange(startDate: DateInput, endDate: DateInput): string {
    if (!startDate) {
        return '';
    }

    const start = dayjs(startDate).format('MMM YYYY');
    const end = endDate ? dayjs(endDate).format('MMM YYYY') : 'Présent';
    return `${start} - ${end}`;
}

export { dayjs };
