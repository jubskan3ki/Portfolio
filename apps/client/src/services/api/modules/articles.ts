import { useQueryClient, useMutation } from '@tanstack/vue-query';
import { computed, unref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';

import {
    httpClient,
    createKeys,
    createListQuery,
    createDetailQuery,
    createStaticQuery,
    createSubResourceMutations,
} from '../core';

import type { ArticleFilters } from '@/types/api/common';
import type {
    Article,
    ArticleDetail,
    Category,
    Tag,
    ArticlesResponse,
    ArticleCreateData,
    ArticleUpdateData,
    CategoryCreateData,
    CategoryUpdateData,
    TagCreateData,
    TagUpdateData,
} from '@/types/feature/blog';
import type { QueryOptions } from '@/types/services/api';
import type { MaybeRef } from 'vue';

export const articleKeys = {
    ...createKeys('articles'),
    featured: () => ['articles', 'featured'] as const,
    popular: (limit: number) => ['articles', 'popular', limit] as const,
    recent: (limit: number) => ['articles', 'recent', limit] as const,
    byCategory: (slug: string) => ['articles', 'by-category', slug] as const,
    byTag: (name: string) => ['articles', 'by-tag', name] as const,
    related: (slug: string) => ['articles', 'related', slug] as const,
    categories: () => ['articles', 'categories'] as const,
    tags: () => ['articles', 'tags'] as const,
};

export const articlesApi = {
    // Manual filter transformation: backend articles expects sortBy/sortDirection (not ordering)
    // and tag (singular, comma-separated) instead of tags[]. Other modules (projects, stacks)
    // use django-filter which accepts filters directly — this difference is intentional.
    getAll: (filters?: ArticleFilters): Promise<ArticlesResponse> => {
        if (!filters) {
            return httpClient.get(API_ENDPOINTS.ARTICLES.BASE);
        }

        const params: Record<string, unknown> = {};

        if (filters.category) {
            params.category = filters.category;
        }
        if (filters.search) {
            params.search = filters.search;
        }
        if (filters.page) {
            params.page = filters.page;
        }
        if (filters.limit) {
            params.limit = filters.limit;
        }

        // Transform ordering (-date) to sortBy/sortDirection for backend
        const ordering = (filters as Record<string, unknown>).ordering as string | undefined;
        if (ordering) {
            const desc = ordering.startsWith('-');
            params.sortBy = desc ? ordering.slice(1) : ordering;
            params.sortDirection = desc ? 'desc' : 'asc';
        } else if (filters.sortBy) {
            params.sortBy = filters.sortBy;
            params.sortDirection = filters.sortDirection || 'desc';
        }

        // Transform tags array to single comma-separated tag param
        if (filters.tags?.length) {
            params.tag = filters.tags.join(',');
        }

        return httpClient.get(API_ENDPOINTS.ARTICLES.BASE, params);
    },

    getBySlug: (slug: string): Promise<ArticleDetail> => httpClient.get(API_ENDPOINTS.ARTICLES.DETAIL(slug)),

    getFeatured: (): Promise<Article[]> => httpClient.get(API_ENDPOINTS.ARTICLES.FEATURED),

    getPopular: (limit = 5): Promise<Article[]> => httpClient.get(API_ENDPOINTS.ARTICLES.POPULAR, { limit }),

    getByCategory: async (categorySlug: string): Promise<Article[]> => {
        const response: ArticlesResponse = await httpClient.get(API_ENDPOINTS.ARTICLES.BY_CATEGORY(categorySlug));
        return response.data;
    },

    getByTag: async (tagName: string): Promise<Article[]> => {
        const response: ArticlesResponse = await httpClient.get(API_ENDPOINTS.ARTICLES.BY_TAG(tagName));
        return response.data;
    },

    getRelated: (slug: string): Promise<Article[]> => httpClient.get(API_ENDPOINTS.ARTICLES.RELATED(slug)),

    recordView: (slug: string): Promise<void> => httpClient.post(API_ENDPOINTS.ARTICLES.VIEW(slug), {}),

    getRecent: async (limit = 5): Promise<Article[]> => {
        const response = await httpClient.get<ArticlesResponse>(API_ENDPOINTS.ARTICLES.BASE, {
            limit,
            sortBy: 'date',
            sortDirection: 'desc',
        });
        return response.data ?? [];
    },

    create: (data: ArticleCreateData): Promise<ArticleDetail> => httpClient.post(API_ENDPOINTS.ARTICLES.BASE, data),

    update: (slug: string, data: ArticleUpdateData): Promise<ArticleDetail> =>
        httpClient.patch(API_ENDPOINTS.ARTICLES.DETAIL(slug), data),

    delete: (slug: string): Promise<void> => httpClient.delete(API_ENDPOINTS.ARTICLES.DETAIL(slug)),

    getCategories: (): Promise<Category[]> => httpClient.get(API_ENDPOINTS.ARTICLES.CATEGORIES),

    getCategory: (slug: string): Promise<Category> => httpClient.get(API_ENDPOINTS.ARTICLES.CATEGORY_DETAIL(slug)),

    createCategory: (data: CategoryCreateData): Promise<Category> =>
        httpClient.post(API_ENDPOINTS.ARTICLES.CATEGORIES, data),

    updateCategory: (slug: string, data: CategoryUpdateData): Promise<Category> =>
        httpClient.patch(API_ENDPOINTS.ARTICLES.CATEGORY_DETAIL(slug), data),

    deleteCategory: (slug: string): Promise<void> => httpClient.delete(API_ENDPOINTS.ARTICLES.CATEGORY_DETAIL(slug)),

    getTags: (): Promise<Tag[]> => httpClient.get(API_ENDPOINTS.ARTICLES.TAGS),

    getTag: (name: string): Promise<Tag> => httpClient.get(API_ENDPOINTS.ARTICLES.TAG_DETAIL(name)),

    createTag: (data: TagCreateData): Promise<Tag> => httpClient.post(API_ENDPOINTS.ARTICLES.TAGS, data),

    updateTag: (name: string, data: TagUpdateData): Promise<Tag> =>
        httpClient.patch(API_ENDPOINTS.ARTICLES.TAG_DETAIL(name), data),

    deleteTag: (name: string): Promise<void> => httpClient.delete(API_ENDPOINTS.ARTICLES.TAG_DETAIL(name)),

    // Admin methods
    getAdminList: <T = unknown>(params: Record<string, unknown>): Promise<T> =>
        httpClient.get(API_ENDPOINTS.ARTICLES.BASE, params),

    createWithForm: <T = ArticleDetail>(formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.ARTICLES.BASE, formData, 'POST'),

    updateWithForm: <T = ArticleDetail>(slug: string, formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.ARTICLES.DETAIL(slug), formData, 'PATCH'),

    togglePublish: (slug: string, isPublished: boolean): Promise<ArticleDetail> =>
        httpClient.patch(API_ENDPOINTS.ARTICLES.DETAIL(slug), { isPublished }),
};

export function useArticles(filters?: MaybeRef<ArticleFilters>) {
    return createListQuery(
        computed(() => articleKeys.list(unref(filters))),
        () => articlesApi.getAll(unref(filters)),
        {
            placeholderData: (prev: ArticlesResponse | undefined) => prev,
        },
    );
}

export function useArticle(slug: MaybeRef<string>) {
    return createDetailQuery(
        computed(() => articleKeys.detail(unref(slug))),
        () => articlesApi.getBySlug(unref(slug)),
        {
            enabled: computed(() => !!unref(slug)),
        },
    );
}

export function usePopularArticles(limit = 5) {
    return createStaticQuery(articleKeys.popular(limit), () => articlesApi.getPopular(limit));
}

export function useRecentArticles(limit = 5, options?: QueryOptions<Article[]>) {
    return createListQuery(articleKeys.recent(limit), () => articlesApi.getRecent(limit), options);
}

export function useArticleCategories() {
    return createStaticQuery(articleKeys.categories(), articlesApi.getCategories, {
        select: (data: Category[] | { data: Category[] }) => (Array.isArray(data) ? data : data.data),
    });
}

export function useArticleTags() {
    return createStaticQuery(articleKeys.tags(), articlesApi.getTags, {
        select: (data: Tag[] | { data: Tag[] }) => (Array.isArray(data) ? data : data.data),
    });
}

export function useRelatedArticles(slug: MaybeRef<string>) {
    return createStaticQuery(
        computed(() => articleKeys.related(unref(slug))),
        () => articlesApi.getRelated(unref(slug)),
        {
            enabled: computed(() => !!unref(slug)),
        },
    );
}

export function useRecordArticleView() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: articlesApi.recordView,
        onSuccess: (_, slug) => {
            queryClient.invalidateQueries({
                queryKey: articleKeys.detail(slug),
                refetchType: 'active',
            });
        },
    });
}

export function useToggleArticlePublish() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ slug, isPublished }: { slug: string; isPublished: boolean }) =>
            articlesApi.togglePublish(slug, isPublished),
        onMutate: async ({ slug, isPublished }) => {
            // Cancel active article queries to prevent overwrites
            await queryClient.cancelQueries({ queryKey: articleKeys.all });

            // Snapshot detail cache for rollback
            const previousDetail = queryClient.getQueryData(articleKeys.detail(slug));
            if (previousDetail) {
                queryClient.setQueryData(articleKeys.detail(slug), (old: ArticleDetail | undefined) =>
                    old ? { ...old, isPublished } : old,
                );
            }

            return { previousDetail, slug };
        },
        onError: (_err, { slug }, context) => {
            // Rollback detail cache
            if (context?.previousDetail) {
                queryClient.setQueryData(articleKeys.detail(slug), context.previousDetail);
            }
        },
        onSettled: () => {
            // Always refetch to ensure consistency
            queryClient.invalidateQueries({ queryKey: articleKeys.all, refetchType: 'active' });
        },
    });
}

const categoryMutations = createSubResourceMutations<Category, CategoryCreateData, CategoryUpdateData, string>(
    {
        create: articlesApi.createCategory,
        update: articlesApi.updateCategory,
        delete: articlesApi.deleteCategory,
    },
    { all: articleKeys.categories },
    'slug',
);

export const useCreateArticleCategory = categoryMutations.useCreate;

const tagMutations = createSubResourceMutations<Tag, TagCreateData, TagUpdateData, string>(
    {
        create: articlesApi.createTag,
        update: articlesApi.updateTag,
        delete: articlesApi.deleteTag,
    },
    { all: articleKeys.tags },
    'name',
);

export const useCreateArticleTag = tagMutations.useCreate;
