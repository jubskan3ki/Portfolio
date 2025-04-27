<!-- src/components/layouts/Header.vue -->
<template>
	<header class="header">
		<!-- NavBar Principal -->
		<NavBar :sticky="true">
			<template #logo>
				<AppLogo :image-path="images.others.logo" width="42" height="42" />
			</template>
			<template #actions>
				<a
					v-for="social in socialLinks"
					:key="social.name"
					:href="social.url"
					target="_blank"
					rel="noopener noreferrer"
					class="header__social-link"
					:aria-label="social.name"
				>
					<BaseIcon :name="social.icon" :size="20" />
				</a>
			</template>
		</NavBar>

		<!-- Mobile Menu Toggle -->
		<MobileMenuToggle :is-active="isMobileMenuOpen" class="header__mobile-toggle" @toggle="toggleMobileMenu" />

		<!-- Menu Mobile -->
		<MobileMenu :is-open="isMobileMenuOpen" :custom-class="'header__mobile-menu'" @close="closeMobileMenu" />
	</header>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import MobileMenu from '@/components/navigation/MobileMenu.vue';
	import MobileMenuToggle from '@/components/navigation/MobileMenuToggle.vue';
	import NavBar from '@/components/navigation/NavBar.vue';
	import AppLogo from '@/components/ui/AppLogo.vue';
	import { images } from '@/config/images';
	import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
	import { useRoute } from 'vue-router';

	// État de la navigation mobile
	const isMobileMenuOpen = ref(false);

	// Référence à la route actuelle
	const route = useRoute();

	// Liens sociaux
	const socialLinks = [
		{ name: 'GitHub', icon: 'github', url: 'https://github.com/' },
		{ name: 'LinkedIn', icon: 'linkedin', url: 'https://linkedin.com/' },
	];

	// Fonctions pour le menu mobile
	const toggleMobileMenu = () => {
		isMobileMenuOpen.value = !isMobileMenuOpen.value;
	};

	const closeMobileMenu = () => {
		isMobileMenuOpen.value = false;
	};

	// Fermer le menu mobile lorsque la route change
	watch(
		() => route.path,
		() => {
			closeMobileMenu();
		}
	);

	// Fonction pour fermer le menu avec la touche Escape
	const handleEscKey = (event: KeyboardEvent) => {
		if (event.key === 'Escape' && isMobileMenuOpen.value) {
			closeMobileMenu();
		}
	};

	// Ajouter les écouteurs d'événements uniquement côté client
	onMounted(() => {
		document.addEventListener('keydown', handleEscKey);
	});

	// Nettoyer les écouteurs d'événements
	onBeforeUnmount(() => {
		document.removeEventListener('keydown', handleEscKey);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.header {
		position: relative;
		z-index: func.z('navbar');
		width: 100%;

		&__social-link {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 36px;
			height: 36px;
			border-radius: 50%;
			background-color: func.color-alpha(vars.$white, 0.15);
			backdrop-filter: blur(5px);
			color: currentColor;
			transition: all vars.$transition-base;

			&:hover {
				transform: translateY(-3px);
				background-color: func.color-alpha(vars.$primary-color, 0.8);
				color: vars.$white;
				box-shadow: 0 5px 15px func.color-alpha(vars.$primary-color, 0.3);
			}
		}

		&__mobile-toggle {
			position: fixed;
			top: 15px;
			right: 15px;
			z-index: func.z('navbar') + 30;
			display: none;

			@include mix.responsive(mobile) {
				display: flex;
			}
		}

		&__mobile-menu {
			z-index: func.z('navbar') + 20;
		}
	}
</style>
