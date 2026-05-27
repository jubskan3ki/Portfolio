import { ref } from 'vue';

import type { UseImagePreviewReturn, UseRawValuesReturn } from '@/types/composables/forms';

export { findItemByIdOrName, mapToIds, toSelectOptions } from '@/services/utils/form';

export function useImagePreview(): UseImagePreviewReturn {
    const previewImage = ref('');

    const setPreviewImage = (url: string) => {
        previewImage.value = url;
    };

    const setImageFromPath = (path: string | undefined | null) => {
        previewImage.value = path ?? '';
    };

    const clearPreview = () => {
        previewImage.value = '';
    };

    return {
        previewImage,
        setPreviewImage,
        setImageFromPath,
        clearPreview,
    };
}

export function useRawValues(): UseRawValuesReturn {
    const rawValues = ref<Record<string, unknown>>({});

    const setRawValue = (key: string, value: unknown) => {
        rawValues.value[key] = value;
    };

    const getRawValue = <T = unknown>(key: string): T | undefined => {
        return rawValues.value[key] as T | undefined;
    };

    const clearRawValues = () => {
        rawValues.value = {};
    };

    return {
        rawValues,
        setRawValue,
        getRawValue,
        clearRawValues,
    };
}
