<template>
	<div :class="['progress', { 'progress--striped': striped }, { 'progress--animated': animated }, customClass]">
		<div v-if="label || $slots.label" class="progress__label">
			<slot name="label">{{ label }}</slot>
			<span v-if="showPercentage" class="progress__percentage">{{ percentage }}%</span>
		</div>

		<div class="progress__container">
			<div class="progress__bar" :class="`progress__bar--${type}`" :style="{ width: `${percentage}%` }">
				<span v-if="showTextInside" class="progress__text">{{ percentage }}%</span>
			</div>

			<div v-if="steps > 0" class="progress__steps">
				<div
					v-for="step in steps"
					:key="step"
					class="progress__step"
					:class="{ 'progress__step--active': (step / steps) * 100 <= percentage }"
				></div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { computed } from 'vue';

	const props = defineProps({
		value: {
			type: Number,
			default: 0,
		},
		max: {
			type: Number,
			default: 100,
		},
		label: {
			type: String,
			default: '',
		},
		showPercentage: {
			type: Boolean,
			default: true,
		},
		showTextInside: {
			type: Boolean,
			default: false,
		},
		striped: {
			type: Boolean,
			default: false,
		},
		animated: {
			type: Boolean,
			default: false,
		},
		type: {
			type: String,
			default: 'primary',
			validator: (value: string) =>
				['primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value),
		},
		steps: {
			type: Number,
			default: 0,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Calcul du pourcentage
	const percentage = computed(() => {
		const value = Math.max(0, Math.min(props.value, props.max));
		return Math.round((value / props.max) * 100);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	@keyframes progress-bar-stripes {
		from {
			background-position: 1rem 0;
		}
		to {
			background-position: 0 0;
		}
	}

	.progress {
		margin-bottom: vars.$spacing-md;

		&__label {
			display: flex;
			justify-content: space-between;
			margin-bottom: vars.$spacing-xs;
			color: vars.$gray-dark;
		}

		&__container {
			position: relative;
			height: 8px;
			background-color: vars.$white-dark;
			border-radius: vars.$border-radius-full;
			overflow: hidden;
		}

		&__bar {
			height: 100%;
			border-radius: vars.$border-radius-full;
			transition: width 0.3s ease;
			position: relative;
			display: flex;
			align-items: center;
			justify-content: center;

			&--primary {
				background-color: vars.$primary-color;
			}

			&--secondary {
				background-color: vars.$secondary-color;
			}

			&--success {
				background-color: vars.$success-color;
			}

			&--danger {
				background-color: vars.$danger-color;
			}

			&--warning {
				background-color: vars.$warning-color;
			}

			&--info {
				background-color: vars.$info-color;
			}
		}

		&__text {
			color: vars.$white;
			font-weight: 600;
			white-space: nowrap;
		}

		&--striped &__bar {
			background-image: linear-gradient(
				45deg,
				rgba(255, 255, 255, 0.15) 25%,
				transparent 25%,
				transparent 50%,
				rgba(255, 255, 255, 0.15) 50%,
				rgba(255, 255, 255, 0.15) 75%,
				transparent 75%,
				transparent
			);
			background-size: 1rem 1rem;
		}

		&--animated &__bar {
			animation: progress-bar-stripes 1s linear infinite;
		}

		&__steps {
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			display: flex;
			justify-content: space-between;
			padding: 0 calc(100% / v-bind(steps) / 2);
			pointer-events: none;
		}

		&__step {
			width: 1px;
			height: 100%;
			background-color: rgba(255, 255, 255, 0.5);
			transition: background-color 0.3s ease;

			&--active {
				background-color: rgba(255, 255, 255, 0.8);
			}
		}
	}
</style>
