<!--
  ArticleTags.vue
  Composant polyvalent pour afficher les tags d'articles
  - Mode affichage simple pour la page détail (display="simple")
  - Mode nuage interactif pour la page de liste (display="cloud")
-->
<template>
	<Card v-if="hasTags" class="article-tags">
		<h3 class="article-tags__title">{{ title }}</h3>

		<!-- Mode affichage simple (pour détail d'article) -->
		<div v-if="display === 'simple'" class="article-tags__grid">
			<BaseLink v-for="tag in stringTags" :key="tag" :to="`/blog?tag=${tag}`" class="article-tags__item">
				<BaseIcon name="hash" :size="14" />
				<span>{{ tag }}</span>
			</BaseLink>
		</div>

		<!-- Mode nuage de tags interactif (pour page liste) -->
		<div v-else class="article-tags__cloud">
			<button
				v-for="tag in objectTags"
				:key="tag.id"
				:class="['article-tags__tag', { 'article-tags__tag--active': isTagActive(tag.id) }]"
				@click="toggleTag(tag.id)"
			>
				<span class="article-tags__tag-name">{{ tag.name }}</span>
				<span v-if="hasCount(tag)" class="article-tags__tag-count">
					{{ getCount(tag) }}
				</span>
			</button>
		</div>
	</Card>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import Card from '@/components/ui/Card.vue';
	import type { Tag } from '@/types/feature/blog';
	import { computed } from 'vue';

	const props = defineProps({
		title: {
			type: String,
			default: 'Tags',
		},
		tags: {
			type: Array as () => string[] | readonly string[] | Tag[] | readonly Tag[],
			default: () => [],
		},
		modelValue: {
			type: Array as () => (string | number)[],
			default: () => [],
		},
		display: {
			type: String,
			default: 'cloud', // 'cloud' ou 'simple'
			validator: (value: string) => ['cloud', 'simple'].includes(value),
		},
		multiSelect: {
			type: Boolean,
			default: true,
		},
	});

	const emit = defineEmits(['update:modelValue', 'tag-toggle', 'tag-select']);

	// Vérifier s'il y a des tags à afficher
	const hasTags = computed(() => props.tags && props.tags.length > 0);

	// Détecter si les tags sont des objets ou des chaînes
	const isTagsObjects = computed(() => {
		if (props.tags.length === 0) return false;
		return typeof props.tags[0] !== 'string';
	});

	// Convertir les tags en tableaux de chaînes pour le mode simple
	const stringTags = computed(() => {
		if (!isTagsObjects.value) {
			return props.tags as string[] | readonly string[];
		}

		// Type guard pour vérifier si un objet a une propriété name
		const hasName = (obj: any): obj is { name: string } => {
			return obj && typeof obj === 'object' && 'name' in obj;
		};

		return (props.tags as any[]).map((tag) => (hasName(tag) ? tag.name : String(tag)));
	});

	// Convertir les tags en objets pour le mode cloud
	const objectTags = computed(() => {
		if (isTagsObjects.value) {
			return props.tags as Tag[] | readonly Tag[];
		}

		return (props.tags as string[] | readonly string[]).map((tag) => ({
			id: tag,
			name: tag,
		}));
	});

	// Fonctions helper pour vérifier et obtenir le count
	const hasCount = (tag: any): boolean => {
		return tag && typeof tag === 'object' && 'count' in tag && tag.count !== undefined;
	};

	const getCount = (tag: any): number => {
		return hasCount(tag) ? tag.count : 0;
	};

	// Vérifier si un tag est actif
	const isTagActive = (tagId: string | number) => {
		return props.modelValue.includes(tagId);
	};

	// Gérer le toggle d'un tag
	const toggleTag = (tagId: string | number) => {
		let newValue;

		if (props.multiSelect) {
			// En mode multi-sélection
			newValue = [...props.modelValue];

			const index = newValue.indexOf(tagId);
			if (index === -1) {
				// Ajouter le tag s'il n'est pas déjà sélectionné
				newValue.push(tagId);
			} else {
				// Retirer le tag s'il est déjà sélectionné
				newValue.splice(index, 1);
			}
		} else {
			// En mode sélection unique
			newValue = isTagActive(tagId) ? [] : [tagId];
		}

		emit('update:modelValue', newValue);
		emit('tag-toggle', tagId);
		emit('tag-select', newValue);
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.article-tags {
		margin-bottom: vars.$spacing-lg;

		&__title {
			margin-bottom: vars.$spacing-md;
			padding-bottom: vars.$spacing-sm;
			border-bottom: 1px solid vars.$white-dark;
			color: vars.$primary-color;
			font-weight: 600;
		}

		// Style pour mode simple (liens)
		&__grid {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
		}

		&__item {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			padding: vars.$spacing-xs vars.$spacing-sm;
			background-color: vars.$white-dark;
			border-radius: vars.$border-radius-full;
			color: vars.$primary-color;
			transition: all vars.$transition-base;

			&:hover {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				transform: translateY(-2px);
			}
		}

		// Style pour mode cloud (boutons)
		&__cloud {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
		}

		&__tag {
			display: inline-flex;
			align-items: center;
			padding: vars.$spacing-xs vars.$spacing-sm;
			background-color: vars.$white-dark;
			border: none;
			border-radius: vars.$border-radius-full;
			color: vars.$gray-dark;
			cursor: pointer;
			transition: all vars.$transition-base;

			&:hover {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				color: vars.$primary-color;
				transform: translateY(-2px);
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

		&__tag-count {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			margin-left: vars.$spacing-xs;
			min-width: 20px;
			height: 20px;
			border-radius: 10px;
			background-color: rgba(255, 255, 255, 0.4);
			padding: 0 vars.$spacing-xxs;
		}
	}
</style>
