<template>
	<NuxtLink
		v-if="isInternalLink"
		:to="resolvedTo"
		:class="[
			'link',
			variant && `link--${variant}`,
			{ 'link--block': block },
			{ 'link--underline': underline },
			customClass,
		]"
		:target="target"
		:aria-label="ariaLabel"
	>
		<slot name="icon-left"></slot>
		<slot>{{ text }}</slot>
		<slot name="icon-right"></slot>
	</NuxtLink>

	<a
		v-else
		:href="resolvedTo"
		:class="[
			'link',
			variant && `link--${variant}`,
			{ 'link--block': block },
			{ 'link--underline': underline },
			customClass,
		]"
		:target="target"
		:rel="target === '_blank' ? 'noopener noreferrer' : undefined"
		:aria-label="ariaLabel"
	>
		<slot name="icon-left"></slot>
		<slot>{{ text }}</slot>
		<slot name="icon-right"></slot>
	</a>
</template>

<script setup lang="ts">
	import { createPath } from '@/config/routes';
	import { computed, PropType } from 'vue';

	// Type pour les objets route
	type RouteObject = { path: string; name?: string };

	const props = defineProps({
		to: {
			type: [String, Object] as PropType<string | RouteObject>,
			required: true,
		},
		params: {
			type: Object as PropType<Record<string, string | number>>,
			default: () => ({}),
		},
		text: {
			type: String,
			default: '',
		},
		variant: {
			type: String,
			default: '',
			validator: (value: string) => ['', 'primary', 'secondary', 'subtle', 'white'].includes(value),
		},
		target: {
			type: String,
			default: '',
			validator: (value: string) => ['', '_blank', '_self', '_parent', '_top'].includes(value),
		},
		block: {
			type: Boolean,
			default: false,
		},
		underline: {
			type: Boolean,
			default: false,
		},
		ariaLabel: {
			type: String,
			default: '',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Résoudre l'URL
	const resolvedTo = computed(() => {
		if (typeof props.to === 'object' && props.to && 'path' in props.to) {
			return createPath(props.to, props.params);
		}
		return props.to as string;
	});

	// Détermine si le lien est interne ou externe
	const isInternalLink = computed(() => {
		const url = resolvedTo.value;
		return !(
			url.startsWith('http://') ||
			url.startsWith('https://') ||
			url.startsWith('//') ||
			url.startsWith('tel:') ||
			url.startsWith('mailto:')
		);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.link {
		display: inline-flex;
		align-items: center;
		gap: vars.$spacing-xs;
		color: vars.$primary-color;
		@include mix.transition(color);
		text-decoration: none;

		&:hover {
			color: func.adjust-color-brightness(vars.$primary-color, -15%);

			&.link--underline,
			&:not(.link--underline) {
				text-decoration: underline;
			}
		}

		&:focus-visible {
			@include mix.focus-outline;
		}

		&--primary {
			color: vars.$primary-color;

			&:hover {
				color: func.adjust-color-brightness(vars.$primary-color, -15%);
			}
		}

		&--secondary {
			color: vars.$secondary-color;

			&:hover {
				color: func.adjust-color-brightness(vars.$secondary-color, -15%);
			}
		}

		&--white {
			color: vars.$white;

			&:hover {
				color: func.adjust-color-brightness(vars.$white, -15%);
			}
		}

		&--subtle {
			color: vars.$gray-dark;

			&:hover {
				color: vars.$black-light;
			}
		}

		&--block {
			display: flex;
		}

		&--underline {
			text-decoration: underline;
		}
	}
</style>
