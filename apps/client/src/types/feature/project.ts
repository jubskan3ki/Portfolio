import type { PaginatedResponse } from '@/types/api/common';

export interface Project {
    id: number;
    title: string;
    slug: string;
    description: string;
    image: string;
    category: string;
    status: string;
    technologies: string[];
    date: string;
    updatedAt?: string;
    views: number;
}

export interface ProjectDetail extends Project {
    longDescription: string;
    features: string[];
    links: {
        demo?: string;
        github?: string;
        documentation?: string;
    };
    seoTitle?: string;
    metaDescription?: string;
}

export interface ProjectCategory {
    id: number;
    name: string;
    description: string;
    slug: string;
    count: number;
}

export interface ProjectStatus {
    id: number;
    name: string;
    description: string;
}

export type ProjectsResponse = PaginatedResponse<Project>;
export type ProjectCategoriesResponse = PaginatedResponse<ProjectCategory>;
export type ProjectStatusesResponse = PaginatedResponse<ProjectStatus>;

export interface ProjectStats {
    totalProjects: number;
    projectsByCategory: Array<{ category: string; count: number }>;
    projectsByStatus: Array<{ status: string; count: number }>;
    averageProjectsPerYear: number;
    totalViews: number;
    mostViewedProjects: Array<{ title: string; views: number }>;
    projectsByYear: Array<{ year: number; count: number }>;
    projectsByMonth: Array<{ month: string; count: number }>;
}

export interface ProjectCreateData {
    title: string;
    description: string;
    longDescription?: string;
    image?: string;
    category: string | number;
    status?: string | number;
    technologies?: string[];
    features?: string[];
    links?: {
        demo?: string;
        github?: string;
        documentation?: string;
    };
}

export type ProjectUpdateData = Partial<ProjectCreateData>;

export interface ProjectCategoryCreateData {
    name: string;
    slug?: string;
    description?: string;
}

export type ProjectCategoryUpdateData = Partial<ProjectCategoryCreateData>;

export interface ProjectStatusCreateData {
    name: string;
    description?: string;
}

export type ProjectStatusUpdateData = Partial<ProjectStatusCreateData>;

export interface ProjectCardProps {
    project: Project;
    featured?: boolean;
    hoverable?: boolean;
    flat?: boolean;
    descriptionLength?: number;
    maxTechnologies?: number;
    customClass?: string;
}

interface ProjectFilterOption {
    label: string;
    value: string;
}

export interface ProjectListProps {
    projects?: Project[];
    layout?: 'grid' | 'list' | 'compact';
    featuredProjects?: Array<string | number>;
    showFilters?: boolean;
    categoryFilters?: ProjectFilterOption[];
    filterLabel?: string;
    allFilterLabel?: string;
    loading?: boolean;
    error?: string;
    retryable?: boolean;
    retryText?: string;
    loadingText?: string;
    emptyTitle?: string;
    emptyDescription?: string;
    currentPage?: number;
    totalPages?: number;
    showPagination?: boolean;
    cardHoverable?: boolean;
    cardFlat?: boolean;
    cardBordered?: boolean;
    descriptionLength?: number;
    maxTechnologies?: number;
    customClass?: string;
}

export interface ProjectCarouselProps {
    limit?: number;
    autoplay?: boolean;
}
