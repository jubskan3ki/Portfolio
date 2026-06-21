import type { QueryKey, UseQueryOptions } from '@tanstack/vue-query';
import type { ApiError } from '@/types/api/common';

// createQuery presets
export type QueryPreset = 'list' | 'detail' | 'static' | 'realtime';

// Token manager
export type AuthFailureHandler = () => void | Promise<void>;

// Query keys factory
export type QueryKeyModule =
    | 'articles'
    | 'projects'
    | 'stacks'
    | 'experiences'
    | 'contact'
    | 'auth'
    | 'stats'
    | 'transfer'
    | 'search';

export interface QueryKeys<T extends string> {
    all: readonly [T];
    list: <F extends object = object>(filters?: F) => readonly [T, 'list', F | undefined];
    detail: (id: string | number) => readonly [T, 'detail', string | number];
    custom: <K extends string>(...keys: [K, ...unknown[]]) => readonly [T, K, ...unknown[]];
}

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface FetchOptions {
    retries?: number;
    skipRefresh?: boolean;
    transformResponse?: boolean;
    transformRequest?: boolean;
    /** Signal d'annulation (ex: AbortSignal fourni par Vue Query) propagé jusqu'au fetch */
    signal?: AbortSignal;
    /** @internal récursion max pour éviter boucle infinie */
    _depth?: number;
}

export type RequestInterceptor = (config: RequestInit, url: string) => RequestInit | Promise<RequestInit>;
export type ResponseInterceptor = (response: Response, request: RequestInit) => Response | Promise<Response>;
export type ErrorInterceptor = (error: ApiError) => ApiError | Promise<ApiError>;

export type QueryOptions<TData, TSelect = TData> = Omit<
    UseQueryOptions<TData, Error, TSelect, QueryKey>,
    'queryKey' | 'queryFn'
>;

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

export type { ApiError } from '@/types/api/common';
