import type { MaybeRef } from 'vue';
import { computed, unref } from 'vue';
import { API_ENDPOINTS } from '@/config/api';

import type { PaginatedResponse, StackFilters } from '@/types/api/common';
import type { Article } from '@/types/feature/blog';
import type { Project } from '@/types/feature/project';
import type {
    RelatedStack,
    Stack,
    StackCategory,
    StackCategoryCreateData,
    StackCategoryUpdateData,
    StackCreateData,
    StackDetail,
    StackResource,
    StackResourceCreateData,
    StackResourceFilters,
    StackResourceUpdateData,
    StackStats,
    StackUpdateData,
} from '@/types/feature/stacks';
import type { QueryOptions } from '@/types/services/api';
import {
    createDetailQuery,
    createKeys,
    createListQuery,
    createStaticQuery,
    createSubResourceMutations,
    httpClient,
} from '../core';

export const stackKeys = {
    ...createKeys('stacks'),
    byCategory: (name: string) => ['stacks', 'by-category', name] as const,
    related: (slug: string) => ['stacks', 'related', slug] as const,
    featured: (limit: number) => ['stacks', 'featured', limit] as const,
    categories: () => ['stacks', 'categories'] as const,
    category: (name: string) => ['stacks', 'category', name] as const,
    resources: () => ['stacks', 'resources'] as const,
    resource: (id: string | number) => ['stacks', 'resource', id] as const,
    stats: () => ['stacks', 'stats'] as const,
    projects: (slug: string) => ['stacks', 'projects', slug] as const,
    articles: (slug: string) => ['stacks', 'articles', slug] as const,
};

export const stacksApi = {
    getAll: (filters?: StackFilters, signal?: AbortSignal): Promise<PaginatedResponse<Stack>> =>
        httpClient.get(API_ENDPOINTS.STACKS.BASE, filters as Record<string, unknown>, signal),

    getBySlug: (slug: string, signal?: AbortSignal): Promise<StackDetail> =>
        httpClient.get(API_ENDPOINTS.STACKS.DETAIL(slug), undefined, signal),

    getByCategory: async (categoryName: string, filters?: StackFilters): Promise<Stack[]> => {
        const response: PaginatedResponse<Stack> = await httpClient.get(
            API_ENDPOINTS.STACKS.BY_CATEGORY(categoryName),
            filters as Record<string, unknown>,
        );
        return response.data;
    },

    getRelated: (slug: string): Promise<RelatedStack[]> => httpClient.get(API_ENDPOINTS.STACKS.RELATED(slug)),

    create: (data: StackCreateData): Promise<StackDetail> => httpClient.post(API_ENDPOINTS.STACKS.BASE, data),

    update: (slug: string, data: StackUpdateData): Promise<StackDetail> =>
        httpClient.patch(API_ENDPOINTS.STACKS.DETAIL(slug), data),

    delete: (slug: string): Promise<void> => httpClient.delete(API_ENDPOINTS.STACKS.DETAIL(slug)),

    getCategories: (signal?: AbortSignal): Promise<StackCategory[]> =>
        httpClient.get(API_ENDPOINTS.STACKS.CATEGORIES, undefined, signal),

    getCategory: (name: string): Promise<StackCategory> => httpClient.get(API_ENDPOINTS.STACKS.CATEGORY_DETAIL(name)),

    createCategory: (data: StackCategoryCreateData): Promise<StackCategory> =>
        httpClient.post(API_ENDPOINTS.STACKS.CATEGORIES, data),

    updateCategory: (name: string, data: StackCategoryUpdateData): Promise<StackCategory> =>
        httpClient.patch(API_ENDPOINTS.STACKS.CATEGORY_DETAIL(name), data),

    deleteCategory: (name: string): Promise<void> => httpClient.delete(API_ENDPOINTS.STACKS.CATEGORY_DETAIL(name)),

    getResources: (filters?: StackResourceFilters): Promise<StackResource[]> =>
        httpClient.get(API_ENDPOINTS.STACKS.RESOURCES, filters as Record<string, unknown>),

    getResource: (id: number | string): Promise<StackResource> =>
        httpClient.get(API_ENDPOINTS.STACKS.RESOURCE_DETAIL(id)),

    createResource: (data: StackResourceCreateData): Promise<StackResource> =>
        httpClient.post(API_ENDPOINTS.STACKS.RESOURCES, data),

    updateResource: (id: number | string, data: StackResourceUpdateData): Promise<StackResource> =>
        httpClient.patch(API_ENDPOINTS.STACKS.RESOURCE_DETAIL(id), data),

    deleteResource: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.STACKS.RESOURCE_DETAIL(id)),

    getStats: (signal?: AbortSignal): Promise<StackStats> =>
        httpClient.get(API_ENDPOINTS.STACKS.STATS, undefined, signal),

    getProjects: async (slug: string, signal?: AbortSignal): Promise<Project[]> => {
        const response: PaginatedResponse<Project> = await httpClient.get(
            API_ENDPOINTS.STACKS.PROJECTS(slug),
            undefined,
            signal,
        );
        return response.data;
    },

    getArticles: async (slug: string, signal?: AbortSignal): Promise<Article[]> => {
        const response: PaginatedResponse<Article> = await httpClient.get(
            API_ENDPOINTS.STACKS.ARTICLES(slug),
            undefined,
            signal,
        );
        return response.data;
    },

    getFeatured: async (limit = 10, signal?: AbortSignal): Promise<Stack[]> => {
        const response = await httpClient.get<PaginatedResponse<Stack>>(
            API_ENDPOINTS.STACKS.BASE,
            { limit } as Record<string, unknown>,
            signal,
        );
        return response.data ?? [];
    },

    getAdminList: <T = unknown>(params: Record<string, unknown>): Promise<T> =>
        httpClient.get(API_ENDPOINTS.STACKS.BASE, params),

    createWithForm: <T = StackDetail>(formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.STACKS.BASE, formData, 'POST'),

    updateWithForm: <T = StackDetail>(slug: string, formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.STACKS.DETAIL(slug), formData, 'PATCH'),
};

export function useStacks(filters?: MaybeRef<StackFilters>) {
    return createListQuery(
        computed(() => stackKeys.list(unref(filters))),
        ({ signal }) => stacksApi.getAll(unref(filters), signal),
        { placeholderData: (prev: PaginatedResponse<Stack> | undefined) => prev },
    );
}

export function useStack(slug: MaybeRef<string>) {
    return createDetailQuery(
        computed(() => stackKeys.detail(unref(slug))),
        ({ signal }) => stacksApi.getBySlug(unref(slug), signal),
        { enabled: computed(() => !!unref(slug)) },
    );
}

export function useFeaturedStacks(limit = 10, options?: QueryOptions<Stack[]>) {
    return createListQuery(stackKeys.featured(limit), ({ signal }) => stacksApi.getFeatured(limit, signal), options);
}

export function useStackCategories() {
    return createStaticQuery(stackKeys.categories(), ({ signal }) => stacksApi.getCategories(signal));
}

export function useStackStats() {
    return createStaticQuery(stackKeys.stats(), ({ signal }) => stacksApi.getStats(signal));
}

const categoryMutations = createSubResourceMutations<
    StackCategory,
    StackCategoryCreateData,
    StackCategoryUpdateData,
    string
>(
    {
        create: stacksApi.createCategory,
        update: stacksApi.updateCategory,
        delete: stacksApi.deleteCategory,
    },
    { all: stackKeys.categories },
    'name',
);

export const useCreateStackCategory = categoryMutations.useCreate;

export function useStackProjects(slug: MaybeRef<string>) {
    return createListQuery(
        computed(() => stackKeys.projects(unref(slug))),
        ({ signal }) => stacksApi.getProjects(unref(slug), signal),
        { enabled: computed(() => !!unref(slug)) },
    );
}

export function useStackArticles(slug: MaybeRef<string>) {
    return createListQuery(
        computed(() => stackKeys.articles(unref(slug))),
        ({ signal }) => stacksApi.getArticles(unref(slug), signal),
        { enabled: computed(() => !!unref(slug)) },
    );
}
