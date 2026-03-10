import { useQuery } from '@tanstack/vue-query';
import { computed } from 'vue';

import { TRANSFER_QUERY_KEYS } from '@/config/transfer';
import { transferApi } from '@/services/api/modules/transfer';

import type { ExportJob, ImportJob, TransferJob } from '@/types/composables/data';

function inferJobType(job: ExportJob | ImportJob): 'export' | 'import' {
    return 'format' in job ? 'export' : 'import';
}

export function useTransferJobs() {
    const {
        data: jobsData,
        isLoading: isLoadingJobs,
        refetch: refetchJobs,
    } = useQuery({
        queryKey: TRANSFER_QUERY_KEYS.jobs,
        queryFn: async (): Promise<TransferJob[]> => {
            const response = (await transferApi.getJobs()) as unknown as
                | { results?: Array<ExportJob | ImportJob> }
                | Array<ExportJob | ImportJob>;
            const raw = Array.isArray(response) ? response : (response.results ?? []);

            // Normalize to TransferJob with explicit type discriminant (single place for duck-typing)
            return raw.slice(0, 10).map((job): TransferJob => {
                const type = inferJobType(job);
                return {
                    id: job.id,
                    type,
                    module: job.module,
                    status: job.status,
                    createdAt: job.createdAt,
                    completedAt: job.completedAt,
                    downloadUrl: type === 'export' ? (job as ExportJob).downloadUrl : undefined,
                };
            });
        },
        staleTime: 1000 * 30, // 30 seconds
    });

    const recentJobs = computed<TransferJob[]>(() => jobsData.value ?? []);

    return {
        jobsData,
        isLoadingJobs,
        recentJobs,
        refetchJobs,
    };
}
