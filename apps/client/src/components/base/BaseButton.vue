<template>
	<!-- Rendu conditionnel : utiliser NuxtLink ou <a> si props 'to' est présent -->
	<NuxtLink
		v-if="to && isInternalLink"
		:to="resolvedPath"
		:class="[
			'button',
			variant && `button--${variant}`,
			size && `button--${size}`,
			{ 'button--disabled': disabled },
			{ 'button--loading': loading },
			{ 'button--full-width': fullWidth },
			customClass,
		]"
		:aria-label="ariaLabel"
		@click="!disabled && !loading ? $emit('click', $event) : null"
	>
		<span v-if="loading" class="button__loader">
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
		</span>
		<span v-else class="button__content">
			<slot name="icon-left"></slot>
			<slot>{{ text }}</slot>
			<slot name="icon-right"></slot>
		</span>
	</NuxtLink>

	<!-- Lien externe si nécessaire -->
	<a
		v-else-if="to && !isInternalLink"
		:href="resolvedPath"
		:target="target"
		:rel="target === '_blank' ? 'noopener noreferrer' : undefined"
		:class="[
			'button',
			variant && `button--${variant}`,
			size && `button--${size}`,
			{ 'button--disabled': disabled },
			{ 'button--loading': loading },
			{ 'button--full-width': fullWidth },
			customClass,
		]"
		:aria-label="ariaLabel"
		@click="!disabled && !loading ? $emit('click', $event) : null"
	>
		<span v-if="loading" class="button__loader">
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
		</span>
		<span v-else class="button__content">
			<slot name="icon-left"></slot>
			<slot>{{ text }}</slot>
			<slot name="icon-right"></slot>
		</span>
	</a>

	<!-- Button original -->
	<button
		v-else
		:type="type"
		:class="[
			'button',
			variant && `button--${variant}`,
			size && `button--${size}`,
			{ 'button--disabled': disabled },
			{ 'button--loading': loading },
			{ 'button--full-width': fullWidth },
			customClass,
		]"
		:disabled="disabled || loading"
		:aria-label="ariaLabel"
		@click="$emit('click', $event)"
	>
		<span v-if="loading" class="button__loader">
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
			<span class="button__loader-dot"></span>
		</span>
		<span v-else class="button__content">
			<slot name="icon-left"></slot>
			<slot>{{ text }}</slot>
			<slot name="icon-right"></slot>
		</span>
	</button>
</template>

<script setup lang="ts">
	import { createPath } from '@/config/routes';
	import { computed, PropType } from 'vue';

	// Type pour les objets route
	type RouteObject = { path: string; name?: string };

	const props = defineProps({
		text: {
			type: String,
			default: '',
		},
		type: {
			type: String as () => 'button' | 'submit' | 'reset',
			default: 'button',
			validator: (value: string) => ['button', 'submit', 'reset'].includes(value),
		},
		variant: {
			type: String,
			default: '',
			validator: (value: string) => ['', 'primary', 'secondary', 'outline'].includes(value),
		},
		size: {
			type: String,
			default: '',
			validator: (value: string) => ['', 'small', 'large'].includes(value),
		},
		disabled: {
			type: Boolean,
			default: false,
		},
		loading: {
			type: Boolean,
			default: false,
		},
		fullWidth: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
		to: {
			type: [String, Object] as PropType<string | RouteObject>,
			default: '',
		},
		params: {
			type: Object as PropType<Record<string, string | number>>,
			default: () => ({}),
		},
		target: {
			type: String,
			default: '',
			validator: (value: string) => ['', '_blank', '_self', '_parent', '_top'].includes(value),
		},
		ariaLabel: {
			type: String,
			default: '',
		},
	});

	defineEmits(['click']);

	// Résoudre l'URL à partir d'un objet route
	const resolvedPath = computed(() => {
		if (typeof props.to === 'object' && props.to && 'path' in props.to) {
			return createPath(props.to, props.params);
		}
		return props.to as string;
	});

	// Détermine si le lien est interne ou externe
	const isInternalLink = computed(() => {
		if (!props.to) return false;

		if (typeof props.to === 'string') {
			return !(
				props.to.startsWith('http://') ||
				props.to.startsWith('https://') ||
				props.to.startsWith('//') ||
				props.to.startsWith('tel:') ||
				props.to.startsWith('mailto:')
			);
		}

		return true; // Les objets route sont toujours des liens internes
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.button {
		@include mix.button-style(
			vars.$primary-color,
			vars.$white,
			func.adjust-color-brightness(vars.$primary-color, -10%)
		);
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border: none;
		font-weight: 500;
		position: relative;
		transition: all vars.$transition-base;
		text-decoration: none;
		cursor: pointer;

		&__content {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
		}

		&--secondary {
			@include mix.button-style(
				vars.$secondary-color,
				vars.$white,
				func.adjust-color-brightness(vars.$secondary-color, -10%)
			);
		}

		&--outline {
			background-color: transparent;
			border: 2px solid vars.$primary-color;
			color: vars.$primary-color;

			&:hover {
				background-color: vars.$primary-color;
				color: vars.$white;
			}
		}

		&--small {
			padding: vars.$spacing-xs vars.$spacing-sm;
		}

		&--large {
			padding: vars.$spacing-md vars.$spacing-lg;
		}

		&--full-width {
			width: 100%;
		}

		&--disabled {
			opacity: 0.6;
			cursor: not-allowed;
			pointer-events: none;
		}

		&__loader {
			display: flex;
			align-items: center;
			justify-content: center;
			gap: vars.$spacing-xs;

			&-dot {
				width: 6px;
				height: 6px;
				background-color: currentColor;
				border-radius: 50%;
				display: inline-block;
				animation: button-loading 1.2s infinite ease-in-out;

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
		}
	}

	@keyframes button-loading {
		0%,
		80%,
		100% {
			transform: scale(0);
			opacity: 0.6;
		}
		40% {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
