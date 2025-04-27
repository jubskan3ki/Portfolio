// types/config/routes.ts

/**
 * Types pour la configuration des routes
 */

// Type de base pour une route
export interface Route {
	path: string;
	name: string;
}

// Type pour une fonction générant une route avec un slug
export type RouteWithSlugGenerator = (slug: string) => Route;

// Type pour les routes du blog
export interface BlogRoutes {
	path: string;
	name: string;
	DETAIL: RouteWithSlugGenerator;
}

// Type pour les routes des projets
export interface ProjectsRoutes {
	path: string;
	name: string;
	DETAIL: RouteWithSlugGenerator;
}

// Type pour les routes des technologies
export interface StacksRoutes {
	path: string;
	name: string;
	DETAIL: RouteWithSlugGenerator;
}

// Type pour l'ensemble des routes de l'application
export interface AppRoutes {
	HOME: Route;
	BLOG: BlogRoutes;
	PROJECTS: ProjectsRoutes;
	STACKS: StacksRoutes;
	CONTACT: Route;
	EXPERIENCE: Route;
	ERROR_404: Route;
	LEGAL: Route;
	PRIVACY: Route;
	TERMS: Route;
}

// Type pour les fonctions de création de chemins
export type PathCreator = (route: { path: string }, params?: Record<string, string | number>) => string;

// Type pour les fonctions de navigation typée
export interface NamedRoutes {
	goToHome: () => Route;
	goToBlog: () => BlogRoutes;
	goToBlogDetail: (slug: string) => Route;
	goToProjects: () => ProjectsRoutes;
	goToProjectDetail: (slug: string) => Route;
	goToStacks: () => StacksRoutes;
	goToStackDetail: (slug: string) => Route;
	goToContact: () => Route;
	goToExperience: () => Route;
	goToNotFound: () => Route;
	goToLegal: () => Route;
	goToPrivacy: () => Route;
	goToTerms: () => Route;
}
