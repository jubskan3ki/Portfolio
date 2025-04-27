<template>
	<div :class="['spinner', `spinner--${size}`, `spinner--${type}`, customClass]" role="status" aria-live="polite">
		<div class="spinner__content">
			<div v-if="type === 'circle'" class="spinner__circle"></div>
			<div v-else-if="type === 'dots'" class="spinner__dots">
				<div class="spinner__dot"></div>
				<div class="spinner__dot"></div>
				<div class="spinner__dot"></div>
			</div>
			<div v-else-if="type === 'pulse'" class="spinner__pulse"></div>
			<span v-if="label" class="spinner__text">{{ label }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
	defineProps({
		size: {
			type: String,
			default: 'medium',
			validator: (value: string) => ['small', 'medium', 'large'].includes(value),
		},
		type: {
			type: String,
			default: 'circle',
			validator: (value: string) => ['circle', 'dots', 'pulse'].includes(value),
		},
		label: {
			type: String,
			default: 'Chargement...',
		},
		customClass: {
			type: String,
			default: '',
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.spinner {
		display: inline-flex;
		justify-content: center;
		align-items: center;

		&__content {
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
		}

		&__text {
			margin-top: vars.$spacing-sm;
			color: vars.$gray-dark;
		}

		// Type: Circle
		&__circle {
			border-radius: 50%;
			border: 2px solid rgba(vars.$primary-color, 0.2);
			border-top-color: vars.$primary-color;
			animation: spinner-rotate 0.8s linear infinite;
		}

		// Type: Dots
		&__dots {
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 4px;
		}

		&__dot {
			width: 8px;
			height: 8px;
			border-radius: 50%;
			background-color: vars.$primary-color;
			animation: spinner-scale 1.5s infinite ease-in-out;

			&:nth-child(1) {
				animation-delay: 0s;
			}

			&:nth-child(2) {
				animation-delay: 0.2s;
			}

			&:nth-child(3) {
				animation-delay: 0.4s;
			}
		}

		// Type: Pulse
		&__pulse {
			width: 20px;
			height: 20px;
			border-radius: 50%;
			background-color: vars.$primary-color;
			animation: spinner-pulse 1.2s infinite cubic-bezier(0.4, 0, 0.2, 1);
		}

		// Tailles
		&--small {
			.spinner__circle {
				width: 16px;
				height: 16px;
				border-width: 2px;
			}

			.spinner__dot {
				width: 6px;
				height: 6px;
			}

			.spinner__pulse {
				width: 16px;
				height: 16px;
			}
		}

		&--medium {
			.spinner__circle {
				width: 24px;
				height: 24px;
				border-width: 2px;
			}

			.spinner__dot {
				width: 8px;
				height: 8px;
			}

			.spinner__pulse {
				width: 24px;
				height: 24px;
			}
		}

		&--large {
			.spinner__circle {
				width: 40px;
				height: 40px;
				border-width: 3px;
			}

			.spinner__dot {
				width: 12px;
				height: 12px;
			}

			.spinner__pulse {
				width: 40px;
				height: 40px;
			}
		}
	}

	// Animations
	@keyframes spinner-rotate {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	@keyframes spinner-scale {
		0%,
		100% {
			transform: scale(0.6);
			opacity: 0.6;
		}
		50% {
			transform: scale(1);
			opacity: 1;
		}
	}

	@keyframes spinner-pulse {
		0% {
			transform: scale(0.8);
			opacity: 1;
		}
		50% {
			transform: scale(1.2);
			opacity: 0.5;
		}
		100% {
			transform: scale(0.8);
			opacity: 1;
		}
	}
</style>
