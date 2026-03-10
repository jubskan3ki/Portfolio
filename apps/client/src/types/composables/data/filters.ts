// Filter types

export interface FilterFieldConfig<T = unknown> {
    default: T;
    urlKey?: string;
    resetOnChange?: boolean;
}

export interface FilterPaginationConfig {
    enabled: boolean;
    pageKey?: string;
    itemsPerPage?: number;
    limitKey?: string;
}

export interface FilterUrlSyncConfig {
    enabled: boolean;
    debounceMs?: number;
}

export interface UseFiltersOptions<T extends Record<string, unknown>> {
    defaults: T;
    fieldConfig?: Partial<Record<keyof T, Partial<FilterFieldConfig>>>;
    pagination?: FilterPaginationConfig;
    urlSync?: FilterUrlSyncConfig;
    searchDebounceMs?: number;
}

// Filter Presets Types (domain-specific filters)

export interface BlogFilters {
    category: string;
    tags: string[];
    search: string;
    ordering: string;
    [key: string]: unknown;
}

export interface ProjectListFilters {
    category: string;
    status: string;
    technologies: string[];
    search: string;
    ordering: string;
    [key: string]: unknown;
}

export interface StackListFilters {
    category: string;
    search: string;
    ordering: string;
    [key: string]: unknown;
}

export interface ExperienceListFilters {
    type: string;
    search: string;
    ordering: string;
    [key: string]: unknown;
}
