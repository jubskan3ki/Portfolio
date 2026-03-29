<template>
	<div class="error-page" ref="pageRef">
		<!-- Background dots -->
		<div class="error-page__dots"></div>

		<!-- Floating shapes with parallax -->
		<div class="error-page__shapes">
			<span
				v-for="shape in shapes"
				:key="shape.id"
				:ref="(el) => setShapeRef(el as HTMLElement, shape.id)"
				class="error-page__shape"
				:class="`error-page__shape--${shape.type}`"
				:style="{
					left: shape.x + '%',
					top: shape.y + '%',
					width: shape.size + 'px',
					height: shape.size + 'px',
					opacity: shape.opacity,
				}"
			/>
		</div>

		<!-- Orbs -->
		<div class="error-page__orb error-page__orb--1"></div>
		<div class="error-page__orb error-page__orb--2"></div>

		<!-- Content -->
		<main class="error-page__content">
			<div class="error-page__card">
				<!-- Error code with bug -->
				<div class="error-page__hero">
					<span class="error-page__code">{{ statusCode }}</span>
					<div class="error-page__bug">
						<BaseIcon :name="currentIcon" size="xl" />
					</div>
				</div>

				<!-- Title -->
				<h2 class="error-page__title">{{ errorTitle }}</h2>

				<!-- Message -->
				<p class="error-page__message">{{ errorMessage }}</p>

				<!-- Actions -->
				<div class="error-page__actions">
					<BaseButton :to="ROUTES.HOME.path" variant="primary" size="lg">
						<BaseIcon name="home" size="sm" />
						Accueil
					</BaseButton>
					<BaseButton variant="outline" size="lg" @click="goBack">
						<BaseIcon name="arrow-left" size="sm" />
						Retour
					</BaseButton>
				</div>

				<!-- Links -->
				<nav class="error-page__nav">
					<BaseLink :to="ROUTES.PROJECTS.path">Projets</BaseLink>
					<BaseLink :to="ROUTES.BLOG.path">Blog</BaseLink>
					<BaseLink :to="ROUTES.STACKS.path">Stacks</BaseLink>
					<BaseLink :to="ROUTES.CONTACT.path">Contact</BaseLink>
				</nav>
			</div>
		</main>

	</div>
</template>

<script setup lang="ts">
	import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import { ROUTES } from '@/config/routes';

	// Props
	const props = withDefaults(
		defineProps<{
			error?: { statusCode?: number; statusMessage?: string };
		}>(),
		{
			error: () => ({ statusCode: 404, statusMessage: '' }),
		}
	);

	// Empêcher l'indexation des pages d'erreur
	useSeoMeta({
		robots: 'noindex, nofollow',
	});

	const pageRef = ref<HTMLElement | null>(null);
	const shapeRefs = ref<Map<number, HTMLElement>>(new Map());

	// Status code — SSR-safe (no client-only query param logic to avoid hydration mismatch)
	const statusCode = computed(() => props.error?.statusCode || 404);

	// Error config
	const errors: Record<number, { title: string; message: string }> = {
		400: { title: 'Requête invalide', message: 'La syntaxe de la requête est incorrecte.' },
		401: { title: 'Non autorisé', message: 'Authentification requise.' },
		403: { title: 'Accès interdit', message: 'Vous n\'avez pas la permission d\'accéder à cette page.' },
		404: { title: 'Page introuvable', message: 'Cette page n\'existe pas ou a été déplacée.' },
		500: { title: 'Erreur serveur', message: 'Une erreur interne est survenue.' },
		503: { title: 'Service indisponible', message: 'Le service est temporairement indisponible.' },
	};

	const errorTitle = computed(() => errors[statusCode.value]?.title || 'Erreur');
	const errorMessage = computed(() => errors[statusCode.value]?.message || 'Une erreur est survenue.');

	// Icons for each error type (Lucide icons)
	const errorIcons: Record<number, string> = {
		400: 'bug',
		401: 'shield-alert',
		403: 'shield-off',
		404: 'search-x',
		500: 'server-off',
		503: 'wifi-off',
	};

	const currentIcon = computed(() => errorIcons[statusCode.value] ?? 'bug');

	// Shapes
	const shapes = [
		{ id: 1, type: 'circle', size: 60, x: 5, y: 10, depth: 20, opacity: 0.4 },
		{ id: 2, type: 'square', size: 40, x: 85, y: 15, depth: 35, opacity: 0.3 },
		{ id: 3, type: 'circle', size: 80, x: 80, y: 70, depth: 25, opacity: 0.25 },
		{ id: 4, type: 'square', size: 50, x: 10, y: 75, depth: 30, opacity: 0.3 },
		{ id: 5, type: 'circle', size: 30, x: 20, y: 40, depth: 45, opacity: 0.35 },
		{ id: 6, type: 'square', size: 35, x: 70, y: 45, depth: 40, opacity: 0.25 },
	];

	const setShapeRef = (el: HTMLElement | null, id: number) => {
		if (el) shapeRefs.value.set(id, el);
	};

	// Parallax
	let targetX = 0;
	let targetY = 0;
	let currentX = 0;
	let currentY = 0;
	let animationId: number;
	const prefersReducedMotion = ref(false);

	const onMouseMove = (e: MouseEvent) => {
		if (!pageRef.value || prefersReducedMotion.value) return;
		const { width, height } = pageRef.value.getBoundingClientRect();
		targetX = (e.clientX / width - 0.5) * 2;
		targetY = (e.clientY / height - 0.5) * 2;
	};

	const animate = () => {
		if (prefersReducedMotion.value) return;

		currentX += (targetX - currentX) * 0.05;
		currentY += (targetY - currentY) * 0.05;

		shapeRefs.value.forEach((el, id) => {
			const shape = shapes.find((s) => s.id === id);
			if (shape) {
				const x = currentX * shape.depth;
				const y = currentY * shape.depth;
				el.style.transform = `translate(${x}px, ${y}px)`;
			}
		});

		animationId = requestAnimationFrame(animate);
	};

	const startParallax = () => {
		if (!prefersReducedMotion.value) {
			window.addEventListener('mousemove', onMouseMove);
			animationId = requestAnimationFrame(animate);
		}
	};

	const stopParallax = () => {
		window.removeEventListener('mousemove', onMouseMove);
		if (animationId) {
			cancelAnimationFrame(animationId);
		}
	};

	const handleVisibilityChange = () => {
		if (document.hidden) {
			stopParallax();
		} else {
			startParallax();
		}
	};

	const goBack = () => {
		if (import.meta.client && window.history.length > 1) {
			window.history.back();
		} else {
			clearError({ redirect: ROUTES.HOME.path });
		}
	};

	onMounted(() => {
		prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		if ('requestIdleCallback' in window) {
			requestIdleCallback(() => startParallax());
		} else {
			setTimeout(() => startParallax(), 300);
		}
		document.addEventListener('visibilitychange', handleVisibilityChange);
	});

	onBeforeUnmount(() => {
		stopParallax();
		document.removeEventListener('visibilitychange', handleVisibilityChange);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as fn;

	.error-page {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: vars.$bg-secondary;
		position: relative;
		overflow: hidden;

		&__dots {
			position: absolute;
			inset: 0;

			@include mix.dots-pattern;

			pointer-events: none;
		}

		&__shapes {
			position: absolute;
			inset: 0;
			pointer-events: none;
		}

		&__shape {
			position: absolute;
			will-change: transform;
			transition: transform 0.1s linear;

			&--circle {
				border-radius: 50%;
				background: vars.$primary-light;
			}

			&--square {
				border-radius: vars.$border-radius-md;
				background: vars.$secondary-color;
			}
		}

		&__orb {
			position: absolute;
			border-radius: 50%;
			filter: blur(100px);
			pointer-events: none;

			&--1 {
				width: 400px;
				height: 400px;
				background: vars.$primary-color;
				opacity: 0.12;
				top: -100px;
				left: -100px;
			}

			&--2 {
				width: 300px;
				height: 300px;
				background: vars.$secondary-color;
				opacity: 0.1;
				bottom: -80px;
				right: -80px;
			}
		}

		&__content {
			position: relative;
			z-index: 10;
			width: 100%;
			max-width: 480px;
			padding: vars.$spacing-lg;

			@include mix.responsive(mobile) {
				padding: vars.$spacing-md;
			}
		}

		&__card {
			background: rgba(255, 255, 255, 0.95);
			backdrop-filter: blur(16px);
			border-radius: vars.$border-radius-xl;
			padding: vars.$spacing-xxl;
			text-align: center;
			box-shadow: 0 16px 48px fn.color-alpha(vars.$black, 0.08);

			@include mix.responsive(mobile) {
				padding: vars.$spacing-xl vars.$spacing-lg;
			}
		}

		&__hero {
			position: relative;
			display: inline-block;
			margin-bottom: vars.$spacing-lg;
		}

		&__code {
			font-size: 8rem;
			font-weight: vars.$font-weight-bold;
			color: vars.$primary-color;
			line-height: 1;
			display: block;

			@include mix.responsive(mobile) {
				font-size: 5rem;
			}
		}

		&__bug {
			position: absolute;
			width: 56px;
			height: 56px;
			top: -16px;
			right: -16px;
			display: flex;
			align-items: center;
			justify-content: center;
			background: vars.$white;
			border: 2px solid vars.$primary-color;
			border-radius: 50%;
			box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.2);
			animation: bug-float 3s ease-in-out infinite;
			color: vars.$primary-dark;

			svg {
				width: 32px;
				height: 32px;
			}

			@include mix.responsive(mobile) {
				width: 48px;
				height: 48px;
				top: -12px;
				right: -12px;

				svg {
					width: 26px;
					height: 26px;
				}
			}
		}

		&__title {
			font-size: vars.$font-size-xl;
			font-weight: vars.$font-weight-semibold;
			color: vars.$text-primary;
			margin-bottom: vars.$spacing-xxs;
		}

		&__message {
			font-size: vars.$font-size-md;
			color: vars.$text-secondary;
			margin-bottom: vars.$spacing-xl;

			@include mix.responsive(mobile) {
				font-size: vars.$font-size-sm;
			}
		}

		&__actions {
			display: flex;
			justify-content: center;
			gap: vars.$spacing-md;
			margin-bottom: vars.$spacing-xl;

			@include mix.responsive(mobile) {
				flex-direction: column;
			}
		}

		&__nav {
			display: flex;
			justify-content: center;
			gap: vars.$spacing-lg;
			padding-top: vars.$spacing-lg;
			border-top: 1px solid vars.$border-color;

			@include mix.responsive(mobile) {
				gap: vars.$spacing-md;
				flex-wrap: wrap;
			}
		}

	}

	@keyframes bug-float {
		0%, 100% {
			transform: translateY(0);
		}

		50% {
			transform: translateY(-6px);
		}
	}
</style>
