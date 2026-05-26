import type { ErrorInterceptor, RequestInterceptor, ResponseInterceptor } from '@/types/services/api';

export const interceptors = {
    request: [] as RequestInterceptor[],
    response: [] as ResponseInterceptor[],
    error: [] as ErrorInterceptor[],
};
