// src/config/navBar.ts
import ROUTES from '@/config/routes';
import type { ActiveRouteChecker, NavigationItems } from '@/types/config/navBar';

// Éléments de navigation avec les routes définies
export const navigationItems: NavigationItems = [
	{
		label: 'Accueil',
		path: ROUTES.HOME.path,
		icon: 'home',
	},
	{
		label: 'Expérience',
		path: ROUTES.EXPERIENCE.path,
		icon: 'experience',
	},
	{
		label: 'Projets',
		path: ROUTES.PROJECTS.path,
		icon: 'projects',
	},
	{
		label: 'Technologies',
		path: ROUTES.STACKS.path,
		icon: 'stacks',
	},
	{
		label: 'Blog',
		path: ROUTES.BLOG.path,
		icon: 'blog',
	},
];

// Fonction utilitaire pour vérifier si une route est active

export const isActiveRoute: ActiveRouteChecker = (path: string, currentPath: string): boolean => {
	// Cas spécial pour la page d'accueil
	if (path === '/' && currentPath === '/') {
		return true;
	}

	return path !== '/' && currentPath.startsWith(path);
};

//Fonction pour vérifier si un des enfants d'un élément de navigation est actif

export const hasActiveChild = (item: NavigationItems[0], currentPath: string): boolean => {
	if (!item.children) return false;

	return item.children.some((child) => isActiveRoute(child.path, currentPath));
};

export default {
	navigationItems,
	isActiveRoute,
	hasActiveChild,
};
