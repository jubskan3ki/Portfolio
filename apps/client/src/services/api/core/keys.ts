import type { QueryKeyModule, QueryKeys } from '@/types/services/api';

export function createKeys<T extends QueryKeyModule>(module: T): QueryKeys<T> {
    return {
        all: [module] as const,
        list: <F extends object = object>(filters?: F) => [module, 'list', filters] as const,
        detail: (id: string | number) => [module, 'detail', id] as const,
        custom: <K extends string>(...keys: [K, ...unknown[]]) => [module, ...keys] as const,
    };
}
