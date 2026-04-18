import { API_ENDPOINTS } from '@/config/api';
import { httpClient } from '@/services/api/core/httpClient';

import type { PaginatedResponse } from '@/types/api/common';
import type { Article } from '@/types/feature/blog';

const FEED_LIMIT = 20;

function toIsoString(value: string | null | undefined, fallback: string): string {
    if (!value) {
        return fallback;
    }
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) {
        return fallback;
    }
    return d.toISOString();
}

export default defineCachedEventHandler(
    async (event) => {
        const site = useSiteConfig(event);
        const siteUrl = (site.url ?? 'https://juba-aitadda.dev').replace(/\/$/, '');
        const siteName = site.name ?? 'Juba Ait-Adda';
        const siteDescription = site.description ?? 'Articles techniques de Juba Ait-Adda';

        let articles: Article[] = [];
        try {
            const response = await httpClient.get<PaginatedResponse<Article>>(
                API_ENDPOINTS.ARTICLES.BASE,
                { limit: FEED_LIMIT, page: 1 },
            );
            articles = response.data ?? [];
        } catch (err) {
            console.warn('[feed.json] Failed to fetch articles:', err);
        }

        const now = new Date().toISOString();
        const items = articles.map((article) => ({
            id: `${siteUrl}/blog/${article.slug}`,
            url: `${siteUrl}/blog/${article.slug}`,
            title: article.title,
            content_text: article.excerpt ?? '',
            summary: article.excerpt ?? '',
            date_published: toIsoString(article.date, now),
            date_modified: toIsoString(article.updatedAt || article.date, now),
            ...(article.image && { image: article.image }),
            tags: article.tags ?? [],
            authors: [{ name: siteName, url: siteUrl }],
        }));

        const feed = {
            version: 'https://jsonfeed.org/version/1.1',
            title: `${siteName} — Blog`,
            description: siteDescription,
            home_page_url: `${siteUrl}/blog`,
            feed_url: `${siteUrl}/feed.json`,
            language: 'fr-FR',
            authors: [{ name: siteName, url: siteUrl }],
            items,
        };

        setResponseHeader(event, 'Content-Type', 'application/feed+json; charset=utf-8');
        setResponseHeader(event, 'Cache-Control', 'public, max-age=3600, s-maxage=3600');
        return feed;
    },
    {
        maxAge: 3600,
        swr: true,
        name: 'feed-json',
        getKey: () => 'feed-json',
    },
);
