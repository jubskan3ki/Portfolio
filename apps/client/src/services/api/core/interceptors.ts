import type { RequestInterceptor, ResponseInterceptor, ErrorInterceptor } from '@/types/services/api';

// Interceptors registry
export const interceptors = {
    request: [] as RequestInterceptor[],
    response: [] as ResponseInterceptor[],
    error: [] as ErrorInterceptor[],
};
