import * as mockData from '@/mock';
import { errorResponse, paginatedResponse, successResponse } from '@/mock/utils/api-response';
import { delayedResponse } from '@/mock/utils/delay';

/**
 * API Mock Service qui simule des appels API backend en utilisant des données mockées
 */
export class ApiMockService {
	/**
	 * Délai par défaut pour simuler la latence réseau (en millisecondes)
	 */
	private defaultDelay = 800;

	/**
	 * Récupère les données d'expérience (professionnelle, éducation, compétences)
	 */
	async getExperienceData() {
		return delayedResponse(successResponse(mockData.experienceMocks.getAllExperienceData()), this.defaultDelay);
	}

	/**
	 * Récupère toutes les technologies
	 */
	async getAllStacks() {
		return delayedResponse(successResponse(mockData.stacksMocks.stacks), this.defaultDelay);
	}

	/**
	 * Récupère une technologie spécifique par son slug
	 */
	async getStackBySlug(slug: string) {
		const stack = mockData.stacksMocks.getStackBySlug(slug);

		if (!stack) {
			return delayedResponse(errorResponse('NOT_FOUND', 'Stack not found'), this.defaultDelay);
		}

		// Récupérer les technologies liées
		const relatedStacks = mockData.stacksMocks.getRelatedStacks(slug);

		// Retourner la technologie avec ses technologies liées
		return delayedResponse(
			successResponse({
				...stack,
				relatedStacks,
			}),
			this.defaultDelay
		);
	}

	/**
	 * Récupère les catégories de technologies et catégories d'expertise
	 */
	async getStackCategories() {
		return delayedResponse(
			successResponse({
				categories: mockData.stacksMocks.stackCategories,
				expertiseCategories: mockData.stacksMocks.expertiseCategories,
			}),
			this.defaultDelay
		);
	}

	/**
	 * Récupère tous les projets
	 */
	async getAllProjects(page = 1, perPage = 1000, category?: string) {
		let projects = [...mockData.projectsMocks.projects];

		// Appliquer le filtre par catégorie si fourni
		if (category && category !== 'all') {
			projects = projects.filter((project) => project.category === category);
		}

		return delayedResponse(paginatedResponse(projects, page, perPage), this.defaultDelay);
	}

	/**
	 * Récupère un projet spécifique par son slug
	 */
	async getProjectBySlug(slug: string) {
		const project = mockData.projectsMocks.getProjectBySlug(slug);

		if (!project) {
			return delayedResponse(errorResponse('NOT_FOUND', 'Project not found'), this.defaultDelay);
		}

		// Récupérer les projets liés
		const relatedProjects = mockData.projectsMocks.getRelatedProjects(slug);

		// Retourner le projet avec ses projets liés
		return delayedResponse(
			successResponse({
				...project,
				relatedProjects,
			}),
			this.defaultDelay
		);
	}

	/**
	 * Récupère les catégories de projets
	 */
	async getProjectCategories() {
		return delayedResponse(successResponse(mockData.projectsMocks.projectCategories), this.defaultDelay);
	}

	/**
	 * Récupère les articles de blog avec filtres optionnels
	 */
	async getBlogArticles(
		page = 1,
		perPage = 6,
		options?: {
			category?: string;
			tags?: string[];
			search?: string;
		}
	) {
		let articles = [...mockData.blogMocks.articles];

		// Appliquer les filtres si fournis
		if (options) {
			// Filtre par catégorie
			if (options.category) {
				articles = articles.filter((article) => article.category === options.category);
			}

			// Filtre par tags (doit inclure tous les tags sélectionnés)
			if (options.tags && options.tags.length > 0) {
				articles = articles.filter((article) => options.tags!.every((tag) => article.tags.includes(tag)));
			}

			// Filtre par recherche (dans le titre ou l'extrait)
			if (options.search) {
				const searchTerm = options.search.toLowerCase();
				articles = articles.filter(
					(article) =>
						article.title.toLowerCase().includes(searchTerm) ||
						article.excerpt.toLowerCase().includes(searchTerm)
				);
			}
		}

		return delayedResponse(paginatedResponse(articles, page, perPage), this.defaultDelay);
	}

	/**
	 * Récupère un article de blog spécifique par son slug
	 */
	async getArticleBySlug(slug: string) {
		const article = mockData.blogMocks.getArticleBySlug(slug);

		if (!article) {
			return delayedResponse(errorResponse('NOT_FOUND', 'Article not found'), this.defaultDelay);
		}

		// Récupérer les articles liés
		const relatedArticles = mockData.blogMocks.getRelatedArticles(slug);

		// Retourner l'article avec ses articles liés
		return delayedResponse(
			successResponse({
				...article,
				relatedArticles,
			}),
			this.defaultDelay
		);
	}

	/**
	 * Récupère les catégories et tags de blog
	 */
	async getBlogCategories() {
		return delayedResponse(
			successResponse({
				categories: mockData.blogMocks.categories,
				tags: mockData.blogMocks.tags,
			}),
			this.defaultDelay
		);
	}

	/**
	 * Récupère les articles populaires du blog
	 */
	async getPopularArticles(limit = 3) {
		const popularArticles = mockData.blogMocks.getPopularArticles(limit);

		return delayedResponse(successResponse(popularArticles), this.defaultDelay);
	}

	/**
	 * Récupère les FAQs de contact
	 */
	async getContactFaqs() {
		return delayedResponse(successResponse(mockData.contactMocks.faqs), this.defaultDelay);
	}

	/**
	 * Simule l'envoi d'un formulaire de contact
	 */
	async sendContactForm(formData: any) {
		// Simuler la soumission du formulaire avec un délai plus long
		return delayedResponse(
			successResponse({
				message: 'Votre message a été envoyé avec succès. Je vous répondrai dans les plus brefs délais.',
				formData,
			}),
			1500
		);
	}

	/**
	 * Simule l'inscription à la newsletter
	 */
	async subscribeToNewsletter(email: string) {
		// Simuler une validation
		if (!email?.includes('@')) {
			return delayedResponse(
				errorResponse('INVALID_EMAIL', 'Veuillez fournir une adresse email valide.'),
				this.defaultDelay
			);
		}

		return delayedResponse(
			successResponse({
				message: 'Vous êtes maintenant inscrit à la newsletter.',
				email,
			}),
			this.defaultDelay
		);
	}
}

// Créer et exporter une instance singleton
export const apiMock = new ApiMockService();

// Exporter le type pour la réponse API
export type { ApiResponse } from '@/mock/utils/api-response';
