import { API_ENDPOINTS } from '@/config/api';
import { httpClient } from '@/services/api/core/httpClient';

import type { PaginatedResponse } from '@/types/api/common';
import type { Article } from '@/types/feature/blog';

const FEED_LIMIT = 20;

function escapeXml(value: string): string {
    return value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
}

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
        const site = useSiteConfig();
        const siteUrl = (site.url ?? 'https://juba-aitadda.dev').replace(/\/$/, '');
        const siteName = site.name ?? 'Juba Ait-Adda';
        const siteDescription = site.description ?? 'Articles techniques de Juba Ait-Adda';

        let articles: Article[] = [];
        try {
            const response = await httpClient.get<PaginatedResponse<Article>>(API_ENDPOINTS.ARTICLES.BASE, {
                limit: FEED_LIMIT,
                page: 1,
            });
            articles = response.data ?? [];
        } catch (err) {
            console.warn('[feed.xml] Failed to fetch articles:', err);
        }

        const now = new Date().toISOString();
        const feedUpdated = articles[0] ? toIsoString(articles[0].updatedAt || articles[0].date, now) : now;

        const entries = articles
            .map((article) => {
                const articleUrl = `${siteUrl}/blog/${article.slug}`;
                const published = toIsoString(article.date, now);
                const updated = toIsoString(article.updatedAt || article.date, now);
                const summary = article.excerpt ?? '';
                const categories = (article.tags ?? [])
                    .map((tag) => `        <category term="${escapeXml(tag)}"/>`)
                    .join('\n');

                return `    <entry>
        <id>${articleUrl}</id>
        <title>${escapeXml(article.title)}</title>
        <link rel="alternate" type="text/html" href="${articleUrl}"/>
        <published>${published}</published>
        <updated>${updated}</updated>
        <summary type="html">${escapeXml(summary)}</summary>
        <author>
            <name>${escapeXml(siteName)}</name>
            <uri>${siteUrl}</uri>
        </author>
${categories}
    </entry>`;
            })
            .join('\n');

        const feed = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>${siteUrl}/</id>
    <title>${escapeXml(siteName)} — Blog</title>
    <subtitle>${escapeXml(siteDescription)}</subtitle>
    <link rel="self" type="application/atom+xml" href="${siteUrl}/feed.xml"/>
    <link rel="alternate" type="text/html" href="${siteUrl}/blog"/>
    <updated>${feedUpdated}</updated>
    <author>
        <name>${escapeXml(siteName)}</name>
        <uri>${siteUrl}</uri>
    </author>
${entries}
</feed>
`;

        setResponseHeader(event, 'Content-Type', 'application/atom+xml; charset=utf-8');
        setResponseHeader(event, 'Cache-Control', 'public, max-age=3600, s-maxage=3600');
        return feed;
    },
    {
        maxAge: 3600,
        swr: true,
        name: 'feed-atom',
        getKey: () => 'feed-atom',
    },
);
