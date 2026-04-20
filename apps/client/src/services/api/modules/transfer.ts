import { API_ENDPOINTS } from '@/config/api';

import { httpClient, createKeys } from '../core';

import type {
    TransferModule,
    ExportFormat,
    ExportJob,
    BulkExportResult,
    BulkImportResult,
    TransferJobsResponse,
    CleanupJobsResponse,
} from '@/types/api/transfer';
import type { ImportJob, ImportPreview } from '@/types/composables/data/transfer';

export const transferKeys = {
    ...createKeys('transfer'),
    jobs: () => ['transfer', 'jobs'] as const,
    exportJob: (jobId: string) => ['transfer', 'export-job', jobId] as const,
    importJob: (jobId: string) => ['transfer', 'import-job', jobId] as const,
};

export const transferApi = {
    exportModule: (module: TransferModule, format: ExportFormat = 'json'): Promise<ExportJob> =>
        httpClient.get(API_ENDPOINTS.TRANSFER.EXPORT_MODULE(module), { export_format: format }),

    downloadExport: (module: TransferModule, format: ExportFormat = 'json'): Promise<Blob> =>
        httpClient.downloadBlob(API_ENDPOINTS.TRANSFER.EXPORT_DOWNLOAD(module), { export_format: format }),

    bulkExport: (): Promise<BulkExportResult> => httpClient.get(API_ENDPOINTS.TRANSFER.EXPORT_BULK),

    importModule: (module: TransferModule, file: File, updateExisting = false): Promise<ImportJob> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('update_existing', String(updateExisting));
        return httpClient.uploadForm(API_ENDPOINTS.TRANSFER.IMPORT_MODULE(module), formData);
    },

    previewImport: (module: TransferModule, file: File): Promise<ImportPreview> => {
        const formData = new FormData();
        formData.append('file', file);
        return httpClient.uploadForm(API_ENDPOINTS.TRANSFER.IMPORT_PREVIEW(module), formData);
    },

    bulkImport: (files: Array<{ module: TransferModule; file: File }>): Promise<BulkImportResult> => {
        const formData = new FormData();
        files.forEach(({ module, file }) => {
            formData.append(module, file);
        });
        return httpClient.uploadForm(API_ENDPOINTS.TRANSFER.IMPORT_BULK, formData);
    },

    getJobs: (): Promise<TransferJobsResponse> => httpClient.get(API_ENDPOINTS.TRANSFER.JOBS),

    getExportJob: (jobId: string): Promise<ExportJob> => httpClient.get(API_ENDPOINTS.TRANSFER.EXPORT_JOB(jobId)),

    getImportJob: (jobId: string): Promise<ImportJob> => httpClient.get(API_ENDPOINTS.TRANSFER.IMPORT_JOB(jobId)),

    cleanupJobs: (): Promise<CleanupJobsResponse> => httpClient.delete(API_ENDPOINTS.TRANSFER.JOBS_CLEANUP),

    importWithImages: (module: TransferModule, formData: FormData): Promise<ImportJob> =>
        httpClient.uploadForm(API_ENDPOINTS.TRANSFER.IMPORT_MODULE(module), formData, 'POST'),

    downloadBulk: (params: Record<string, unknown>): Promise<Blob> =>
        httpClient.downloadBlob(API_ENDPOINTS.TRANSFER.EXPORT_BULK, params),

    downloadModuleExport: (module: TransferModule, params?: Record<string, unknown>): Promise<Blob> =>
        httpClient.downloadBlob(API_ENDPOINTS.TRANSFER.EXPORT_DOWNLOAD(module), params),
};
