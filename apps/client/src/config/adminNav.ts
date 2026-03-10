// src/config/adminNav.ts
import { ADMIN_ROUTES, isActiveRoute } from '@/config/routes';

import type { AdminMenuItem } from '@/types/components/layouts';

// Admin Navigation Items

// Main navigation items for admin sidebar
export const adminMenuItems: AdminMenuItem[] = [
    {
        label: 'Dashboard',
        path: ADMIN_ROUTES.DASHBOARD.path,
        icon: 'layout-dashboard',
    },
    {
        label: 'Articles',
        path: ADMIN_ROUTES.ARTICLES.path,
        icon: 'file-text',
    },
    {
        label: 'Projets',
        path: ADMIN_ROUTES.PROJECTS.path,
        icon: 'folder',
    },
    {
        label: 'Stacks',
        path: ADMIN_ROUTES.STACKS.path,
        icon: 'layers',
    },
    {
        label: 'Experiences',
        path: ADMIN_ROUTES.EXPERIENCES.path,
        icon: 'briefcase',
    },
    {
        label: 'Messages',
        path: ADMIN_ROUTES.MESSAGES.path,
        icon: 'mail',
    },
    {
        label: 'Historique',
        path: ADMIN_ROUTES.HISTORY.path,
        icon: 'activity',
    },
    {
        label: 'Import/Export',
        path: ADMIN_ROUTES.IMPORT_EXPORT.path,
        icon: 'database',
    },

    {
        label: 'Parametres',
        path: ADMIN_ROUTES.SETTINGS.path,
        icon: 'settings',
    },
];

// Breadcrumb Configuration

// Route labels for breadcrumb generation
const adminRouteLabels: Record<string, string> = {
    admin: 'Dashboard',
    dashboard: 'Dashboard',
    articles: 'Articles',
    projects: 'Projets',
    stacks: 'Stacks',
    experiences: 'Experiences',
    messages: 'Messages',
    settings: 'Parametres',
    'import-export': 'Import/Export',
    create: 'Creer',
    edit: 'Modifier',
};

// Get breadcrumb label for a route segment
export const getBreadcrumbLabel = (segment: string): string => {
    // Check if it's a known route
    if (adminRouteLabels[segment]) {
        return adminRouteLabels[segment];
    }

    // Check if it's an ID (numeric or UUID-like)
    if (/^[\d]+$/.test(segment) || /^[a-f0-9-]{36}$/i.test(segment)) {
        return 'Details';
    }

    // Fallback: capitalize the segment
    return segment.charAt(0).toUpperCase() + segment.slice(1);
};

// Helpers

// Check if a menu item is active based on current path
export const isMenuItemActive = (itemPath: string, currentPath: string): boolean => {
    // Special case for dashboard
    if (itemPath === ADMIN_ROUTES.DASHBOARD.path) {
        return currentPath === '/admin' || currentPath === ADMIN_ROUTES.DASHBOARD.path;
    }

    return isActiveRoute(itemPath, currentPath);
};
