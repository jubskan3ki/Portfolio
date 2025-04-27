<template>
	<div>
		<div v-if="isLoading" class="project-loader">
			<Spinner type="circle" size="large" label="Chargement du projet..." />
		</div>

		<div v-else-if="error" class="project-error">
			<ErrorMessage :message="error" action-text="Retour aux projets" :to="ROUTES.PROJECTS" />
		</div>

		<template v-else-if="currentProject">
			<!-- En-tête du projet avec le composant Hero -->
			<Hero :title="currentProject.title" variant="primary" show-title-underline has-meta>
				<template #meta>
					<div class="hero__meta-item">
						<BaseIcon name="calendar" :size="16" />
						<span>{{ formatDate(currentProject.date) }}</span>
					</div>
					<div class="hero__meta-item">
						<BaseIcon name="folder" :size="16" />
						<span>{{ getCategoryLabel(currentProject.category) }}</span>
					</div>
				</template>
			</Hero>

			<!-- Contenu principal du projet -->
			<Section class="project-content">
				<div class="container">
					<div class="project-content__wrapper">
						<!-- Colonne principale -->
						<div class="project-content__main">
							<div class="project-content__description animate-fade-in delay-1">
								<h2>Description du projet</h2>
								<p>{{ currentProject.description }}</p>
								<p v-if="currentProject.longDescription">{{ currentProject.longDescription }}</p>
							</div>

							<div
								v-if="currentProject.features && currentProject.features.length > 0"
								class="project-content__features animate-fade-in delay-2"
							>
								<h2>Fonctionnalités principales</h2>
								<ul>
									<li v-for="(feature, index) in currentProject.features" :key="index">
										{{ feature }}
									</li>
								</ul>
							</div>
						</div>

						<!-- Sidebar -->
						<div class="project-content__sidebar animate-fade-in-up">
							<div class="project-content__image animate-fade-in">
								<img :src="currentProject.image" :alt="currentProject.title" />
							</div>

							<div class="project-content__technologies-container">
								<h3>Technologies utilisées</h3>
								<div class="project-content__technologies">
									<StackBadge
										v-for="tech in currentProject.technologies"
										:key="tech"
										:stack="{ id: tech, name: tech }"
										size="medium"
										:show-name="true"
										:clickable="false"
									/>
								</div>
							</div>

							<div v-if="currentProject.links" class="project-content__links-container">
								<h3>Liens du projet</h3>
								<div class="project-content__links">
									<BaseLink
										v-if="currentProject.links.demo"
										:to="currentProject.links.demo"
										target="_blank"
										class="project-content__link"
									>
										<BaseIcon name="external-link" :size="16" />
										<span>Voir la démo</span>
									</BaseLink>
									<BaseLink
										v-if="currentProject.links.github"
										:to="currentProject.links.github"
										target="_blank"
										class="project-content__link"
									>
										<BaseIcon name="github" :size="16" />
										<span>Code source</span>
									</BaseLink>
									<BaseLink
										v-if="currentProject.links.documentation"
										:to="currentProject.links.documentation"
										target="_blank"
										class="project-content__link"
									>
										<BaseIcon name="book" :size="16" />
										<span>Documentation</span>
									</BaseLink>
								</div>
							</div>
						</div>
					</div>
				</div>
			</Section>

			<!-- Projets similaires -->
			<Section v-if="relatedProjects && relatedProjects.length > 0" class="project-related" variant="light">
				<div class="container">
					<ProjectList
						:projects="relatedProjects"
						:loading="isLoading"
						title="Projets similaires"
						:error="error !== null ? String(error) : ''"
						layout="grid"
						:show-filters="false"
					/>
				</div>
			</Section>

			<!-- Call-to-action avec le composant CTA -->
			<CTA
				title="Vous avez un projet similaire en tête ?"
				description="Discutons de la façon dont je peux vous aider à concrétiser votre vision avec les mêmes technologies et expertise."
				type="card"
				variant="light"
				:primary-button="{
					label: 'Me contacter',
					to: ROUTES.CONTACT,
					variant: 'secondary',
					icon: 'mail',
				}"
				:secondary-button="{
					label: 'Voir tous les projets',
					to: ROUTES.PROJECTS,
					variant: 'outline',
					icon: 'folder',
				}"
			/>
		</template>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import ProjectList from '@/components/feature/projects/ProjectList.vue';
	import StackBadge from '@/components/feature/stacks/StackBadge.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted, watch } from 'vue';
	import { useRoute, useRouter } from 'vue-router';

	// Router et route
	const route = useRoute();
	const router = useRouter();
	const slug = computed(() => route.params.slug as string);

	// Utiliser le service useMock pour récupérer les données du projet
	const { isLoading, error, currentProject, relatedProjects, fetchProjectBySlug } = useMock();

	// Charger les données du projet lorsque le slug change
	watch(
		() => route.params.slug,
		async (newSlug) => {
			if (newSlug) {
				await fetchProjectBySlug(newSlug as string);
			}
		}
	);

	// Chargement initial des données
	onMounted(async () => {
		if (slug.value) {
			await fetchProjectBySlug(slug.value);

			// Redirection en cas d'échec
			if (error.value && !currentProject.value) {
				router.push(ROUTES.PROJECTS);
			}
		}
	});

	// Formatage de la date
	const formatDate = (dateString: string) => {
		const date = new Date(dateString);
		return new Intl.DateTimeFormat('fr-FR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
		}).format(date);
	};

	// Obtenir le libellé de la catégorie
	const getCategoryLabel = (category: string) => {
		const categories: Record<string, string> = {
			web: 'Application Web',
			mobile: 'Application Mobile',
			devops: 'Solution DevOps',
			design: 'Design UI/UX',
			backend: 'Backend',
			frontend: 'Frontend',
		};
		return categories[category] || category;
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Loader et écrans d'erreur
	.project-loader,
	.project-error {
		min-height: 60vh;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: vars.$spacing-xl 0;
	}

	// Contenu principal du projet
	.project-content {
		padding: vars.$spacing-xl 0;

		&__wrapper {
			display: grid;
			grid-template-columns: 2fr 1fr;
			gap: vars.$spacing-xl;

			@include mix.responsive(tablet) {
				grid-template-columns: 1fr;
				gap: vars.$spacing-lg;
			}
		}

		&__main {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
		}

		&__image {
			border-radius: vars.$border-radius-lg;
			overflow: hidden;
			box-shadow: vars.$box-shadow-medium;
			position: relative;
			margin-bottom: vars.$spacing-lg;

			&::after {
				content: '';
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				background: linear-gradient(
					to bottom,
					func.color-alpha(vars.$black, 0),
					func.color-alpha(vars.$black, 0.05)
				);
				pointer-events: none;
			}

			img {
				width: 100%;
				height: auto;
				display: block;
				transition: transform vars.$transition-base;

				&:hover {
					transform: scale(1.02);
				}
			}
		}

		&__description,
		&__features {
			background-color: vars.$white;
			border-radius: vars.$border-radius-lg;
			padding: vars.$spacing-lg;
			box-shadow: vars.$box-shadow-small;

			h2 {
				margin-bottom: vars.$spacing-md;
				position: relative;
				padding-bottom: vars.$spacing-sm;
				color: vars.$primary-color;

				&::after {
					content: '';
					position: absolute;
					bottom: 0;
					left: 0;
					width: 60px;
					height: 3px;
					background-color: vars.$primary-color;
					border-radius: vars.$border-radius-full;
				}
			}

			p {
				margin-bottom: vars.$spacing-md;
				line-height: 1.7;
				color: vars.$black-light;

				&:last-child {
					margin-bottom: 0;
				}
			}
		}

		&__features {
			ul {
				padding-left: vars.$spacing-sm;
				margin-top: vars.$spacing-md;

				li {
					margin-bottom: vars.$spacing-sm;
					position: relative;
					padding-left: vars.$spacing-md;
					line-height: 1.6;

					&::before {
						content: '✓';
						position: absolute;
						left: 0;
						color: vars.$primary-color;
						font-weight: bold;
					}

					&:last-child {
						margin-bottom: 0;
					}
				}
			}
		}

		// Sidebar
		&__sidebar {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
			height: fit-content;

			@include mix.responsive(tablet) {
				order: -1;
			}
		}

		&__technologies-container,
		&__links-container {
			h3 {
				margin-bottom: vars.$spacing-md;
				color: vars.$primary-color;
				font-weight: 600;
				padding-bottom: vars.$spacing-xs;
				border-bottom: 1px solid vars.$white-dark;
			}
		}

		&__technologies {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-md;
			justify-content: flex-start;
		}

		&__links {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
		}

		&__link {
			display: flex;
			align-items: center;
			gap: vars.$spacing-sm;
			padding: vars.$spacing-sm;
			border-radius: vars.$border-radius-md;
			transition: all vars.$transition-base;
			color: vars.$primary-color;

			&:hover {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				transform: translateX(5px);
			}
		}
	}

	// Projets similaires
	.project-related {
		padding: vars.$spacing-xl 0;
		background-color: func.color-alpha(vars.$white-dark, 0.7);
	}
</style>
