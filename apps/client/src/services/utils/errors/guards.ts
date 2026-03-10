import type { ApiError } from '@/types/api/common';

export function isApiError(error: unknown): error is ApiError {
    if (!error || typeof error !== 'object') {
        return false;
    }
    const e = error as Record<string, unknown>;
    return (
        typeof e.code === 'string'
        && typeof e.status === 'number'
        && typeof e.message === 'string'
        && typeof e.timestamp === 'number'
    );
}
