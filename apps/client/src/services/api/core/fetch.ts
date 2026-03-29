import { HTTP_CONFIG, defaultRequestInit, getBaseUrl } from '@/config/api';
import { API_RETRY } from '@/config/constants';
import { isApiError } from '@/services/utils/errors/guards';
import { decodeHtmlEntities } from '@/services/utils/helpers';
import { transformKeysToCamel, transformKeysToSnake } from '@/services/utils/responseNormalizer';

import { createApiError } from './errors';
import { interceptors } from './interceptors';
import { refreshTokenManager, notifyAuthFailure } from './token';

import type { ApiError } from '@/types/api/common';
import type { HttpMethod, FetchOptions } from '@/types/services/api';

export type { HttpMethod } from '@/types/services/api';

const MAX_FETCH_DEPTH = 3;
const MUTATION_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

// ETag store: maps endpoint URLs to their last ETag + response body
const etagStore = new Map<string, { etag: string; data: unknown }>();

// SSR request deduplication: prevents duplicate concurrent GET requests
const ssrPendingRequests = new Map<string, Promise<unknown>>();

/**
 * Read the Django CSRF token from the cookie.
 */
function getCsrfToken(): string | null {
    if (import.meta.server) {
        return null;
    }
    const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]*)/);
    return match ? decodeURIComponent(match[1] as string) : null;
}

// Calculate delay for exponential backoff with jitter
function calculateRetryDelay(attemptNumber: number): number {
    const exponentialDelay = API_RETRY.INITIAL_DELAY * Math.pow(API_RETRY.BACKOFF_MULTIPLIER, attemptNumber);
    const cappedDelay = Math.min(exponentialDelay, API_RETRY.MAX_DELAY);
    // Add jitter (0-100ms) to prevent thundering herd
    const jitter = Math.random() * 100;
    return cappedDelay + jitter;
}

export function buildUrl(endpoint: string, params?: Record<string, unknown>): string {
    const baseUrl = getBaseUrl();
    const url = new URL(`${baseUrl}${endpoint}`);

    if (params) {
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null && value !== '') {
                if (Array.isArray(value)) {
                    value.forEach((v) => url.searchParams.append(key, String(v)));
                } else {
                    url.searchParams.append(key, String(value));
                }
            }
        });
    }

    return url.toString();
}

export async function runRequestInterceptors(requestInit: RequestInit, url: string): Promise<RequestInit> {
    const result = await interceptors.request.reduce(
        async (initPromise, interceptor) => interceptor(await initPromise, url),
        Promise.resolve(requestInit),
    );
    return result;
}

export async function handleAuthRefresh(response: Response, endpoint: string): Promise<boolean> {
    if (response.status !== 401 || endpoint.includes('/auth/')) {
        return false;
    }
    const refreshed = await refreshTokenManager.refresh();
    if (refreshed) {
        return true;
    }
    await notifyAuthFailure();
    throw createApiError(401, 'Session expired');
}

export async function fetchWithTimeout(
    url: string,
    options: RequestInit,
    timeout = import.meta.server ? HTTP_CONFIG.SSR_TIMEOUT : HTTP_CONFIG.DEFAULT_TIMEOUT,
): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });
        return response;
    } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
            throw new TypeError('fetch timeout: Request took too long');
        }
        throw error;
    } finally {
        clearTimeout(timeoutId);
    }
}

export async function handleResponse<T>(
    response: Response,
    requestConfig: RequestInit,
    transformKeys = true,
): Promise<T> {
    // Run response interceptors sequentially using reduce
    const processedResponse = await interceptors.response.reduce(
        async (responsePromise, interceptor) => interceptor(await responsePromise, requestConfig),
        Promise.resolve(response),
    );

    if (!processedResponse.ok) {
        let errorData: Record<string, unknown> = {};
        let message = processedResponse.statusText || 'An error occurred';

        try {
            const data = await processedResponse.json();
            message = data.errors?.[0]?.message || data.detail || data.message || message;
            errorData = data;
        } catch {
            // Response has no JSON body
        }

        // Run error interceptors sequentially using reduce
        const error = await interceptors.error.reduce(
            async (errorPromise, interceptor) => interceptor(await errorPromise),
            Promise.resolve(createApiError(processedResponse.status, message, errorData)),
        );

        throw error;
    }

    if (processedResponse.status === 204) {
        return {} as T;
    }

    const jsonData = await processedResponse.json();

    // Transform snake_case keys to camelCase, then decode HTML entities
    if (transformKeys) {
        return decodeHtmlEntities(transformKeysToCamel<T>(jsonData));
    }

    return decodeHtmlEntities(jsonData as T);
}

export async function fetchApi<T>(
    endpoint: string,
    method: HttpMethod = 'GET',
    data?: unknown,
    params?: Record<string, unknown>,
    options: FetchOptions = {},
): Promise<T> {
    const { retries = 0, skipRefresh = false, transformResponse = true, transformRequest = true, _depth = 0 } = options;

    if (_depth >= MAX_FETCH_DEPTH) {
        throw createApiError(0, 'Maximum fetch depth exceeded — possible infinite loop');
    }
    const url = buildUrl(endpoint, params);

    // SSR deduplication: reuse in-flight GET requests to avoid duplicate calls
    if (import.meta.server && method === 'GET') {
        const pending = ssrPendingRequests.get(url);
        if (pending) {
            return pending as Promise<T>;
        }
    }

    let requestInit: RequestInit = {
        ...defaultRequestInit,
        method,
    };

    if (data && method !== 'GET') {
        // Transform camelCase keys to snake_case for outgoing requests
        const requestData = transformRequest ? transformKeysToSnake(data) : data;
        requestInit.body = JSON.stringify(requestData);
    }

    // Attach CSRF token for state-changing requests
    if (MUTATION_METHODS.has(method)) {
        const csrfToken = getCsrfToken();
        if (csrfToken) {
            requestInit.headers = {
                ...requestInit.headers,
                'X-CSRFToken': csrfToken,
            };
        }
    }

    // Attach ETag for conditional GET requests
    if (method === 'GET') {
        const cached = etagStore.get(url);
        if (cached) {
            requestInit.headers = {
                ...requestInit.headers,
                'If-None-Match': cached.etag,
            };
        }
    }

    requestInit = await runRequestInterceptors(requestInit, url);

    // Core fetch execution (extracted for SSR dedup wrapping)
    const executeFetch = async (): Promise<T> => {
        try {
            const response = await fetchWithTimeout(url, requestInit);

            if (!skipRefresh && (await handleAuthRefresh(response, endpoint))) {
                return fetchApi<T>(endpoint, method, data, params, {
                    ...options,
                    skipRefresh: true,
                    _depth: _depth + 1,
                });
            }

            // 304 Not Modified — return previously cached data
            if (response.status === 304) {
                const cached = etagStore.get(url);
                if (cached) {
                    return cached.data as T;
                }
            }

            // Capture ETag before response body is consumed
            const etag = response.headers.get('etag');

            const result = await handleResponse<T>(response, requestInit, transformResponse);

            // Store ETag + response for future conditional requests
            if (etag && method === 'GET') {
                etagStore.set(url, { etag, data: result });
            }

            return result;
        } catch (error) {
            // Network error
            if (error instanceof TypeError && error.message.includes('fetch')) {
                const networkError: ApiError = {
                    code: 'NETWORK_ERROR',
                    status: 0,
                    message: 'Network error: Unable to connect to server',
                    timestamp: Date.now(),
                };

                // Run error interceptors sequentially using reduce
                const processedError = await interceptors.error.reduce<Promise<ApiError>>(
                    async (errorPromise, interceptor) => interceptor(await errorPromise),
                    Promise.resolve(networkError),
                );

                throw processedError;
            }

            // Retry on server errors / rate limit with exponential backoff
            if (isApiError(error)) {
                if (retries > 0 && (error.code === 'SERVER_ERROR' || error.code === 'RATE_LIMITED')) {
                    // For rate limited errors, respect server's retry-after header if present
                    const delay
                        = error.code === 'RATE_LIMITED' && 'retryAfter' in error
                            ? (error.retryAfter || 1) * 1000
                            : calculateRetryDelay(API_RETRY.MAX_RETRIES - retries);

                    await new Promise((resolve) => setTimeout(resolve, delay));
                    return fetchApi<T>(endpoint, method, data, params, {
                        retries: retries - 1,
                        skipRefresh,
                        _depth: _depth + 1,
                    });
                }
            }

            throw error;
        }
    };

    // SSR dedup: register promise so concurrent calls reuse it
    if (import.meta.server && method === 'GET') {
        const promise = executeFetch().finally(() => {
            ssrPendingRequests.delete(url);
        });
        ssrPendingRequests.set(url, promise);
        return promise;
    }

    return executeFetch();
}
