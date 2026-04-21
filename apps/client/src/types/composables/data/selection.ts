import type { ComputedRef, Ref } from 'vue';

// useSelection (for bulk actions)

export interface UseSelectionOptions<T extends { id: number | string }> {
    items: Ref<T[]> | ComputedRef<T[]>;
}

export interface UseSelectionReturn<T extends { id: number | string }> {
    selectedIds: ComputedRef<Array<number | string>>;
    selectedItems: ComputedRef<T[]>;
    selectedCount: ComputedRef<number>;
    isAllSelected: ComputedRef<boolean>;
    isPartiallySelected: ComputedRef<boolean>;
    isSelected: (item: T) => boolean;
    toggle: (item: T) => void;
    select: (item: T) => void;
    deselect: (item: T) => void;
    selectAll: () => void;
    deselectAll: () => void;
    toggleAll: () => void;
    selectByIds: (ids: Array<number | string>) => void;
}

// useDeleteConfirmation

export interface UseDeleteConfirmationReturn<T> {
    showModal: Ref<boolean>;
    itemToDelete: Ref<T | null>;
    isDeleting: ComputedRef<boolean>;
    confirm: (item: T) => void;
    cancel: () => void;
    execute: () => Promise<void>;
}

// useBulkDeleteConfirmation

export interface BulkDeleteResult {
    successCount: number;
    errorCount: number;
    errors: Array<{ id: number | string; error: string }>;
}

export interface UseBulkDeleteConfirmationReturn<T> {
    showModal: Ref<boolean>;
    itemsToDelete: Ref<T[]>;
    isDeleting: ComputedRef<boolean>;
    progress: Ref<number>;
    confirm: (items: T[]) => void;
    cancel: () => void;
    execute: () => Promise<BulkDeleteResult>;
}

// useBulkDelete (composable-level | wraps both deletion flows)

export interface UseBulkDeleteOptions<T extends { id: number | string }> {
    deleteFn: (item: T) => Promise<void>;
    onRefresh: () => void;
    onDeleteSuccess?: () => void;
    onDeleteError?: (error: Error) => void;
    onBulkDeleteSuccess?: (result: BulkDeleteResult) => void;
    onBulkDeleteError?: (error: Error) => void;
}

export interface UseBulkDeleteReturn<T extends { id: number | string }> {
    deletion: UseDeleteConfirmationReturn<T>;
    bulkDeletion: UseBulkDeleteConfirmationReturn<T>;
}
