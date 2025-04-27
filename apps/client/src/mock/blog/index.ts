// Export all blog mock data
export * from './articles';
export * from './categories';
export * from './tags';

// Export a method to get all blog data
import { articles } from './articles';
import { categories } from './categories';
import { tags } from './tags';

export const getAllBlogData = () => {
	return {
		articles,
		categories,
		tags,
	};
};

// Get a specific article by slug
export const getArticleBySlug = (slug: string) => {
	return articles.find((article) => article.slug === slug);
};

// Get popular articles
export const getPopularArticles = (limit = 3) => {
	return [...articles].sort((a, b) => b.views - a.views).slice(0, limit);
};

// Get related articles for a specific article
export const getRelatedArticles = (slug: string, limit = 3) => {
	const currentArticle = getArticleBySlug(slug);
	if (!currentArticle) return [];

	return articles
		.filter(
			(article) =>
				article.slug !== slug &&
				(article.category === currentArticle.category ||
					article.tags.some((tag) => currentArticle.tags.includes(tag)))
		)
		.slice(0, limit);
};
