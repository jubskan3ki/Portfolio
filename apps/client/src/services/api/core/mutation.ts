import { useMutation, useQueryClient } from '@tanstack/vue-query';

import type { EntityApi, IdField, MutationOptions, SubResourceKeys } from '@/types/services/api';

export function createSubResourceMutations<T, TCreate, TUpdate, TId extends string | number = string>(
    api: EntityApi<T, TCreate, TUpdate, TId>,
    keys: SubResourceKeys,
    idField: IdField = 'slug',
) {
    return {
        useCreate: (options?: MutationOptions<T, TCreate>) => {
            const queryClient = useQueryClient();
            return useMutation({
                mutationFn: api.create,
                onSuccess: (data, variables, context) => {
                    queryClient.invalidateQueries({
                        queryKey: keys.all(),
                        refetchType: 'active',
                    });

                    options?.onSuccess?.(data, variables, context);
                },
                onError: options?.onError,
                onSettled: options?.onSettled,
            });
        },

        useUpdate: (options?: MutationOptions<T, { [K in IdField]?: TId } & { data: TUpdate }>) => {
            const queryClient = useQueryClient();
            return useMutation({
                mutationFn: (variables: { [K in IdField]?: TId } & { data: TUpdate }) => {
                    const id = variables[idField] as TId;
                    return api.update(id, variables.data);
                },
                onSuccess: (data, variables, context) => {
                    const id = variables[idField] as TId;

                    if (keys.detail) {
                        queryClient.setQueryData(keys.detail(id as string | number), data);
                    }

                    queryClient.invalidateQueries({
                        queryKey: keys.list ? keys.list() : keys.all(),
                        refetchType: 'active',
                    });

                    options?.onSuccess?.(data, variables, context);
                },
                onError: options?.onError,
                onSettled: options?.onSettled,
            });
        },

        useDelete: (options?: MutationOptions<void, TId>) => {
            const queryClient = useQueryClient();
            return useMutation({
                mutationFn: api.delete,
                onSuccess: (data, variables, context) => {
                    queryClient.invalidateQueries({
                        queryKey: keys.all(),
                        refetchType: 'active',
                    });

                    options?.onSuccess?.(data, variables, context);
                },
                onError: options?.onError,
                onSettled: options?.onSettled,
            });
        },
    };
}
