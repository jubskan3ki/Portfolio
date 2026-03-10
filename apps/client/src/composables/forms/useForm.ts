import { computed, onMounted, ref, toValue } from 'vue';

import { useFormMutation } from '@/composables/forms/useFormMutation';
import { useFormState } from '@/composables/forms/useFormState';
import { useImagePreview, useRawValues } from '@/composables/forms/useFormUtils';
import { isApiError } from '@/services/utils/errors/guards';

import type { ComputedRef, MaybeRef, Ref, UnwrapRef } from 'vue';

// --- Types ---

interface FormContext<TForm extends Record<string, unknown>> {
    setFieldValue: <K extends keyof TForm>(field: K, value: TForm[K]) => void;
    setRawValue: (key: string, value: unknown) => void;
    setPreviewImage: (url: string) => void;
}

interface UseFormOptions<TForm extends Record<string, unknown>, TEntity = unknown> {
    /** Initial form values */
    initialValues: TForm;

    /** Validation function — returns field-level errors */
    validate?: (values: TForm) => Partial<Record<string, string>>;

    /** API methods */
    api: {
        create: (payload: FormData | TForm) => Promise<unknown>;
        update?: (id: string, payload: FormData | TForm) => Promise<unknown>;
        fetch?: (id: string) => Promise<TEntity>;
    };

    /** TanStack Query keys to invalidate on success */
    queryKeys: ReadonlyArray<readonly unknown[]>;

    /** Post-success behavior */
    onSuccess?: {
        route?: string;
        messages?: { create: string; update: string };
    };

    /** Map entity data to form fields (edit mode) */
    mapEntityToForm?: (entity: TEntity, ctx: FormContext<TForm>) => void;

    /** Build the payload to submit */
    buildPayload: (form: UnwrapRef<TForm>, ctx: { isEditMode: boolean }) => FormData | TForm;

    /** Entity ID — if provided and truthy, enables edit mode */
    id?: MaybeRef<string | undefined>;

    /** Error messages */
    notFoundMessage?: string;
    loadErrorMessage?: string;
}

interface UseFormReturn<TForm extends Record<string, unknown>, TEntity> {
    // Mode
    isEditMode: ComputedRef<boolean>;

    // State
    isLoading: Ref<boolean>;
    isSubmitting: Ref<boolean>;
    pageError: Ref<string>;
    entity: Ref<TEntity | null>;

    // Form
    form: UnwrapRef<TForm>;
    errors: Ref<Partial<Record<keyof TForm, string>>>;
    isDirty: Ref<boolean>;
    isValid: Ref<boolean>;
    setFieldValue: <K extends keyof TForm>(field: K, value: TForm[K]) => void;
    resetForm: (newValues?: Partial<TForm>) => void;

    // Image preview
    previewImage: Ref<string>;
    setPreviewImage: (url: string) => void;

    // Raw values (for deferred matching)
    setRawValue: (key: string, value: unknown) => void;
    getRawValue: <T = unknown>(key: string) => T | undefined;

    // Actions
    onSubmit: () => void;
    fetchData: () => Promise<void>;
}

// --- Composable ---

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

    // Edit mode
    const isEditMode = computed(() => !!toValue(options.id));

    // Page-level state
    const isLoading = ref(true);
    const pageError = ref('');
    const entity = ref<TEntity | null>(null) as Ref<TEntity | null>;

    // Form state
    const formState = useFormState<TForm>({
        initialValues,
        validate: validate as ((values: TForm) => Partial<Record<keyof TForm, string>>) | undefined,
        isEditMode,
    });

    const { form, errors, setFieldValue, isDirty, isValid } = formState;

    // Mutation
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

    // Image preview & raw values
    const { previewImage, setPreviewImage } = useImagePreview();
    const { setRawValue, getRawValue } = useRawValues();

    // Submit
    const onSubmit = () => {
        const payload = buildPayload(form, { isEditMode: isEditMode.value });
        submitWith(payload as unknown as FormData | TForm);
    };

    // Fetch entity (edit mode)
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

    // Lifecycle
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
