import type { ErrorInfo } from './constants';
import { API_ERROR_MESSAGES, RETRYABLE_ERRORS } from './constants';
import { isApiError } from './guards';

export function parseError(error: unknown): ErrorInfo {
    if (isApiError(error)) {
        return {
            message: error.message || API_ERROR_MESSAGES[error.code],
            code: error.code,
            status: error.status,
            details: 'fields' in error ? error.fields : undefined,
            isRetryable: RETRYABLE_ERRORS.includes(error.code),
        };
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
        return {
            message: 'Connexion au serveur impossible. Vérifiez votre connexion.',
            code: 'NETWORK_ERROR',
            status: 0,
            isRetryable: true,
        };
    }

    if (error instanceof DOMException && error.name === 'AbortError') {
        return {
            message: 'La requête a été annulée.',
            code: 'UNKNOWN',
            status: 0,
            isRetryable: false,
        };
    }

    if (error instanceof Error) {
        return {
            message: error.message,
            code: 'UNKNOWN',
            status: 0,
            isRetryable: false,
        };
    }

    if (typeof error === 'string') {
        return {
            message: error,
            code: 'UNKNOWN',
            status: 0,
            isRetryable: false,
        };
    }

    if (error && typeof error === 'object') {
        const obj = error as Record<string, unknown>;
        const message = (obj.detail || obj.message || obj.error) as string | undefined;
        const status = (obj.status || obj.statusCode || 0) as number;

        return {
            message: message || API_ERROR_MESSAGES.UNKNOWN,
            code: 'UNKNOWN',
            status,
            isRetryable: status >= 500,
        };
    }

    return {
        message: API_ERROR_MESSAGES.UNKNOWN,
        code: 'UNKNOWN',
        status: 0,
        isRetryable: false,
    };
}
