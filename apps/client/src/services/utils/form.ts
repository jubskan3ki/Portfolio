import { getBaseUrl } from '@/services/api/core';

import type { SelectOption } from '@/types/composables/forms';

export function toSelectOptions<T extends { id: number | string; name: string }>(
    items: T[],
    options?: { valueKey?: keyof T; labelKey?: keyof T; imageKey?: keyof T },
): SelectOption[] {
    const { valueKey = 'id', labelKey = 'name', imageKey } = options || {};
    return items.map((item) => ({
        value: item[valueKey] as number | string,
        label: String(item[labelKey]),
        ...(imageKey && item[imageKey] ? { image: String(item[imageKey]) } : {}),
    }));
}

export function findItemByIdOrName<T extends { id: number | string; name?: string; slug?: string }>(
    items: T[],
    value: unknown,
): T | undefined {
    if (!value) {
        return undefined;
    }

    if (typeof value === 'object' && value !== null && 'id' in value) {
        const id = (value as { id: number | string }).id;
        return items.find((item) => item.id === id);
    }

    if (typeof value === 'number') {
        return items.find((item) => item.id === value);
    }

    if (typeof value === 'string') {
        return items.find((item) => item.name === value || item.slug === value || String(item.id) === value);
    }

    return undefined;
}

export function mapToIds<T extends { id: number | string; name?: string }>(rawValues: unknown[], items: T[]): number[] {
    return rawValues
        .map((raw) => {
            if (typeof raw === 'object' && raw !== null && 'id' in raw) {
                return (raw as { id: number }).id;
            }
            if (typeof raw === 'string') {
                const match = items.find((item) => item.name === raw);
                return match?.id as number | undefined;
            }
            if (typeof raw === 'number') {
                return raw;
            }
            return undefined;
        })
        .filter((id): id is number => typeof id === 'number');
}

export function buildImageUrl(path: string | undefined | null, baseUrl?: string): string {
    if (!path) {
        return '';
    }
    if (path.startsWith('http')) {
        return path;
    }
    return `${baseUrl || getBaseUrl()}${path}`;
}
