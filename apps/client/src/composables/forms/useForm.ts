import { useQuery } from '@tanstack/vue-query';
import { computed, toValue, watch } from 'vue';
import { useFormMutation } from '@/composables/forms/useFormMutation';
import { useFormState } from '@/composables/forms/useFormState';
import { useImagePreview, useRawValues } from '@/composables/forms/useFormUtils';
import { isApiError } from '@/services/utils/errors/guards';
import type { UseFormOptions, UseFormReturn } from '@/types/composables/forms';

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

    // Chargement de l'entité en mode édition via Vue Query : cache partagé avec la clé
    // detail du module (sync avec setQueryData des mutations), dédup, annulation à la
    // navigation. Gated client pour conserver le comportement client-only d'origine
    // (admin = SSR sauté) et éviter un fetch SSR sans cookies.
    const detailKey = computed<readonly unknown[]>(() => {
        const prefix = queryKeys[0] ?? [];
        return [...prefix, 'detail', toValue(options.id)];
    });

    const detailEnabled = computed(
        () => import.meta.client && isEditMode.value && !!toValue(options.id) && !!api.fetch,
    );

    const detailQuery = useQuery({
        queryKey: detailKey,
        queryFn: () => {
            const fetchFn = api.fetch;
            if (!fetchFn) {
                throw new Error('useForm: api.fetch est requis en mode édition');
            }
            return fetchFn(toValue(options.id) as string);
        },
        enabled: detailEnabled,
        staleTime: 0,
    });

    const entity = computed<TEntity | null>(() => detailQuery.data.value ?? null);

    const isLoading = computed(() => detailEnabled.value && detailQuery.isLoading.value);

    const pageError = computed<string>(() => {
        const err = detailQuery.error.value;
        if (!err) {
            return '';
        }
        if (isApiError(err) && (err.code === 'NOT_FOUND' || err.status === 404)) {
            return notFoundMessage;
        }
        return loadErrorMessage;
    });

    // Alimente le formulaire dès que la donnée est disponible (cache chaud ou fetch)
    watch(
        () => detailQuery.data.value,
        (data) => {
            if (data && mapEntityToForm) {
                mapEntityToForm(data as TEntity, { setFieldValue, setRawValue, setPreviewImage });
            }
        },
        { immediate: true },
    );

    // Conservé pour le handler @retry des formulaires
    const fetchData = async () => {
        await detailQuery.refetch();
    };

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
