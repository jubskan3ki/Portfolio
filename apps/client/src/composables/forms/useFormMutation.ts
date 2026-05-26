import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { useRouter } from 'vue-router';

import { useAlert } from '@/composables/ui/useAlert';

import type { UseFormMutationOptions, UseFormStateReturn } from '@/types/composables/forms';

export function useFormMutation<TForm extends Record<string, unknown>, TPayload = unknown, TResult = unknown>(
    formState: UseFormStateReturn<TForm>,
    options: UseFormMutationOptions<TPayload, TResult>,
) {
    const queryClient = useQueryClient();
    const router = useRouter();
    const { success: showSuccess } = useAlert();

    const mutation = useMutation({
        mutationFn: options.mutationFn,
        onSuccess: (result) => {
            if (options.invalidateKeys) {
                for (const key of options.invalidateKeys) {
                    queryClient.invalidateQueries({ queryKey: key, refetchType: 'active' });
                }
            }

            const message =
                typeof options.successMessage === 'function' ? options.successMessage() : options.successMessage;
            showSuccess(message ?? 'Opération réussie');
            options.onSuccess?.(result);

            if (options.successRoute) {
                router.push(options.successRoute);
            }
        },
        onError: (error: unknown) => {
            formState.handleApiErrors(error);
        },
    });

    const submit = () => {
        if (!formState.validateForm()) {
            return;
        }
        mutation.mutate(formState.form as unknown as TPayload);
    };

    const submitFormData = () => {
        if (!formState.validateForm()) {
            return;
        }
        mutation.mutate(formState.getFormData() as unknown as TPayload);
    };

    const submitWith = (payload: TPayload) => {
        if (!formState.validateForm()) {
            return;
        }
        mutation.mutate(payload);
    };

    return {
        submit,
        submitFormData,
        submitWith,
        isPending: mutation.isPending,
        isError: mutation.isError,
        error: mutation.error,
        reset: mutation.reset,
    };
}
