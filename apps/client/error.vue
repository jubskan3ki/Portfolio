<template>
	<div class="error-page">
		<div class="error-page__content">
			<h1 class="error-page__title">{{ error.statusCode || '404' }}</h1>
			<div class="error-page__graphic">
				<!-- Visage triste animé -->
				<div class="error-page__face">
					<div class="error-page__eyes">
						<div class="error-page__eye"></div>
						<div class="error-page__eye"></div>
					</div>
					<div class="error-page__mouth"></div>
				</div>
			</div>
			<p class="error-page__message">
				{{ error.statusMessage || "La page que vous recherchez n'existe pas" }}
			</p>
			<p class="error-page__submessage">Peut-être que l'URL a été mal tapée ou que la page a été déplacée.</p>

			<div class="error-page__actions">
				<BaseButton :to="ROUTES.HOME" variant="primary" class="error-page__button">
					<BaseIcon name="home" size="sm" class="mr-xs" />
					Retour à l'accueil
				</BaseButton>
			</div>

			<div class="error-page__suggestions">
				<p class="error-page__suggestion-title">Pages populaires:</p>
				<div class="error-page__links">
					<BaseLink :to="ROUTES.PROJECTS" variant="secondary" class="mr-md">Projets</BaseLink>
					<BaseLink :to="ROUTES.BLOG" variant="secondary" class="mr-md">Blog</BaseLink>
					<BaseLink :to="ROUTES.CONTACT" variant="secondary">Contact</BaseLink>
				</div>
			</div>
		</div>

		<!-- Éléments décoratifs en arrière-plan -->
		<div class="error-page__decoration error-page__decoration--1"></div>
		<div class="error-page__decoration error-page__decoration--2"></div>
		<div class="error-page__decoration error-page__decoration--3"></div>
		<div class="error-page__decoration error-page__decoration--4"></div>
	</div>
</template>

<script setup lang="ts">
	import { useRouter } from 'vue-router';
	import BaseButton from './src/components/base/BaseButton.vue';
	import BaseIcon from './src/components/base/BaseIcon.vue';
	import BaseLink from './src/components/base/BaseLink.vue';
	import { ROUTES } from './src/config/routes';

	defineProps({
		error: {
			type: Object,
			default: () => ({
				statusCode: 404,
				statusMessage: "La page que vous recherchez n'existe pas",
			}),
		},
	});

	useRouter();
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.error-page {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		background: linear-gradient(
			135deg,
			func.color-alpha(vars.$primary-color, 0.03),
			func.color-alpha(vars.$secondary-color, 0.05)
		);
		position: relative;
		overflow: hidden;

		&__content {
			text-align: center;
			padding: vars.$spacing-xl;
			max-width: 650px;
			background-color: vars.$white;
			border-radius: vars.$border-radius-lg;
			box-shadow: vars.$box-shadow-medium;
			position: relative;
			z-index: 5;

			@include mix.responsive(mobile) {
				padding: vars.$spacing-lg vars.$spacing-md;
				margin: 0 vars.$spacing-sm;
			}
		}

		&__title {
			font-size: 8rem;
			font-weight: 800;
			background: linear-gradient(135deg, vars.$primary-color, vars.$secondary-color);
			-webkit-background-clip: text;
			-webkit-text-fill-color: transparent;
			background-clip: text;
			margin-bottom: vars.$spacing-sm;
			text-shadow: 0 4px 15px func.color-alpha(vars.$primary-color, 0.2);

			@include mix.responsive(mobile) {
				font-size: 6rem;
			}
		}

		&__graphic {
			width: 150px;
			height: 150px;
			margin: 0 auto vars.$spacing-lg;
			border-radius: 50%;
			position: relative;
			background: linear-gradient(135deg, vars.$primary-color, vars.$secondary-color);
			box-shadow: 0 10px 30px func.color-alpha(vars.$primary-color, 0.3);
			animation: pulse 3s infinite ease-in-out;
		}

		&__face {
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
		}

		&__eyes {
			display: flex;
			gap: 30px;
			margin-bottom: 20px;
		}

		&__eye {
			width: 15px;
			height: 15px;
			border-radius: 50%;
			background-color: vars.$white;
			position: relative;

			// Animation des yeux
			animation: blink 4s infinite;
		}

		&__mouth {
			width: 60px;
			height: 20px;
			border-radius: 0 0 40px 40px;
			border: 5px solid vars.$white;
			border-top: none;
			transform: rotate(180deg);
		}

		&__message {
			font-size: 1.5rem;
			margin-bottom: vars.$spacing-sm;
			color: vars.$black-light;
			font-weight: 600;
		}

		&__submessage {
			font-size: 1rem;
			margin-bottom: vars.$spacing-lg;
			color: vars.$gray-dark;
		}

		&__actions {
			display: flex;
			justify-content: center;
			gap: vars.$spacing-md;
			margin-bottom: vars.$spacing-lg;

			@include mix.responsive(mobile) {
				flex-direction: column;
				align-items: center;
				gap: vars.$spacing-sm;
			}
		}

		&__button {
			display: inline-flex;
			align-items: center;
			gap: vars.$spacing-xs;
			min-width: 180px;

			@include mix.responsive(mobile) {
				width: 100%;
			}
		}

		&__suggestions {
			margin-top: vars.$spacing-lg;
			padding-top: vars.$spacing-md;
			border-top: 1px solid func.color-alpha(vars.$gray-light, 0.5);
		}

		&__suggestion-title {
			margin-bottom: vars.$spacing-sm;
			color: vars.$gray-dark;
			font-size: 0.9rem;
		}

		&__links {
			display: flex;
			justify-content: center;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
		}

		// Décorations d'arrière-plan
		&__decoration {
			position: absolute;
			border-radius: 50%;
			opacity: 0.5;
			z-index: 1;

			&--1 {
				top: 10%;
				left: 10%;
				width: 100px;
				height: 100px;
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				animation: float 8s infinite ease-in-out;
			}

			&--2 {
				bottom: 15%;
				right: 10%;
				width: 150px;
				height: 150px;
				background-color: func.color-alpha(vars.$secondary-color, 0.1);
				animation: float 12s infinite ease-in-out;
			}

			&--3 {
				top: 50%;
				right: 20%;
				width: 70px;
				height: 70px;
				background-color: func.color-alpha(vars.$info-color, 0.1);
				animation: float 9s infinite ease-in-out;
			}

			&--4 {
				bottom: 30%;
				left: 15%;
				width: 120px;
				height: 120px;
				background-color: func.color-alpha(vars.$success-color, 0.1);
				animation: float 10s infinite ease-in-out;
			}
		}
	}

	// Animations
	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1);
		}
	}

	@keyframes blink {
		0%,
		45%,
		55%,
		100% {
			transform: scaleY(1);
		}
		50% {
			transform: scaleY(0.1);
		}
	}

	@keyframes float {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-20px);
		}
	}
</style>
