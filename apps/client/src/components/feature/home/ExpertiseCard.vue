<!-- components/feature/home/ExpertiseCard.vue -->
<template>
	<div
		class="expertise-card"
		:class="{ 'expertise-card': true, 'animate-on-scroll': animateOnScroll }"
		tabindex="0"
		role="button"
		:aria-label="`Expertise en ${title}`"
		:style="cardStyle"
	>
		<div class="expertise-card__header">
			<div class="expertise-card__icon" :style="iconStyle">
				<BaseIcon :name="icon" size="md" />
			</div>
			<h3 class="expertise-card__title">{{ title }}</h3>
		</div>
		<small class="expertise-card__description">{{ description }}</small>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed } from 'vue';

	interface ExpertiseCardProps {
		title: string;
		description: string;
		icon: string;
		color?: string;
		animateOnScroll?: boolean;
	}

	const props = withDefaults(defineProps<ExpertiseCardProps>(), {
		color: '',
		animateOnScroll: false,
	});

	const emit = defineEmits(['toggle']);

	// Calcule les couleurs du gradient en fonction de la couleur fournie
	const getGradientColors = computed(() => {
		const baseColor = props.color || 'var(--primary-color)';
		const lightColor = props.color ? adjustColorBrightness(props.color, 20) : 'var(--primary-light)';

		return {
			base: baseColor,
			light: lightColor,
		};
	});

	// Style pour la carte avec les variables CSS pour le before
	const cardStyle = computed(() => {
		return {
			'--card-base-color': getGradientColors.value.base,
			'--card-light-color': getGradientColors.value.light,
		};
	});

	// Style pour l'icône avec gradient
	const iconStyle = computed(() => {
		return {
			background: `linear-gradient(135deg, var(--card-base-color), var(--card-light-color))`,
		};
	});

	// Fonction pour ajuster la luminosité d'une couleur
	function adjustColorBrightness(color: string, percent: number): string {
		// Une implémentation simple pour les couleurs hexadécimales
		if (color.startsWith('#')) {
			const hex = color.slice(1);
			const r = parseInt(hex.slice(0, 2), 16);
			const g = parseInt(hex.slice(2, 4), 16);
			const b = parseInt(hex.slice(4, 6), 16);

			const newR = Math.min(255, Math.max(0, r + (r * percent) / 100));
			const newG = Math.min(255, Math.max(0, g + (g * percent) / 100));
			const newB = Math.min(255, Math.max(0, b + (b * percent) / 100));

			return `#${Math.round(newR).toString(16).padStart(2, '0')}${Math.round(newG).toString(16).padStart(2, '0')}${Math.round(newB).toString(16).padStart(2, '0')}`;
		}
		return color;
	}
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.expertise-card {
		background-color: vars.$white;
		border-radius: vars.$border-radius-lg;
		box-shadow: vars.$box-shadow-small;
		overflow: hidden;
		cursor: pointer;
		height: 100%;
		display: flex;
		flex-direction: column;
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease;
		position: relative;

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 5px;
			background: linear-gradient(90deg, var(--card-base-color), var(--card-light-color));
			z-index: 1;
		}

		&:hover {
			transform: translateY(-5px);
			box-shadow: vars.$box-shadow-large;
		}

		&__header {
			display: flex;
			align-items: center;
			gap: vars.$spacing-md;
			padding: vars.$spacing-md;
			transition:
				padding 0.3s ease,
				border-bottom 0.3s ease;
		}

		&__icon {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 48px;
			height: 48px;
			border-radius: vars.$border-radius-md;
			color: vars.$white;
			flex-shrink: 0;
			transition: transform 0.2s ease;
		}

		&__title {
			font-weight: 600;
			color: vars.$black-light;
			margin: 0;
		}

		&__description {
			line-height: 1.6;
			color: vars.$gray-dark;
			margin: 0;
			padding: 0 vars.$spacing-md vars.$spacing-md;
			transition: all 0.3s ease;
		}
	}

	// Support pour l'animation au scroll
	.animate-on-scroll {
		opacity: 0;
		transform: translateY(20px);
		transition:
			opacity 0.6s ease,
			transform 0.6s ease;

		&.animate-in {
			opacity: 1;
			transform: translateY(-5px);
		}
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
