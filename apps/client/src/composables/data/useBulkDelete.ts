import { useMutation } from '@tanstack/vue-query';
import type { Ref } from 'vue';
import { computed, ref } from 'vue';
import type {
    BulkDeleteResult,
    UseBulkDeleteConfirmationReturn,
    UseBulkDeleteOptions,
    UseBulkDeleteReturn,
    UseDeleteConfirmationReturn,
} from '@/types/composables';

export function useBulkDelete<T extends { id: number | string }>(
    options: UseBulkDeleteOptions<T>,
): UseBulkDeleteReturn<T> {
    const { deleteFn, onRefresh, onDeleteSuccess, onDeleteError, onBulkDeleteSuccess, onBulkDeleteError } = options;

    const showDeleteModal = ref(false);
    const itemToDelete = ref<T | null>(null) as Ref<T | null>;

    const deleteMutation = useMutation({
        mutationFn: deleteFn,
        onSuccess: () => {
            showDeleteModal.value = false;
            itemToDelete.value = null;
            onRefresh();
            onDeleteSuccess?.();
        },
        onError: (error) => {
            onDeleteError?.(error instanceof Error ? error : new Error(String(error)));
        },
    });

    const deletion: UseDeleteConfirmationReturn<T> = {
        showModal: showDeleteModal,
        itemToDelete,
        isDeleting: computed(() => deleteMutation.isPending.value),
        confirm: (item: T) => {
            itemToDelete.value = item;
            showDeleteModal.value = true;
        },
        cancel: () => {
            showDeleteModal.value = false;
            itemToDelete.value = null;
        },
        execute: async () => {
            if (itemToDelete.value) {
                await deleteMutation.mutateAsync(itemToDelete.value);
            }
        },
    };

    const showBulkDeleteModal = ref(false);
    const itemsToDelete = ref<T[]>([]) as Ref<T[]>;
    const isBulkDeleting = ref(false);
    const bulkProgress = ref(0);

    const bulkDeletion: UseBulkDeleteConfirmationReturn<T> = {
        showModal: showBulkDeleteModal,
        itemsToDelete,
        isDeleting: computed(() => isBulkDeleting.value),
        progress: bulkProgress,
        confirm: (items: T[]) => {
            itemsToDelete.value = items;
            showBulkDeleteModal.value = true;
        },
        cancel: () => {
            showBulkDeleteModal.value = false;
            itemsToDelete.value = [];
            bulkProgress.value = 0;
        },
        execute: async (): Promise<BulkDeleteResult> => {
            const items = itemsToDelete.value;
            if (!items.length) {
                return { successCount: 0, errorCount: 0, errors: [] };
            }

            isBulkDeleting.value = true;
            bulkProgress.value = 0;

            const result: BulkDeleteResult = {
                successCount: 0,
                errorCount: 0,
                errors: [],
            };

            let completed = 0;
            const total = items.length;
            const queue = [...items];
            const BULK_CONCURRENCY = 3;

            const processItem = async (item: T) => {
                try {
                    await deleteFn(item);
                    result.successCount++;
                } catch (err) {
                    result.errorCount++;
                    result.errors.push({
                        id: item.id,
                        error: err instanceof Error ? err.message : String(err),
                    });
                }
                completed++;
                bulkProgress.value = Math.round((completed / total) * 100);
            };

            const processNext = async (): Promise<void> => {
                const item = queue.shift();
                if (!item) {
                    return;
                }
                await processItem(item);
                return processNext();
            };

            try {
                await Promise.all(Array.from({ length: Math.min(BULK_CONCURRENCY, total) }, () => processNext()));

                showBulkDeleteModal.value = false;
                itemsToDelete.value = [];
                onRefresh();

                if (result.successCount > 0) {
                    onBulkDeleteSuccess?.(result);
                }
                if (result.errorCount > 0 && result.successCount === 0) {
                    onBulkDeleteError?.(new Error(`Failed to delete ${result.errorCount} items`));
                }

                return result;
            } finally {
                isBulkDeleting.value = false;
                bulkProgress.value = 0;
            }
        },
    };

    return { deletion, bulkDeletion };
}
