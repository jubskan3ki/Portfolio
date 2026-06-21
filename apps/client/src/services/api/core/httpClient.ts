import { getBaseUrl, HTTP_CONFIG } from '@/config/api';

import { createApiError } from './errors';
import type { HttpMethod } from './fetch';
import {
    buildUrl,
    fetchApi,
    fetchWithTimeout,
    handleAuthRefresh,
    handleResponse,
    runRequestInterceptors,
} from './fetch';

export const httpClient = {
    get<T>(endpoint: string, params?: Record<string, unknown>, signal?: AbortSignal): Promise<T> {
        return fetchApi<T>(endpoint, 'GET', undefined, params, { signal });
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

        const response = await fetchWithTimeout(url, requestInit, HTTP_CONFIG.UPLOAD_TIMEOUT);

        // skipRefresh=true sur retry: max 1 refresh auth, empêche récursion
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

        const response = await fetchWithTimeout(url, requestInit, HTTP_CONFIG.DOWNLOAD_TIMEOUT);

        // skipRefresh=true sur retry: max 1 refresh auth, empêche récursion
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
                // no JSON body
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

export { onAuthFailure } from './token';
export { getBaseUrl };
