import { ref, watch, toValue } from 'vue';

import type { MaybeRefOrGetter, Ref } from 'vue';

interface UseViewRecordingReturn {
    viewRecorded: Ref<boolean>;
}

/**
 * Records a single view for an entity when its data becomes available.
 * Ensures the view is recorded only once per component lifecycle.
 */
export function useViewRecording(
    data: MaybeRefOrGetter<{ slug: string } | null | undefined>,
    recordFn: (slug: string) => void,
): UseViewRecordingReturn {
    const viewRecorded = ref(false);

    watch(
        () => toValue(data),
        (item) => {
            if (item && !viewRecorded.value) {
                recordFn(item.slug);
                viewRecorded.value = true;
            }
        },
        { immediate: true },
    );

    return { viewRecorded };
}
