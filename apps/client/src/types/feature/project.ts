// types/feature/project.ts

/**
 * Types pour les fonctionnalités de projets
 */

// Type pour un projet
export interface Project {
	id: string;
	title: string;
	slug: string;
	description: string;
	longDescription?: string;
	image: string;
	category: string;
	technologies: string[] | readonly string[];
	date: string;
	features?: string[] | readonly string[];
	links?: {
		demo?: string;
		github?: string;
		documentation?: string;
	};
}

// Type pour une catégorie de projets
export interface ProjectCategory {
	id: string;
	name: string;
	description?: string;
	count?: number;
	slug?: string;
}

// Type pour un statut de projet
export interface ProjectStatus {
	id: string;
	name: 'Terminé' | 'En cours' | 'Planifié' | 'Archivé';
	color?: string;
}

// Type pour les images de projet
export interface ProjectImage {
	id: string;
	projectId: string;
	url: string;
	alt?: string;
	sortOrder?: number;
	isFeatured?: boolean;
}

// Type pour un témoignage lié à un projet
export interface ProjectTestimonial {
	id: string;
	projectId: string;
	author: string;
	role?: string;
	company?: string;
	avatar?: string;
	content: string;
	rating?: number;
}

// Type pour les statistiques d'un projet
export interface ProjectStats {
	viewCount: number;
	likeCount: number;
	commentCount: number;
	shareCount: number;
}

// Type pour les paramètres de filtre de projets
export interface ProjectFilterParams {
	category?: string;
	status?: string;
	technologies?: string[];
	search?: string;
	sortBy?: 'date' | 'title' | 'views';
	sortDirection?: 'asc' | 'desc';
}

// Type pour la réponse paginée de projets
export interface ProjectPaginatedResponse {
	data: Project[];
	pagination: {
		total: number;
		page: number;
		limit: number;
		totalPages: number;
	};
}
