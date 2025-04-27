import { readonly, ref } from 'vue';

import { apiMock } from '@/services/utils/mock';
import type { Article, Category, Tag } from '@/types/feature/blog';
import type { FAQ } from '@/types/feature/contact';
import type { Experience } from '@/types/feature/experience';
import type { Project } from '@/types/feature/project';
import type { ExpertiseCategory, Stack, StackCategory } from '@/types/feature/stacks';

/**
 * Service centralisé pour accéder aux données mockées
 */
export function useMock() {
	// Données générales
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	// Projets
	const projects = ref<Project[]>([]);
	const projectCategories = ref<Category[]>([]);
	const currentProject = ref<Project | null>(null);
	const relatedProjects = ref<Project[]>([]);

	// Expérience
	const professionalExperiences = ref<Experience[]>([]);
	const educationExperiences = ref<Experience[]>([]);

	// Technologies
	const stacks = ref<Stack[]>([]);
	const stackCategories = ref<StackCategory[]>([]);
	const expertiseCategories = ref<ExpertiseCategory[]>([]);
	const currentStack = ref<Stack | null>(null);
	const relatedStacks = ref<Stack[]>([]);

	// Blog
	const articles = ref<Article[]>([]);
	const blogCategories = ref<Category[]>([]);
	const blogTags = ref<Tag[]>([]);
	const popularArticles = ref<Article[]>([]);
	const currentArticle = ref<Article | null>(null);
	const relatedArticles = ref<Article[]>([]);

	// Contact
	const faqs = ref<FAQ[]>([]);

	// ------------------- MÉTHODES -------------------

	/**
	 * Réinitialise l'état d'erreur et définit isLoading à true
	 */
	const startLoading = () => {
		isLoading.value = true;
		error.value = null;
	};

	/**
	 * Définit isLoading à false
	 */
	const stopLoading = () => {
		isLoading.value = false;
	};

	/**
	 * Gère les erreurs des requêtes
	 */
	const handleError = (err: unknown, defaultMessage: string) => {
		console.error(defaultMessage, err);
		error.value = defaultMessage;
		stopLoading();
	};

	// Méthodes pour les projets
	const fetchProjects = async (limit?: number, category?: string) => {
		startLoading();

		try {
			const response = await apiMock.getAllProjects(1, limit, category);

			if (response.success && response.data) {
				projects.value = response.data as Project[];
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des projets.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des projets.');
		} finally {
			stopLoading();
		}
	};

	const fetchProjectCategories = async () => {
		startLoading();

		try {
			const response = await apiMock.getProjectCategories();

			if (response.success && response.data) {
				projectCategories.value = response.data as Category[];
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des catégories de projets.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des catégories de projets.');
		} finally {
			stopLoading();
		}
	};

	const fetchProjectBySlug = async (slug: string) => {
		startLoading();

		try {
			const response = await apiMock.getProjectBySlug(slug);

			if (response.success && response.data) {
				const projectData = response.data as Project & { relatedProjects?: Project[] };
				currentProject.value = projectData;
				relatedProjects.value = projectData.relatedProjects || [];
			} else {
				error.value = response.error?.message || 'Projet non trouvé.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des détails du projet.');
		} finally {
			stopLoading();
		}
	};

	// Méthodes pour l'expérience
	const fetchExperience = async () => {
		startLoading();

		try {
			const response = await apiMock.getExperienceData();

			if (response.success && response.data) {
				const experienceData = response.data as {
					professionalExperiences: Experience[];
					educationExperiences: Experience[];
				};

				professionalExperiences.value = experienceData.professionalExperiences;
				educationExperiences.value = experienceData.educationExperiences;
			} else {
				error.value = response.error?.message || "Erreur lors du chargement des données d'expérience.";
			}
		} catch (err) {
			handleError(err, "Erreur lors du chargement des données d'expérience.");
		} finally {
			stopLoading();
		}
	};

	// Méthodes pour les technologies
	const fetchStacks = async (limit?: number) => {
		startLoading();

		try {
			const response = await apiMock.getAllStacks();

			if (response.success && response.data) {
				const stacksData = response.data as Stack[];
				stacks.value = limit ? stacksData.slice(0, limit) : stacksData;
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des technologies.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des technologies.');
		} finally {
			stopLoading();
		}
	};

	const fetchStackCategories = async () => {
		startLoading();

		try {
			const response = await apiMock.getStackCategories();

			if (response.success && response.data) {
				const categoriesData = response.data as {
					categories: StackCategory[];
					expertiseCategories: ExpertiseCategory[];
				};

				stackCategories.value = categoriesData.categories;
				expertiseCategories.value = categoriesData.expertiseCategories;
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des catégories de technologies.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des catégories de technologies.');
		} finally {
			stopLoading();
		}
	};

	const fetchStackBySlug = async (slug: string) => {
		startLoading();

		try {
			const response = await apiMock.getStackBySlug(slug);

			if (response.success && response.data) {
				const stackData = response.data as Stack & { relatedStacks?: Stack[] };
				currentStack.value = stackData;
				relatedStacks.value = stackData.relatedStacks || [];
			} else {
				error.value = response.error?.message || 'Technologie non trouvée.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des détails de la technologie.');
		} finally {
			stopLoading();
		}
	};

	// Méthodes pour le blog
	const fetchArticles = async (
		page = 1,
		perPage = 1000, // Changez la valeur par défaut à un nombre beaucoup plus grand
		options?: { category?: string; tags?: string[]; search?: string }
	) => {
		startLoading();

		try {
			const response = await apiMock.getBlogArticles(page, perPage, options);

			if (response.success && response.data) {
				articles.value = response.data as Article[];
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des articles.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des articles.');
		} finally {
			stopLoading();
		}
	};

	const fetchBlogCategories = async () => {
		startLoading();

		try {
			const response = await apiMock.getBlogCategories();

			if (response.success && response.data) {
				const categoriesData = response.data as {
					categories: Category[];
					tags: Tag[];
				};

				blogCategories.value = categoriesData.categories;
				blogTags.value = categoriesData.tags;
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des catégories du blog.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des catégories du blog.');
		} finally {
			stopLoading();
		}
	};

	// Ajout pour corriger l'erreur - cette méthode est une alias de fetchBlogCategories
	const fetchBlogTags = async () => {
		await fetchBlogCategories();
	};

	const fetchArticleBySlug = async (slug: string) => {
		startLoading();

		try {
			const response = await apiMock.getArticleBySlug(slug);

			if (response.success && response.data) {
				const articleData = response.data as Article & { relatedArticles?: Article[] };
				currentArticle.value = articleData;
				relatedArticles.value = articleData.relatedArticles || [];
			} else {
				error.value = response.error?.message || 'Article non trouvé.';
			}
		} catch (err) {
			handleError(err, "Erreur lors du chargement des détails de l'article.");
		} finally {
			stopLoading();
		}
	};

	const fetchPopularArticles = async (limit = 3) => {
		startLoading();

		try {
			const response = await apiMock.getPopularArticles(limit);

			if (response.success && response.data) {
				popularArticles.value = response.data as Article[];
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des articles populaires.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des articles populaires.');
		} finally {
			stopLoading();
		}
	};

	// Méthodes pour FAQs
	const fetchFaqs = async () => {
		startLoading();

		try {
			const response = await apiMock.getContactFaqs();

			if (response.success && response.data) {
				faqs.value = response.data as FAQ[];
			} else {
				error.value = response.error?.message || 'Erreur lors du chargement des FAQs.';
			}
		} catch (err) {
			handleError(err, 'Erreur lors du chargement des FAQs.');
		} finally {
			stopLoading();
		}
	};

	// Méthodes pour le formulaire de contact
	const sendContactForm = async (formData: Record<string, any>) => {
		startLoading();

		try {
			const response = await apiMock.sendContactForm(formData);

			if (!response.success) {
				error.value = response.error?.message || "Erreur lors de l'envoi du formulaire de contact.";
			}

			return response;
		} catch (err) {
			handleError(err, "Erreur lors de l'envoi du formulaire de contact.");
			return { success: false, error: { message: "Erreur lors de l'envoi du formulaire de contact." } };
		} finally {
			stopLoading();
		}
	};

	// Méthode pour l'inscription à la newsletter
	const subscribeToNewsletter = async (email: string) => {
		startLoading();

		try {
			const response = await apiMock.subscribeToNewsletter(email);

			if (!response.success) {
				error.value = response.error?.message || "Erreur lors de l'inscription à la newsletter.";
			}

			return response;
		} catch (err) {
			handleError(err, "Erreur lors de l'inscription à la newsletter.");
			return { success: false, error: { message: "Erreur lors de l'inscription à la newsletter." } };
		} finally {
			stopLoading();
		}
	};

	return {
		// État général
		isLoading: readonly(isLoading),
		error: readonly(error),

		// Projets
		projects: readonly(projects),
		currentProject: readonly(currentProject),
		relatedProjects: readonly(relatedProjects),
		projectCategories: readonly(projectCategories),

		// Expérience
		professionalExperiences: readonly(professionalExperiences),
		educationExperiences: readonly(educationExperiences),

		// Technologies
		stacks: readonly(stacks),
		currentStack: readonly(currentStack),
		relatedStacks: readonly(relatedStacks),
		stackCategories: readonly(stackCategories),
		expertiseCategories: readonly(expertiseCategories),

		// Blog
		articles: readonly(articles),
		currentArticle: readonly(currentArticle),
		relatedArticles: readonly(relatedArticles),
		blogCategories: readonly(blogCategories),
		blogTags: readonly(blogTags),
		popularArticles: readonly(popularArticles),

		// Contact
		faqs: readonly(faqs),

		// Méthodes
		fetchProjects,
		fetchProjectCategories,
		fetchProjectBySlug,
		fetchExperience,
		fetchStacks,
		fetchStackCategories,
		fetchStackBySlug,
		fetchArticles,
		fetchBlogCategories,
		fetchBlogTags,
		fetchArticleBySlug,
		fetchPopularArticles,
		fetchFaqs,
		sendContactForm,
		subscribeToNewsletter,
	};
}
