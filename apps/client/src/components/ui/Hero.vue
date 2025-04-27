<template>
	<Section :class="['hero', `hero--${variant}`, { 'hero--has-logo': !!logo }]" :variant="variant">
		<div class="container">
			<div class="hero__content">
				<!-- Logo section (for stack pages) -->
				<div v-if="logo" class="hero__logo-container animate-fade-in">
					<img :src="logo" :alt="logoAlt || title" class="hero__logo" />
				</div>

				<div class="hero__text">
					<!-- Title -->
					<h1 class="hero__title" :class="{ 'has-underline': showTitleUnderline }">
						<slot name="title">{{ title }}</slot>
					</h1>

					<!-- Description -->
					<p v-if="description || $slots.description" class="hero__description">
						<slot name="description">{{ description }}</slot>
					</p>

					<!-- Meta information (dates, categories, etc) -->
					<div v-if="hasMeta || $slots.meta" class="hero__meta">
						<slot name="meta"></slot>
					</div>

					<!-- Links section (for stack pages) -->
					<div v-if="$slots.links" class="hero__links">
						<slot name="links"></slot>
					</div>

					<!-- Additional content -->
					<slot></slot>
				</div>
			</div>
		</div>
	</Section>
</template>

<script setup lang="ts">
	import Section from '@/components/layouts/Section.vue';

	defineProps({
		// Main content
		title: {
			type: String,
			required: true,
		},
		description: {
			type: String,
			default: '',
		},

		// Styling
		variant: {
			type: String,
			default: 'primary',
			validator: (value: string) => ['primary', 'secondary', 'info', 'success'].includes(value),
		},
		showTitleUnderline: {
			type: Boolean,
			default: false,
		},

		// Logo (for stack pages)
		logo: {
			type: String,
			default: '',
		},
		logoAlt: {
			type: String,
			default: '',
		},

		// Meta info flag
		hasMeta: {
			type: Boolean,
			default: false,
		},
	});
</script>

<style lang="scss">
	@use '@/styles/abstracts/functions' as func;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/variables' as vars;

	.hero {
		padding: vars.$spacing-lg 0;
		position: relative;
		overflow: hidden;

		// Background gradient
		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: linear-gradient(
				135deg,
				func.color-alpha(vars.$primary-color, 0.95),
				func.color-alpha(vars.$secondary-color, 0.85)
			);
			z-index: -1;
		}

		// Variants
		&--secondary {
			&::before {
				background: linear-gradient(
					135deg,
					func.color-alpha(vars.$secondary-color, 0.95),
					func.color-alpha(vars.$primary-color, 0.85)
				);
			}
		}

		&--info {
			&::before {
				background: linear-gradient(
					135deg,
					func.color-alpha(vars.$info-color, 0.95),
					func.color-alpha(vars.$primary-color, 0.85)
				);
			}
		}

		&--success {
			&::before {
				background: linear-gradient(
					135deg,
					func.color-alpha(vars.$success-color, 0.95),
					func.color-alpha(vars.$secondary-color, 0.85)
				);
			}
		}

		// Content container
		&__content {
			// When has logo, display flex layout
			.hero--has-logo & {
				display: flex;
				align-items: center;
				gap: vars.$spacing-lg;

				@include mix.responsive(mobile) {
					flex-direction: column;
					text-align: center;
					gap: vars.$spacing-md;
				}
			}
		}

		// Logo styling (for stack pages)
		&__logo-container {
			background-color: func.color-alpha(vars.$white, 0.9);
			border-radius: vars.$border-radius-full;
			padding: vars.$spacing-md;
			width: 120px;
			height: 120px;
			display: flex;
			align-items: center;
			justify-content: center;
			box-shadow: vars.$box-shadow-medium;
			flex-shrink: 0;

			@include mix.responsive(mobile) {
				width: 100px;
				height: 100px;
			}
		}

		&__logo {
			max-width: 80%;
			max-height: 80%;
			object-fit: contain;
		}

		// Text content container
		&__text {
			flex-grow: 1;
		}

		// Title styling
		&__title {
			color: vars.$white;
			margin-bottom: vars.$spacing-md;
			font-weight: 800;
			text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

			// Text alignment for different pages
			.hero--has-logo & {
				text-align: left;
				margin-bottom: vars.$spacing-sm;

				@include mix.responsive(mobile) {
					text-align: center;
				}
			}

			&.has-underline {
				position: relative;
				text-align: center;

				&::after {
					content: '';
					display: block;
					width: 80px;
					height: 4px;
					background-color: vars.$white;
					margin: vars.$spacing-sm auto 0;
					border-radius: vars.$border-radius-full;
				}

				.hero--has-logo & {
					text-align: left;

					&::after {
						margin: vars.$spacing-sm 0 0;
					}

					@include mix.responsive(mobile) {
						text-align: center;

						&::after {
							margin: vars.$spacing-sm auto 0;
						}
					}
				}
			}
		}

		// Description styling
		&__description {
			color: func.color-alpha(vars.$white, 0.95);
			max-width: 800px;
			line-height: 1.6;

			.hero--has-logo & {
				margin: 0;
				text-align: left;

				@include mix.responsive(mobile) {
					text-align: center;
					margin: 0 auto;
				}
			}

			&:not(.hero--has-logo &) {
				margin: 0 auto;
				text-align: center;
			}
		}

		// Meta information styling
		&__meta {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-md;
			color: func.color-alpha(vars.$white, 0.9);
			margin-top: vars.$spacing-sm;

			.hero--has-logo & {
				margin-bottom: vars.$spacing-md;

				@include mix.responsive(mobile) {
					justify-content: center;
				}
			}

			// Common meta item style (applied to slotted content)
			:deep(.hero__meta-item) {
				display: flex;
				align-items: center;
				gap: vars.$spacing-xs;
			}
		}

		// Links section styling
		&__links {
			display: flex;
			gap: vars.$spacing-md;
			margin-top: vars.$spacing-md;

			@include mix.responsive(mobile) {
				justify-content: center;
			}

			// Link item styling (applied to slotted content)
			:deep(.hero__link) {
				display: flex;
				align-items: center;
				gap: vars.$spacing-xs;
				padding: vars.$spacing-xs vars.$spacing-sm;
				background-color: func.color-alpha(vars.$white, 0.2);
				border-radius: vars.$border-radius-md;
				color: vars.$white;
				transition: all vars.$transition-base;

				&:hover {
					background-color: func.color-alpha(vars.$white, 0.3);
					transform: translateY(-2px);
				}
			}
		}
	}
</style>
