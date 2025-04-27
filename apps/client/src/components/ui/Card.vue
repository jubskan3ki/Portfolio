<template>
	<div
		:class="[
			'card',
			{ 'card--hoverable': hoverable },
			{ 'card--flat': flat },
			{ 'card--bordered': bordered },
			customClass,
		]"
	>
		<div v-if="$slots.image" class="card__image">
			<slot name="image"></slot>
		</div>

		<div v-if="$slots.header || title" class="card__header">
			<slot name="header">
				<h3 class="card__title">{{ title }}</h3>
				<p v-if="subtitle" class="card__subtitle">{{ subtitle }}</p>
			</slot>
		</div>

		<div class="card__body">
			<slot></slot>
		</div>

		<div v-if="$slots.footer" class="card__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	defineProps({
		title: {
			type: String,
			default: '',
		},
		subtitle: {
			type: String,
			default: '',
		},
		hoverable: {
			type: Boolean,
			default: false,
		},
		flat: {
			type: Boolean,
			default: false,
		},
		bordered: {
			type: Boolean,
			default: false,
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

	.card {
		background-color: vars.$white;
		border-radius: vars.$border-radius-md;
		overflow: hidden;
		position: relative;
		transition: all vars.$transition-base;

		// Par défaut, avec ombre
		&:not(.card--flat):not(.card--bordered) {
			box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
		}

		// Avec bordure
		&--bordered {
			border: 1px solid func.color-alpha(vars.$gray-light, 0.6);
		}

		// Header de la carte
		&__header {
			padding: vars.$spacing-md;
			border-bottom: 1px solid func.color-alpha(vars.$white-dark, 0.7);
		}

		// Image
		&__image {
			width: 100%;
			position: relative;
			overflow: hidden;

			&::after {
				content: '';
				position: absolute;
				top: 0;
				left: 0;
				right: 0;
				bottom: 0;
				background: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.02));
				pointer-events: none;
			}

			img {
				width: 100%;
				display: block;
				height: auto;
			}
		}

		// Titre et sous-titre
		&__title {
			margin: 0;
			margin-bottom: vars.$spacing-xs;
			color: vars.$black-light;
			font-weight: 600;
		}

		&__subtitle {
			margin: 0;
			color: vars.$gray-dark;
		}

		// Corps de la carte
		&__body {
			padding: vars.$spacing-md;
		}

		// Pied de la carte
		&__footer {
			padding: vars.$spacing-md;
			border-top: 1px solid func.color-alpha(vars.$white-dark, 0.7);
			background-color: func.color-alpha(vars.$white-dark, 0.5);
		}

		// Effet hover
		&--hoverable {
			transition:
				transform vars.$transition-base,
				box-shadow vars.$transition-base;

			&:hover {
				transform: translateY(-5px);
				box-shadow: vars.$box-shadow-medium;
			}
		}

		@include mix.responsive(mobile) {
			&--hoverable:hover {
				transform: translateY(-3px);
			}
		}
	}
</style>
