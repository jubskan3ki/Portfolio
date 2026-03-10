import { getBaseUrl } from '@/config/api';

import { createApiError } from './errors';
import {
    buildUrl,
    fetchApi,
    fetchWithTimeout,
    handleAuthRefresh,
    handleResponse,
    runRequestInterceptors,
} from './fetch';

import type { HttpMethod } from './fetch';

export const httpClient = {
    get<T>(endpoint: string, params?: Record<string, unknown>): Promise<T> {
        return fetchApi<T>(endpoint, 'GET', undefined, params);
    },

    post<T>(endpoint: string, data?: unknown): Promise<T> {
        return fetchApi<T>(endpoint, 'POST', data);
    },

    put<T>(endpoint: string, data?: unknown): Promise<T> {
        return fetchApi<T>(endpoint, 'PUT', data);
    },

    patch<T>(endpoint: string, data?: unknown): Promise<T> {
        return fetchApi<T>(endpoint, 'PATCH', data);
    },

    delete<T>(endpoint: string): Promise<T> {
        return fetchApi<T>(endpoint, 'DELETE');
    },

    async uploadForm<T>(
        endpoint: string,
        formData: FormData,
        method: 'POST' | 'PUT' | 'PATCH' = 'POST',
        skipRefresh = false,
    ): Promise<T> {
        const url = buildUrl(endpoint);
        const requestInit = await runRequestInterceptors({ method, credentials: 'include', body: formData }, url);

        const response = await fetchWithTimeout(url, requestInit);

        // skipRefresh=true on retry prevents further recursion (max 1 retry for auth refresh)
        if (!skipRefresh && (await handleAuthRefresh(response, endpoint))) {
            return httpClient.uploadForm<T>(endpoint, formData, method, true);
        }

        return handleResponse<T>(response, requestInit);
    },

    async downloadBlob(endpoint: string, params?: Record<string, unknown>, skipRefresh = false): Promise<Blob> {
        const url = buildUrl(endpoint, params);
        const requestInit = await runRequestInterceptors(
            {
                method: 'GET',
                credentials: 'include',
                headers: { Accept: 'application/octet-stream, application/zip, */*' },
            },
            url,
        );

        const response = await fetchWithTimeout(url, requestInit);

        // skipRefresh=true on retry prevents further recursion (max 1 retry for auth refresh)
        if (!skipRefresh && (await handleAuthRefresh(response, endpoint))) {
            return httpClient.downloadBlob(endpoint, params, true);
        }

        if (!response.ok) {
            let errorMessage = response.statusText || 'Download error';
            try {
                const errorData = await response.json();
                if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch {
                // No JSON body
            }
            throw createApiError(response.status, errorMessage);
        }

        return response.blob();
    },

    withRetry<T>(
        endpoint: string,
        method: HttpMethod = 'GET',
        data?: unknown,
        params?: Record<string, unknown>,
        retries = 3,
    ): Promise<T> {
        return fetchApi<T>(endpoint, method, data, params, { retries });
    },
};

export { getBaseUrl };
export { onAuthFailure } from './token';
