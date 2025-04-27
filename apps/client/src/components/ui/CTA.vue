<template>
	<Section
		:class="['cta-section', `cta-section--${variant}`, `cta-section--${type}`, className]"
		:variant="variant"
		primary
	>
		<div class="container">
			<div :class="['cta-section__content', { 'animate-fade-in-up': animate }]">
				<!-- Titre avec underline optionnel -->
				<h2 :class="['cta-section__title', { 'has-underline': showTitleUnderline }]">
					<slot name="title">{{ title }}</slot>
				</h2>

				<!-- Description -->
				<p class="cta-section__description">
					<slot name="description">{{ description }}</slot>
				</p>

				<!-- Boutons d'action -->
				<div class="cta-section__actions">
					<slot name="actions">
						<!-- Bouton principal -->
						<BaseButton
							v-if="primaryButtonConfig.show !== false"
							:to="primaryButtonConfig.to"
							:variant="primaryButtonConfig.variant"
							:size="primaryButtonConfig.size"
						>
							<BaseIcon
								v-if="primaryButtonConfig.icon"
								:name="primaryButtonConfig.icon"
								:size="20"
								class="mr-xs"
							/>
							{{ primaryButtonConfig.label }}
						</BaseButton>

						<!-- Bouton secondaire -->
						<BaseButton
							v-if="secondaryButtonConfig.show !== false"
							:to="secondaryButtonConfig.to"
							:variant="secondaryButtonConfig.variant"
							:size="secondaryButtonConfig.size"
						>
							<BaseIcon
								v-if="secondaryButtonConfig.icon"
								:name="secondaryButtonConfig.icon"
								:size="20"
								class="mr-xs"
							/>
							{{ secondaryButtonConfig.label }}
						</BaseButton>
					</slot>
				</div>

				<!-- Contenu supplémentaire -->
				<slot></slot>
			</div>
		</div>
	</Section>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import Section from '@/components/layouts/Section.vue';
	import { computed } from 'vue';

	const props = defineProps({
		// Contenu principal
		title: {
			type: String,
			default: 'Vous avez un projet en tête ?',
		},
		description: {
			type: String,
			default: 'Discutons de vos besoins et voyons comment je peux vous aider à concrétiser votre vision.',
		},

		// Apparence
		type: {
			type: String,
			default: 'card',
			validator: (value: string) => ['card', 'overlay'].includes(value),
		},
		variant: {
			type: String,
			default: 'primary',
			validator: (value: string) => ['primary', 'secondary', 'light'].includes(value),
		},
		showTitleUnderline: {
			type: Boolean,
			default: true,
		},
		animate: {
			type: Boolean,
			default: true,
		},
		className: {
			type: String,
			default: '',
		},

		// Boutons
		primaryButton: {
			type: Object,
			default: () => ({
				show: true,
				label: 'Me contacter',
				to: '/contact',
				icon: 'mail',
				size: 'large',
			}),
		},
		secondaryButton: {
			type: Object,
			default: () => ({
				show: true,
				label: 'Voir mes projets',
				to: '/projects',
				icon: 'folder',
				size: 'large',
			}),
		},
	});

	// Calcul de la variante par défaut du bouton principal
	const defaultPrimaryVariant = computed(() => {
		return props.type === 'card' ? 'primary' : 'secondary';
	});

	// Configuration complète des boutons avec valeurs par défaut
	const primaryButtonConfig = computed(() => {
		return {
			show: props.primaryButton?.show !== false,
			label: props.primaryButton?.label || 'Me contacter',
			to: props.primaryButton?.to || '/contact',
			variant: props.primaryButton?.variant || defaultPrimaryVariant.value,
			icon: props.primaryButton?.icon || 'mail',
			size: props.primaryButton?.size || 'large',
		};
	});

	const secondaryButtonConfig = computed(() => {
		return {
			show: props.secondaryButton?.show !== false,
			label: props.secondaryButton?.label || 'Voir mes projets',
			to: props.secondaryButton?.to || '/projects',
			variant: props.secondaryButton?.variant || 'outline',
			icon: props.secondaryButton?.icon || 'folder',
			size: props.secondaryButton?.size || 'large',
		};
	});
</script>

<style lang="scss">
	@use '@/styles/abstracts/functions' as func;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/variables' as vars;

	.cta-section {
		padding: vars.$spacing-xl 0;
		position: relative;
		overflow: hidden;

		// Variantes de fond
		&--light {
			background: linear-gradient(
				135deg,
				func.color-alpha(vars.$primary-color, 0.95),
				func.color-alpha(vars.$secondary-color, 0.85)
			);
		}

		&--primary,
		&--secondary {
			position: relative;

			&::before {
				content: '';
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				z-index: -1;
			}
		}

		&--primary::before {
			background: linear-gradient(
				135deg,
				func.color-alpha(vars.$primary-color, 0.9),
				func.color-alpha(vars.$secondary-color, 0.8)
			);
		}

		&--secondary::before {
			background: linear-gradient(
				135deg,
				func.color-alpha(vars.$secondary-color, 0.9),
				func.color-alpha(vars.$primary-color, 0.8)
			);
		}

		// Types de CTA
		&--card {
			// Contenu pour type "card"
			.cta-section__content {
				max-width: 800px;
				margin: 0 auto;
				text-align: center;
				padding: vars.$spacing-xl vars.$spacing-lg;
				border-radius: vars.$border-radius-lg;
				background-color: vars.$white;
				box-shadow: vars.$box-shadow-medium;
				border-top: 5px solid vars.$primary-color;
			}

			.cta-section__title {
				margin-bottom: vars.$spacing-md;
				color: vars.$primary-color;
				position: relative;
				display: inline-block;

				&.has-underline::after {
					content: '';
					display: block;
					width: 50%;
					height: 3px;
					background-color: vars.$secondary-color;
					margin: vars.$spacing-xs auto 0;
					border-radius: vars.$border-radius-full;
				}
			}

			.cta-section__description {
				margin-bottom: vars.$spacing-lg;
				color: vars.$gray-dark;
				max-width: 80%;
				margin-left: auto;
				margin-right: auto;
			}

			// Adaptation pour les variantes
			&.cta-section--primary,
			&.cta-section--secondary {
				.cta-section__content {
					background-color: func.color-alpha(vars.$white, 0.9);
				}
			}
		}

		&--overlay {
			// Contenu pour type "overlay"
			.cta-section__content {
				max-width: 800px;
				margin: 0 auto;
				text-align: center;
			}

			.cta-section__title {
				color: vars.$white;
				margin-bottom: vars.$spacing-md;

				&.has-underline::after {
					content: '';
					display: block;
					width: 60px;
					height: 3px;
					background-color: vars.$white;
					margin: vars.$spacing-sm auto 0;
					border-radius: vars.$border-radius-full;
				}
			}

			.cta-section__description {
				color: func.color-alpha(vars.$white, 0.9);
				margin-bottom: vars.$spacing-lg;
				line-height: 1.6;
			}
		}

		// Conteneur des actions (boutons)
		&__actions {
			display: flex;
			justify-content: center;
			gap: vars.$spacing-md;

			@include mix.responsive(mobile) {
				flex-direction: column;
				align-items: center;
			}
		}
	}
</style>
