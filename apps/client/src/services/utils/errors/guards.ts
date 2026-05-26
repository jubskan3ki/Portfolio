import type { ApiError } from '@/types/api/common';

export function isApiError(error: unknown): error is ApiError {
    if (!error || typeof error !== 'object') {
        return false;
    }
    const e = error as Record<string, unknown>;
    return (
        typeof e.code === 'string' &&
        typeof e.status === 'number' &&
        typeof e.message === 'string' &&
        typeof e.timestamp === 'number'
    );
}

// Walks an error and its `cause` chain (Nuxt wraps thrown values in H3Error)
// to find an HTTP status code. Returns undefined if none is discoverable.
export function extractErrorStatus(error: unknown): number | undefined {
    let current: unknown = error;
    let depth = 0;
    while (current && typeof current === 'object' && depth < 5) {
        const e = current as Record<string, unknown>;
        if (typeof e.status === 'number') {
            return e.status;
        }
        if (typeof e.statusCode === 'number') {
            return e.statusCode;
        }
        current = e.cause;
        depth += 1;
    }
    return undefined;
}
