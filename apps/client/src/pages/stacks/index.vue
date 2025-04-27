<template>
	<div>
		<!-- En-tête des technologies avec le composant Hero -->
		<Hero
			title="Technologies"
			description="Découvrez les technologies que j'utilise pour développer des applications web modernes et performantes."
			variant="primary"
			show-title-underline
		/>

		<Section class="stacks-content">
			<div class="container">
				<div class="stacks-filters">
					<div class="stacks-filters__categories">
						<button
							v-for="stackCategories in stackCategories"
							:key="stackCategories.id"
							class="stacks-filters__category"
							:class="{ 'stacks-filters__category--active': selectedCategory === stackCategories.id }"
							@click="selectCategory(stackCategories.id)"
						>
							{{ stackCategories.name }}
						</button>
					</div>

					<div class="stacks-filters__search">
						<BaseInput
							v-model="searchQuery"
							placeholder="Rechercher une technologie..."
							type="search"
							:prepend-icon="'search'"
						/>
					</div>
				</div>

				<div v-if="isLoading" class="stacks-loader">
					<Spinner type="circle" size="large" label="Chargement des technologies..." />
				</div>

				<div v-else-if="filteredStacks.length === 0" class="stacks-empty">
					<EmptyState
						title="Aucune technologie trouvée"
						description="Aucune technologie ne correspond à vos critères de recherche."
						action-text="Réinitialiser les filtres"
						@action="resetFilters"
					/>
				</div>

				<div v-else>
					<div
						v-for="(group, groupName) in groupedStacks"
						v-show="group.length > 0"
						:key="groupName"
						class="stacks-group"
					>
						<h2 v-if="Object.keys(groupedStacks).length > 1" class="stacks-group__title">
							{{ getCategoryName(String(groupName)) }}
						</h2>
						<div class="stacks-grid animate-fade-in">
							<StackCard
								v-for="stack in group"
								:key="stack.id"
								:stack="stack"
								class="stack-card-item"
								@click="navigateToStack(stack.slug)"
							/>
						</div>
					</div>
				</div>
			</div>
		</Section>

		<!-- Call-to-action avec le composant CTA -->
		<CTA
			title="Travaillons ensemble"
			description="Vous cherchez un développeur maîtrisant ces technologies pour votre prochain projet ? Contactez-moi pour discuter de votre projet et voir comment je peux vous aider."
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
				label: 'Voir mes projets',
				to: ROUTES.PROJECTS,
				variant: 'outline',
				icon: 'projects',
				size: 'large',
			}"
		/>
	</div>
</template>

<script setup lang="ts">
	import BaseInput from '@/components/base/BaseInput.vue';
	import StackCard from '@/components/feature/stacks/StackCard.vue';
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { createPath, namedRoutes, ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import type { Stack } from '@/types/feature/stacks';
	import { computed, onMounted, ref } from 'vue';
	import { useRouter } from 'vue-router';

	// Router
	const router = useRouter();

	// Récupération des données depuis le service mock
	const { isLoading, stacks, stackCategories, fetchStacks, fetchStackCategories } = useMock();

	// État local
	const selectedCategory = ref('all');
	const searchQuery = ref('');

	// Technologies filtrées
	const filteredStacks = computed(() => {
		let result = [...stacks.value];

		// Filtrer par catégorie
		if (selectedCategory.value !== 'all') {
			result = result.filter((stack) => stack.category === selectedCategory.value);
		}

		// Filtrer par recherche
		if (searchQuery.value.trim()) {
			const query = searchQuery.value.toLowerCase().trim();
			result = result.filter(
				(stack) =>
					stack.name.toLowerCase().includes(query) ||
					stack.description.toLowerCase().includes(query) ||
					stack.tags.some((tag: string) => tag.toLowerCase().includes(query))
			);
		}

		return result;
	});

	// Regrouper les technologies par catégorie
	const groupedStacks = computed(() => {
		if (selectedCategory.value !== 'all') {
			return { [selectedCategory.value]: filteredStacks.value };
		}

		return filteredStacks.value.reduce<Record<string, Stack[]>>((groups, stack) => {
			const category = stack.category;
			if (!groups[category]) {
				groups[category] = [];
			}
			groups[category].push(stack);
			return groups;
		}, {});
	});

	// Méthodes
	const selectCategory = (categoryId: string) => {
		selectedCategory.value = categoryId;
	};

	const resetFilters = () => {
		selectedCategory.value = 'all';
		searchQuery.value = '';
	};

	const navigateToStack = (slug: string) => {
		const route = namedRoutes.goToStackDetail(slug);
		router.push(createPath(route));
	};

	// Obtenir le nom de la catégorie à partir de son ID
	const getCategoryName = (categoryId: string) => {
		const category = stackCategories.value.find((cat) => cat.id === categoryId);
		return category ? category.name : categoryId.charAt(0).toUpperCase() + categoryId.slice(1);
	};

	// Chargement initial des données
	onMounted(async () => {
		try {
			await Promise.all([fetchStacks(), fetchStackCategories()]);
		} catch (error) {
			console.error('Erreur lors du chargement des données:', error);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stacks-content {
		padding: vars.$spacing-xl 0;
		background-color: func.color-alpha(vars.$white-dark, 0.6);
		min-height: 60vh; // Assurer une hauteur minimale
	}

	.stacks-group {
		margin-bottom: vars.$spacing-xl;

		&__title {
			color: vars.$primary-color;
			margin-bottom: vars.$spacing-md;
			position: relative;
			padding-left: vars.$spacing-md;

			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 4px;
				height: 70%;
				background-color: vars.$primary-color;
				border-radius: vars.$border-radius-full;
			}
		}
	}

	.stacks-filters {
		margin-bottom: vars.$spacing-xl;
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: vars.$spacing-md;
		padding: vars.$spacing-md;
		background-color: vars.$white;
		border-radius: vars.$border-radius-md;
		box-shadow: vars.$box-shadow-small;

		@include mix.responsive(mobile) {
			flex-direction: column;
			align-items: stretch;
		}

		&__categories {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
		}

		&__category {
			padding: vars.$spacing-sm vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			background-color: vars.$white;
			color: vars.$gray-dark;
			border: 1px solid vars.$white-dark;
			cursor: pointer;
			font-weight: 500;
			@include mix.transition(transform, background-color, color, border-color);

			&:hover {
				background-color: vars.$white-dark;
				color: vars.$black-light;
				transform: translateY(-2px);
			}

			&--active {
				background-color: vars.$primary-color;
				color: vars.$white;
				border-color: vars.$primary-color;

				&:hover {
					background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
					color: vars.$white;
				}
			}
		}

		&__search {
			width: 300px;

			@include mix.responsive(mobile) {
				width: 100%;
			}
		}
	}

	.stacks-loader,
	.stacks-empty {
		min-height: 300px;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: func.color-alpha(vars.$white, 0.7);
		border-radius: vars.$border-radius-lg;
		box-shadow: vars.$box-shadow-small;
	}

	.stacks-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: vars.$spacing-lg;
		opacity: 0;
		animation: fadeIn vars.$transition-base forwards;
	}

	.stack-card-item {
		@include mix.transition(transform, box-shadow);
		border-radius: vars.$border-radius-md;
		overflow: hidden;
		background-color: vars.$white;
		box-shadow: vars.$box-shadow-small;

		&:hover {
			transform: translateY(-5px);
			box-shadow: vars.$box-shadow-medium;
		}
	}

	// Animation pour l'apparition des éléments
	.animate-fade-in {
		animation: fadeIn vars.$transition-base forwards;
	}

	.animate-fade-in-up {
		animation: fadeInUp vars.$transition-base forwards;
	}

	@for $i from 1 through 10 {
		.delay-#{$i} {
			animation-delay: #{$i * 0.1}s;
		}
	}
</style>
