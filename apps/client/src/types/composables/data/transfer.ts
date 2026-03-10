import type { TransferModule, ExportFormat, JobStatus } from '@/types/api/transfer';
import type { Ref } from 'vue';

// Re-export base types from api/transfer for consistency
export type { TransferModule, ExportFormat, JobStatus } from '@/types/api/transfer';

export interface ModuleInfo {
    key: TransferModule;
    name: string;
    icon: string;
    count: number;
}

export interface ExportJob {
    id: string;
    module: TransferModule;
    format: ExportFormat;
    status: JobStatus;
    recordsCount: number;
    errorMessage?: string;
    downloadUrl?: string;
    createdAt: string;
    completedAt?: string;
}

export interface ImportJob {
    id: string;
    module: TransferModule;
    status: JobStatus;
    originalFilename: string;
    fileFormat: string;
    totalRecords: number;
    processedRecords: number;
    successCount: number;
    errorCount: number;
    errors?: ImportError[];
    progress: number;
    createdAt: string;
    completedAt?: string;
}

export interface TransferJob {
    id: string;
    type: 'export' | 'import';
    module: TransferModule;
    status: JobStatus;
    createdAt: string;
    completedAt?: string;
    downloadUrl?: string;
}

export interface ImportError {
    row: number;
    field: string;
    message: string;
}

export interface ImportImage {
    key: string;
    file: File;
}

export interface ImportPreview {
    totalRecords: number;
    previewData: Array<Record<string, unknown>>;
    columns: string[];
    validationErrors: ImportError[];
    fileFormat: string;
    validCount: number;
}

export interface TransferStats {
    articles?: number | { count?: number };
    projects?: number | { count?: number };
    stacks?: number | { count?: number };
    experiences?: number | { count?: number };
}

// useExport

export interface UseExportOptions {
    onSuccess?: () => void;
}

// useImport

export interface UseImportOptions {
    onSuccess?: () => void;
}

// useViewRecording

export interface UseViewRecordingReturn {
    viewRecorded: Ref<boolean>;
}
