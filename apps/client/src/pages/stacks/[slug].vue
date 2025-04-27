<template>
	<div>
		<div v-if="isLoading" class="stack-loader">
			<Spinner type="circle" size="large" label="Chargement de la technologie..." />
		</div>

		<div v-else-if="error" class="stack-error">
			<ErrorMessage :message="error" action-text="Retour aux technologies" :to="ROUTES.STACKS" />
		</div>

		<template v-else-if="currentStack">
			<!-- En-tête de la technologie avec le composant Hero -->
			<Hero
				:title="currentStack.name"
				variant="primary"
				:logo="currentStack.logo"
				:logo-alt="currentStack.name"
				has-meta
			>
				<template #meta>
					<div class="hero__meta-item">
						<BaseIcon name="folder" :size="16" />
						<span>{{ currentStack.category }}</span>
					</div>
					<div v-if="currentStack.firstRelease" class="hero__meta-item">
						<BaseIcon name="calendar" :size="16" />
						<span>Première version : {{ currentStack.firstRelease }}</span>
					</div>
					<div v-if="currentStack.license" class="hero__meta-item">
						<BaseIcon name="code" :size="16" />
						<span>Licence : {{ currentStack.license }}</span>
					</div>
				</template>

				<template #links>
					<BaseLink
						v-if="currentStack.website"
						variant="white"
						:to="currentStack.website"
						target="_blank"
						class="hero__link"
					>
						<BaseIcon name="external-link" :size="16" />
						<span>{{ currentStack.websiteLabel || 'Site officiel' }}</span>
					</BaseLink>

					<BaseLink
						v-if="currentStack.github"
						variant="white"
						:to="currentStack.github"
						target="_blank"
						class="hero__link"
					>
						<BaseIcon name="github" :size="16" />
						<span>{{ currentStack.githubLabel || 'GitHub' }}</span>
					</BaseLink>
				</template>
			</Hero>

			<!-- Contenu principal de la technologie -->
			<Section class="stack-content">
				<div class="container">
					<div class="stack-content__wrapper">
						<!-- Colonne principale -->
						<div class="stack-content__main">
							<div class="stack-content__overview animate-fade-in delay-1">
								<h2>Présentation</h2>
								<div class="stack-content__description">
									<p>{{ currentStack.description }}</p>
								</div>
							</div>

							<div v-if="currentStack.content" class="stack-content__details animate-fade-in delay-2">
								<h2>Détails techniques</h2>
								<div class="stack-content__details-text">
									<p>{{ currentStack.content }}</p>
								</div>
							</div>

							<!-- Utilisation du composant StackResources -->
							<StackResources :resources="currentStack.resources" />
						</div>

						<!-- Sidebar -->
						<div class="stack-content__sidebar animate-fade-in-up">
							<div class="stack-content__experience">
								<h3>Mon expérience</h3>
								<div class="stack-content__experience-info">
									<div class="stack-content__experience-years">
										<BaseIcon name="clock" :size="16" />
										<span>{{ currentStack.experience }} ans d'expérience</span>
									</div>
									<div class="stack-content__experience-level">
										<h4>Niveau de maîtrise</h4>
										<div class="stack-content__level-bar">
											<div
												class="stack-content__level-progress"
												:style="{ width: `${currentStack.level * 10}%` }"
											></div>
										</div>
										<div class="stack-content__level-label">
											{{ getLevelLabel(currentStack.level) }}
										</div>
									</div>
								</div>
							</div>

							<!-- Utilisation du composant StackRelated -->
							<StackRelated :stacks="relatedStacks" />

							<!-- Utilisation du composant StackTags -->
							<StackTags :tags="currentStack.tags" />
						</div>
					</div>
				</div>
			</Section>

			<!-- Call-to-action avec le composant CTA -->
			<CTA
				:title="`Besoin d'un développeur ${currentStack.name} ?`"
				:description="`Avec ${currentStack.experience} ans d'expérience en ${currentStack.name}, je peux vous aider à réaliser votre projet. Discutons de vos besoins et voyons comment ma maîtrise de cette technologie peut servir vos objectifs.`"
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
					label: 'Voir toutes les technologies',
					to: ROUTES.STACKS,
					variant: 'outline',
					icon: 'layers',
					size: 'large',
				}"
			/>
		</template>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted, watch } from 'vue';
	import { useRoute, useRouter } from 'vue-router';

	// Importation des composants personnalisés
	import StackRelated from '@/components/feature/stacks/StackRelated.vue';
	import StackResources from '@/components/feature/stacks/StackResources.vue';
	import StackTags from '@/components/feature/stacks/StackTags.vue';

	// Router et route
	const route = useRoute();
	const router = useRouter();
	const slug = computed(() => route.params.slug as string);

	// Utiliser le service useMock pour récupérer les données avec typage
	const { isLoading, error, currentStack, relatedStacks, fetchStackBySlug } = useMock();

	// Charger les données lorsque le slug change
	watch(
		() => route.params.slug,
		async (newSlug) => {
			if (newSlug) {
				await fetchStackBySlug(newSlug as string);
			}
		}
	);

	// Chargement initial des données
	onMounted(async () => {
		if (slug.value) {
			await fetchStackBySlug(slug.value);

			// Redirection en cas d'échec
			if (error.value && !currentStack.value) {
				router.push(ROUTES.STACKS);
			}
		}
	});

	// Obtenir le libellé du niveau de maîtrise
	const getLevelLabel = (level: number) => {
		const levels = {
			1: 'Débutant',
			2: 'Novice',
			3: 'Intermédiaire',
			4: 'Compétent',
			5: 'Avancé',
			6: 'Expert',
			7: 'Maître',
			8: 'Spécialiste',
			9: 'Expert reconnu',
			10: 'Référence',
		};
		return levels[level as keyof typeof levels] || `Niveau ${level}/10`;
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Loader et écrans d'erreur
	.stack-loader,
	.stack-error {
		min-height: 60vh;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: vars.$spacing-xl 0;
	}

	// Contenu principal
	.stack-content {
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

		// Sections du contenu principal
		&__overview,
		&__details {
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

		// Sidebar
		&__sidebar {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
			height: fit-content;

			@include mix.responsive(tablet) {
				order: -1;
			}

			> div {
				background-color: vars.$white;
				border-radius: vars.$border-radius-lg;
				padding: vars.$spacing-lg;
				box-shadow: vars.$box-shadow-small;
			}

			h3 {
				margin-bottom: vars.$spacing-md;
				color: vars.$primary-color;
				font-weight: 600;
				padding-bottom: vars.$spacing-xs;
				border-bottom: 1px solid vars.$white-dark;
			}
		}

		// Expérience
		&__experience-info {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}

		&__experience-years {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$gray-dark;
			font-weight: 500;
		}

		&__experience-level {
			h4 {
				color: vars.$gray-dark;
				margin-bottom: vars.$spacing-xs;
			}
		}

		&__level-bar {
			height: 8px;
			background-color: vars.$white-dark;
			border-radius: vars.$border-radius-full;
			overflow: hidden;
			margin-bottom: vars.$spacing-xs;
		}

		&__level-progress {
			height: 100%;
			background: linear-gradient(to right, vars.$primary-color, vars.$secondary-color);
			border-radius: vars.$border-radius-full;
		}

		&__level-label {
			text-align: right;
			color: vars.$gray;
		}
	}
</style>
