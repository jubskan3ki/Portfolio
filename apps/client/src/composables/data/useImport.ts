import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { ref } from 'vue';

import { useAlert } from '@/composables/ui/useAlert';
import { TRANSFER_QUERY_KEYS } from '@/config/transfer';
import { transferApi } from '@/services/api/modules/transfer';

import type { ImportImage, ImportPreview, TransferModule, UseImportOptions } from '@/types/composables/data';

export function useImport(options: UseImportOptions = {}) {
    const queryClient = useQueryClient();
    const { success: showSuccess, error: showError } = useAlert();

    const isImporting = ref(false);
    const isPreviewing = ref(false);
    const importPreview = ref<ImportPreview | null>(null);

    const previewMutation = useMutation({
        mutationFn: ({ module, file }: { module: TransferModule; file: File }) =>
            transferApi.previewImport(module, file),
        onSuccess: (data) => {
            importPreview.value = data;
        },
        onError: () => {
            showError('Erreur lors de la prévisualisation', 'Import');
            importPreview.value = null;
        },
    });

    const importMutation = useMutation({
        mutationFn: ({
            module,
            file,
            updateExisting,
            skipErrors,
            images,
        }: {
            module: TransferModule;
            file: File;
            updateExisting: boolean;
            skipErrors: boolean;
            images?: ImportImage[];
        }) => {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('update_existing', String(updateExisting));
            formData.append('skip_errors', String(skipErrors));

            if (images && images.length > 0) {
                images.forEach((img) => {
                    formData.append(`images[${img.key}]`, img.file, img.file.name);
                });
            }

            return transferApi.importWithImages(module, formData);
        },
        onSuccess: (job) => {
            const { successCount, errorCount, status } = job;

            if (status === 'failed' || (errorCount > 0 && successCount === 0)) {
                showError(`Import échoué: ${errorCount} erreur(s)`, 'Import');
            } else if (status === 'partially_completed') {
                showSuccess(`Import partiel: ${successCount} créé(s), ${errorCount} erreur(s)`, 'Import');
            } else {
                showSuccess(`Import réussi: ${successCount} enregistrement(s) importé(s)`, 'Import');
            }

            queryClient.invalidateQueries({ queryKey: TRANSFER_QUERY_KEYS.jobs });
            queryClient.invalidateQueries({ queryKey: TRANSFER_QUERY_KEYS.stats });
        },
        onError: () => {
            showError("Erreur lors de l'import", 'Import');
        },
    });

    async function previewImport(module: TransferModule, file: File) {
        isPreviewing.value = true;
        importPreview.value = null;

        try {
            await previewMutation.mutateAsync({ module, file });
        } finally {
            isPreviewing.value = false;
        }
    }

    async function importData(
        module: TransferModule,
        file: File,
        importOptions: { updateExisting: boolean; skipErrors: boolean; images?: ImportImage[] },
    ) {
        isImporting.value = true;

        try {
            await importMutation.mutateAsync({
                module,
                file,
                updateExisting: importOptions.updateExisting,
                skipErrors: importOptions.skipErrors,
                images: importOptions.images,
            });
            options.onSuccess?.();
            return true;
        } catch {
            return false;
        } finally {
            isImporting.value = false;
            importPreview.value = null;
        }
    }

    function clearPreview() {
        importPreview.value = null;
    }

    return {
        isImporting,
        isPreviewing,
        importPreview,
        previewMutation,
        importMutation,
        previewImport,
        importData,
        clearPreview,
    };
}
