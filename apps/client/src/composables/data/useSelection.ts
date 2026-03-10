import { shallowRef, triggerRef, computed } from 'vue';

import type { UseSelectionOptions, UseSelectionReturn } from '@/types/composables/data';

export function useSelection<T extends { id: number | string }>(
    options: UseSelectionOptions<T>,
): UseSelectionReturn<T> {
    const { items } = options;

    const selectedSet = shallowRef<Set<number | string>>(new Set());

    const selectedIds = computed(() => Array.from(selectedSet.value));

    const selectedItems = computed(() => items.value.filter((item) => selectedSet.value.has(item.id)));

    const selectedCount = computed(() => selectedSet.value.size);

    const isAllSelected = computed(
        () => items.value.length > 0 && items.value.every((item) => selectedSet.value.has(item.id)),
    );

    const isPartiallySelected = computed(() => {
        const count = selectedSet.value.size;
        return count > 0 && count < items.value.length;
    });

    const isSelected = (item: T): boolean => selectedSet.value.has(item.id);

    const toggle = (item: T): void => {
        if (selectedSet.value.has(item.id)) {
            selectedSet.value.delete(item.id);
        } else {
            selectedSet.value.add(item.id);
        }
        triggerRef(selectedSet);
    };

    const select = (item: T): void => {
        selectedSet.value.add(item.id);
        triggerRef(selectedSet);
    };

    const deselect = (item: T): void => {
        selectedSet.value.delete(item.id);
        triggerRef(selectedSet);
    };

    const selectAll = (): void => {
        items.value.forEach((item) => selectedSet.value.add(item.id));
        triggerRef(selectedSet);
    };

    const deselectAll = (): void => {
        selectedSet.value.clear();
        triggerRef(selectedSet);
    };

    const toggleAll = (): void => {
        if (isAllSelected.value) {
            deselectAll();
        } else {
            selectAll();
        }
    };

    const selectByIds = (ids: Array<number | string>): void => {
        ids.forEach((id) => selectedSet.value.add(id));
        triggerRef(selectedSet);
    };

    return {
        selectedIds,
        selectedItems,
        selectedCount,
        isAllSelected,
        isPartiallySelected,
        isSelected,
        toggle,
        select,
        deselect,
        selectAll,
        deselectAll,
        toggleAll,
        selectByIds,
    };
}
