// Types for Admin components

import type { ActivityType } from '@/types/api/stats';
import type { DataItem } from '@/types/feature/admin';

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
