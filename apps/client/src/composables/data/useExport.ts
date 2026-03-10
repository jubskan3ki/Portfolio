import { useMutation } from '@tanstack/vue-query';
import { ref } from 'vue';

import { useAlert } from '@/composables/ui/useAlert';
import { transferApi } from '@/services/api/modules/transfer';
import { downloadFile } from '@/services/utils/dom';

import type { ExportFormat, TransferModule, UseExportOptions } from '@/types/composables/data';

export function useExport(options: UseExportOptions = {}) {
    const { success: showSuccess, error: showError } = useAlert();
    const isExporting = ref(false);

    const exportMutation = useMutation({
        mutationFn: async ({ module, format }: { module: TransferModule; format: ExportFormat }) => {
            const blob = await transferApi.downloadModuleExport(module, { export_format: format });
            return { blob, module, format };
        },
        onSuccess: ({ blob, module, format }) => {
            const filename = `${module}_export_${new Date().toISOString().split('T')[0]}.${format}`;
            downloadFile(blob, filename);
        },
        onError: () => {
            showError('Erreur lors de l\'export', 'Export');
        },
    });

    async function exportModules(selectedModules: TransferModule[], format: ExportFormat) {
        if (selectedModules.length === 0) {
            showError('Veuillez sélectionner au moins un module', 'Export');
            return;
        }

        isExporting.value = true;

        try {
            if (selectedModules.length > 1) {
                const blob = await transferApi.downloadBulk({
                    modules: selectedModules.join(','),
                    export_format: format,
                });

                const filename = `export_bulk_${new Date().toISOString().split('T')[0]}.zip`;
                downloadFile(blob, filename);

                showSuccess(`${selectedModules.length} module(s) exporté(s) dans un ZIP`, 'Export');
            } else {
                const singleModule = selectedModules[0] as TransferModule;
                await exportMutation.mutateAsync({ module: singleModule, format });
                showSuccess('Export réussi', 'Export');
            }

            options.onSuccess?.();
        } catch {
            showError('Erreur lors de l\'export', 'Export');
        } finally {
            isExporting.value = false;
        }
    }

    return {
        isExporting,
        exportMutation,
        exportModules,
    };
}
