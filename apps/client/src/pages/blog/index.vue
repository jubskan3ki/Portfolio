<template>
	<div>
		<!-- En-tête du blog avec le composant Hero -->
		<Hero
			title="Blog"
			description="Articles techniques et partage de connaissances sur le développement web et DevOps."
			variant="primary"
			show-title-underline
		/>

		<!-- Contenu principal du blog -->
		<Section class="blog-content">
			<div class="container">
				<!-- Barre de recherche en haut (sur toute la largeur) -->
				<div class="blog-search">
					<BaseInput
						v-model="searchQuery"
						placeholder="Rechercher un article..."
						type="search"
						prepend-icon="search"
						class="blog-search__input"
						@keyup.enter="handleSearch"
					/>
				</div>

				<!-- Filtres actifs -->
				<ArticleActiveFilters
					v-if="hasActiveFilters"
					:active-category="selectedCategory"
					:active-tags="selectedTags"
					:categories="blogCategories"
					:tags="blogTags"
					class="blog-active-filters"
					@remove-category="handleCategorySelect(null)"
					@remove-tag="handleTagToggle"
					@clear-all="resetFilters"
				/>

				<!-- Layout principal (grille) -->
				<div class="blog-layout">
					<!-- Colonne principale -->
					<div class="blog-layout__main">
						<!-- Loader / État vide -->
						<div v-if="isLoading" class="blog-loader">
							<Spinner type="circle" size="large" label="Chargement des articles..." />
						</div>

						<div v-else-if="displayedArticles.length === 0" class="blog-empty">
							<EmptyState
								title="Aucun article trouvé"
								description="Aucun article ne correspond aux critères de recherche actuels."
								action-text="Réinitialiser les filtres"
								@action="resetFilters"
							/>
						</div>

						<!-- Liste des articles -->
						<div v-else>
							<ArticleList
								:articles="displayedArticles"
								class="animate-fade-in"
								layout="grid"
								:card-hoverable="true"
								:show-author="true"
							/>

							<Pagination
								v-if="totalPages > 1"
								:current-page="currentPage"
								:total-pages="totalPages"
								class="blog-pagination"
								@page-change="handlePageChange"
							/>
						</div>
					</div>

					<!-- Sidebar -->
					<div class="blog-layout__sidebar">
						<!-- Catégories -->
						<ArticleCategories
							:categories="blogCategories"
							:model-value="selectedCategory"
							@select="handleCategorySelect"
						/>

						<!-- Tags -->
						<ArticleTagCloud :tags="blogTags" :model-value="selectedTags" @tag-toggle="handleTagToggle" />

						<!-- Articles populaires -->
						<ArticlePopular :articles="popularArticles" />
					</div>
				</div>
			</div>
		</Section>

		<!-- Call to Action Section avec le composant CTA -->
		<CTA
			title="Vous avez un projet en tête ?"
			description="En tant que développeur passionné, je suis toujours à la recherche de nouveaux défis. Discutons de votre projet et voyons comment je peux vous aider à le concrétiser."
			type="card"
			variant="light"
			class-name="blog-cta"
			:primary-button="{
				label: 'Me contacter',
				to: ROUTES.CONTACT,
				variant: 'secondary',
				icon: 'mail',
			}"
			:secondary-button="{
				label: 'Voir mes projets',
				to: ROUTES.PROJECTS,
				variant: 'outline',
				icon: 'projects',
			}"
		/>
	</div>
</template>

<script setup lang="ts">
	import BaseInput from '@/components/base/BaseInput.vue';
	import ArticleActiveFilters from '@/components/feature/blog/ArticleActiveFilters.vue';
	import ArticleCategories from '@/components/feature/blog/ArticleCategories.vue';
	import ArticleList from '@/components/feature/blog/ArticleList.vue';
	import ArticlePopular from '@/components/feature/blog/ArticlePopular.vue';
	import ArticleTagCloud from '@/components/feature/blog/ArticleTags.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Pagination from '@/components/navigation/Pagination.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted, ref, watch } from 'vue';

	// Récupération des données depuis le service mock
	const {
		isLoading,
		articles,
		blogCategories,
		blogTags,
		popularArticles,
		fetchArticles,
		fetchBlogCategories,
		fetchBlogTags,
		fetchPopularArticles,
	} = useMock();

	// État
	const selectedCategory = ref('');
	const selectedTags = ref<string[]>([]);
	const searchQuery = ref('');
	const currentPage = ref(1);
	const itemsPerPage = 6;

	// Vérifier s'il y a des filtres actifs
	const hasActiveFilters = computed(() => {
		return selectedCategory.value || selectedTags.value.length > 0 || searchQuery.value;
	});

	// Réinitialiser la page lors d'un changement de filtre
	watch([selectedCategory, selectedTags, searchQuery], () => {
		currentPage.value = 1;
	});

	// Articles filtrés
	const filteredArticles = computed(() => {
		let result = [...articles.value];

		// Filtrer par recherche
		if (searchQuery.value.trim()) {
			const query = searchQuery.value.toLowerCase();
			result = result.filter(
				(article) =>
					article.title.toLowerCase().includes(query) || article.excerpt.toLowerCase().includes(query)
			);
		}

		// Filtrer par catégorie
		if (selectedCategory.value) {
			result = result.filter((article) => article.category === selectedCategory.value);
		}

		// Filtrer par tags
		if (selectedTags.value.length > 0) {
			result = result.filter((article) => selectedTags.value.every((tag) => article.tags.includes(tag)));
		}

		return result;
	});

	// Articles paginés
	const displayedArticles = computed(() => {
		// Convertir les tableaux readonly en tableaux modifiables pour les composants
		const start = (currentPage.value - 1) * itemsPerPage;
		const end = start + itemsPerPage;

		// Créer une copie modifiable pour éviter les problèmes de readonly
		return filteredArticles.value.slice(start, end).map((article) => ({
			...article,
			content: article.content ? Array.from(article.content) : [],
			tags: article.tags ? Array.from(article.tags) : [],
		}));
	});

	// Total des pages pour la pagination
	const totalPages = computed(() => {
		return Math.ceil(filteredArticles.value.length / itemsPerPage);
	});

	// Méthodes
	const resetFilters = () => {
		selectedCategory.value = '';
		selectedTags.value = [];
		searchQuery.value = '';
		currentPage.value = 1;
	};

	const handleSearch = () => {};

	const handleCategorySelect = (categoryId: string | null) => {
		selectedCategory.value = categoryId || '';
	};

	const handleTagToggle = (tagId: string) => {
		const index = selectedTags.value.indexOf(tagId);
		if (index === -1) {
			selectedTags.value.push(tagId);
		} else {
			selectedTags.value.splice(index, 1);
		}
	};

	const handlePageChange = (page: number) => {
		currentPage.value = page;
		// Remonter en haut de la page avec animation fluide
		window.scrollTo({ top: 0, behavior: 'smooth' });
	};

	// Chargement initial des données
	onMounted(async () => {
		try {
			await Promise.all([fetchArticles(), fetchBlogCategories(), fetchBlogTags(), fetchPopularArticles()]);
		} catch (error) {
			console.error('Erreur lors du chargement des données du blog:', error);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Contenu du blog
	.blog-content {
		padding: vars.$spacing-xl 0;
		position: relative;
		background-color: func.color-alpha(vars.$white-dark, 0.7);
	}

	// Barre de recherche
	.blog-search {
		margin-bottom: vars.$spacing-lg;

		&__input {
			max-width: 800px;
			margin: 0 auto;
		}
	}

	// Filtres actifs
	.blog-active-filters {
		margin-bottom: vars.$spacing-lg;
	}

	// Layout principal
	.blog-layout {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: vars.$spacing-xl;

		@include mix.responsive(tablet) {
			grid-template-columns: 1fr;
			gap: vars.$spacing-lg;
		}

		&__main {
			min-height: 600px;
		}

		&__sidebar {
			@include mix.responsive(tablet) {
				order: -1;
			}
		}
	}

	// États de chargement et vides
	.blog-loader,
	.blog-empty {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 400px;
		background-color: vars.$white;
		border-radius: vars.$border-radius-md;
		box-shadow: vars.$box-shadow-medium;
	}

	// Pagination
	.blog-pagination {
		margin-top: vars.$spacing-lg;
		padding: vars.$spacing-md;
		border-top: 1px solid vars.$white-dark;
	}

	// Animation pour l'apparition des éléments
	.animate-fade-in {
		animation: fadeIn vars.$transition-base forwards;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
