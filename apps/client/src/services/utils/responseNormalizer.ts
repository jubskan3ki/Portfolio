// src/services/utils/responseNormalizer.ts
// Unified response normalization for API responses

import type { PaginationMeta } from '@/types/composables/data';

function snakeToCamel(str: string): string {
    return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function camelToSnake(str: string): string {
    return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

// Convert snake_case keys to camelCase recursively
export function transformKeysToCamel<T>(obj: unknown): T {
    if (obj === null || obj === undefined) {
        return obj as T;
    }

    if (Array.isArray(obj)) {
        return obj.map((item) => transformKeysToCamel(item)) as T;
    }

    if (typeof obj === 'object') {
        const result: Record<string, unknown> = {};
        for (const [key, value] of Object.entries(obj)) {
            const camelKey = snakeToCamel(key);
            result[camelKey] = transformKeysToCamel(value);
        }
        return result as T;
    }

    return obj as T;
}

// Convert camelCase keys to snake_case recursively
export function transformKeysToSnake<T>(obj: unknown): T {
    if (obj === null || obj === undefined) {
        return obj as T;
    }

    if (Array.isArray(obj)) {
        return obj.map((item) => transformKeysToSnake(item)) as T;
    }

    if (typeof obj === 'object') {
        const result: Record<string, unknown> = {};
        for (const [key, value] of Object.entries(obj)) {
            const snakeKey = camelToSnake(key);
            result[snakeKey] = transformKeysToSnake(value);
        }
        return result as T;
    }

    return obj as T;
}

export type { PaginationMeta };

export interface NormalizedPaginatedData<T> {
    data: T[];
    pagination: PaginationMeta;
}

// Normalize array responses from various formats
function normalizeArrayResponse<T>(response: unknown): T[] {
    if (!response) {
        return [];
    }

    // Direct array
    if (Array.isArray(response)) {
        return response;
    }

    // Object response
    if (typeof response === 'object' && response !== null) {
        const obj = response as Record<string, unknown>;

        // { data: T[] }
        if ('data' in obj && Array.isArray(obj.data)) {
            return obj.data;
        }

        // { results: T[] } (Django REST Framework)
        if ('results' in obj && Array.isArray(obj.results)) {
            return obj.results;
        }

        // { items: T[] }
        if ('items' in obj && Array.isArray(obj.items)) {
            return obj.items;
        }

        // Single object (wrap in array)
        if ('id' in obj || 'slug' in obj) {
            return [obj as T];
        }
    }

    return [];
}

// Normalize paginated responses from various formats
export function normalizePaginatedResponse<T>(response: unknown, defaultPageSize = 10): NormalizedPaginatedData<T> {
    const emptyResult: NormalizedPaginatedData<T> = {
        data: [],
        pagination: {
            page: 1,
            pageSize: defaultPageSize,
            totalCount: 0,
            totalPages: 0,
            hasNext: false,
            hasPrevious: false,
        },
    };

    if (!response) {
        return emptyResult;
    }

    // Direct array (no pagination)
    if (Array.isArray(response)) {
        return {
            data: response,
            pagination: {
                page: 1,
                pageSize: response.length,
                totalCount: response.length,
                totalPages: 1,
                hasNext: false,
                hasPrevious: false,
            },
        };
    }

    if (typeof response !== 'object' || response === null) {
        return emptyResult;
    }

    const obj = response as Record<string, unknown>;

    // Extract data array
    const data = normalizeArrayResponse<T>(response);

    // Django REST Framework format: { count, next, previous, results }
    if ('count' in obj && 'results' in obj) {
        const count = Number(obj.count) || 0;
        const pageSize = data.length || defaultPageSize;
        const totalPages = Math.ceil(count / pageSize);

        // Try to extract current page from next/previous URLs
        let page = 1;
        const next = obj.next as string | null;
        const previous = obj.previous as string | null;

        if (next) {
            const match = next.match(/[?&]page=(\d+)/);
            if (match) {
                page = Number(match[1]) - 1;
            }
        } else if (previous) {
            const match = previous.match(/[?&]page=(\d+)/);
            if (match) {
                page = Number(match[1]) + 1;
            }
        }

        return {
            data,
            pagination: {
                page,
                pageSize,
                totalCount: count,
                totalPages,
                hasNext: !!next,
                hasPrevious: !!previous,
            },
        };
    }

    // Custom format with pagination object
    if ('pagination' in obj && typeof obj.pagination === 'object') {
        const pag = obj.pagination as Record<string, unknown>;

        return {
            data,
            pagination: {
                page: Number(pag.page ?? pag.current_page ?? 1),
                pageSize: Number(pag.pageSize ?? pag.page_size ?? pag.per_page ?? defaultPageSize),
                totalCount: Number(pag.totalCount ?? pag.total_count ?? pag.total ?? 0),
                totalPages: Number(pag.totalPages ?? pag.total_pages ?? pag.last_page ?? 1),
                hasNext: Boolean(pag.hasNext ?? pag.has_next ?? pag.next_page),
                hasPrevious: Boolean(pag.hasPrevious ?? pag.has_previous ?? pag.prev_page),
            },
        };
    }

    // Simple format with top-level pagination fields
    if ('total' in obj || 'total_count' in obj) {
        const total = Number(obj.total ?? obj.total_count ?? obj.count ?? 0);
        const page = Number(obj.page ?? obj.current_page ?? 1);
        const pageSize = Number(obj.page_size ?? obj.pageSize ?? obj.per_page ?? defaultPageSize);
        const totalPages = Math.ceil(total / pageSize);

        return {
            data,
            pagination: {
                page,
                pageSize,
                totalCount: total,
                totalPages,
                hasNext: page < totalPages,
                hasPrevious: page > 1,
            },
        };
    }

    // No pagination info - return data as single page
    return {
        data,
        pagination: {
            page: 1,
            pageSize: data.length || defaultPageSize,
            totalCount: data.length,
            totalPages: 1,
            hasNext: false,
            hasPrevious: false,
        },
    };
}
