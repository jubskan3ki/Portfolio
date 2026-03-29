import type { AppRoutes, AdminRoutes, PathCreator } from '@/types/config/routes';

// Routes publiques
export const ROUTES: AppRoutes = {
    HOME: {
        path: '/',
        name: 'Home',
    },

    // Routes du blog
    BLOG: {
        path: '/blog',
        name: 'Blog',
        DETAIL: (slug: string) => ({
            path: `/blog/${slug}`,
            name: 'BlogDetail',
        }),
    },

    // Routes des projets
    PROJECTS: {
        path: '/projects',
        name: 'Projects',
        DETAIL: (slug: string) => ({
            path: `/projects/${slug}`,
            name: 'ProjectDetail',
        }),
    },

    // Routes des stacks
    STACKS: {
        path: '/stacks',
        name: 'Stacks',
        DETAIL: (slug: string) => ({
            path: `/stacks/${slug}`,
            name: 'StackDetail',
        }),
    },

    // Autres routes principales
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

    // Pages legales
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

    // Pages d'erreur
    ERROR_404: {
        path: '/404',
        name: 'NotFound',
    },
};

// Routes admin
export const ADMIN_ROUTES: AdminRoutes = {
    // Base
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

    // Articles
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

    // Projets
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

    // Stacks
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

    // Experiences
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

    // Messages
    MESSAGES: {
        path: '/admin/messages',
        name: 'AdminMessages',
    },

    // Parametres
    SETTINGS: {
        path: '/admin/settings',
        name: 'AdminSettings',
    },

    // Import/Export
    IMPORT_EXPORT: {
        path: '/admin/import-export',
        name: 'AdminImportExport',
    },

    // Historique
    HISTORY: {
        path: '/admin/history',
        name: 'AdminHistory',
    },
};

// Fonctions helpers

// Cree un chemin avec des parametres dynamiques
export const createPath: PathCreator = (route: { path: string }, params: Record<string, string | number> = {}) => {
    let path = route.path;

    Object.entries(params).forEach(([key, value]) => {
        path = path.replace(`:${key}`, String(value));
    });

    return path;
};

// Verifie si un chemin correspond a la route actuelle
export const isActiveRoute = (path: string, currentPath: string): boolean => {
    if (path === '/' && currentPath === '/') {
        return true;
    }
    if (path === '/admin' && currentPath === '/admin') {
        return true;
    }
    return path !== '/' && path !== '/admin' && currentPath.startsWith(path);
};
