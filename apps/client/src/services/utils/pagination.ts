import { computed, type ComputedRef, type Ref } from 'vue';

// Ordre de résolution: data -> results -> fallbackKeys -> tableau brut
export function extractPaginatedData<T>(response: unknown, fallbackKeys?: string[]): T[] {
    if (!response) {
        return [];
    }

    if (response && typeof response === 'object' && 'data' in response) {
        const data = (response as { data: unknown }).data;
        return Array.isArray(data) ? (data as T[]) : [];
    }

    if (response && typeof response === 'object' && 'results' in response) {
        const results = (response as { results: unknown }).results;
        return Array.isArray(results) ? (results as T[]) : [];
    }

    if (fallbackKeys && response && typeof response === 'object') {
        for (const key of fallbackKeys) {
            if (key in response && Array.isArray((response as Record<string, unknown>)[key])) {
                return (response as Record<string, T[]>)[key] ?? [];
            }
        }
    }

    return Array.isArray(response) ? response : [];
}

export function usePaginatedData<T>(dataRef: Ref<unknown>, fallbackKeys?: string[]): ComputedRef<T[]> {
    return computed(() => extractPaginatedData<T>(dataRef.value, fallbackKeys));
}
