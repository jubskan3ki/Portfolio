// Types pour la configuration des routes

export interface Route {
    path: string;
    name: string;
}

type RouteWithSlugGenerator = (slug: string) => Route;
type RouteWithIdGenerator = (id: string | number) => Route;

// Routes publiques
export interface BlogRoutes extends Route {
    DETAIL: RouteWithSlugGenerator;
}

export interface ProjectsRoutes extends Route {
    DETAIL: RouteWithSlugGenerator;
}

export interface StacksRoutes extends Route {
    DETAIL: RouteWithSlugGenerator;
}

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

// Routes admin
export interface AdminCrudRoutes extends Route {
    CREATE: Route;
    EDIT: RouteWithIdGenerator;
}

export interface AdminRoutes {
    BASE: Route;
    LOGIN: Route;
    DASHBOARD: Route;
    ARTICLES: AdminCrudRoutes;
    PROJECTS: AdminCrudRoutes;
    STACKS: AdminCrudRoutes;
    EXPERIENCES: AdminCrudRoutes;
    MESSAGES: Route;
    SETTINGS: Route;
    IMPORT_EXPORT: Route;
    HISTORY: Route;
}

// Helper pour creer des chemins
export type PathCreator = (route: { path: string }, params?: Record<string, string | number>) => string;
