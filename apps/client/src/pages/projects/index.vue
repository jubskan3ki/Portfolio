<template>
	<div class="projects-page">
		<!-- En-tête des projets avec le composant Hero -->
		<Hero
			title="Mes Projets"
			description="Découvrez les projets sur lesquels j'ai travaillé, des applications web aux solutions DevOps."
			variant="primary"
			:show-title-underline="true"
		/>

		<Section class="projects-section">
			<div class="container">
				<!-- Filtres de projets améliorés mais simples -->
				<div class="projects-filters">
					<div class="projects-filters__row flex">
						<!-- Filtre par catégorie -->
						<div class="projects-filters__select">
							<BaseSelect v-model="selectedCategory" :options="categoryOptions" label="Catégorie" />
						</div>

						<!-- Filtre par technologie (corrigé) -->
						<div class="projects-filters__select">
							<BaseSelect v-model="selectedTechnology" :options="techOptions" label="Technologie" />
						</div>

						<!-- Actions de filtres -->
						<div class="projects-filters__actions">
							<BaseButton
								v-if="hasActiveFilters"
								variant="secondary"
								class="projects-filters__reset-btn"
								@click="resetFilters"
							>
								<BaseIcon name="x-circle" :size="16" class="mr-xs" />
								Réinitialiser les filtres
							</BaseButton>
						</div>
					</div>

					<!-- Affichage des filtres actifs -->
					<div v-if="hasActiveFilters" class="projects-filters__active">
						<div class="active-filters-label">Filtres actifs:</div>
						<div class="active-filters-tags">
							<div v-if="selectedCategory" class="active-filter">
								<span>{{ getCategoryName(selectedCategory) }}</span>
								<BaseIcon
									name="close"
									:size="14"
									class="active-filter__remove"
									@click="selectedCategory = ''"
								/>
							</div>
							<div v-if="selectedTechnology" class="active-filter">
								<span>{{ getTechName(selectedTechnology) }}</span>
								<BaseIcon
									name="close"
									:size="14"
									class="active-filter__remove"
									@click="selectedTechnology = ''"
								/>
							</div>
						</div>
					</div>
				</div>

				<!-- État de chargement -->
				<div v-if="isLoading" class="projects-loader flex flex--center">
					<Spinner type="circle" size="large" label="Chargement des projets..." />
				</div>

				<!-- État vide -->
				<div v-else-if="filteredProjects.length === 0" class="projects-empty flex flex--center">
					<EmptyState
						title="Aucun projet trouvé"
						description="Aucun projet ne correspond aux critères de filtrage actuels."
						action-text="Réinitialiser les filtres"
						@action="resetFilters"
					/>
				</div>

				<!-- Mode liste -->
				<div v-else class="projects-list">
					<ProjectList :projects="filteredProjects" class="animate-fade-in-up" />
				</div>
			</div>

			<!-- Pagination -->
			<Pagination
				v-if="totalPages > 1"
				:current-page="currentPage"
				:total-pages="totalPages"
				class="projects-pagination mt-xl"
				@page-change="handlePageChange"
			/>
		</Section>

		<!-- Call-to-action -->
		<CTA
			title="Vous avez un projet en tête ?"
			description="Je serais ravi de discuter de vos idées et de voir comment je peux vous aider à concrétiser votre vision."
			type="card"
			variant="light"
			:primary-button="{
				label: 'Me contacter',
				to: ROUTES.CONTACT,
				variant: 'secondary',
				icon: 'mail',
				size: 'large',
			}"
			:secondary-button="{
				label: 'Voir mon parcours',
				to: ROUTES.EXPERIENCE,
				variant: 'outline',
				icon: 'experience',
				size: 'large',
			}"
		/>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseSelect from '@/components/base/BaseSelect.vue';
	import ProjectList from '@/components/feature/projects/ProjectList.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Pagination from '@/components/navigation/Pagination.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import type { Project, ProjectCategory } from '@/types/feature/project';
	import type { Stack } from '@/types/feature/stacks';
	import { computed, onMounted, ref, watch } from 'vue';

	// Récupération des données depuis le service mock
	const { isLoading, projects, projectCategories, stacks, fetchProjects, fetchProjectCategories, fetchStacks } =
		useMock();

	// État local
	const selectedCategory = ref('');
	const selectedTechnology = ref('');
	const currentPage = ref(1);
	const itemsPerPage = 6;

	// Options pour les sélecteurs
	const categoryOptions = computed(() => {
		return [
			...projectCategories.value.map((category) => ({
				value: category.id,
				label: category.name,
			})),
		];
	});

	// Utilisons les stacks à la place de projectTechnologies
	const techOptions = computed(() => {
		const baseOption = [{ value: '', label: 'Toutes les technologies' }];

		if (!stacks.value || stacks.value.length === 0) {
			return baseOption;
		}

		return [
			...baseOption,
			...stacks.value.map((tech: Stack) => ({
				value: tech.name, // Utiliser le nom au lieu de l'id
				label: tech.name,
			})),
		];
	});

	// Fonction pour vérifier si une technologie est présente dans les technologies d'un projet
	const hasTechnology = (project: Project, techName: string): boolean => {
		if (!project.technologies) return false;

		// Vérifier si technologies est un tableau
		if (Array.isArray(project.technologies)) {
			// Effectuer une recherche insensible à la casse
			return project.technologies.some(
				(tech) => typeof tech === 'string' && tech.toLowerCase() === techName.toLowerCase()
			);
		}

		return false;
	};

	// Projets filtrés (tous, avant pagination)
	const filteredProjectsAll = computed(() => {
		let result = [...projects.value];

		// Filtre par catégorie
		if (selectedCategory.value) {
			result = result.filter((project) => project.category === selectedCategory.value);
		}

		// Filtre par technologie (corrigé)
		if (selectedTechnology.value) {
			result = result.filter((project) => hasTechnology(project, selectedTechnology.value));
		}

		return result;
	});

	// Projets filtrés avec pagination
	const filteredProjects = computed(() => {
		const start = (currentPage.value - 1) * itemsPerPage;
		const end = start + itemsPerPage;
		return filteredProjectsAll.value.slice(start, end);
	});

	// Total des pages pour la pagination
	const totalPages = computed(() => {
		return Math.ceil(filteredProjectsAll.value.length / itemsPerPage) || 1;
	});

	// Vérifier si des filtres sont actifs
	const hasActiveFilters = computed(() => selectedCategory.value !== '' || selectedTechnology.value !== '');

	// Fonctions utilitaires
	const getCategoryName = (categoryId: string) => {
		const category = projectCategories.value?.find((c: ProjectCategory) => c.id === categoryId);
		return category ? category.name : categoryId;
	};

	const getTechName = (techName: string) => {
		// Comme on utilise le nom directement, on peut simplement le retourner
		return techName;
	};

	// Méthodes
	const resetFilters = () => {
		selectedCategory.value = '';
		selectedTechnology.value = '';
		currentPage.value = 1;
	};

	const handlePageChange = (page: number) => {
		currentPage.value = page;
		// Remonter en haut de la section des projets
		const projectsSection = document.querySelector('.projects-section');
		if (projectsSection) {
			projectsSection.scrollIntoView({ behavior: 'smooth' });
		}
	};

	// Réinitialiser la page lorsque les filtres changent
	watch([selectedCategory, selectedTechnology], () => {
		currentPage.value = 1;
	});

	// Chargement initial des données
	onMounted(async () => {
		try {
			// Charger les projets et catégories
			await Promise.all([
				fetchProjects(),
				fetchProjectCategories(),
				fetchStacks(), // Charger les stacks pour le filtre de technologies
			]);
		} catch (error) {
			console.error('Error loading data:', error);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.projects-page {
		position: relative;
	}

	.projects-section {
		min-height: 60vh;
		padding: vars.$spacing-xl 0;
		background-color: func.color-alpha(vars.$white-dark, 0.6);
	}

	.projects-filters {
		margin-bottom: vars.$spacing-xl;
		padding: vars.$spacing-md;
		background-color: vars.$white;
		border-radius: vars.$border-radius-md;
		box-shadow: vars.$box-shadow-small;

		&__row {
			display: flex;
			gap: vars.$spacing-md;
			align-items: center;

			@include mix.responsive(mobile) {
				flex-direction: column;
				align-items: stretch;
			}
		}

		&__select {
			flex: 1;
		}

		&__actions {
			@include mix.responsive(mobile) {
				margin-top: vars.$spacing-sm;
			}
		}

		&__reset-btn {
			@include mix.transition(transform);

			&:hover {
				transform: translateY(-2px);
			}
		}

		&__active {
			margin-top: vars.$spacing-md;
			padding-top: vars.$spacing-sm;
			border-top: 1px solid func.color-alpha(vars.$gray, 0.2);
			display: flex;
			align-items: center;

			@include mix.responsive(mobile) {
				flex-direction: column;
				align-items: flex-start;
			}

			.active-filters-label {
				font-weight: 500;
				margin-right: vars.$spacing-md;
				color: vars.$gray-dark;

				@include mix.responsive(mobile) {
					margin-bottom: vars.$spacing-xs;
				}
			}

			.active-filters-tags {
				display: flex;
				flex-wrap: wrap;
				gap: vars.$spacing-xs;
			}

			.active-filter {
				display: flex;
				align-items: center;
				padding: 4px 10px;
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				border-radius: vars.$border-radius-full;
				color: vars.$primary-color;

				&__remove {
					margin-left: vars.$spacing-xs;
					cursor: pointer;
					opacity: 0.7;

					&:hover {
						opacity: 1;
					}
				}
			}
		}
	}

	.projects-loader,
	.projects-empty {
		min-height: 300px;
		background-color: func.color-alpha(vars.$white, 0.7);
		border-radius: vars.$border-radius-lg;
		box-shadow: vars.$box-shadow-small;
	}

	// Styles de la pagination centrée
	.projects-pagination {
		display: flex;
		justify-content: center;
	}

	// Animations
	.animate-fade-in {
		animation: fadeIn vars.$transition-base forwards;
	}

	.animate-fade-in-up {
		animation: fadeInUp vars.$transition-base forwards;
	}
</style>
