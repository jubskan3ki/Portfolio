<template>
	<div :class="['stack-list', customClass]">
		<!-- En-tête -->
		<div v-if="title || $slots.header" class="stack-list__header">
			<slot name="header">
				<h2 v-if="title" class="stack-list__title">{{ title }}</h2>
				<p v-if="description" class="stack-list__description">{{ description }}</p>
			</slot>
		</div>

		<!-- Filtres par catégorie -->
		<div v-if="showFilters && categoryFilters.length > 0" class="stack-list__filters">
			<div class="stack-list__filter-label">{{ filterLabel }}:</div>
			<div class="stack-list__filter-options">
				<button
					class="stack-list__filter-btn"
					:class="{ 'stack-list__filter-btn--active': activeFilter === 'all' }"
					@click="setFilter('all')"
				>
					{{ allFilterLabel }}
				</button>
				<button
					v-for="filter in categoryFilters"
					:key="filter.value"
					class="stack-list__filter-btn"
					:class="{ 'stack-list__filter-btn--active': activeFilter === filter.value }"
					@click="setFilter(filter.value)"
				>
					{{ filter.label }}
				</button>
			</div>
		</div>

		<!-- État de chargement -->
		<div v-if="loading" class="stack-list__loading">
			<Spinner size="large" :label="loadingText" />
		</div>

		<!-- Message d'erreur -->
		<div v-else-if="error" class="stack-list__error">
			<ErrorMessage :message="error" />
			<div v-if="retryable" class="stack-list__retry">
				<BaseButton variant="primary" size="small" @click="$emit('retry')">
					{{ retryText }}
				</BaseButton>
			</div>
		</div>

		<!-- État vide -->
		<EmptyState
			v-else-if="!filteredStacks || filteredStacks.length === 0"
			:title="emptyTitle"
			:description="emptyDescription"
			icon="folder"
			:icon-size="48"
		>
			<template v-if="$slots['empty-action']" #action>
				<slot name="empty-action"></slot>
			</template>
		</EmptyState>

		<!-- Mode badges -->
		<div v-else-if="displayMode === 'badges'" class="stack-list__badges">
			<StackBadge
				v-for="stack in filteredStacks"
				:key="stack.id"
				:stack="stack"
				:size="badgeSize"
				:show-name="showStackName"
				:show-level="showStackLevel"
				:clickable="clickableItems"
				@click="handleStackClick(stack)"
			/>
		</div>

		<!-- Mode grille ou liste -->
		<div v-else :class="['stack-list__grid', `stack-list__grid--${displayMode}`]">
			<template v-for="(stack, index) in filteredStacks" :key="stack.id || index">
				<slot name="stack" :stack="stack" :index="index">
					<StackCard
						:stack="stack"
						:hoverable="cardHoverable"
						:flat="cardFlat"
						:bordered="cardBordered"
						:show-level="showStackLevel"
						:description-length="descriptionLength"
					/>
				</slot>
			</template>
		</div>

		<!-- Pied de liste -->
		<div v-if="$slots.footer" class="stack-list__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import type { Stack } from '@/types/feature/stacks';
	import { computed, ref } from 'vue';
	import StackBadge from './StackBadge.vue';
	import StackCard from './StackCard.vue';

	interface FilterOption {
		label: string;
		value: string;
	}

	const props = defineProps({
		stacks: {
			type: Array as () => Stack[],
			default: () => [],
		},
		title: {
			type: String,
			default: 'Compétences Techniques',
		},
		description: {
			type: String,
			default: '',
		},
		displayMode: {
			type: String,
			default: 'grid',
			validator: (value: string) => ['grid', 'list', 'badges'].includes(value),
		},
		showFilters: {
			type: Boolean,
			default: true,
		},
		categoryFilters: {
			type: Array as () => FilterOption[],
			default: () => [],
		},
		filterLabel: {
			type: String,
			default: 'Filtrer par',
		},
		allFilterLabel: {
			type: String,
			default: 'Toutes les technologies',
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
			default: 'Chargement des technologies...',
		},
		emptyTitle: {
			type: String,
			default: 'Aucune technologie',
		},
		emptyDescription: {
			type: String,
			default: 'Aucune technologie ne correspond à votre recherche.',
		},
		// Options pour les badges
		badgeSize: {
			type: String,
			default: 'medium',
			validator: (value: string) => ['small', 'medium', 'large'].includes(value),
		},
		showStackName: {
			type: Boolean,
			default: true,
		},
		showStackLevel: {
			type: Boolean,
			default: true,
		},
		clickableItems: {
			type: Boolean,
			default: false,
		},
		// Options pour les cartes
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
		descriptionLength: {
			type: Number,
			default: 200,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['filter-change', 'stack-click', 'retry']);

	// Filtre actif
	const activeFilter = ref('all');

	// Définir le filtre
	const setFilter = (filter: string) => {
		activeFilter.value = filter;
		emit('filter-change', filter);
	};

	// Technologies filtrées
	const filteredStacks = computed(() => {
		let filtered = [...props.stacks];

		// Filtrer par catégorie
		if (activeFilter.value !== 'all') {
			filtered = filtered.filter((stack) => stack.category === activeFilter.value);
		}

		// Trier les stacks par niveau (du plus élevé au plus bas)
		return filtered.sort((a, b) => {
			// Si les deux ont un niveau, trier par niveau décroissant
			if (a.level !== undefined && b.level !== undefined) {
				return b.level - a.level;
			}

			// Si seulement a a un niveau, a vient en premier
			if (a.level !== undefined) return -1;

			// Si seulement b a un niveau, b vient en premier
			if (b.level !== undefined) return 1;

			// Sinon, trier par nom
			return a.name.localeCompare(b.name);
		});
	});

	// Gérer le clic sur une technologie
	const handleStackClick = (stack: Stack) => {
		emit('stack-click', stack);
	};
</script>

<style lang="scss" scoped>
	@use '../../../styles/abstracts/variables' as vars;
	@use '../../../styles/abstracts/mixins' as mix;
	@use '../../../styles/abstracts/functions' as func;

	.stack-list {
		width: 100%;

		&__header {
			text-align: center;
			margin-bottom: vars.$spacing-xl;
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

		&__filters {
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
			margin-bottom: vars.$spacing-lg;
			padding: vars.$spacing-md 0;
			border-bottom: 1px solid vars.$gray-light;
		}

		&__filter-label {
			font-weight: 600;
			margin-right: vars.$spacing-sm;
		}

		&__filter-options {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
		}

		&__filter-btn {
			padding: vars.$spacing-xs vars.$spacing-sm;
			background-color: vars.$white-dark;
			border: 1px solid vars.$gray-light;
			border-radius: vars.$border-radius-sm;
			cursor: pointer;
			transition: all 0.2s ease;

			&:hover {
				background-color: func.adjust-color-brightness(vars.$primary-color, 35%);
			}

			&--active {
				background-color: vars.$primary-color;
				color: white;
				border-color: vars.$primary-color;

				&:hover {
					background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
				}
			}
		}

		&__loading {
			display: flex;
			justify-content: center;
			padding: vars.$spacing-xl 0;
		}

		&__error {
			text-align: center;
			padding: vars.$spacing-xl 0;
		}

		&__retry {
			margin-top: vars.$spacing-md;
		}

		&__badges {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-md;
			margin: vars.$spacing-lg 0;
			justify-content: center;
		}

		&__grid {
			width: 100%;
			display: grid;
			gap: vars.$spacing-lg;

			&--grid {
				grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));

				@include mix.responsive(mobile) {
					grid-template-columns: 1fr;
				}
			}

			&--list {
				grid-template-columns: 1fr;
			}
		}

		&__footer {
			margin-top: vars.$spacing-xl;
			text-align: center;
		}
	}

	// Animations pour les filtres
	.filter-enter-active,
	.filter-leave-active {
		transition:
			opacity 0.3s,
			transform 0.3s;
	}

	.filter-enter-from,
	.filter-leave-to {
		opacity: 0;
		transform: translateY(10px);
	}

	// Animations pour les cartes
	.stack-enter-active,
	.stack-leave-active {
		transition:
			opacity 0.4s,
			transform 0.4s;
	}

	.stack-enter-from {
		opacity: 0;
		transform: translateY(20px);
	}

	.stack-leave-to {
		opacity: 0;
		transform: scale(0.9);
	}

	// Responsive adjustments
	@include mix.responsive(tablet) {
		.stack-list {
			&__filters {
				flex-direction: column;
				align-items: flex-start;
			}

			&__filter-label {
				margin-bottom: vars.$spacing-xs;
			}
		}
	}
</style>
