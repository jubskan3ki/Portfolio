import type { PaginationMeta } from '@/types/composables/data';

export interface PaginationData {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
}

export interface PaginatedResponse<T> {
    data: T[];
    pagination: PaginationData;
}

export interface NormalizedPaginatedData<T> {
    data: T[];
    pagination: PaginationMeta;
}

export interface DjangoPaginatedResponse<T> {
    results: T[];
    count: number;
    next?: string | null;
    previous?: string | null;
}

export type ApiErrorCode =
    | 'VALIDATION_ERROR'
    | 'AUTH_ERROR'
    | 'NOT_FOUND'
    | 'FORBIDDEN'
    | 'RATE_LIMITED'
    | 'SERVER_ERROR'
    | 'NETWORK_ERROR'
    | 'TIMEOUT'
    | 'UNKNOWN';

interface BaseApiError {
    code: ApiErrorCode;
    status: number;
    message: string;
    timestamp: number;
}

export interface ValidationError extends BaseApiError {
    code: 'VALIDATION_ERROR';
    status: 400 | 422;
    fields: Record<string, string[]>;
}

export interface AuthError extends BaseApiError {
    code: 'AUTH_ERROR';
    status: 401;
}

export interface ForbiddenError extends BaseApiError {
    code: 'FORBIDDEN';
    status: 403;
}

export interface NotFoundError extends BaseApiError {
    code: 'NOT_FOUND';
    status: 404;
    resource?: string;
}

export interface RateLimitError extends BaseApiError {
    code: 'RATE_LIMITED';
    status: 429;
    retryAfter?: number;
}

export interface ServerError extends BaseApiError {
    code: 'SERVER_ERROR';
    status: 500 | 502 | 503 | 504;
}

export interface NetworkError extends BaseApiError {
    code: 'NETWORK_ERROR';
    status: 0;
}

export interface TimeoutError extends BaseApiError {
    code: 'TIMEOUT';
    status: 0;
}

export interface UnknownError extends BaseApiError {
    code: 'UNKNOWN';
}

export type ApiError =
    | ValidationError
    | AuthError
    | ForbiddenError
    | NotFoundError
    | RateLimitError
    | ServerError
    | NetworkError
    | TimeoutError
    | UnknownError;

// Normalized error info produced by the error handler (services/utils/errors/)

export interface ErrorInfo {
    message: string;
    code: ApiErrorCode | 'UNKNOWN';
    status: number;
    details?: Record<string, string[]>;
    isRetryable: boolean;
}

interface PaginationFilters {
    page?: number;
    limit?: number;
}

interface SearchFilters {
    search?: string;
}

interface CategoryFilters {
    category?: string;
}

type SortDirection = 'asc' | 'desc';

interface SortFilters<TSortBy extends string = string> {
    sortBy?: TSortBy;
    sortDirection?: SortDirection;
}

export type ArticleSortBy = 'date' | 'views' | 'readTime' | 'title';

export interface ArticleFilters extends PaginationFilters, SearchFilters, CategoryFilters, SortFilters<ArticleSortBy> {
    tags?: string[];
}

export interface ProjectFilters extends PaginationFilters, SearchFilters, CategoryFilters {
    status?: string;
    technology?: string;
}

export interface StackFilters extends SearchFilters, CategoryFilters {
    limit?: number;
}

export interface ExperienceFilters {
    type?: string;
    limit?: number;
    page?: number;
}
