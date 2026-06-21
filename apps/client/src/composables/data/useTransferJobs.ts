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
        queryFn: async ({ signal }): Promise<TransferJob[]> => {
            // Le backend renvoie { exports, imports } : on fusionne et on trie par date décroissante.
            const response = await transferApi.getJobs(signal);
            const raw = [...(response.exports ?? []), ...(response.imports ?? [])] as unknown as Array<
                ExportJob | ImportJob
            >;
            raw.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

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
        staleTime: 1000 * 30,
    });

    const recentJobs = computed<TransferJob[]>(() => jobsData.value ?? []);

    return {
        jobsData,
        isLoadingJobs,
        recentJobs,
        refetchJobs,
    };
}
