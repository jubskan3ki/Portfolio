import { API_ENDPOINTS } from '@/config/api';
import { httpClient } from '@/services/api/core/httpClient';

import type { PaginatedResponse } from '@/types/api/common';
import type { Article } from '@/types/feature/blog';
import type { Project } from '@/types/feature/project';
import type { Stack } from '@/types/feature/stacks';

interface SitemapImage {
    loc: string;
    title?: string;
}

interface SitemapEntry {
    loc: string;
    lastmod?: string;
    changefreq?: string;
    priority?: number;
    images?: SitemapImage[];
}

function toDateString(value: string | null | undefined): string | undefined {
    if (!value) return undefined;
    return value.substring(0, 10);
}

async function fetchAllPages<T>(endpoint: string, params: Record<string, unknown> = {}): Promise<T[]> {
    const allItems: T[] = [];
    let page = 1;
    let totalPages = 1;

    do {
        const response = await httpClient.get<PaginatedResponse<T>>(endpoint, { ...params, limit: 100, page });
        allItems.push(...response.data);
        totalPages = response.pagination.totalPages;
        page++;
    } while (page <= totalPages);

    return allItems;
}

const STATIC_PAGES: SitemapEntry[] = [
    { loc: '/', changefreq: 'weekly', priority: 1.0 },
    { loc: '/blog', changefreq: 'daily', priority: 0.8 },
    { loc: '/projects', changefreq: 'weekly', priority: 0.8 },
    { loc: '/stacks', changefreq: 'weekly', priority: 0.7 },
    { loc: '/experience', changefreq: 'monthly', priority: 0.6 },
    { loc: '/contact', changefreq: 'weekly', priority: 0.9 },
    { loc: '/legal', changefreq: 'yearly', priority: 0.1 },
    { loc: '/privacy', changefreq: 'yearly', priority: 0.1 },
    { loc: '/terms', changefreq: 'yearly', priority: 0.1 },
];

export default defineCachedEventHandler(
    async () => {
        const [articlesResult, projectsResult, stacksResult] = await Promise.allSettled([
            fetchAllPages<Article>(API_ENDPOINTS.ARTICLES.BASE),
            fetchAllPages<Project>(API_ENDPOINTS.PROJECTS.BASE),
            fetchAllPages<Stack>(API_ENDPOINTS.STACKS.BASE),
        ]);

        const articles = articlesResult.status === 'fulfilled' ? articlesResult.value : [];
        const projects = projectsResult.status === 'fulfilled' ? projectsResult.value : [];
        const stacks = stacksResult.status === 'fulfilled' ? stacksResult.value : [];

        if (articlesResult.status === 'rejected')
            console.warn('[sitemap] Failed to fetch articles:', articlesResult.reason);
        if (projectsResult.status === 'rejected')
            console.warn('[sitemap] Failed to fetch projects:', projectsResult.reason);
        if (stacksResult.status === 'rejected') console.warn('[sitemap] Failed to fetch stacks:', stacksResult.reason);

        const articleUrls: SitemapEntry[] = articles.map((a) => ({
            loc: `/blog/${a.slug}`,
            lastmod: toDateString(a.updatedAt || a.date),
            changefreq: 'monthly',
            priority: 0.7,
            ...(a.image && { images: [{ loc: a.image, title: a.title }] }),
        }));

        const projectUrls: SitemapEntry[] = projects.map((p) => ({
            loc: `/projects/${p.slug}`,
            lastmod: toDateString(p.updatedAt || p.date),
            changefreq: 'monthly',
            priority: 0.6,
            ...(p.image && { images: [{ loc: p.image, title: p.title }] }),
        }));

        const stackUrls: SitemapEntry[] = stacks.map((s) => ({
            loc: `/stacks/${s.slug}`,
            lastmod: toDateString(s.startedDate),
            changefreq: 'monthly',
            priority: 0.5,
            ...(s.logo && { images: [{ loc: s.logo, title: s.name }] }),
        }));

        return [...STATIC_PAGES, ...articleUrls, ...projectUrls, ...stackUrls];
    },
    {
        maxAge: 3600,
        swr: true,
        name: 'sitemap-urls',
        getKey: () => 'sitemap-urls',
    },
);
