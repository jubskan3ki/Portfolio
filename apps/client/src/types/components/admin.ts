// Types for Admin components

import type { ActivityType, DashboardModuleStats } from '@/types/api/stats';
import type { JobStatus, TransferModule } from '@/types/api/transfer';
import type { ListParams } from '@/types/composables';
import type { DataItem, Session } from '@/types/feature/admin';

// SessionItem

export type { DataItem };

export type SortOrder = 'asc' | 'desc';

export interface DataTableColumn {
    key: string;
    label: string;
    sortable?: boolean;
    width?: string;
    class?: string;
    skeletonWidth?: string;
    format?: (value: unknown) => string;
}

export interface DataTableFilter {
    key: string;
    label: string;
    options: Array<{ value: string; label: string }>;
}

export interface DataTableProps {
    data: DataItem[];
    columns: DataTableColumn[];
    loading?: boolean;
    selectable?: boolean;
    itemKey?: string;
    sortBy?: string;
    sortOrder?: SortOrder;
    searchPlaceholder?: string;
    emptyMessage?: string;
    showToolbar?: boolean;
    showPagination?: boolean;
    currentPage?: number;
    totalItems?: number;
    perPage?: number;
    perPageOptions?: number[];
    filters?: DataTableFilter[];
    skeletonRows?: number;
}

export interface QueryChangePayload {
    search?: string;
    filters?: Record<string, string>;
}

export interface PaginationChangePayload {
    page?: number;
    perPage?: number;
}

// StatsCard
export interface StatsCardProps {
    label: string;
    value: string | number;
    icon: string;
    trend?: string;
    color?: string;
    loading?: boolean;
}

interface Activity {
    id: number;
    type: ActivityType;
    text: string;
    date: Date;
}

export interface ActivityFeedProps {
    activities: Activity[];
    loading?: boolean;
}

export interface EntityFormProps {
    id?: string;
}

export type ArticleFormProps = EntityFormProps;
export type ProjectFormProps = EntityFormProps;
export type StackFormProps = EntityFormProps;
export type ExperienceFormProps = EntityFormProps;

// Transfer (Export / Import / Jobs)

export interface TransferModuleInfo {
    key: TransferModule;
    name: string;
    icon: string;
    count: number;
}

export interface TransferJob {
    id: string | number;
    type: 'export' | 'import';
    module: string;
    status: JobStatus;
    createdAt: string;
    downloadUrl?: string;
}

export interface ImportProgressProps {
    isImporting: boolean;
    canImport: boolean;
    imagesCount: number;
    updateExisting: boolean;
    skipErrors: boolean;
}

export interface ImageItem {
    id: string;
    file: File;
    preview: string;
    key: string;
    error?: string;
}

export interface FilePreviewListProps {
    show: boolean;
    images: ImageItem[];
}

export interface FileDropZoneProps {
    accept?: string;
    acceptLabel?: string;
    maxSize?: number;
    multiple?: boolean;
    placeholderText?: string;
    placeholderIcon?: string;
    error?: string | null;
    file?: File | null;
    id?: string;
}

export interface SessionItemProps {
    session: Session;
    isRevoking?: boolean;
}

export interface SessionItemEmits {
    (e: 'revoke', sessionId: string): void;
}

// AdminFormLayout

export interface AdminFormLayoutProps {
    title: string;
    subtitle?: string;
    loading?: boolean;
    loadingText?: string;
    error?: string;
    errorTitle?: string;
    errorIcon?: string;
    showRetry?: boolean;
    backUrl: string;
    backText?: string;
    cancelText?: string;
    submitText?: string;
    submittingText?: string;
    submitting?: boolean;
    submitDisabled?: boolean;
}

// AdminListPage (generic)

export interface AdminListPageProps<T> {
    // Page header
    title: string;
    subtitle: string;
    createRoute: string;
    createLabel?: string;

    // SEO
    seoTitle: string;
    seoDescription: string;

    // Table
    columns: DataTableColumn[];

    // Data fetching (useDataList config)
    queryKey: string[];
    queryFn: (params: ListParams) => Promise<unknown>;
    deleteFn?: (item: T) => Promise<void>;
    defaultSort?: string;
    defaultSortOrder?: 'asc' | 'desc';
    sortFieldMap?: Record<string, string>;

    // Navigation
    editRoute: (item: T) => string;
    viewRoute?: (item: T) => string;
    showView?: boolean;

    // Type guard for casting DataItem -> T
    typeGuard: (item: DataItem) => T;

    // Delete messages
    deleteTitle?: string;
    deleteMessage?: (item: T) => string;
    bulkDeleteTitle?: string;
    bulkDeleteMessage?: (count: number) => string;

    // Alert messages
    resourceName: string;
}

// Admin Dashboard Props

export interface DashboardTopItem {
    id: number;
    title: string;
    slug: string;
    views: number;
    category?: string;
    level?: number;
    type: 'article' | 'project' | 'stack';
}

export interface DashboardTopContentProps {
    articles: DashboardTopItem[];
    projects: DashboardTopItem[];
    stacks: DashboardTopItem[];
    loading?: boolean;
}

export interface DashboardDistributionItem {
    label: string;
    count: number;
    color: string;
}

export interface DashboardDonutChartProps {
    distribution: DashboardDistributionItem[];
}

export interface DashboardHeaderProps {
    userName?: string;
    isRefreshing?: boolean;
}

export interface DashboardActivity {
    id: number;
    type: string;
    text: string;
    date: Date;
}

export interface DashboardActivityFeedProps {
    activities: DashboardActivity[];
    loading?: boolean;
}

export interface DashboardViewData {
    date: string;
    views: number;
}

export interface DashboardViewsChartProps {
    data: DashboardViewData[];
    totalViews?: number;
}

export interface DashboardStatsGridProps {
    stats: DashboardModuleStats | null;
    loading?: boolean;
}
