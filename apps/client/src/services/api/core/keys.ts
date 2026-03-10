type QueryKeyModule = 'articles' | 'projects' | 'stacks' | 'experiences' | 'contact' | 'auth' | 'stats' | 'transfer';

interface QueryKeys<T extends string> {
    all: readonly [T];
    list: <F extends object = object>(filters?: F) => readonly [T, 'list', F | undefined];
    detail: (id: string | number) => readonly [T, 'detail', string | number];
    custom: <K extends string>(...keys: [K, ...unknown[]]) => readonly [T, K, ...unknown[]];
}

export function createKeys<T extends QueryKeyModule>(module: T): QueryKeys<T> {
    return {
        all: [module] as const,
        list: <F extends object = object>(filters?: F) => [module, 'list', filters] as const,
        detail: (id: string | number) => [module, 'detail', id] as const,
        custom: <K extends string>(...keys: [K, ...unknown[]]) => [module, ...keys] as const,
    };
}
