import type { ApiError, ApiErrorCode } from '@/types/api/common';

// Normalise backend [{code,message,field}] ou DRF {field:[...]} -> {field:[msg]}
function extractFieldErrors(errors: unknown): Record<string, string[]> {
    if (!errors) {
        return {};
    }

    if (Array.isArray(errors)) {
        const fields: Record<string, string[]> = {};
        for (const err of errors) {
            if (err && typeof err === 'object' && 'field' in err && typeof err.field === 'string') {
                const msg = typeof err.message === 'string' ? err.message : String(err.message);
                const fieldErrors = fields[err.field] ?? [];
                fieldErrors.push(msg);
                fields[err.field] = fieldErrors;
            }
        }
        return fields;
    }

    if (typeof errors === 'object') {
        const result: Record<string, string[]> = {};
        for (const [key, val] of Object.entries(errors as Record<string, unknown>)) {
            if (Array.isArray(val)) {
                result[key] = val.map(String);
            } else if (typeof val === 'string') {
                result[key] = [val];
            }
        }
        return result;
    }

    return {};
}

function mapStatusToErrorCode(status: number): ApiErrorCode {
    if (status === 400 || status === 422) {
        return 'VALIDATION_ERROR';
    }
    if (status === 401) {
        return 'AUTH_ERROR';
    }
    if (status === 403) {
        return 'FORBIDDEN';
    }
    if (status === 404) {
        return 'NOT_FOUND';
    }
    if (status === 429) {
        return 'RATE_LIMITED';
    }
    if (status >= 500) {
        return 'SERVER_ERROR';
    }
    return 'UNKNOWN';
}

export function createApiError(status: number, message: string, data?: Record<string, unknown>): ApiError {
    const code = mapStatusToErrorCode(status);
    const timestamp = Date.now();

    switch (code) {
        case 'VALIDATION_ERROR':
            return {
                code,
                status: status as 400 | 422,
                message,
                timestamp,
                fields: extractFieldErrors(data?.errors),
            };
        case 'AUTH_ERROR':
            return { code, status: 401, message, timestamp };
        case 'FORBIDDEN':
            return { code, status: 403, message, timestamp };
        case 'NOT_FOUND':
            return { code, status: 404, message, timestamp, resource: data?.resource as string | undefined };
        case 'RATE_LIMITED':
            return { code, status: 429, message, timestamp, retryAfter: data?.retryAfter as number | undefined };
        case 'SERVER_ERROR':
            return { code, status: status as 500 | 502 | 503 | 504, message, timestamp };
        default:
            return { code: 'UNKNOWN', status, message, timestamp };
    }
}
