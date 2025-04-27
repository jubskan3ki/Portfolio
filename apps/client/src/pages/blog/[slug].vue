<template>
	<div>
		<div v-if="isLoading" class="article-loader">
			<Spinner type="circle" size="large" label="Chargement de l'article..." />
		</div>

		<div v-else-if="error" class="article-error">
			<ErrorMessage :message="error" action-text="Retour au blog" :to="ROUTES.BLOG" />
		</div>

		<template v-else-if="currentArticle">
			<!-- En-tête de l'article avec le composant Hero -->
			<Hero :title="currentArticle.title" variant="primary" has-meta>
				<template #meta>
					<div class="hero__meta-item">
						<BaseIcon name="calendar" :size="16" />
						<span>{{ formatDate(currentArticle.date) }}</span>
					</div>
					<div class="hero__meta-item">
						<BaseIcon name="clock" :size="16" />
						<span>{{ currentArticle.readTime }} min de lecture</span>
					</div>
					<div class="hero__meta-item">
						<BaseIcon name="eye" :size="16" />
						<span>{{ formatViews(currentArticle.views) }} vues</span>
					</div>
					<div class="hero__meta-item">
						<BaseIcon name="folder" :size="16" />
						<span>{{ getCategoryName(currentArticle.category) }}</span>
					</div>
				</template>
			</Hero>

			<!-- Contenu de l'article -->
			<Section class="article-content">
				<div class="container">
					<div class="article-layout">
						<div class="article-layout__main">
							<div class="article-layout__image animate-fade-in">
								<img :src="currentArticle.image" :alt="currentArticle.title" />
							</div>

							<div class="article-layout__content">
								<p class="article-layout__intro animate-fade-in delay-1">
									{{ currentArticle.excerpt }}
								</p>

								<div class="article-layout__body animate-fade-in delay-2">
									<p v-for="(paragraph, index) in currentArticle.content" :key="index">
										{{ paragraph }}
									</p>
								</div>
							</div>
						</div>

						<div class="article-layout__sidebar animate-fade-in-up">
							<!-- Auteur de l'article (composant) -->
							<AuthorInfo
								:name="currentArticle.author?.name"
								:avatar="currentArticle.author?.avatar"
								:bio="currentArticle.author?.bio"
								:github="currentArticle.author?.social?.github"
								:linkedin="currentArticle.author?.social?.linkedin"
								:twitter="currentArticle.author?.social?.twitter"
							/>

							<!-- Tags de l'article (composant) -->
							<ArticleTags :tags="currentArticle.tags" />

							<!-- Articles populaires (composant) -->
							<PopularArticles :articles="popularArticlesProcessed" />
						</div>
					</div>
				</div>
			</Section>

			<!-- Articles similaires avec ArticleList au lieu de ArticleCard -->
			<Section v-if="relatedArticles && relatedArticles.length > 0" class="article-related" variant="light">
				<div class="container">
					<ArticleList
						:articles="relatedArticlesProcessed"
						title="Articles similaires"
						layout="grid"
						:card-hoverable="true"
						:show-author="true"
					/>
				</div>
			</Section>

			<!-- Call-to-action avec le composant CTA -->
			<CTA
				title="Vous avez un projet en tête ?"
				description="Discutons de vos besoins et voyons comment je peux vous aider à concrétiser votre vision avec mon expertise."
				type="card"
				variant="light"
				:primary-button="{
					label: 'Me contacter',
					to: ROUTES.CONTACT,
					variant: 'secondary',
					icon: 'mail',
				}"
				:secondary-button="{
					label: 'Voir tous les articles',
					to: ROUTES.BLOG,
					variant: 'outline',
					icon: 'blog',
				}"
			/>
		</template>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted, watch } from 'vue';
	import { useRoute, useRouter } from 'vue-router';

	// Importation des composants personnalisés
	import ArticleList from '@/components/feature/blog/ArticleList.vue';
	import PopularArticles from '@/components/feature/blog/ArticlePopular.vue';
	import ArticleTags from '@/components/feature/blog/ArticleTags.vue';
	import AuthorInfo from '@/components/feature/blog/AuthorInfo.vue';

	// Router et route
	const route = useRoute();
	const router = useRouter();
	const slug = computed(() => route.params.slug as string);

	// Utiliser le service useMock pour récupérer les données
	const {
		isLoading,
		error,
		currentArticle,
		relatedArticles,
		popularArticles,
		fetchArticleBySlug,
		fetchPopularArticles,
	} = useMock();

	// Conversion des articles en lecture seule vers le format attendu par les composants
	const relatedArticlesProcessed = computed(() => {
		if (!relatedArticles.value) return [];
		return Array.from(relatedArticles.value).map((article) => {
			return {
				...article,
				content: article.content ? Array.from(article.content) : [],
				tags: article.tags ? Array.from(article.tags) : [],
			};
		});
	});

	const popularArticlesProcessed = computed(() => {
		if (!popularArticles.value) return [];
		return Array.from(popularArticles.value).map((article) => {
			return {
				...article,
				content: article.content ? Array.from(article.content) : [],
				tags: article.tags ? Array.from(article.tags) : [],
			};
		});
	});

	// Charger les données lorsque le slug change
	watch(
		() => route.params.slug,
		async (newSlug) => {
			if (newSlug) {
				await fetchArticleBySlug(newSlug as string);
			}
		}
	);

	// Chargement initial des données
	onMounted(async () => {
		if (slug.value) {
			await fetchArticleBySlug(slug.value);
			await fetchPopularArticles(3); // Charger 3 articles populaires

			// Redirection en cas d'échec
			if (error.value && !currentArticle.value) {
				router.push(ROUTES.BLOG);
			}
		}
	});

	// Formatage de la date
	const formatDate = (dateString: string) => {
		const date = new Date(dateString);
		return new Intl.DateTimeFormat('fr-FR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
		}).format(date);
	};

	// Formatage du nombre de vues
	const formatViews = (views: number) => {
		if (views >= 1000) {
			return `${(views / 1000).toFixed(1)}k`;
		}
		return views;
	};

	// Obtenir le nom de la catégorie
	const getCategoryName = (categoryId: string) => {
		const categories: Record<string, string> = {
			web: 'Web',
			vue: 'Vue.js',
			react: 'React',
			typescript: 'TypeScript',
			javascript: 'JavaScript',
			node: 'Node.js',
			devops: 'DevOps',
			design: 'Design',
			ux: 'UX/UI',
			tools: 'Outils',
			tutorials: 'Tutoriels',
			other: 'Divers',
		};
		return categories[categoryId] || categoryId;
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Loader et écrans d'erreur
	.article-loader,
	.article-error {
		min-height: 60vh;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: vars.$spacing-xl 0;
	}

	// Contenu principal
	.article-content {
		padding: vars.$spacing-xl 0;
	}

	.article-layout {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: vars.$spacing-xl;

		@include mix.responsive(tablet) {
			grid-template-columns: 1fr;
		}

		&__main {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
		}

		&__image {
			border-radius: vars.$border-radius-lg;
			overflow: hidden;
			box-shadow: vars.$box-shadow-medium;

			img {
				width: 100%;
				height: auto;
				display: block;
			}
		}

		&__content {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
			background-color: vars.$white;
			border-radius: vars.$border-radius-lg;
			padding: vars.$spacing-lg;
			box-shadow: vars.$box-shadow-small;
		}

		&__intro {
			font-weight: 500;
			color: vars.$black-light;
			line-height: 1.6;
			padding-left: vars.$spacing-md;
			border-left: 3px solid vars.$primary-color;
		}

		&__body {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;

			p {
				line-height: 1.8;
				color: vars.$black-light;
			}
		}

		// Sidebar
		&__sidebar {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
			height: fit-content;

			@include mix.responsive(tablet) {
				order: -1;
			}
		}
	}

	// Articles similaires - Styles réduits car ArticleList gère l'affichage
	.article-related {
		padding: vars.$spacing-xl 0;
	}
</style>
