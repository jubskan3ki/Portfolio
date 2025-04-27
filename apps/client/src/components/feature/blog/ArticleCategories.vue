<!--
  ArticleCategories.vue
  Composant pour afficher et filtrer par catégories d'articles
-->
<template>
	<Card class="article-categories">
		<h3 class="article-categories__title">{{ title }}</h3>
		<ul class="article-categories__list">
			<li v-for="category in categories" :key="category.id || category.slug" class="article-categories__item">
				<button
					class="article-categories__button"
					:class="{ 'article-categories__button--active': isActive(category) }"
					@click="handleSelect(category)"
				>
					<span class="article-categories__name">{{ category.name }}</span>
					<Badge
						v-if="category.count !== undefined"
						:text="category.count.toString()"
						type="primary"
						variant="subtle"
						rounded
					/>
				</button>
			</li>
		</ul>
	</Card>
</template>

<script setup lang="ts">
	import Badge from '@/components/ui/Badge.vue';
	import Card from '@/components/ui/Card.vue';

	interface Category {
		id: string | number;
		name: string;
		count?: number;
		slug?: string;
	}

	const props = defineProps({
		title: {
			type: String,
			default: 'Catégories',
		},
		categories: {
			type: Array as () => Category[] | readonly Category[],
			default: () => [],
		},
		modelValue: {
			type: [String, Number, Object],
			default: null,
		},
	});

	const emit = defineEmits(['update:modelValue', 'select']);

	const isActive = (category: Category) => {
		if (!props.modelValue) return false;

		if (typeof props.modelValue === 'object') {
			return (
				(category.id && props.modelValue.id === category.id) ||
				(category.slug && props.modelValue.slug === category.slug)
			);
		}

		return (
			(category.id && props.modelValue === category.id) || (category.slug && props.modelValue === category.slug)
		);
	};

	const handleSelect = (category: Category) => {
		const categoryId = category.id || category.slug;

		// Si la catégorie est déjà active, on la désélectionne
		if (isActive(category)) {
			emit('update:modelValue', null);
			emit('select', null);
		} else {
			emit('update:modelValue', categoryId);
			emit('select', categoryId);
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.article-categories {
		margin-bottom: vars.$spacing-lg;

		&__title {
			margin-bottom: vars.$spacing-md;
			padding-bottom: vars.$spacing-sm;
			border-bottom: 1px solid vars.$white-dark;
			color: vars.$primary-color;
			font-weight: 600;
		}

		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-xs;
		}

		&__button {
			display: flex;
			justify-content: space-between;
			align-items: center;
			width: 100%;
			padding: vars.$spacing-sm vars.$spacing-md;
			background-color: vars.$white-dark;
			border: none;
			border-radius: vars.$border-radius-sm;
			text-align: left;
			color: vars.$black-light;
			cursor: pointer;
			transition: all vars.$transition-base;
			font-weight: 500;

			&:hover {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				color: vars.$primary-color;
				transform: translateX(5px);
			}

			&--active {
				background-color: vars.$primary-color;
				color: vars.$white;
				box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

				&:hover {
					background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
					color: vars.$white;
				}
			}
		}
	}
</style>
