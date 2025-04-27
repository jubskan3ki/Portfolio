<template>
	<div :class="['experience-timeline', customClass]">
		<div v-if="showHeader && (title || subtitle || $slots.header)" class="experience-timeline__header">
			<slot name="header">
				<h2 v-if="title" class="experience-timeline__title">{{ title }}</h2>
				<p v-if="subtitle" class="experience-timeline__subtitle">{{ subtitle }}</p>
			</slot>
		</div>

		<!-- Filtres -->
		<div v-if="showFilters && filters.length > 0" class="experience-timeline__filters">
			<div class="experience-timeline__filter-label">{{ filterLabel }}:</div>
			<div class="experience-timeline__filter-options">
				<button
					class="experience-timeline__filter-btn"
					:class="{ 'experience-timeline__filter-btn--active': activeFilter === 'all' }"
					@click="setFilter('all')"
				>
					{{ allFilterLabel }}
				</button>
				<button
					v-for="filter in filters"
					:key="filter.value"
					class="experience-timeline__filter-btn"
					:class="{ 'experience-timeline__filter-btn--active': activeFilter === filter.value }"
					@click="setFilter(filter.value)"
				>
					{{ filter.label }}
				</button>
			</div>
		</div>

		<!-- Timeline -->
		<div class="experience-timeline__timeline">
			<div v-for="(experience, index) in filteredExperiences" :key="index" class="experience-timeline__item">
				<!-- Marqueur de timeline -->
				<div class="experience-timeline__marker">
					<div class="experience-timeline__dot"></div>
					<div v-if="index < filteredExperiences.length - 1" class="experience-timeline__line"></div>
				</div>

				<!-- Contenu -->
				<div class="experience-timeline__content">
					<slot name="experience-item" :experience="experience" :index="index">
						<ExperienceCard
							:title="experience.title"
							:company="experience.company"
							:logo="experience.logo"
							:location="experience.location"
							:start-date="experience.startDate"
							:end-date="experience.endDate"
							:description="experience.description"
							:skills="experience.technologies || experience.skills"
							:achievements="experience.achievements"
							:date-format="dateFormat"
							:current-text="currentText"
						/>
					</slot>
				</div>
			</div>

			<!-- État vide -->
			<div v-if="!loading && filteredExperiences.length === 0" class="experience-timeline__empty">
				<EmptyState :title="emptyTitle" :description="emptyDescription" icon="info" />
			</div>

			<!-- État de chargement -->
			<div v-if="loading" class="experience-timeline__loading">
				<Spinner size="large" :label="loadingText" />
			</div>
		</div>

		<!-- Pied de page -->
		<div v-if="$slots.footer" class="experience-timeline__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import ExperienceCard from '@/components/feature/experience/ExperienceCard.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import type { Experience } from '@/types/feature/experience';
	import { computed, ref } from 'vue';

	interface FilterOption {
		label: string;
		value: string;
	}

	const props = defineProps({
		experiences: {
			type: Array as () => Experience[] | readonly Experience[],
			default: () => [],
		},
		limit: {
			type: Number,
			default: undefined,
		},
		title: {
			type: String,
			default: '',
		},
		subtitle: {
			type: String,
			default: '',
		},
		showHeader: {
			type: Boolean,
			default: true,
		},
		showFilters: {
			type: Boolean,
			default: false,
		},
		filters: {
			type: Array as () => FilterOption[],
			default: () => [],
		},
		filterLabel: {
			type: String,
			default: 'Filtrer par',
		},
		allFilterLabel: {
			type: String,
			default: 'Tout',
		},
		defaultFilter: {
			type: String,
			default: 'all',
		},
		dateFormat: {
			type: String,
			default: 'MMM yyyy',
		},
		currentText: {
			type: String,
			default: 'Présent',
		},
		emptyTitle: {
			type: String,
			default: 'Aucune expérience',
		},
		emptyDescription: {
			type: String,
			default: 'Aucune expérience ne correspond à votre recherche.',
		},
		loading: {
			type: Boolean,
			default: false,
		},
		loadingText: {
			type: String,
			default: 'Chargement des expériences...',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['filter-change']);

	// Filtre actif
	const activeFilter = ref(props.defaultFilter);

	// Définir le filtre
	const setFilter = (filter: string) => {
		activeFilter.value = filter;
		emit('filter-change', filter);
	};

	// Expériences filtrées
	const filteredExperiences = computed(() => {
		let filtered;

		if (activeFilter.value === 'all') {
			filtered = [...props.experiences];
		} else {
			filtered = [...props.experiences].filter((experience) => experience.type === activeFilter.value);
		}

		// Trier par date de début (décroissante)
		filtered.sort((a, b) => {
			return new Date(b.startDate).getTime() - new Date(a.startDate).getTime();
		});

		// Appliquer la limite si elle est définie
		if (props.limit !== undefined) {
			return filtered.slice(0, props.limit);
		}

		return filtered;
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.experience-timeline {
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

		&__subtitle {
			color: vars.$gray-dark;
			max-width: 700px;
			margin: 0 auto;
		}

		&__filters {
			display: flex;
			align-items: center;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
			margin-bottom: vars.$spacing-lg;
			justify-content: center;
		}

		&__filter-label {
			font-weight: 500;
			color: vars.$black-light;
			margin-right: vars.$spacing-xs;
		}

		&__filter-options {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
		}

		&__filter-btn {
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
			}

			&--active {
				background-color: vars.$primary-color;
				color: vars.$white;

				&:hover {
					background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
				}
			}
		}

		&__timeline {
			position: relative;
			padding-left: 30px; // Espace pour la ligne et les points de la timeline

			@include mix.responsive(mobile) {
				padding-left: 20px;
			}
		}

		&__item {
			position: relative;
			padding-bottom: vars.$spacing-lg;

			&:last-child {
				padding-bottom: 0;
			}
		}

		&__marker {
			position: absolute;
			left: -30px;
			top: 0;
			height: 100%;
			display: flex;
			flex-direction: column;
			align-items: center;

			@include mix.responsive(mobile) {
				left: -20px;
			}
		}

		&__dot {
			width: 16px;
			height: 16px;
			border-radius: 50%;
			background-color: vars.$primary-color;
			box-shadow: 0 0 0 4px func.color-alpha(vars.$primary-color, 0.2);
			z-index: 2;
		}

		&__line {
			width: 2px;
			flex: 1;
			background-color: func.color-alpha(vars.$primary-color, 0.3);
			margin-top: 4px;
		}

		&__empty,
		&__loading {
			padding: vars.$spacing-xl 0;
			display: flex;
			justify-content: center;
		}

		&__footer {
			margin-top: vars.$spacing-xl;
			text-align: center;
		}
	}
</style>
