<template>
	<BaseLink :to="articleLink" class="article-card-wrapper">
		<Card :class="['article-card', customClass]" :hoverable="hoverable" :flat="flat" :bordered="bordered">
			<template v-if="article.image" #image>
				<div class="article-card__image">
					<img :src="article.image" :alt="article.title" />
				</div>
			</template>

			<template #header>
				<div class="article-card__meta">
					<div v-if="article.publishedAt || article.date" class="article-card__date">
						<BaseIcon name="calendar" :size="14" />
						<small>{{ formatDate(article.publishedAt || article.date) }}</small>
					</div>
					<div v-if="article.readTime" class="article-card__read-time">
						<BaseIcon name="clock" :size="14" />
						<small>{{ article.readTime }} min</small>
					</div>
					<div v-if="article.views" class="article-card__views">
						<BaseIcon name="eye" :size="14" />
						<small>{{ formatViews(article.views) }}</small>
					</div>
				</div>
				<h4 class="article-card__title">
					{{ article.title }}
				</h4>
			</template>

			<div class="article-card__content">
				<p v-if="article.excerpt" class="article-card__excerpt">
					{{ truncateText(article.excerpt, excerptLength) }}
				</p>
				<div v-if="showTags && article.tags?.length" class="article-card__tags">
					<Badge
						v-for="(tag, index) in article.tags.slice(0, maxTags)"
						:key="index"
						:text="'#' + tag"
						type="secondary"
						variant="subtle"
						rounded
						class="article-card__tag-badge"
					/>
				</div>
			</div>
		</Card>
	</BaseLink>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import Badge from '@/components/ui/Badge.vue';
	import Card from '@/components/ui/Card.vue';
	import { computed } from 'vue';

	interface Author {
		name: string;
		avatar?: string;
		bio?: string;
		social?: {
			github?: string;
			linkedin?: string;
			twitter?: string;
		};
	}

	interface Article {
		id: string | number;
		slug?: string;
		title: string;
		excerpt?: string;
		content?: string[] | readonly string[];
		image?: string;
		category?: string;
		tags?: string[] | readonly string[];
		date?: string;
		publishedAt?: string | Date;
		readTime?: number;
		views?: number;
		commentsCount?: number;
		likesCount?: number;
		toc?: string[] | readonly string[];
		author?: Author;
		[key: string]: any;
	}

	const props = defineProps({
		article: {
			type: Object as () => Article,
			required: true,
		},
		hoverable: {
			type: Boolean,
			default: true,
		},
		flat: {
			type: Boolean,
			default: false,
		},
		bordered: {
			type: Boolean,
			default: false,
		},
		excerptLength: {
			type: Number,
			default: 150,
		},
		customClass: {
			type: String,
			default: '',
		},
		showTags: {
			type: Boolean,
			default: true,
		},
		maxTags: {
			type: Number,
			default: 3,
		},
	});

	// Calculer le lien vers l'article
	const articleLink = computed(() => {
		if (props.article.slug) {
			return `/blog/${props.article.slug}`;
		}
		return `/blog/${props.article.id}`;
	});

	// Formater la date
	const formatDate = (date: string | Date | undefined) => {
		if (!date) return '';

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

	// Formater le nombre de vues
	const formatViews = (views: number) => {
		if (views >= 1000) {
			return `${Math.floor(views / 100) / 10}k`;
		}
		return views.toString();
	};

	// Tronquer le texte
	const truncateText = (text: string, length: number) => {
		if (text.length <= length) return text;
		return text.slice(0, length) + '...';
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.article-card-wrapper {
		display: block;
		height: 100%;
		text-decoration: none;
		color: inherit;
	}

	.article-card {
		height: 100%;
		display: flex;
		flex-direction: column;
		transition:
			transform vars.$transition-base,
			box-shadow vars.$transition-base;
		overflow: hidden;

		&:hover {
			transform: translateY(-3px);
		}

		:deep(.card__body) {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		&__image {
			position: relative;
			overflow: hidden;
			height: 200px;

			img {
				width: 100%;
				height: 200px;

				object-fit: cover;
				transition: transform vars.$transition-base;

				.article-card:hover & {
					transform: scale(1.05);
				}
			}
		}

		&__category {
			position: absolute;
			top: vars.$spacing-sm;
			left: vars.$spacing-sm;
			z-index: 10;
		}

		&__meta {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-md;
			margin-bottom: vars.$spacing-xs;
			color: vars.$gray-dark;

			@include mix.responsive(mobile) {
				gap: vars.$spacing-sm;
			}
		}

		&__date,
		&__read-time,
		&__views {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xxs;
		}

		&__title {
			margin: 0;
			margin-bottom: vars.$spacing-sm;
			line-height: 1.3;
			color: vars.$black-light;
			transition: color vars.$transition-base;

			.article-card:hover & {
				color: vars.$primary-color;
			}
		}

		&__content {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		&__excerpt {
			color: vars.$gray-dark;
			margin-bottom: vars.$spacing-md;
			line-height: 1.6;
			@include mix.truncate(3);
		}

		&__tags {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
			margin-top: auto;
			padding-top: vars.$spacing-sm;
		}

		&__tag-badge {
			font-weight: 400;
			transition: transform vars.$transition-fast;

			&:hover {
				transform: translateY(-2px);
			}
		}

		@include mix.responsive(tablet) {
			&__excerpt {
				@include mix.truncate(2);
			}
		}
	}
</style>
