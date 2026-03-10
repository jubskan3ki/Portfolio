// Types for Forms composables

import type { Ref, UnwrapRef } from 'vue';

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

export interface SelectOption {
    value: number | string;
    label: string;
    image?: string;
    disabled?: boolean;
}

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
