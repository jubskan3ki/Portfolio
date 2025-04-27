<template>
	<div :class="['article-list', `article-list--${layout}`, customClass]">
		<!-- En-tête de la liste -->
		<div v-if="title || $slots.header" class="article-list__header">
			<slot name="header">
				<h2 v-if="title" class="article-list__title">{{ title }}</h2>
				<p v-if="description" class="article-list__description">{{ description }}</p>
			</slot>
		</div>

		<!-- État de chargement -->
		<div v-if="loading" class="article-list__loading">
			<Spinner size="large" :label="loadingText" />
		</div>

		<!-- Message d'erreur -->
		<div v-else-if="error" class="article-list__error">
			<ErrorMessage :message="error" />
			<div v-if="retryable" class="article-list__retry">
				<BaseButton variant="primary" size="small" @click="$emit('retry')">
					{{ retryText }}
				</BaseButton>
			</div>
		</div>

		<!-- État vide -->
		<EmptyState
			v-else-if="!articles || articles.length === 0"
			:title="emptyTitle"
			:description="emptyDescription"
			icon="info"
			:icon-size="48"
		>
			<template v-if="$slots['empty-action']" #action>
				<slot name="empty-action"></slot>
			</template>
		</EmptyState>

		<!-- Liste des articles -->
		<div v-else :class="['article-list__grid', `article-list__grid--${layout}`]">
			<template v-for="(article, index) in articles" :key="article.id || index">
				<slot name="article" :article="article" :index="index">
					<ArticleCard
						:article="article"
						:hoverable="cardHoverable"
						:flat="cardFlat"
						:bordered="cardBordered"
						:excerpt-length="excerptLength"
						:show-author="showAuthor"
						:show-footer="showFooter"
						:show-stats="showStats"
						:read-more-text="readMoreText"
					/>
				</slot>
			</template>
		</div>

		<!-- Pagination -->
		<div v-if="showPagination && totalPages > 1" class="article-list__pagination">
			<Pagination
				:current-page="currentPage"
				:total-pages="totalPages"
				@update:current-page="$emit('update:currentPage', $event)"
				@page-change="$emit('page-change', $event)"
			/>
		</div>

		<!-- Pied de liste -->
		<div v-if="$slots.footer" class="article-list__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import ArticleCard from '@/components/feature/blog/ArticleCard.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Pagination from '@/components/navigation/Pagination.vue';

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

	defineProps({
		articles: {
			type: Array as () => Article[],
			default: () => [],
		},
		title: {
			type: String,
			default: '',
		},
		description: {
			type: String,
			default: '',
		},
		layout: {
			type: String,
			default: 'grid',
			validator: (value: string) => ['grid', 'list', 'compact'].includes(value),
		},
		loading: {
			type: Boolean,
			default: false,
		},
		error: {
			type: String,
			default: '',
		},
		retryable: {
			type: Boolean,
			default: false,
		},
		retryText: {
			type: String,
			default: 'Réessayer',
		},
		loadingText: {
			type: String,
			default: 'Chargement des articles...',
		},
		emptyTitle: {
			type: String,
			default: 'Aucun article trouvé',
		},
		emptyDescription: {
			type: String,
			default: "Il n'y a pas d'articles disponibles pour le moment.",
		},
		currentPage: {
			type: Number,
			default: 1,
		},
		totalPages: {
			type: Number,
			default: 1,
		},
		showPagination: {
			type: Boolean,
			default: true,
		},
		cardHoverable: {
			type: Boolean,
			default: true,
		},
		cardFlat: {
			type: Boolean,
			default: false,
		},
		cardBordered: {
			type: Boolean,
			default: false,
		},
		excerptLength: {
			type: Number,
			default: 150,
		},
		showAuthor: {
			type: Boolean,
			default: true,
		},
		showFooter: {
			type: Boolean,
			default: true,
		},
		showStats: {
			type: Boolean,
			default: true,
		},
		readMoreText: {
			type: String,
			default: 'Lire la suite',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	defineEmits(['update:currentPage', 'page-change', 'retry']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.article-list {
		width: 100%;

		&__header {
			margin-bottom: vars.$spacing-lg;
			text-align: center;
		}

		&__title {
			margin-bottom: vars.$spacing-sm;
			position: relative;
			display: inline-block;

			&::after {
				content: '';
				display: block;
				width: 50px;
				height: 3px;
				background-color: vars.$primary-color;
				margin: vars.$spacing-sm auto 0;
			}
		}

		&__description {
			max-width: 700px;
			margin: 0 auto;
			color: vars.$gray-dark;
		}

		&__loading,
		&__error {
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			padding: vars.$spacing-xl 0;
		}

		&__retry {
			margin-top: vars.$spacing-md;
		}

		&__grid {
			display: grid;
			grid-gap: vars.$spacing-lg;

			&--grid {
				grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));

				@include mix.responsive(mobile) {
					grid-template-columns: 1fr;
				}
			}

			&--list {
				grid-template-columns: 1fr;
			}

			&--compact {
				grid-template-columns: 1fr;
				grid-gap: vars.$spacing-md;
			}
		}

		&__pagination {
			margin-top: vars.$spacing-xl;
			display: flex;
			justify-content: center;
		}

		&__footer {
			margin-top: vars.$spacing-lg;
		}

		// Variante liste
		&--list {
			.article-list__grid {
				grid-template-columns: 1fr;
			}
		}
	}
</style>
