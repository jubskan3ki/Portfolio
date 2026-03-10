import { useInfiniteQuery, useQueryClient, useMutation } from '@tanstack/vue-query';
import { computed, unref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';

import {
    httpClient,
    createKeys,
    CACHE_TIMES,
    createDetailQuery,
    createStaticQuery,
    createSubResourceMutations,
} from '../core';

import type { ProjectFilters } from '@/types/api/common';
import type {
    Project,
    ProjectDetail,
    ProjectCategory,
    ProjectStatus,
    ProjectsResponse,
    ProjectCategoriesResponse,
    ProjectStatusesResponse,
    ProjectStats,
    ProjectCreateData,
    ProjectUpdateData,
    ProjectCategoryCreateData,
    ProjectCategoryUpdateData,
    ProjectStatusCreateData,
    ProjectStatusUpdateData,
} from '@/types/feature/project';
import type { MaybeRef } from 'vue';

export const projectKeys = {
    ...createKeys('projects'),
    featured: () => ['projects', 'featured'] as const,
    byCategory: (slug: string) => ['projects', 'by-category', slug] as const,
    categories: () => ['projects', 'categories'] as const,
    category: (slug: string) => ['projects', 'category', slug] as const,
    statuses: () => ['projects', 'statuses'] as const,
    status: (id: string | number) => ['projects', 'status', id] as const,
    stats: () => ['projects', 'stats'] as const,
    infinite: (filters?: Omit<ProjectFilters, 'page'>) => ['projects', 'infinite', filters] as const,
};

export const projectsApi = {
    getAll: (filters?: ProjectFilters): Promise<ProjectsResponse> =>
        httpClient.get(API_ENDPOINTS.PROJECTS.BASE, filters as Record<string, unknown>),

    getBySlug: (slug: string): Promise<ProjectDetail> => httpClient.get(API_ENDPOINTS.PROJECTS.DETAIL(slug)),

    getByCategory: (categorySlug: string, filters?: ProjectFilters): Promise<ProjectsResponse> =>
        httpClient.get(API_ENDPOINTS.PROJECTS.BY_CATEGORY(categorySlug), filters as Record<string, unknown>),

    getFeatured: (limit = 6): Promise<Project[]> => httpClient.get(API_ENDPOINTS.PROJECTS.FEATURED, { limit }),

    create: (data: ProjectCreateData): Promise<ProjectDetail> => httpClient.post(API_ENDPOINTS.PROJECTS.BASE, data),

    update: (slug: string, data: ProjectUpdateData): Promise<ProjectDetail> =>
        httpClient.patch(API_ENDPOINTS.PROJECTS.DETAIL(slug), data),

    delete: (slug: string): Promise<void> => httpClient.delete(API_ENDPOINTS.PROJECTS.DETAIL(slug)),

    getCategories: (): Promise<ProjectCategoriesResponse> => httpClient.get(API_ENDPOINTS.PROJECTS.CATEGORIES),

    getCategory: (slug: string): Promise<ProjectCategory> =>
        httpClient.get(API_ENDPOINTS.PROJECTS.CATEGORY_DETAIL(slug)),

    createCategory: (data: ProjectCategoryCreateData): Promise<ProjectCategory> =>
        httpClient.post(API_ENDPOINTS.PROJECTS.CATEGORIES, data),

    updateCategory: (slug: string, data: ProjectCategoryUpdateData): Promise<ProjectCategory> =>
        httpClient.patch(API_ENDPOINTS.PROJECTS.CATEGORY_DETAIL(slug), data),

    deleteCategory: (slug: string): Promise<void> => httpClient.delete(API_ENDPOINTS.PROJECTS.CATEGORY_DETAIL(slug)),

    getStatuses: (): Promise<ProjectStatusesResponse> => httpClient.get(API_ENDPOINTS.PROJECTS.STATUSES),

    getStatus: (id: number | string): Promise<ProjectStatus> =>
        httpClient.get(API_ENDPOINTS.PROJECTS.STATUS_DETAIL(id)),

    createStatus: (data: ProjectStatusCreateData): Promise<ProjectStatus> =>
        httpClient.post(API_ENDPOINTS.PROJECTS.STATUSES, data),

    updateStatus: (id: number | string, data: ProjectStatusUpdateData): Promise<ProjectStatus> =>
        httpClient.patch(API_ENDPOINTS.PROJECTS.STATUS_DETAIL(id), data),

    deleteStatus: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.PROJECTS.STATUS_DETAIL(id)),

    recordView: (slug: string): Promise<void> => httpClient.post(API_ENDPOINTS.PROJECTS.VIEW(slug), {}),

    getStats: (): Promise<ProjectStats> => httpClient.get(API_ENDPOINTS.PROJECTS.STATS),

    // Admin methods
    getAdminList: <T = unknown>(params: Record<string, unknown>): Promise<T> =>
        httpClient.get(API_ENDPOINTS.PROJECTS.BASE, params),

    createWithForm: <T = ProjectDetail>(formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.PROJECTS.BASE, formData, 'POST'),

    updateWithForm: <T = ProjectDetail>(slug: string, formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.PROJECTS.DETAIL(slug), formData, 'PATCH'),
};

export function useInfiniteProjects(filters?: MaybeRef<Omit<ProjectFilters, 'page'>>, itemsPerPage = 6) {
    return useInfiniteQuery({
        queryKey: computed(() => projectKeys.infinite(unref(filters))),
        queryFn: ({ pageParam = 1 }) =>
            projectsApi.getAll({
                ...unref(filters),
                page: pageParam,
                limit: itemsPerPage,
            }),
        initialPageParam: 1,
        getNextPageParam: (lastPage) => {
            const { page, totalPages } = lastPage.pagination;
            return page < totalPages ? page + 1 : undefined;
        },
        staleTime: CACHE_TIMES.LIST,
    });
}

export function useProject(slug: MaybeRef<string>) {
    return createDetailQuery(
        computed(() => projectKeys.detail(unref(slug))),
        () => projectsApi.getBySlug(unref(slug)),
        { enabled: computed(() => !!unref(slug)) },
    );
}

export function useFeaturedProjects(limit = 6) {
    return createStaticQuery(projectKeys.featured(), () => projectsApi.getFeatured(limit));
}

export function useProjectCategories() {
    return createStaticQuery(projectKeys.categories(), projectsApi.getCategories);
}

export function useProjectStatuses() {
    return createStaticQuery(projectKeys.statuses(), projectsApi.getStatuses);
}

export function useProjectStats() {
    return createStaticQuery(projectKeys.stats(), projectsApi.getStats);
}

const categoryMutations = createSubResourceMutations<
    ProjectCategory,
    ProjectCategoryCreateData,
    ProjectCategoryUpdateData,
    string
>(
    {
        create: projectsApi.createCategory,
        update: projectsApi.updateCategory,
        delete: projectsApi.deleteCategory,
    },
    { all: projectKeys.categories },
    'slug',
);

export const useCreateProjectCategory = categoryMutations.useCreate;

export function useRecordProjectView() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: projectsApi.recordView,
        onSuccess: (_, slug) => {
            queryClient.invalidateQueries({
                queryKey: projectKeys.detail(slug),
                refetchType: 'active',
            });
        },
    });
}
