// Types for Forms composables

import type { ComputedRef, MaybeRef, Ref, UnwrapRef } from 'vue';

// useFormState Types
export interface UseFormStateOptions<TForm extends Record<string, unknown>, TData = unknown> {
    initialValues: TForm;
    validate?: (values: TForm) => Partial<Record<keyof TForm, string>>;
    mapDataToForm?: (data: TData) => Partial<TForm>;
    mapFormToPayload?: (values: TForm) => unknown;
    buildFormData?: (values: TForm) => FormData;
    successRoute?: string;
    successMessage?: string;
    isEditMode?: Ref<boolean> | boolean;
}

export interface UseFormStateReturn<TForm extends Record<string, unknown>> {
    form: UnwrapRef<TForm>;
    errors: Ref<Partial<Record<keyof TForm, string>>>;
    isLoading: Ref<boolean>;
    isSubmitting: Ref<boolean>;
    pageError: Ref<string>;
    isDirty: Ref<boolean>;
    isValid: Ref<boolean>;
    setFieldValue: <K extends keyof TForm>(field: K, value: TForm[K]) => void;
    setFieldError: (field: keyof TForm, error: string) => void;
    clearErrors: () => void;
    validateForm: () => boolean;
    resetForm: (newValues?: Partial<TForm>) => void;
    setFormFromData: (data: unknown) => void;
    handleApiErrors: (error: unknown) => void;
    getFormData: () => FormData;
    /** @deprecated Use useFormMutation instead for automatic cache invalidation */
    handleSubmit: (submitFn: (values: TForm) => Promise<unknown>) => Promise<void>;
    /** @deprecated Use useFormMutation instead for automatic cache invalidation */
    handleSubmitFormData: (submitFn: (data: FormData) => Promise<unknown>) => Promise<void>;
}

// useFormMutation Types
export interface UseFormMutationOptions<TPayload, TResult> {
    mutationFn: (payload: TPayload) => Promise<TResult>;
    invalidateKeys?: ReadonlyArray<readonly unknown[]>;
    onSuccess?: (result: TResult) => void;
    successMessage?: string | (() => string);
    successRoute?: string;
}

// useFormUtils Types

export interface UseImagePreviewReturn {
    previewImage: Ref<string>;
    setPreviewImage: (url: string) => void;
    setImageFromPath: (path: string | undefined | null) => void;
    clearPreview: () => void;
}

export interface UseRawValuesReturn {
    rawValues: Ref<Record<string, unknown>>;
    setRawValue: (key: string, value: unknown) => void;
    getRawValue: <T = unknown>(key: string) => T | undefined;
    clearRawValues: () => void;
}

export interface UseFetchEntityOptions<TEntity> {
    fetchFn: (id: string) => Promise<TEntity>;
    notFoundMessage?: string;
    errorMessage?: string;
}

export interface UseFetchEntityReturn<TEntity> {
    isLoading: Ref<boolean>;
    pageError: Ref<string>;
    entity: Ref<TEntity | null>;
    fetchData: (id: string | undefined) => Promise<TEntity | null>;
}

// useForm | high-level composable orchestrating state, mutation, preview & raw values

export interface FormContext<TForm extends Record<string, unknown>> {
    setFieldValue: <K extends keyof TForm>(field: K, value: TForm[K]) => void;
    setRawValue: (key: string, value: unknown) => void;
    setPreviewImage: (url: string) => void;
}

export interface UseFormOptions<TForm extends Record<string, unknown>, TEntity = unknown> {
    /** Initial form values */
    initialValues: TForm;

    /** Validation function | returns field-level errors */
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

    /** Entity ID | if provided and truthy, enables edit mode */
    id?: MaybeRef<string | undefined>;

    /** Error messages */
    notFoundMessage?: string;
    loadErrorMessage?: string;
}

export interface UseFormReturn<TForm extends Record<string, unknown>, TEntity> {
    // Mode
    isEditMode: ComputedRef<boolean>;

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

// useSlugGenerator

export interface UseSlugGeneratorOptions {
    auto?: boolean;
    trackManualEdit?: boolean;
}

export interface UseSlugGeneratorReturn {
    slug: Ref<string>;
    generate: () => void;
    setSlug: (value: string) => void;
    wasManuallyEdited: Ref<boolean>;
}
