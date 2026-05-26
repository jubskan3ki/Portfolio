import { useQuery } from '@tanstack/vue-query';
import { computed } from 'vue';

import { TRANSFER_MODULES, TRANSFER_QUERY_KEYS } from '@/config/transfer';
import { statsApi } from '@/services/api/modules/stats';
import { extractStatsCount } from '@/services/utils/transfer';
import type { ModuleInfo, TransferStats } from '@/types/composables/data';
import { useExport } from './useExport';
import { useImport } from './useImport';
import { useTransferJobs } from './useTransferJobs';

export {
    formatFileSize,
    formatTransferDate,
    getTransferStatusLabel as getStatusLabel,
} from '@/services/utils/transfer';
export type { ExportFormat, ImportImage, TransferModule } from '@/types/composables/data';

export function useTransfer() {
    const { data: statsData, refetch: refetchStats } = useQuery({
        queryKey: TRANSFER_QUERY_KEYS.stats,
        queryFn: () => statsApi.getStats<TransferStats>(),
        staleTime: 1000 * 60 * 5,
    });

    const modules = computed<ModuleInfo[]>(() =>
        TRANSFER_MODULES.map((m) => ({
            ...m,
            count: statsData.value
                ? extractStatsCount(
                      (statsData.value as Record<string, unknown>)[m.key] as number | { count?: number } | undefined,
                  )
                : m.count,
        })),
    );

    const moduleOptions = computed(() =>
        modules.value.map((m) => ({
            value: m.key,
            label: `${m.name} (${m.count})`,
        })),
    );

    const { isLoadingJobs, recentJobs, refetchJobs } = useTransferJobs();

    const { isExporting, exportModules } = useExport({
        onSuccess: () => refetchJobs(),
    });

    const { isImporting, isPreviewing, importPreview, previewImport, importData, clearPreview } = useImport({
        onSuccess: () => refetchStats(),
    });

    return {
        isExporting,
        isImporting,
        isPreviewing,
        isLoadingJobs,
        importPreview,
        modules,
        moduleOptions,
        recentJobs,
        exportModules,
        previewImport,
        importData,
        clearPreview,
        refetchJobs,
        refetchStats,
    };
}
