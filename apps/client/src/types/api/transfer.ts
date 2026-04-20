export type TransferModule = 'articles' | 'projects' | 'stacks' | 'experiences' | 'contacts';
export type ExportFormat = 'json' | 'csv' | 'xlsx';
export type JobStatus = 'pending' | 'validating' | 'processing' | 'completed' | 'partially_completed' | 'failed';

export interface ExportJob {
    id: string;
    module: TransferModule;
    format: ExportFormat;
    status: JobStatus;
    fileUrl?: string;
    error?: string;
    createdAt: string;
    completedAt?: string;
}

export interface BulkExportResult {
    jobs: ExportJob[];
}

export interface ImportJob {
    id: string;
    module: TransferModule;
    status: JobStatus;
    totalRecords: number;
    importedRecords: number;
    failedRecords: number;
    errors?: string[];
    createdAt: string;
    completedAt?: string;
}

export interface ImportPreview {
    module: TransferModule;
    totalRecords: number;
    validRecords: number;
    invalidRecords: number;
    preview: Array<Record<string, unknown>>;
    warnings?: string[];
    errors?: string[];
}

export interface BulkImportResult {
    jobs: ImportJob[];
}

export interface TransferJobsResponse {
    exports: ExportJob[];
    imports: ImportJob[];
}

export interface CleanupJobsResponse {
    deleted: number;
}
