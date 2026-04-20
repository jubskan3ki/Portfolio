import { dayjs } from '@/services/utils/date';

import type { JobStatus } from '@/types/composables/data';

export function formatFileSize(bytes: number): string {
    if (bytes < 1024) {
        return `${bytes} B`;
    }
    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
    }
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatTransferDate(date: string): string {
    return dayjs(date).format('D MMM HH:mm');
}

export function getTransferStatusLabel(status: JobStatus): string {
    const labels: Record<JobStatus, string> = {
        pending: 'En attente',
        validating: 'Validation',
        processing: 'En cours',
        completed: 'Terminé',
        partially_completed: 'Partiel',
        failed: 'Échoué',
    };
    return labels[status] || status;
}

export function extractStatsCount(val: number | { count?: number } | undefined): number {
    if (typeof val === 'number') {
        return val;
    }
    if (typeof val === 'object' && val !== null) {
        return val.count ?? 0;
    }
    return 0;
}
