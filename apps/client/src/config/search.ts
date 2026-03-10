import { API_ENDPOINTS } from '@/config/api';
import { ROUTES, ADMIN_ROUTES } from '@/config/routes';

import type {
    SearchResultType,
    SearchMode,
    SearchTypeConfig,
    SearchResult,
    SearchResultGroup,
    SearchSourceConfig,
} from '@/types/config/search';

export const SEARCH_TYPE_CONFIG: Record<SearchResultType, SearchTypeConfig> = {
    article: { label: 'Articles', icon: 'file-text', color: '#3b82f6' },
    project: { label: 'Projets', icon: 'folder-kanban', color: '#10b981' },
    stack: { label: 'Stacks', icon: 'layers', color: '#8b5cf6' },
    experience: { label: 'Expériences', icon: 'briefcase', color: '#f59e0b' },
};

const SEARCH_TYPE_ORDER: SearchResultType[] = ['article', 'project', 'stack', 'experience'];

export const SEARCH_DEFAULTS = {
    DEBOUNCE_MS: 300,
    MIN_QUERY_LENGTH: 2,
    PAGE_SIZE: 5,
    STALE_TIME_MS: 1000 * 60 * 2,
} as const;

export const SEARCH_SOURCES: SearchSourceConfig[] = [
    {
        key: 'articles',
        type: 'article',
        endpoint: API_ENDPOINTS.ARTICLES.BASE,
        mapItem: (item) => ({
            title: item.title as string,
            subtitle: getCategoryName(item.category as { name: string } | string | undefined),
            slug: item.slug as string,
        }),
    },
    {
        key: 'projects',
        type: 'project',
        endpoint: API_ENDPOINTS.PROJECTS.BASE,
        mapItem: (item) => ({
            title: item.title as string,
            subtitle: getCategoryName(item.category as { name: string } | string | undefined),
            slug: item.slug as string,
        }),
    },
    {
        key: 'stacks',
        type: 'stack',
        endpoint: API_ENDPOINTS.STACKS.BASE,
        mapItem: (item) => ({
            title: item.name as string,
            subtitle: getCategoryName(item.category as { name: string } | string | undefined),
            slug: item.slug as string,
        }),
    },
    {
        key: 'experiences',
        type: 'experience',
        endpoint: API_ENDPOINTS.EXPERIENCES.BASE,
        mapItem: (item) => ({
            title: item.title as string,
            subtitle: item.company as string,
        }),
    },
];

export function getCategoryName(category: { name: string } | string | undefined): string | undefined {
    if (!category) {
        return undefined;
    }
    if (typeof category === 'string') {
        return category;
    }
    if (typeof category === 'object' && 'name' in category) {
        return category.name;
    }
    return undefined;
}

export function generateSearchLink(
    type: SearchResultType,
    id: number,
    slug?: string,
    mode: SearchMode = 'public',
): string {
    if (mode === 'admin') {
        const adminRoutes: Record<SearchResultType, (id: number) => { path: string }> = {
            article: ADMIN_ROUTES.ARTICLES.EDIT,
            project: ADMIN_ROUTES.PROJECTS.EDIT,
            stack: ADMIN_ROUTES.STACKS.EDIT,
            experience: ADMIN_ROUTES.EXPERIENCES.EDIT,
        };
        return adminRoutes[type](id).path;
    }

    const publicRoutes: Record<SearchResultType, { path: string; DETAIL?: (slug: string) => { path: string } }> = {
        article: ROUTES.BLOG,
        project: ROUTES.PROJECTS,
        stack: ROUTES.STACKS,
        experience: ROUTES.EXPERIENCE,
    };

    const route = publicRoutes[type];
    if (slug && 'DETAIL' in route && route.DETAIL) {
        return route.DETAIL(slug).path;
    }
    return route.path;
}

export function groupSearchResults(results: SearchResult[]): SearchResultGroup[] {
    if (!results.length) {
        return [];
    }

    const groups = new Map<SearchResultType, SearchResult[]>();

    results.forEach((result) => {
        const existing = groups.get(result.type) || [];
        existing.push(result);
        groups.set(result.type, existing);
    });

    return SEARCH_TYPE_ORDER.filter((type) => groups.has(type)).map((type) => ({
        type,
        ...SEARCH_TYPE_CONFIG[type],
        results: groups.get(type) || [],
    }));
}
