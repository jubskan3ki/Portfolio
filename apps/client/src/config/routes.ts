// src/config/routes.ts
import type { AppRoutes, NamedRoutes, PathCreator } from '@/types/config/routes';

export const ROUTES: AppRoutes = {
	HOME: {
		path: '/',
		name: 'Home',
	},

	// Blog routes
	BLOG: {
		path: '/blog',
		name: 'Blog',
		DETAIL: (slug: string) => ({
			path: `/blog/${slug}`,
			name: 'BlogDetail',
		}),
	},

	// Projects routes
	PROJECTS: {
		path: '/projects',
		name: 'Projects',
		DETAIL: (slug: string) => ({
			path: `/projects/${slug}`,
			name: 'ProjectDetail',
		}),
	},

	// Stacks routes
	STACKS: {
		path: '/stacks',
		name: 'Stacks',
		DETAIL: (slug: string) => ({
			path: `/stacks/${slug}`,
			name: 'StackDetail',
		}),
	},

	// Other main routes
	CONTACT: {
		path: '/contact',
		name: 'Contact',
	},
	EXPERIENCE: {
		path: '/experience',
		name: 'Experience',
	},

	// Legal pages
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

	// Error pages
	ERROR_404: {
		path: '/404',
		name: 'NotFound',
	},
};

// Helper functions for navigation
export const createPath: PathCreator = (route: { path: string }, params: Record<string, string | number> = {}) => {
	let path = route.path;

	// Replace path parameters
	Object.entries(params).forEach(([key, value]) => {
		path = path.replace(`:${key}`, String(value));
	});

	return path;
};

// For strongly typed navigation with params
export const namedRoutes: NamedRoutes = {
	goToHome: () => ROUTES.HOME,
	goToBlog: () => ROUTES.BLOG,
	goToBlogDetail: (slug: string) => ROUTES.BLOG.DETAIL(slug),
	goToProjects: () => ROUTES.PROJECTS,
	goToProjectDetail: (slug: string) => ROUTES.PROJECTS.DETAIL(slug),
	goToStacks: () => ROUTES.STACKS,
	goToStackDetail: (slug: string) => ROUTES.STACKS.DETAIL(slug),
	goToContact: () => ROUTES.CONTACT,
	goToExperience: () => ROUTES.EXPERIENCE,
	goToLegal: () => ROUTES.LEGAL,
	goToPrivacy: () => ROUTES.PRIVACY,
	goToTerms: () => ROUTES.TERMS,
	goToNotFound: () => ROUTES.ERROR_404,
};

export default ROUTES;
