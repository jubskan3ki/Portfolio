// types/feature/stacks.ts

/**
 * Types pour les fonctionnalités de stacks techniques
 */

// Type pour une stack technique
export interface Stack {
	id: string;
	name: string;
	description: string;
	logo: string;
	category: string;
	tags: string[] | readonly string[];
	slug: string;
	experience: number;
	level: number;
	website?: string;
	websiteLabel?: string;
	github?: string;
	githubLabel?: string;
	firstRelease?: string;
	license?: string;
	content?: string;
	resources?:
		| {
				title: string;
				description: string;
				url: string;
		  }[]
		| readonly {
				title: string;
				description: string;
				url: string;
		  }[];
	relatedStacks?:
		| {
				name: string;
				logo: string; // Image URL from images.ts
				slug: string;
				category: string;
		  }[]
		| readonly {
				name: string;
				logo: string; // Image URL from images.ts
				slug: string;
				category: string;
		  }[];
}

// Type pour une catégorie de stack technique
export interface StackCategory {
	id: string;
	name: string;
	description?: string;
	icon?: string;
	count?: number;
}

// Type pour une catégorie d'expertise
export interface ExpertiseCategory {
	name: string;
	description: string;
	skills: string[] | readonly string[];
	icon?: string;
}

// Type pour un niveau de compétence
export interface ProficiencyLevel {
	value: number;
	label: string;
	description: string;
}

// Type pour un badge de stack
export interface StackBadge {
	name: string;
	logo: string;
	category: string;
	level: number;
}

// Type pour les paramètres de filtre de stacks
export interface StackFilterParams {
	category?: string;
	tags?: string[];
	minLevel?: number;
	minExperience?: number;
	search?: string;
	sortBy?: 'name' | 'level' | 'experience';
	sortDirection?: 'asc' | 'desc';
}

// Type pour une ressource de stack
export interface StackResource {
	title: string;
	description: string;
	url: string;
	type?: 'documentation' | 'tutorial' | 'article' | 'video' | 'other';
	isFeatured?: boolean;
}

// Type pour une stack associée
export interface RelatedStack {
	name: string;
	logo: string;
	slug: string;
	category: string;
	relationship?: 'alternative' | 'complementary' | 'dependency' | 'similarTo';
}

// Type pour les statistiques de stacks
export interface StackStats {
	totalStacks: number;
	stacksByCategory: { category: string; count: number }[];
	averageProficiency: number;
	topStacks: { name: string; level: number }[];
	yearsOfExperience: { name: string; years: number }[];
}
