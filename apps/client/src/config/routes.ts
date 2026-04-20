import type { AppRoutes, AdminRoutes, PathCreator } from '@/types/config/routes';

export const ROUTES: AppRoutes = {
    HOME: {
        path: '/',
        name: 'Home',
    },

    BLOG: {
        path: '/blog',
        name: 'Blog',
        DETAIL: (slug: string) => ({
            path: `/blog/${slug}`,
            name: 'BlogDetail',
        }),
    },

    PROJECTS: {
        path: '/projects',
        name: 'Projects',
        DETAIL: (slug: string) => ({
            path: `/projects/${slug}`,
            name: 'ProjectDetail',
        }),
    },

    STACKS: {
        path: '/stacks',
        name: 'Stacks',
        DETAIL: (slug: string) => ({
            path: `/stacks/${slug}`,
            name: 'StackDetail',
        }),
    },

    ABOUT: {
        path: '/about',
        name: 'About',
    },
    CONTACT: {
        path: '/contact',
        name: 'Contact',
    },
    EXPERIENCE: {
        path: '/experience',
        name: 'Experience',
    },

    LEGAL: {
        path: '/legal',
        name: 'Legal',
    },
    PRIVACY: {
        path: '/privacy',
        name: 'Privacy',
    },
    TERMS: {
        path: '/terms',
        name: 'Terms',
    },

    ERROR_404: {
        path: '/404',
        name: 'NotFound',
    },
};

export const ADMIN_ROUTES: AdminRoutes = {
    BASE: {
        path: '/admin',
        name: 'Admin',
    },
    LOGIN: {
        path: '/admin',
        name: 'AdminLogin',
    },
    DASHBOARD: {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
    },

    ARTICLES: {
        path: '/admin/articles',
        name: 'AdminArticles',
        CREATE: {
            path: '/admin/articles/create',
            name: 'AdminArticleCreate',
        },
        EDIT: (id: string | number) => ({
            path: `/admin/articles/${id}`,
            name: 'AdminArticleEdit',
        }),
    },

    PROJECTS: {
        path: '/admin/projects',
        name: 'AdminProjects',
        CREATE: {
            path: '/admin/projects/create',
            name: 'AdminProjectCreate',
        },
        EDIT: (id: string | number) => ({
            path: `/admin/projects/${id}`,
            name: 'AdminProjectEdit',
        }),
    },

    STACKS: {
        path: '/admin/stacks',
        name: 'AdminStacks',
        CREATE: {
            path: '/admin/stacks/create',
            name: 'AdminStackCreate',
        },
        EDIT: (id: string | number) => ({
            path: `/admin/stacks/${id}`,
            name: 'AdminStackEdit',
        }),
    },

    EXPERIENCES: {
        path: '/admin/experiences',
        name: 'AdminExperiences',
        CREATE: {
            path: '/admin/experiences/create',
            name: 'AdminExperienceCreate',
        },
        EDIT: (id: string | number) => ({
            path: `/admin/experiences/${id}`,
            name: 'AdminExperienceEdit',
        }),
    },

    MESSAGES: {
        path: '/admin/messages',
        name: 'AdminMessages',
    },

    SETTINGS: {
        path: '/admin/settings',
        name: 'AdminSettings',
    },

    IMPORT_EXPORT: {
        path: '/admin/import-export',
        name: 'AdminImportExport',
    },

    HISTORY: {
        path: '/admin/history',
        name: 'AdminHistory',
    },
};

export const createPath: PathCreator = (route: { path: string }, params: Record<string, string | number> = {}) => {
    let path = route.path;

    Object.entries(params).forEach(([key, value]) => {
        path = path.replace(`:${key}`, String(value));
    });

    return path;
};

export const isActiveRoute = (path: string, currentPath: string): boolean => {
    if (path === '/' && currentPath === '/') {
        return true;
    }
    if (path === '/admin' && currentPath === '/admin') {
        return true;
    }
    return path !== '/' && path !== '/admin' && currentPath.startsWith(path);
};
