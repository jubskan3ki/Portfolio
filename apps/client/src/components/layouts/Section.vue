<template>
	<section
		:id="id"
		:class="[
			'section',
			size && `section--${size}`,
			{
				'section--with-container': withContainer,
				'section--dark': dark,
				'section--light': light,
				'section--primary': primary,
				'section--animated': animated,
			},
			customClass,
		]"
		:data-animation="animationType"
	>
		<div :class="{ container: withContainer }">
			<!-- Header slot with title/subtitle fallback -->
			<div v-if="hasHeader" class="section__header" :class="{ 'animate-fade-in-down': animated }">
				<slot name="header">
					<h2 v-if="title" class="section__title" :class="{ 'font-bold': true }">{{ title }}</h2>
					<p v-if="subtitle" class="section__subtitle">{{ subtitle }}</p>
				</slot>
			</div>

			<!-- Main content -->
			<div class="section__content" :class="{ 'animate-fade-in-up': animated }">
				<slot></slot>
			</div>

			<!-- Footer slot -->
			<div v-if="$slots.footer" class="section__footer" :class="{ 'animate-fade-in-up delay-2': animated }">
				<slot name="footer"></slot>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
	import { computed, useSlots } from 'vue';

	type AnimationType = 'fade' | 'slide' | 'scale' | 'none';

	const props = defineProps({
		id: {
			type: String,
			default: '',
		},
		title: {
			type: String,
			default: '',
		},
		subtitle: {
			type: String,
			default: '',
		},
		size: {
			type: String,
			default: '',
			validator: (value: string) => ['', 'tight', 'large'].includes(value),
		},
		withContainer: {
			type: Boolean,
			default: true,
		},
		dark: {
			type: Boolean,
			default: false,
		},
		light: {
			type: Boolean,
			default: false,
		},
		primary: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
		animated: {
			type: Boolean,
			default: false,
		},
		animationType: {
			type: String as () => AnimationType,
			default: 'fade',
			validator: (value: string) => ['fade', 'slide', 'scale', 'none'].includes(value),
		},
	});

	const slots = useSlots();

	// Check if header exists
	const hasHeader = computed(() => slots.header || props.title || props.subtitle);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.section {
		padding: vars.$spacing-lg 0 vars.$spacing-xl 0;
		position: relative;
		overflow: hidden;

		@include mix.responsive(mobile) {
			padding: vars.$spacing-md 0 vars.$spacing-lg 0;
		}

		&__header {
			text-align: center;
			max-width: 800px;
			margin: 0 auto vars.$spacing-xl;
			position: relative;
			z-index: 5;

			@include mix.responsive(mobile) {
				margin-bottom: vars.$spacing-lg;
			}
		}

		&__title {
			margin-bottom: vars.$spacing-md;
			position: relative;
			display: inline-block;

			&::after {
				content: '';
				display: block;
				width: 50px;
				height: 3px;
				background-color: vars.$primary-color;
				margin: vars.$spacing-sm auto 0;
			}
		}

		&__subtitle {
			color: vars.$gray-dark;
			line-height: 1.6;
		}

		&__content {
			width: 100%;
			position: relative;
			z-index: 5;
		}

		&__footer {
			margin-top: vars.$spacing-xl;
			text-align: center;
			position: relative;
			z-index: 5;

			@include mix.responsive(mobile) {
				margin-top: vars.$spacing-lg;
			}
		}

		// Size variants
		&--tight {
			padding: vars.$spacing-md 0 vars.$spacing-lg 0;

			@include mix.responsive(mobile) {
				padding: vars.$spacing-sm 0 vars.$spacing-md 0;
			}

			.section__header {
				margin-bottom: vars.$spacing-lg;

				@include mix.responsive(mobile) {
					margin-bottom: vars.$spacing-md;
				}
			}
		}

		&--large {
			padding: vars.$spacing-xl 0 calc(vars.$spacing-xl * 1.5) 0;

			@include mix.responsive(mobile) {
				padding: vars.$spacing-lg 0 vars.$spacing-xl 0;
			}
		}

		// Color variants
		&--dark {
			background-color: vars.$black-light;
			color: vars.$white;

			.section__title {
				color: vars.$white;

				&::after {
					background-color: vars.$secondary-color;
				}
			}

			.section__subtitle {
				color: vars.$gray-light;
			}
		}

		&--light {
			background-color: vars.$white-dark;
		}

		&--primary {
			background-color: func.color-alpha(vars.$primary-color, 0.1);

			.section__title::after {
				background-color: vars.$primary-color;
			}
		}

		// Animation support
		&--animated {
			[data-animation='fade'] & {
				.animate-fade-in-up,
				.animate-fade-in-down {
					animation-duration: vars.$transition-base;
				}
			}

			[data-animation='slide'] & {
				.section__content {
					animation: slideInRight vars.$transition-base forwards;
				}
			}

			[data-animation='scale'] & {
				.section__content {
					animation: scaleIn vars.$transition-base forwards;
				}
			}
		}
	}

	@keyframes morph {
		0% {
			border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
		}
		50% {
			border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
		}
		100% {
			border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
		}
	}

	// Additional animations
	@keyframes slideInRight {
		from {
			opacity: 0;
			transform: translateX(-30px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes scaleIn {
		from {
			opacity: 0;
			transform: scale(0.95);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}
</style>
