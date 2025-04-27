<template>
	<div class="experience-page">
		<!-- En-tête avec le composant Hero -->
		<Hero
			title="Mon Parcours"
			description="Découvrez mon expérience professionnelle et mon parcours académique dans le domaine du développement web."
			variant="primary"
			show-title-underline
		/>

		<Section class="experience-content">
			<div class="container">
				<div class="experience-tabs">
					<Tabs v-model="activeTab" :tabs="tabs" />
				</div>

				<div class="experience-timeline-wrapper">
					<div v-if="isLoading" class="experience-loader">
						<Spinner type="circle" size="large" label="Chargement des données..." />
					</div>

					<template v-else>
						<!-- Expérience professionnelle -->
						<div v-if="activeTab === 'professional'" class="experience-section">
							<ExperienceTimeline :experiences="professionalExperiences" />
						</div>

						<!-- Formation -->
						<div v-if="activeTab === 'education'" class="experience-section">
							<ExperienceTimeline :experiences="educationExperiences" />
						</div>
					</template>
				</div>
			</div>
		</Section>

		<!-- Call-to-action avec le composant CTA -->
		<CTA
			title="Intéressé par mon profil?"
			description="N'hésitez pas à me contacter pour discuter de vos projets ou opportunités professionnelles."
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
				icon: 'folder',
				size: 'large',
			}"
		/>
	</div>
</template>

<script setup lang="ts">
	import ExperienceTimeline from '@/components/feature/experience/ExperienceTimeline.vue';
	import Section from '@/components/layouts/Section.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Tabs from '@/components/navigation/Tabs.vue';
	import CTA from '@/components/ui/CTA.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { onMounted, ref } from 'vue';

	// Récupération des données depuis le service mock
	const { isLoading, professionalExperiences, educationExperiences, fetchExperience } = useMock();

	// Chemins des routes pour les liens

	// Onglets
	const activeTab = ref('professional');
	const tabs = [
		{ id: 'professional', label: 'Expérience professionnelle' },
		{ id: 'education', label: 'Formation' },
	];

	// Chargement des données au montage du composant
	onMounted(async () => {
		await fetchExperience();
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.experience-page {
		display: flex;
		flex-direction: column;
		min-height: 100%;
	}

	.experience-content {
		padding: vars.$spacing-xl 0;
		background-color: func.color-alpha(vars.$white-dark, 0.6);
	}

	.experience-tabs {
		margin-bottom: vars.$spacing-xl;
		display: flex;
		justify-content: center;
	}

	.experience-loader {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 300px;
		background-color: func.color-alpha(vars.$white, 0.7);
		border-radius: vars.$border-radius-lg;
		box-shadow: vars.$box-shadow-small;
	}

	.experience-timeline-wrapper {
		min-height: 500px;
	}

	.skills-categories {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: vars.$spacing-xl;

		@include mix.responsive(mobile) {
			grid-template-columns: 1fr;
		}
	}

	.skills-category {
		&__title {
			margin-bottom: vars.$spacing-md;
			padding-bottom: vars.$spacing-sm;
			border-bottom: 3px solid vars.$primary-color;
			color: vars.$black-light;
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: -3px;
				left: 0;
				width: 30%;
				height: 3px;
				background-color: vars.$secondary-color;
			}
		}

		&__items {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}
	}

	.skill-item {
		display: flex;
		align-items: center;
		gap: vars.$spacing-md;
		padding: vars.$spacing-sm;
		border-radius: vars.$border-radius-sm;
		@include mix.transition(background-color);

		&:hover {
			background-color: func.color-alpha(vars.$white, 0.7);
		}

		&__name {
			min-width: 180px;
			font-weight: 500;
			color: vars.$black-light;
		}

		&__level {
			flex: 1;
		}
	}

	// Animation et effets
	.experience-section {
		animation: fadeIn vars.$transition-base forwards;
	}

	.skill-item {
		animation: fadeInUp vars.$transition-base forwards;
		opacity: 0;
	}

	@for $i from 1 through 10 {
		.delay-#{$i} {
			animation-delay: #{$i * 0.1}s;
		}
	}
</style>
