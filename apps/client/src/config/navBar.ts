// src/config/navBar.ts
import { ROUTES } from '@/config/routes';

import type { ActiveRouteChecker, NavigationItems } from '@/types/config/navBar';

// Public Navigation Items

// Main navigation items for public site header
export const navigationItems: NavigationItems = [
    {
        label: 'Accueil',
        path: ROUTES.HOME.path,
        icon: 'home',
    },
    {
        label: 'Experience',
        path: ROUTES.EXPERIENCE.path,
        icon: 'briefcase',
    },
    {
        label: 'Projets',
        path: ROUTES.PROJECTS.path,
        icon: 'folder',
    },
    {
        label: 'Stacks',
        path: ROUTES.STACKS.path,
        icon: 'layers',
    },
    {
        label: 'Blog',
        path: ROUTES.BLOG.path,
        icon: 'file-text',
    },
];

// Helper Functions

// Check if a route is currently active
export const isActiveRoute: ActiveRouteChecker = (path: string, currentPath: string): boolean => {
    // Special case for home page
    if (path === '/' && currentPath === '/') {
        return true;
    }

    return path !== '/' && currentPath.startsWith(path);
};
