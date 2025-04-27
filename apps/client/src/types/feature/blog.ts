// types/feature/blog.ts

/**
 * Types pour les fonctionnalités de blog
 */

// Type pour un article de blog
export interface Article {
	id: string;
	title: string;
	slug: string;
	excerpt: string;
	content: string[] | readonly string[];
	image: string;
	category: string;
	tags: string[] | readonly string[];
	date: string;
	readTime: number;
	views: number;
	toc?: string[] | readonly string[];
	author?: {
		name: string;
		avatar: string;
		bio: string;
		social?: {
			github?: string;
			linkedin?: string;
			twitter?: string;
		};
	};
}

// Type pour une catégorie d'articles
export interface Category {
	id: string;
	name: string;
	count: number;
	slug?: string;
}

// Type pour un tag d'article
export interface Tag {
	id: string;
	name: string;
	count: number;
}

// Types pour les paramètres de requêtes API d'articles
export interface ArticleQueryParams {
	page?: number;
	limit?: number;
	category?: string;
	tag?: string;
	search?: string;
	sortBy?: 'date' | 'views' | 'readTime';
	sortDirection?: 'asc' | 'desc';
}

// Type pour la réponse paginée d'articles
export interface ArticlePaginatedResponse {
	data: Article[];
	pagination: {
		total: number;
		page: number;
		limit: number;
		totalPages: number;
	};
}

// Type pour les filtres actifs d'articles
export interface ArticleActiveFilters {
	categories: string[];
	tags: string[];
	search: string;
	sortBy: string;
	sortDirection: string;
}
