import { watch } from 'vue';

import type { ComputedRef, Ref } from 'vue';

export interface UseDeferredMatchOptions<TItem, TRaw = unknown> {
    /** Reactive source of loaded items (e.g. categories, tags from API) */
    source: Ref<TItem[]> | ComputedRef<TItem[]>;

    /** Getter for the raw value stored before items were loaded */
    getRawValue: () => TRaw | undefined;

    /** Returns true when the form field has not been matched yet */
    isUnmatched: () => boolean;

    /** Match raw value against loaded items, return the resolved value or undefined if no match */
    match: (items: TItem[], rawValue: TRaw) => unknown;

    /** Set the matched value on the form field */
    setFieldValue: (value: unknown) => void;
}

/**
 * Watches a reactive data source and matches raw values once data is loaded.
 *
 * Useful when a form loads in edit mode: the entity references related data
 * (e.g. category name, tag IDs) but the related data is fetched asynchronously.
 * This composable watches the async source and sets the form field once a match is found.
 */
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
