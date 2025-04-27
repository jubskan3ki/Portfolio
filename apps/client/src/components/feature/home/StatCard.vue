<!-- components/feature/home/StatCard.vue -->
<template>
	<div class="stat-card" :class="`stat-card--${variant}`" @mouseenter="startCount">
		<div class="stat-card__icon">
			<BaseIcon :name="icon" size="lg" />
		</div>
		<div class="stat-card__content">
			<div class="stat-card__number">
				<span class="counter">{{ displayValue }}</span>
				<span v-if="suffix">{{ suffix }}</span>
			</div>
			<p class="stat-card__label">{{ label }}</p>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed, onMounted, ref } from 'vue';

	const props = defineProps({
		value: {
			type: [Number, String],
			required: true,
		},
		label: {
			type: String,
			required: true,
		},
		icon: {
			type: String,
			required: true,
		},
		variant: {
			type: String,
			default: 'primary',
			validator: (value: string) => ['primary', 'secondary', 'accent'].includes(value),
		},
		suffix: {
			type: String,
			default: '',
		},
		duration: {
			type: Number,
			default: 2000, // ms
		},
	});

	const currentValue = ref(0);
	const counted = ref(false);
	const displayValue = computed(() => {
		// Si c'est une chaîne avec un "+" à la fin (comme "25+"), on affiche juste la valeur complète
		if (typeof props.value === 'string' && props.value.endsWith('+')) {
			const numPart = parseInt(props.value.replace('+', ''));
			return Math.min(numPart, currentValue.value);
		}

		// Sinon c'est un nombre normal
		return currentValue.value;
	});

	const targetValue = computed(() => {
		if (typeof props.value === 'string') {
			// Si c'est une chaîne comme "25+", on extrait juste le nombre
			if (props.value.endsWith('+')) {
				return parseInt(props.value.replace('+', ''));
			}
			return parseInt(props.value);
		}
		return props.value;
	});

	const startCount = () => {
		if (counted.value) return;

		counted.value = true;
		const startTime = Date.now();
		const endTime = startTime + props.duration;

		const updateCounter = () => {
			const now = Date.now();
			const remaining = Math.max(0, endTime - now);
			const progress = 1 - remaining / props.duration;

			currentValue.value = Math.floor(progress * targetValue.value);

			if (remaining > 0) {
				requestAnimationFrame(updateCounter);
			} else {
				currentValue.value = targetValue.value;
			}
		};

		updateCounter();
	};

	onMounted(() => {
		// Vérifier si la carte est visible dans le viewport
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						startCount();
						observer.disconnect();
					}
				});
			},
			{ threshold: 0.5 }
		);

		// Trouver l'élément parent ou la carte elle-même
		const element = document.querySelector('.stat-card');
		if (element) {
			observer.observe(element);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stat-card {
		display: flex;
		padding: vars.$spacing-lg;
		background-color: vars.$white;
		border-radius: vars.$border-radius-lg;
		box-shadow: vars.$box-shadow-small;
		height: 100%;
		@include mix.transition(transform, box-shadow);
		position: relative;
		overflow: hidden;
		z-index: 1;

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 5px;
			background: linear-gradient(
				90deg,
				vars.$primary-color,
				func.adjust-color-brightness(vars.$primary-color, 20%)
			);
			z-index: 1;
		}

		&:hover {
			transform: translateY(-5px);
			box-shadow: vars.$box-shadow-medium;
		}

		&--primary::before {
			background: linear-gradient(
				90deg,
				vars.$primary-color,
				func.adjust-color-brightness(vars.$primary-color, 20%)
			);
		}

		&--secondary::before {
			background: linear-gradient(
				90deg,
				vars.$secondary-color,
				func.adjust-color-brightness(vars.$secondary-color, 20%)
			);
		}

		&--accent::before {
			background: linear-gradient(90deg, vars.$info-color, func.adjust-color-brightness(vars.$info-color, 20%));
		}

		&__icon {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 60px;
			height: 60px;
			border-radius: vars.$border-radius-md;
			margin-right: vars.$spacing-md;
			color: vars.$white;
			flex-shrink: 0;

			.stat-card--primary & {
				background: linear-gradient(
					135deg,
					vars.$primary-color,
					func.adjust-color-brightness(vars.$primary-color, 15%)
				);
			}

			.stat-card--secondary & {
				background: linear-gradient(
					135deg,
					vars.$secondary-color,
					func.adjust-color-brightness(vars.$secondary-color, 15%)
				);
			}

			.stat-card--accent & {
				background: linear-gradient(
					135deg,
					vars.$info-color,
					func.adjust-color-brightness(vars.$info-color, 15%)
				);
			}
		}

		&__content {
			display: flex;
			flex-direction: column;
			justify-content: center;
		}

		&__number {
			font-weight: 700;
			line-height: 1.2;
			margin-bottom: vars.$spacing-xs;

			.stat-card--primary & {
				color: vars.$primary-color;
			}

			.stat-card--secondary & {
				color: vars.$secondary-color;
			}

			.stat-card--accent & {
				color: vars.$info-color;
			}
		}

		&__label {
			font-weight: 500;
			color: vars.$gray-dark;
			margin: 0;
		}
	}
</style>
