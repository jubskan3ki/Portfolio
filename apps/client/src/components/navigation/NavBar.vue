<!-- src/components/navigation/NavBar.vue -->
<template>
	<nav
		:class="['navbar', { 'navbar--sticky': sticky, 'navbar--scrolled': isScrolled }, customClass]"
		:aria-label="ariaLabel"
	>
		<div class="container_large">
			<div class="navbar__container">
				<!-- Logo -->
				<div class="navbar__logo">
					<slot name="logo">
						<AppLogo />
					</slot>
				</div>

				<!-- Navigation -->
				<ul class="navbar__nav">
					<NavbarItem
						v-for="(item, index) in navigationItems"
						:key="index"
						:item="item"
						:index="index"
						:is-active="isActiveRoute(item.path, route.path)"
						@mouseenter="hoverIndex = item.children ? index : null"
						@mouseleave="hoverIndex = null"
					/>
				</ul>
			</div>
		</div>
	</nav>
</template>

<script setup lang="ts">
	import NavbarItem from '@/components/navigation/NavbarItem.vue';
	import AppLogo from '@/components/ui/AppLogo.vue';
	import { isActiveRoute, navigationItems } from '@/config/navBar';
	import { onBeforeUnmount, onMounted, ref } from 'vue';
	import { useRoute } from 'vue-router';

	// Props
	defineProps({
		sticky: {
			type: Boolean,
			default: false,
		},
		ariaLabel: {
			type: String,
			default: 'Navigation principale',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const route = useRoute();
	const hoverIndex = ref<number | null>(null);
	const isScrolled = ref(false);

	// Détecter le défilement
	const handleScroll = () => {
		isScrolled.value = window.scrollY > 20;
	};

	// Gestion des événements
	onMounted(() => {
		window.addEventListener('scroll', handleScroll);
		// Vérification initiale du défilement
		handleScroll();
	});

	onBeforeUnmount(() => {
		window.removeEventListener('scroll', handleScroll);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.navbar {
		padding: 0;
		transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		width: 100%;

		.container_large {
			width: 100%;
			max-width: 100%;
			padding: 0 vars.$spacing-xl;
			margin-left: auto;
			margin-right: auto;

			@include mix.responsive(mobile) {
				padding: 0 vars.$spacing-md;
			}
		}

		&.navbar--scrolled {
			background-color: func.color-alpha(vars.$white, 0.5);
			backdrop-filter: blur(20px);
			box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);

			.navbar__link {
				color: vars.$black-light;

				&::after {
					background-color: vars.$primary-color;
				}
			}
		}

		&__container {
			display: flex;
			align-items: center;
			justify-content: space-between;
			height: 75px;
			transition: height 0.4s cubic-bezier(0.16, 1, 0.3, 1);

			@include mix.responsive(mobile) {
				height: 65px;
			}
		}

		&--scrolled &__container {
			height: 75px;

			@include mix.responsive(mobile) {
				height: 65px;
			}
		}

		&__logo {
			display: flex;
			align-items: center;
			margin-right: vars.$spacing-md;
			transition: transform 0.3s ease;

			&:hover {
				transform: translateY(-2px);
			}

			@include mix.responsive(mobile) {
				margin-right: 0;
			}
		}

		&__nav {
			display: flex;
			align-items: center;
			gap: 16px;
			justify-content: flex-end;
			flex-direction: row;

			@include mix.responsive(mobile) {
				display: none;
			}
		}

		&--sticky {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			z-index: func.z('navbar');
		}
	}

	// Animation du dropdown
	.dropdown-enter-active,
	.dropdown-leave-active {
		transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
		transform-origin: top center;
	}

	.dropdown-enter-from,
	.dropdown-leave-to {
		opacity: 0;
		transform: translateY(-10px) translateX(-50%) scale(0.95);
	}
</style>
