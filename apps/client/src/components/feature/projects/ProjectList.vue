<template>
	<div :class="['project-list', customClass]">
		<!-- En-tête -->

		<!-- Filtres par catégorie -->
		<div v-if="showFilters && categoryFilters.length > 0" class="project-list__filters">
			<div class="project-list__filter-label">{{ filterLabel }}:</div>
			<div class="project-list__filter-options">
				<button
					class="project-list__filter-btn"
					:class="{ 'project-list__filter-btn--active': activeFilter === 'all' }"
					@click="setFilter('all')"
				>
					{{ allFilterLabel }}
				</button>
				<button
					v-for="filter in categoryFilters"
					:key="filter.value"
					class="project-list__filter-btn"
					:class="{ 'project-list__filter-btn--active': activeFilter === filter.value }"
					@click="setFilter(filter.value)"
				>
					{{ filter.label }}
				</button>
			</div>
		</div>

		<!-- État de chargement -->
		<div v-if="loading" class="project-list__loading">
			<Spinner size="large" :label="loadingText" />
		</div>

		<!-- Message d'erreur -->
		<div v-else-if="error" class="project-list__error">
			<ErrorMessage :message="error" />
			<div v-if="retryable" class="project-list__retry">
				<BaseButton variant="primary" size="small" @click="$emit('retry')">
					{{ retryText }}
				</BaseButton>
			</div>
		</div>

		<!-- État vide -->
		<EmptyState
			v-else-if="!filteredProjects || filteredProjects.length === 0"
			:title="emptyTitle"
			:description="emptyDescription"
			icon="folder"
			:icon-size="48"
		>
			<template v-if="$slots['empty-action']" #action>
				<slot name="empty-action"></slot>
			</template>
		</EmptyState>

		<!-- Liste des projets -->
		<div v-else :class="['project-list__grid', `project-list__grid--${layout}`]">
			<template v-for="(project, index) in filteredProjects" :key="project.id || index">
				<slot name="project" :project="project" :index="index">
					<ProjectCard
						:project="project"
						:featured="isFeaturedProject(project)"
						:hoverable="cardHoverable"
						:flat="cardFlat"
						:bordered="cardBordered"
						:description-length="descriptionLength"
						:max-technologies="maxTechnologies"
					/>
				</slot>
			</template>
		</div>

		<!-- Pagination -->
		<div v-if="showPagination && totalPages > 1" class="project-list__pagination">
			<Pagination
				:current-page="currentPage"
				:total-pages="totalPages"
				@update:current-page="$emit('update:currentPage', $event)"
				@page-change="$emit('page-change', $event)"
			/>
		</div>

		<!-- Pied de liste -->
		<div v-if="$slots.footer" class="project-list__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Pagination from '@/components/navigation/Pagination.vue';
	import type { Project } from '@/types/feature/project';
	import { computed, ref } from 'vue';

	interface FilterOption {
		label: string;
		value: string;
	}

	// Interface projectData étendue pour le typage interne
	interface ProjectWithMeta extends Project {
		_featured?: boolean; // Propriété interne pour gérer les projets mis en avant
	}

	const props = defineProps({
		projects: {
			// Accepter à la fois Project[] et readonly Project[]
			type: Array as () => readonly Project[] | Project[],
			default: () => [],
		},
		layout: {
			type: String,
			default: 'grid',
			validator: (value: string) => ['grid', 'list', 'compact'].includes(value),
		},
		featuredProjects: {
			type: Array as () => (string | number)[],
			default: () => [],
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
			default: 'Tous les projets',
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
			default: 'Chargement des projets...',
		},
		emptyTitle: {
			type: String,
			default: 'Aucun projet',
		},
		emptyDescription: {
			type: String,
			default: 'Aucun projet ne correspond à votre recherche.',
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
		// Options pour ProjectCard
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
			default: 150,
		},
		maxTechnologies: {
			type: Number,
			default: 3,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['filter-change', 'update:currentPage', 'page-change', 'retry']);

	// Filtre actif
	const activeFilter = ref('all');

	// Définir le filtre
	const setFilter = (filter: string) => {
		activeFilter.value = filter;
		emit('filter-change', filter);
	};

	// Projets filtrés
	const filteredProjects = computed(() => {
		let filtered = [...props.projects];

		// Filtrer par catégorie
		if (activeFilter.value !== 'all') {
			filtered = filtered.filter((project) => project.category === activeFilter.value);
		}

		// Trier les projets (projets mis en avant en premier, puis par date)
		return filtered.sort((a, b) => {
			// Les projets mis en avant d'abord
			const aFeatured = isFeaturedProject(a);
			const bFeatured = isFeaturedProject(b);

			if (aFeatured && !bFeatured) return -1;
			if (!aFeatured && bFeatured) return 1;

			// Ensuite par date si disponible (du plus récent au plus ancien)
			if (a.date && b.date) {
				return new Date(b.date).getTime() - new Date(a.date).getTime();
			}

			return 0;
		});
	});

	// Vérifier si un projet est mis en avant
	const isFeaturedProject = (project: Project | Readonly<Project>): boolean => {
		// On vérifie d'abord dans le tableau des projets mis en avant
		if (props.featuredProjects.length > 0) {
			if (props.featuredProjects.includes(project.id)) {
				return true;
			}

			if (typeof project.slug === 'string' && props.featuredProjects.includes(project.slug)) {
				return true;
			}
		}

		// Si le projet a une propriété _featured (pour la compatibilité interne)
		const projectWithMeta = project as ProjectWithMeta;
		if (projectWithMeta._featured === true) {
			return true;
		}

		return false;
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.project-list {
		width: 100%;

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
				grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));

				@include mix.responsive(mobile) {
					grid-template-columns: 1fr;
				}
			}

			&--list {
				grid-template-columns: 1fr;

				:deep(.project-card) {
					@include mix.responsive(tablet-up) {
						:deep(.card) {
							display: flex;
							flex-direction: row;
							align-items: stretch;

							.card__image {
								width: 220px;
								flex-shrink: 0;
								margin-right: 0;
							}

							.card__content {
								flex: 1;
							}
						}

						.project-card__image {
							height: 100%;

							img {
								height: 100%;
							}
						}
					}
				}
			}

			&--compact {
				grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
				grid-gap: vars.$spacing-md;

				:deep(.project-card) {
					.project-card__image {
						height: 150px;
					}

					.project-card__description {
						display: none;
					}

					.project-card__technologies {
						margin-bottom: vars.$spacing-sm;
					}
				}
			}
		}

		&__pagination {
			margin-top: vars.$spacing-xl;
			display: flex;
			justify-content: center;
		}

		&__footer {
			margin-top: vars.$spacing-xl;
		}
	}

	// Animation pour les transitions
	.fade-enter-active,
	.fade-leave-active {
		transition: opacity 0.3s ease;
	}

	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}
</style>
