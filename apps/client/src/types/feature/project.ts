// Project Types
import type { PaginatedResponse } from '@/types/api/common';

// Note: Import PaginatedResponse directly from @/types/api/common

// Type pour un projet (liste)
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
    views: number;
}

// Type pour un projet (detail)
export interface ProjectDetail extends Project {
    longDescription: string;
    features: string[];
    links: {
        demo?: string;
        github?: string;
        documentation?: string;
    };
}

// Type pour une categorie de projets
export interface ProjectCategory {
    id: number;
    name: string;
    description: string;
    slug: string;
    count: number;
}

// Type pour un statut de projet
export interface ProjectStatus {
    id: number;
    name: string;
    description: string;
}

// API Response Types
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

// API Request Types (Create/Update)

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

// Props pour ProjectCard
export interface ProjectCardProps {
    project: Project;
    featured?: boolean;
    hoverable?: boolean;
    flat?: boolean;
    descriptionLength?: number;
    maxTechnologies?: number;
    customClass?: string;
}

// Filter option pour ProjectList
interface ProjectFilterOption {
    label: string;
    value: string;
}

// Props pour ProjectList
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

// Props pour ProjectCarousel
export interface ProjectCarouselProps {
    limit?: number;
    autoplay?: boolean;
}
