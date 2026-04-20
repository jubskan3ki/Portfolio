import { ref, watch, toValue } from 'vue';

import type { UseViewRecordingReturn } from '@/types/composables/data';
import type { MaybeRefOrGetter } from 'vue';

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
