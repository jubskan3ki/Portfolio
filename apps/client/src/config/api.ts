export const HTTP_CONFIG = {
    DEFAULT_API_URL: 'http://localhost:8000',
    REFRESH_ENDPOINT: '/api/users/auth/refresh/',
    DEFAULT_TIMEOUT: 5000,
    // Shorter timeout for SSR to avoid blocking page rendering
    SSR_TIMEOUT: 1500,
} as const;

export const defaultRequestInit: RequestInit = {
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
    },
    credentials: 'include',
};

let _configuredBase: string | null = null;
let _resolvedClientBase: string | null = null;

export function setBaseUrl(url: string): void {
    _configuredBase = url;
    _resolvedClientBase = null;
}

export function getBaseUrl(): string {
    if (import.meta.server) {
        return (
            _configuredBase
            || process.env.NUXT_API_BASE_SERVER
            || process.env.NUXT_PUBLIC_API_BASE
            || HTTP_CONFIG.DEFAULT_API_URL
        );
    }
    if (_resolvedClientBase) {
        return _resolvedClientBase;
    }

    const base = _configuredBase || HTTP_CONFIG.DEFAULT_API_URL;

    // Align API hostname with page hostname to keep cookies same-site
    // (SameSite=Lax blocks cookies on cross-site fetch requests)
    if (typeof window !== 'undefined') {
        try {
            const url = new URL(base);
            if (url.hostname !== window.location.hostname) {
                url.hostname = window.location.hostname;
                _resolvedClientBase = url.origin;
                return _resolvedClientBase;
            }
        } catch {
            // Invalid URL — use base as-is
        }
    }

    _resolvedClientBase = base;
    return _resolvedClientBase;
}

export const API_ENDPOINTS = {
    ARTICLES: {
        BASE: '/api/articles/',
        DETAIL: (slug: string) => `/api/articles/${slug}/`,
        FEATURED: '/api/articles/featured/',
        POPULAR: '/api/articles/popular/',
        BY_CATEGORY: (categorySlug: string) => `/api/articles/by-category/${categorySlug}/`,
        BY_TAG: (tagName: string) => `/api/articles/by-tag/${tagName}/`,
        RELATED: (slug: string) => `/api/articles/${slug}/related/`,
        VIEW: (slug: string) => `/api/articles/${slug}/view/`,
        CATEGORIES: '/api/articles/categories/',
        CATEGORY_DETAIL: (slug: string) => `/api/articles/categories/${slug}/`,
        TAGS: '/api/articles/tags/',
        TAG_DETAIL: (name: string) => `/api/articles/tags/${name}/`,
    },

    PROJECTS: {
        BASE: '/api/projects/',
        DETAIL: (slug: string) => `/api/projects/${slug}/`,
        FEATURED: '/api/projects/featured/',
        BY_CATEGORY: (categorySlug: string) => `/api/projects/by-category/${categorySlug}/`,
        CATEGORIES: '/api/projects/categories/',
        CATEGORY_DETAIL: (slug: string) => `/api/projects/categories/${slug}/`,
        STATUSES: '/api/projects/statuses/',
        STATUS_DETAIL: (id: number | string) => `/api/projects/statuses/${id}/`,
        VIEW: (slug: string) => `/api/projects/${slug}/view/`,
        STATS: '/api/projects/stats/',
    },

    STACKS: {
        BASE: '/api/stacks/',
        DETAIL: (slug: string) => `/api/stacks/${slug}/`,
        BY_CATEGORY: (categoryName: string) => `/api/stacks/by-category/${categoryName}/`,
        RELATED: (slug: string) => `/api/stacks/${slug}/related/`,
        CATEGORIES: '/api/stacks/categories/',
        CATEGORY_DETAIL: (name: string) => `/api/stacks/categories/${name}/`,
        RESOURCES: '/api/stacks/resources/',
        RESOURCE_DETAIL: (id: number | string) => `/api/stacks/resources/${id}/`,
        STATS: '/api/stacks/stats/',
        PROJECTS: (slug: string) => `/api/stacks/${slug}/projects/`,
        ARTICLES: (slug: string) => `/api/stacks/${slug}/articles/`,
    },

    EXPERIENCES: {
        BASE: '/api/experiences/',
        DETAIL: (id: number | string) => `/api/experiences/${id}/`,
        BY_TYPE: (typeName: string) => `/api/experiences/by-type/${typeName}/`,
        CURRENT: '/api/experiences/current/',
        TIMELINE: '/api/experiences/timeline/',
        TYPES: '/api/experiences/types/',
        TYPE_DETAIL: (id: number | string) => `/api/experiences/types/${id}/`,
        STATS: '/api/experiences/stats/',
    },

    CONTACT: {
        BASE: '/api/contacts/',
        DETAIL: (id: number | string) => `/api/contacts/${id}/`,
        FAQS: '/api/contacts/faqs/',
        FAQ_DETAIL: (id: number | string) => `/api/contacts/faqs/${id}/`,
        INFO: '/api/contacts/infos/',
        INFO_DETAIL: (id: number | string) => `/api/contacts/infos/${id}/`,
        STATS: '/api/contacts/stats/',
    },

    USERS: {
        LOGIN: '/api/users/auth/login/',
        LOGOUT: '/api/users/auth/logout/',
        REFRESH: '/api/users/auth/refresh/',
        PROFILE: '/api/users/profile/',
        AVATAR: '/api/users/profile/avatar/',
        PASSWORD_CHANGE: '/api/users/password/change/',
        REQUEST_RESET_PASSWORD: '/api/users/request-reset-password/',
        VERIFY_RESET_CODE: '/api/users/verify-reset-code/',
        CONFIRM_RESET_PASSWORD: '/api/users/confirm-reset-password/',
        SESSIONS: '/api/users/sessions/',
    },

    STATS: {
        BASE: '/api/stats/',
        QUICK: '/api/stats/quick/',
        ACTIVITY: '/api/stats/activity/',
        CHARTS: '/api/stats/charts/',
        OVERVIEW: '/api/stats/overview/',
        WEB_VITALS: '/api/stats/web-vitals/',
        WEB_VITALS_SUMMARY: '/api/stats/web-vitals/summary/',
    },

    TRANSFER: {
        EXPORT_MODULE: (module: string) => `/api/transfer/export/module/${module}/`,
        EXPORT_DOWNLOAD: (module: string) => `/api/transfer/export/download/${module}/`,
        EXPORT_BULK: '/api/transfer/export/bulk/',
        IMPORT_MODULE: (module: string) => `/api/transfer/import/module/${module}/`,
        IMPORT_PREVIEW: (module: string) => `/api/transfer/import/preview/${module}/`,
        IMPORT_BULK: '/api/transfer/import/bulk/',
        JOBS: '/api/transfer/jobs/',
        JOBS_CLEANUP: '/api/transfer/jobs/cleanup/',
        EXPORT_JOB: (jobId: string) => `/api/transfer/jobs/export/${jobId}/`,
        IMPORT_JOB: (jobId: string) => `/api/transfer/jobs/import/${jobId}/`,
    },
} as const;
