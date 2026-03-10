import { reactive, ref, computed, shallowRef, type UnwrapRef } from 'vue';
import { useRouter } from 'vue-router';

import { useAlert } from '@/composables/ui/useAlert';
import { isApiError } from '@/services/utils/errors/guards';

import type { UseFormStateOptions, UseFormStateReturn } from '@/types/composables/forms';

export function useFormState<TForm extends Record<string, unknown>, TData = unknown>(
    options: UseFormStateOptions<TForm, TData>,
): UseFormStateReturn<TForm> {
    const {
        initialValues,
        validate,
        mapDataToForm,
        mapFormToPayload,
        buildFormData,
        successRoute,
        successMessage = 'Opération réussie',
        isEditMode = false,
    } = options;

    const router = useRouter();
    const { success: showSuccess, error: showError } = useAlert();

    const form = reactive<TForm>({ ...initialValues });
    const errors = shallowRef<Partial<Record<keyof TForm, string>>>({});
    const pageError = ref('');
    const isLoading = ref(false);
    const isSubmitting = ref(false);
    const initialSnapshot = ref<string>(JSON.stringify(initialValues));

    const isDirty = computed(() => JSON.stringify(form) !== initialSnapshot.value);

    const isValid = computed(() => {
        if (!validate) {
            return true;
        }
        const validationErrors = validate(form as TForm);
        return Object.keys(validationErrors).length === 0;
    });

    const getIsEditMode = (): boolean => {
        return typeof isEditMode === 'boolean' ? isEditMode : isEditMode.value;
    };

    const setFieldValue = <K extends keyof TForm>(field: K, value: TForm[K]): void => {
        (form as TForm)[field] = value;
        if (errors.value[field]) {
            const newErrors = { ...errors.value };
            newErrors[field] = undefined;
            errors.value = newErrors;
        }
    };

    const setFieldError = (field: keyof TForm, error: string): void => {
        errors.value = { ...errors.value, [field]: error };
    };

    const clearErrors = (): void => {
        errors.value = {};
        pageError.value = '';
    };

    const resetForm = (newValues?: Partial<TForm>): void => {
        const resetValues = newValues ? { ...initialValues, ...newValues } : initialValues;

        Object.keys(resetValues).forEach((key) => {
            (form as Record<string, unknown>)[key] = resetValues[key as keyof TForm];
        });

        initialSnapshot.value = JSON.stringify(form);
        clearErrors();
    };

    const setFormFromData = (data: unknown): void => {
        if (!mapDataToForm || !data) {
            return;
        }

        const mappedValues = mapDataToForm(data as TData);
        Object.entries(mappedValues).forEach(([key, value]) => {
            if (key in form) {
                (form as Record<string, unknown>)[key] = value;
            }
        });

        initialSnapshot.value = JSON.stringify(form);
    };

    const getFormData = (): FormData => {
        if (buildFormData) {
            return buildFormData(form as TForm);
        }

        const formData = new FormData();
        const payload = mapFormToPayload ? mapFormToPayload(form as TForm) : form;

        Object.entries(payload as Record<string, unknown>).forEach(([key, value]) => {
            if (value === null || value === undefined) {
                return;
            }

            if (value instanceof File) {
                formData.append(key, value);
            } else if (Array.isArray(value)) {
                value.forEach((item) => {
                    if (item instanceof File) {
                        formData.append(key, item);
                    } else {
                        formData.append(key, String(item));
                    }
                });
            } else if (typeof value === 'object') {
                formData.append(key, JSON.stringify(value));
            } else {
                formData.append(key, String(value));
            }
        });

        return formData;
    };

    const validateForm = (): boolean => {
        clearErrors();

        if (!validate) {
            return true;
        }

        const validationErrors = validate(form as TForm);
        if (Object.keys(validationErrors).length > 0) {
            errors.value = validationErrors;
            return false;
        }

        return true;
    };

    const handleApiErrors = (error: unknown): void => {
        if (isApiError(error)) {
            // Handle validation errors with field-level details
            if (error.code === 'VALIDATION_ERROR' && 'fields' in error) {
                const fieldErrors: Partial<Record<keyof TForm, string>> = {};
                let hasFieldErrors = false;

                for (const [key, messages] of Object.entries(error.fields)) {
                    if (key in form) {
                        fieldErrors[key as keyof TForm] = Array.isArray(messages) ? messages[0] : String(messages);
                        hasFieldErrors = true;
                    }
                }

                if (hasFieldErrors) {
                    errors.value = fieldErrors;
                    return;
                }
            }

            // Use the error message from the API
            pageError.value = error.message;
            showError(error.message);
            return;
        }

        const message = getIsEditMode() ? 'Erreur lors de la modification' : 'Erreur lors de la création';
        pageError.value = message;
        showError(message);
    };

    const _executeSubmit = async (fn: () => Promise<unknown>): Promise<void> => {
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;
        pageError.value = '';

        try {
            await fn();
            showSuccess(successMessage);

            if (successRoute) {
                router.push(successRoute);
            }
        } catch (error) {
            handleApiErrors(error);
        } finally {
            isSubmitting.value = false;
        }
    };

    const handleSubmit = (submitFn: (values: TForm) => Promise<unknown>): Promise<void> =>
        _executeSubmit(() => {
            const payload = mapFormToPayload ? mapFormToPayload(form as TForm) : form;
            return submitFn(payload as TForm);
        });

    const handleSubmitFormData = (submitFn: (data: FormData) => Promise<unknown>): Promise<void> =>
        _executeSubmit(() => submitFn(getFormData()));

    return {
        form: form as UnwrapRef<TForm>,
        errors,
        isLoading,
        isSubmitting,
        pageError,
        isDirty,
        isValid,
        setFieldValue,
        setFieldError,
        clearErrors,
        resetForm,
        setFormFromData,
        handleApiErrors,
        getFormData,
        validateForm,
        handleSubmit,
        handleSubmitFormData,
    };
}
