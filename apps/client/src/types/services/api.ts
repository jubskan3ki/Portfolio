// Types pour les services API core

import type { ApiError } from '@/types/api/common';
import type { QueryKey, UseQueryOptions } from '@tanstack/vue-query';

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface FetchOptions {
    retries?: number;
    skipRefresh?: boolean;
    transformResponse?: boolean;
    transformRequest?: boolean;
    /** @internal Tracks recursive call depth to prevent infinite loops */
    _depth?: number;
}

export type RequestInterceptor = (config: RequestInit, url: string) => RequestInit | Promise<RequestInit>;
export type ResponseInterceptor = (response: Response, request: RequestInit) => Response | Promise<Response>;
export type ErrorInterceptor = (error: ApiError) => ApiError | Promise<ApiError>;

export type QueryOptions<TData> = Omit<UseQueryOptions<TData, Error, TData, QueryKey>, 'queryKey' | 'queryFn'>;

interface MutationCallbacks<TData, TVariables> {
    onSuccess?: (data: TData, variables: TVariables, context: unknown) => void;
    onError?: (error: ApiError, variables: TVariables, context: unknown) => void;
    onSettled?: (data: TData | undefined, error: ApiError | null, variables: TVariables, context: unknown) => void;
    onMutate?: (variables: TVariables) => Promise<unknown> | unknown;
}

export interface MutationOptions<TData, TVariables> extends MutationCallbacks<TData, TVariables> {
    retry?: number | boolean;
    retryDelay?: number;
    meta?: Record<string, unknown>;
}

export type IdField = 'id' | 'slug' | 'name';

export interface EntityApi<T, TCreate, TUpdate, TId extends string | number = string | number> {
    create: (data: TCreate) => Promise<T>;
    update: (id: TId, data: TUpdate) => Promise<T>;
    delete: (id: TId) => Promise<void>;
}

export interface SubResourceKeys {
    all: () => readonly unknown[];
    list?: () => readonly unknown[];
    detail?: (id: string | number) => readonly unknown[];
}

// Re-export common types for convenience
export type { ApiError } from '@/types/api/common';
