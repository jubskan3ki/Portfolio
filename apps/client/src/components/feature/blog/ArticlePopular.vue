<!--
  PopularArticles.vue
  Composant pour afficher les articles populaires dans la sidebar
-->
<template>
	<Card class="popular-articles">
		<h3 class="popular-articles__title">Articles populaires</h3>
		<div class="popular-articles__list">
			<BaseLink
				v-for="article in articles"
				:key="article.id"
				:to="`/blog/${article.slug}`"
				class="popular-articles__item"
			>
				<div class="popular-articles__image">
					<img :src="article.image" :alt="article.title" />
				</div>
				<div class="popular-articles__info">
					<h4 class="popular-articles__name">{{ article.title }}</h4>
					<div class="popular-articles__meta">
						<span>{{ formatDate(article.date) }}</span>
						<span>•</span>
						<span>{{ article.readTime }} min</span>
					</div>
				</div>
			</BaseLink>
		</div>
	</Card>
</template>

<script setup lang="ts">
	import BaseLink from '@/components/base/BaseLink.vue';
	import Card from '@/components/ui/Card.vue';

	interface Article {
		id: string | number;
		slug: string;
		title: string;
		image: string;
		date: string;
		readTime: number;
	}

	defineProps({
		articles: {
			type: Array as () => Article[] | readonly Article[],
			default: () => [],
		},
	});

	// Formater la date
	const formatDate = (date: string | Date) => {
		try {
			const dateObj = date instanceof Date ? date : new Date(date);
			return dateObj.toLocaleDateString('fr-FR', {
				day: 'numeric',
				month: 'long',
				year: 'numeric',
			});
		} catch (e) {
			return '';
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.popular-articles {
		&__title {
			margin-bottom: vars.$spacing-md;
			padding-bottom: vars.$spacing-sm;
			border-bottom: 1px solid vars.$white-dark;
			color: vars.$primary-color;
		}

		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}

		&__item {
			display: flex;
			gap: vars.$spacing-md;
			padding-bottom: vars.$spacing-sm;
			border-bottom: 1px solid vars.$white-dark;
			transition: transform 0.3s ease;

			&:last-child {
				border-bottom: none;
				padding-bottom: 0;
			}

			&:hover {
				transform: translateX(5px);
			}
		}

		&__image {
			width: 80px;
			height: 60px;
			border-radius: vars.$border-radius-md;
			overflow: hidden;
			flex-shrink: 0;

			img {
				width: 100%;
				height: 100%;
				object-fit: cover;
			}
		}

		&__info {
			display: flex;
			flex-direction: column;
			justify-content: space-between;
		}

		&__name {
			font-weight: 500;
			color: vars.$black-light;
			@include mix.truncate(2);
		}

		&__meta {
			color: vars.$gray;
			display: flex;
			gap: vars.$spacing-xs;
		}
	}
</style>
