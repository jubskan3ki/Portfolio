import { computed, onMounted, ref, toValue } from 'vue';

import { useFormMutation } from '@/composables/forms/useFormMutation';
import { useFormState } from '@/composables/forms/useFormState';
import { useImagePreview, useRawValues } from '@/composables/forms/useFormUtils';
import { isApiError } from '@/services/utils/errors/guards';

import type { UseFormOptions, UseFormReturn } from '@/types/composables/forms';
import type { Ref } from 'vue';

export function useForm<TForm extends Record<string, unknown>, TEntity = unknown>(
    options: UseFormOptions<TForm, TEntity>,
): UseFormReturn<TForm, TEntity> {
    const {
        initialValues,
        validate,
        api,
        queryKeys,
        onSuccess,
        mapEntityToForm,
        buildPayload,
        notFoundMessage = 'Élément non trouvé ou supprimé.',
        loadErrorMessage = 'Impossible de charger les données. Veuillez réessayer.',
    } = options;

    const isEditMode = computed(() => !!toValue(options.id));

    const isLoading = ref(true);
    const pageError = ref('');
    const entity = ref<TEntity | null>(null) as Ref<TEntity | null>;

    const formState = useFormState<TForm>({
        initialValues,
        validate: validate as ((values: TForm) => Partial<Record<keyof TForm, string>>) | undefined,
        isEditMode,
    });

    const { form, errors, setFieldValue, isDirty, isValid } = formState;

    const mutationFn = (payload: FormData | TForm) => {
        const id = toValue(options.id);
        if (isEditMode.value && id && api.update) {
            return api.update(id, payload);
        }
        return api.create(payload);
    };

    const { submitWith, isPending } = useFormMutation(formState, {
        mutationFn: mutationFn as (payload: unknown) => Promise<unknown>,
        invalidateKeys: queryKeys,
        successMessage: () => {
            if (onSuccess?.messages) {
                return isEditMode.value ? onSuccess.messages.update : onSuccess.messages.create;
            }
            return 'Opération réussie';
        },
        successRoute: onSuccess?.route,
    });

    const { previewImage, setPreviewImage } = useImagePreview();
    const { setRawValue, getRawValue } = useRawValues();

    const onSubmit = () => {
        const payload = buildPayload(form, { isEditMode: isEditMode.value });
        submitWith(payload as unknown as FormData | TForm);
    };

    const fetchData = async () => {
        if (!isEditMode.value) {
            isLoading.value = false;
            return;
        }

        const id = toValue(options.id);
        if (!id || !api.fetch) {
            isLoading.value = false;
            return;
        }

        pageError.value = '';
        isLoading.value = true;

        try {
            const data = await api.fetch(id);
            entity.value = data;

            if (mapEntityToForm) {
                mapEntityToForm(data, { setFieldValue, setRawValue, setPreviewImage });
            }
        } catch (err) {
            if (isApiError(err) && (err.code === 'NOT_FOUND' || err.status === 404)) {
                pageError.value = notFoundMessage;
            } else {
                pageError.value = loadErrorMessage;
            }
        } finally {
            isLoading.value = false;
        }
    };

    onMounted(fetchData);

    return {
        isEditMode,
        isLoading,
        isSubmitting: isPending,
        pageError,
        entity,
        form,
        errors,
        isDirty,
        isValid,
        setFieldValue,
        resetForm: formState.resetForm,
        previewImage,
        setPreviewImage,
        setRawValue,
        getRawValue,
        onSubmit,
        fetchData,
    };
}
