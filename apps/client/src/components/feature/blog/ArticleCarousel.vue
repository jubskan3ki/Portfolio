<!-- components/feature/blog/ArticleCarousel.vue -->
<template>
	<div class="article-carousel">
		<div v-if="isLoading" class="article-carousel__loader">
			<Spinner type="circle" label="Chargement des articles..." />
		</div>

		<div v-else-if="error" class="article-carousel__error">
			<p>{{ error }}</p>
		</div>

		<div v-else-if="displayedArticles.length === 0" class="article-carousel__empty">
			<EmptyState title="Aucun article" description="Aucun article n'est disponible pour le moment." />
		</div>

		<div v-else class="article-carousel__content">
			<div v-if="title || subtitle" class="article-carousel__header">
				<h2 v-if="title" class="article-carousel__title">{{ title }}</h2>
				<p v-if="subtitle" class="article-carousel__subtitle">{{ subtitle }}</p>
			</div>

			<Swiper
				:slides="displayedArticles.length"
				:slides-to-show="slidesToShow"
				:slides-to-scroll="1"
				:autoplay="autoplay"
				:autoplay-interval="autoplaySpeed"
				:show-controls="false"
				:show-dots="showDots"
				@change="onSlideChange"
			>
				<template v-for="(article, index) in displayedArticles" :key="article.id" v-slot:[`slide-${index}`]>
					<ArticleCard
						:article="article"
						:hoverable="true"
						:show-author="showAuthor"
						:show-footer="showFooter"
						:show-stats="showStats"
						:excerpt-length="excerptLength"
						custom-class="article-carousel__card"
					/>
				</template>
			</Swiper>
		</div>
	</div>
</template>

<script setup lang="ts">
	import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Swiper from '@/components/ui/Swiper.vue';
	import { computed, ref, watch } from 'vue';

	// Types
	interface Author {
		name: string;
		avatar?: string;
	}

	interface Article {
		id: string | number;
		slug?: string;
		title: string;
		excerpt?: string;
		content?: string[] | readonly string[];
		image?: string;
		category?: string;
		publishedAt?: string | Date;
		readTime?: number;
		commentsCount?: number;
		likesCount?: number;
		author?: Author;
		[key: string]: any;
	}

	// Props
	interface ArticleCarouselProps {
		articles: Article[] | readonly Article[];
		title?: string;
		subtitle?: string;
		limit?: number;
		showAuthor?: boolean;
		showFooter?: boolean;
		showStats?: boolean;
		showDots?: boolean;
		autoplay?: boolean;
		autoplaySpeed?: number;
		excerptLength?: number;
		isLoading?: boolean;
		error?: string | null;
		category?: string;
	}

	const props = withDefaults(defineProps<ArticleCarouselProps>(), {
		limit: 5,
		showAuthor: true,
		showFooter: true,
		showStats: true,
		showDots: true,
		showViewAllButton: true,
		viewAllLink: '/blog',
		autoplay: false,
		autoplaySpeed: 5000,
		excerptLength: 100,
		isLoading: false,
		error: null,
	});

	// Émetteurs d'événements
	const emit = defineEmits(['change']);

	// État du carousel
	const currentIndex = ref(0);

	// Filtrer les articles pour respecter la limite et la catégorie
	const displayedArticles = computed(() => {
		let filteredArticles = [...props.articles];

		// Filtrer par catégorie si définie
		if (props.category) {
			filteredArticles = filteredArticles.filter(
				(article) => article.category && article.category.toLowerCase() === props.category!.toLowerCase()
			);
		}

		// Limiter le nombre d'articles
		return filteredArticles.slice(0, props.limit);
	});

	// Calculer le nombre de slides à afficher en fonction de la largeur d'écran
	const slidesToShow = computed(() => {
		// Vérifie si window est défini (pour SSR)
		if (typeof window === 'undefined') return 1;

		const width = window.innerWidth;
		if (width < 768) return 1;
		if (width < 1024) return 2;
		return 3;
	});

	// Gérer le changement de slide
	const onSlideChange = (index: number) => {
		currentIndex.value = index;
		emit('change', index);
	};

	// Réinitialiser l'index quand les articles changent
	watch(
		() => props.articles,
		() => {
			currentIndex.value = 0;
		}
	);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.article-carousel {
		position: relative;
		overflow: hidden;

		&__loader,
		&__error,
		&__empty {
			display: flex;
			justify-content: center;
			align-items: center;
			min-height: 200px;
		}

		&__header {
			text-align: center;
			margin-bottom: vars.$spacing-xl;
		}

		&__title {
			font-weight: 700;
			margin-bottom: vars.$spacing-sm;
			color: vars.$black-light;
		}

		&__subtitle {
			color: vars.$gray-dark;
			max-width: 800px;
			margin: 0 auto;
		}

		&__content {
			width: 100%;
		}

		&__card {
			height: 100%;
		}

		&__actions {
			display: flex;
			justify-content: center;
			align-items: center;
			margin-top: vars.$spacing-xl;
		}

		&__view-all {
			display: inline-flex;
			align-items: center;
			gap: vars.$spacing-xs;
		}
	}
</style>
