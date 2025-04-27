<!-- src/components/footer/PortfolioSummary.vue -->
<template>
	<div class="portfolio-summary">
		<div class="summary__content">
			<h3 class="summary__title">{{ title }}</h3>
			<p class="summary__description">{{ description }}</p>
			<div class="summary__cta">
				<BaseButton
					:to="ctaLinks.primary.url"
					:text="ctaLinks.primary.label"
					variant="primary"
					class="summary-button"
				/>
				<BaseButton
					:to="ctaLinks.secondary.url"
					:text="ctaLinks.secondary.label"
					variant="outline"
					custom-class="summary-button summary-button--white"
				/>
			</div>
		</div>
		<div class="summary__stats">
			<div v-for="(stat, index) in stats" :key="index" class="stat__item">
				<h3 class="stat__number">{{ stat.value }}+</h3>
				<p class="stat__label">{{ stat.label }}</p>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import { ROUTES } from '@/config/routes';
	import { StatItem } from '@/types/config/footer';
	import { PropType } from 'vue';

	// Type pour les objets route
	type RouteObject = { path: string; name?: string };

	// Interface pour les liens CTA
	interface CtaLink {
		label: string;
		url: string | RouteObject;
	}

	interface CtaLinks {
		primary: CtaLink;
		secondary: CtaLink;
	}

	defineProps({
		title: {
			type: String,
			default: 'Transformez vos idées en réalité numérique',
		},
		description: {
			type: String,
			default:
				"Développeur web passionné spécialisé dans la création d'expériences digitales innovantes et performantes. Expertise en Vue.js, Nuxt, et design responsive.",
		},
		ctaLinks: {
			type: Object as PropType<CtaLinks>,
			default: () => ({
				primary: {
					label: 'Discutons de votre projet',
					url: ROUTES.CONTACT,
				},
				secondary: {
					label: 'Voir mes réalisations',
					url: ROUTES.PROJECTS,
				},
			}),
		},
		stats: {
			type: Array as PropType<StatItem[]>,
			default: () => [
				{ value: 25, label: 'Projets réalisés' },
				{ value: 5, label: "Années d'expérience" },
				{ value: 18, label: 'Clients satisfaits' },
			],
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.portfolio-summary {
		background: linear-gradient(135deg, vars.$primary-color, vars.$secondary-color);
		border-radius: vars.$border-radius-lg;
		color: vars.$white;
		padding: vars.$spacing-lg;
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: vars.$spacing-lg;
		box-shadow: vars.$box-shadow-medium;
		position: relative;

		@include mix.responsive(tablet) {
			grid-template-columns: 1fr;
		}

		&::before,
		&::after {
			content: '';
			position: absolute;
			background: func.color-alpha(vars.$white, 0.1);
			border-radius: 50%;
		}

		&::before {
			top: 0;
			right: 0;
			width: 150px;
			height: 150px;
			transform: translate(50%, -50%);
		}

		&::after {
			bottom: 0;
			left: 0;
			width: 100px;
			height: 100px;
			transform: translate(-30%, 30%);
		}

		.summary {
			&__content {
				z-index: 1;
			}

			&__title {
				margin-bottom: vars.$spacing-md;
				color: vars.$white;
				font-weight: 600;
			}

			&__description {
				margin-bottom: vars.$spacing-lg;
				max-width: 600px;
				line-height: 1.6;
				color: func.color-alpha(vars.$white, 0.9);
			}

			&__cta {
				display: flex;
				gap: vars.$spacing-md;

				@include mix.responsive(mobile) {
					flex-direction: column;
				}
			}

			&__stats {
				display: flex;
				flex-direction: column;
				gap: vars.$spacing-md;
				z-index: 1;
			}
		}

		.stat {
			&__item {
				display: flex;
				flex-direction: column;
				align-items: center;
				padding: vars.$spacing-md;
				background: func.color-alpha(vars.$white, 0.1);
				border-radius: vars.$border-radius-md;
				text-align: center;
				backdrop-filter: blur(5px);
				transition: transform 0.3s ease;

				&:hover {
					transform: translateY(-5px);
				}
			}

			&__number {
				margin-bottom: vars.$spacing-xs;
				background: linear-gradient(90deg, vars.$white, #f0f0f0);
				background-clip: text;
				-webkit-background-clip: text;
				-webkit-text-fill-color: transparent;
			}

			&__label {
				color: func.color-alpha(vars.$white, 0.8);
			}
		}
	}

	/* Styles pour les boutons du sommaire */
	:deep(.summary-button) {
		padding: vars.$spacing-sm vars.$spacing-lg;
		border-radius: vars.$border-radius-md;
		font-weight: 500;
		transition: all vars.$transition-base;
		color: vars.$white;

		&:hover {
			transform: translateY(-3px);
		}
	}

	/* Ce sélecteur est séparé pour éviter l'erreur Sass */
	:deep(.summary-button--white) {
		background: transparent;
		border: 2px solid vars.$white;
		color: vars.$white;

		&:hover {
			background: func.color-alpha(vars.$white, 0.2);
		}
	}
</style>
