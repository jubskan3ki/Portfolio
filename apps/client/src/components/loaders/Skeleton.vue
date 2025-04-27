<template>
	<div
		class="skeleton"
		:class="[`skeleton--${type}`, { 'skeleton--animate': animate }, customClass]"
		:style="computedStyle"
		aria-hidden="true"
	></div>
</template>

<script setup lang="ts">
	import { computed } from 'vue';

	const props = defineProps({
		type: {
			type: String,
			default: 'block',
			validator: (value: string) => ['block', 'circle', 'text', 'image', 'button', 'avatar'].includes(value),
		},
		width: {
			type: [String, Number],
			default: null,
		},
		height: {
			type: [String, Number],
			default: null,
		},
		radius: {
			type: [String, Number],
			default: null,
		},
		animate: {
			type: Boolean,
			default: true,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Helper pour convertir les nombres en pixels
	const formatSize = (size: string | number | null) => {
		if (size === null) return null;
		if (typeof size === 'number') return `${size}px`;
		return size;
	};

	// Calcul des dimensions et du rayon selon le type
	const computedWidth = computed(() => {
		if (props.width) return formatSize(props.width);

		switch (props.type) {
			case 'circle':
			case 'avatar':
				return '48px';
			case 'text':
				return '100%';
			case 'button':
				return '120px';
			case 'image':
				return '300px';
			default:
				return '100%';
		}
	});

	const computedHeight = computed(() => {
		if (props.height) return formatSize(props.height);

		switch (props.type) {
			case 'circle':
			case 'avatar':
				return '48px';
			case 'text':
				return '16px';
			case 'button':
				return '40px';
			case 'image':
				return '200px';
			default:
				return '20px';
		}
	});

	const computedRadius = computed(() => {
		if (props.radius) return formatSize(props.radius);

		switch (props.type) {
			case 'circle':
			case 'avatar':
				return '50%';
			case 'button':
				return '4px';
			case 'text':
				return '2px';
			default:
				return '4px';
		}
	});

	const computedStyle = computed(() => ({
		width: computedWidth.value ?? undefined,
		height: computedHeight.value ?? undefined,
		borderRadius: computedRadius.value ?? undefined,
	}));
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	@keyframes skeleton-pulse {
		0% {
			opacity: 0.6;
		}
		50% {
			opacity: 0.8;
		}
		100% {
			opacity: 0.6;
		}
	}

	.skeleton {
		display: inline-block;
		background-color: func.color-alpha(vars.$gray-light, 0.8);
		position: relative;
		overflow: hidden;

		&::after {
			content: '';
			position: absolute;
			top: 0;
			left: -150%;
			width: 150%;
			height: 100%;
			background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
			transform: skewX(-20deg);
		}

		&--animate {
			animation: skeleton-pulse 1.5s ease-in-out infinite;

			&::after {
				animation: shimmer 2s infinite;
			}
		}

		&--text {
			margin-bottom: 8px;

			&:last-of-type {
				width: 80%;
			}
		}

		&--avatar {
			margin-right: 8px;
		}

		&--button {
			margin-top: 16px;
		}
	}

	@keyframes shimmer {
		0% {
			left: -150%;
		}
		100% {
			left: 150%;
		}
	}
</style>
