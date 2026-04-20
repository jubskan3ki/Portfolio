import { watch } from 'vue';

import type { UseDeferredMatchOptions } from '@/types/composables/data';

export function useDeferredMatch<TItem, TRaw = unknown>(options: UseDeferredMatchOptions<TItem, TRaw>): void {
    watch(
        options.source,
        (items) => {
            const raw = options.getRawValue();
            if (raw === undefined || raw === null) {
                return;
            }
            if (items.length === 0 || !options.isUnmatched()) {
                return;
            }

            const result = options.match(items, raw);
            if (result !== undefined && result !== null) {
                options.setFieldValue(result);
            }
        },
        { immediate: true },
    );
}
