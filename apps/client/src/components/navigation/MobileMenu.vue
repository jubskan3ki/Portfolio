<!-- src/components/navigation/MobileMenu.vue -->
<template>
	<div :class="['mobile-menu', { 'mobile-menu--open': isOpen }, customClass]">
		<!-- Backdrop -->
		<transition name="fade">
			<div
				v-if="isOpen"
				class="mobile-menu__backdrop"
				role="button"
				tabindex="0"
				aria-label="Fermer le menu"
				@click="close"
				@keydown.enter="close"
				@keydown.space.prevent="close"
			></div>
		</transition>

		<!-- Menu Panel -->
		<div class="mobile-menu__panel">
			<!-- Header -->
			<div class="mobile-menu__header">
				<div class="mobile-menu__logo">
					<AppLogo />
				</div>
				<button class="mobile-menu__close" aria-label="Fermer le menu" @click="close">
					<BaseIcon name="close" :size="24" />
				</button>
			</div>

			<!-- Navigation -->
			<nav class="mobile-menu__nav" aria-label="Menu de navigation mobile">
				<ul class="mobile-menu__nav-list">
					<MobileMenuItem
						v-for="(item, index) in navigationItems"
						:key="index"
						:item="item"
						:index="index"
						:expanded-index="expandedSubmenu"
						@close="close"
						@expand="expandSubmenu"
						@collapse="collapseSubmenu"
					/>
				</ul>
			</nav>

			<!-- Footer -->
			<div class="mobile-menu__footer">
				<div class="mobile-menu__buttons">
					<BaseButton to="/contact" variant="primary" :full-width="true" @click="close">
						Me contacter
					</BaseButton>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import MobileMenuItem from '@/components/navigation/MobileMenuItem.vue';
	import AppLogo from '@/components/ui/AppLogo.vue';
	import { navigationItems } from '@/config/navBar';
	import { onBeforeUnmount, onMounted, ref, watch } from 'vue';

	// Props
	const props = defineProps({
		isOpen: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Emits
	const emit = defineEmits(['close', 'update:isOpen']);

	// State
	const expandedSubmenu = ref<number | null>(null);
	const isMounted = ref(false);

	// Methods
	const close = () => {
		emit('close');
		emit('update:isOpen', false);
	};

	const expandSubmenu = (index: number) => {
		expandedSubmenu.value = index;
	};

	const collapseSubmenu = () => {
		expandedSubmenu.value = null;
	};

	// Gestion du clic externe en utilisant un gestionnaire manuel pour éviter les problèmes SSR
	const handleClickOutside = (event: MouseEvent) => {
		// Ne s'exécute que si le menu est ouvert et si on a cliqué en dehors du panneau
		if (props.isOpen) {
			const panel = document.querySelector('.mobile-menu__panel');
			const toggle = document.querySelector('.mobile-menu-toggle');

			if (panel && !panel.contains(event.target as Node) && toggle && !toggle.contains(event.target as Node)) {
				close();
			}
		}
	};

	const handleEscapeKey = (event: KeyboardEvent) => {
		if (event.key === 'Escape' && props.isOpen) {
			close();
		}
	};

	// Gestionnaire de redimensionnement
	const handleResize = () => {
		if (import.meta.client && window.innerWidth >= 768 && props.isOpen) {
			close();
		}
	};

	// Watcher pour gérer l'état du menu
	watch(
		() => props.isOpen,
		(newValue) => {
			if (!isMounted.value) return;

			if (import.meta.client) {
				if (newValue) {
					document.body.style.overflow = 'hidden';
					// Ajouter les gestionnaires d'événements quand le menu est ouvert
					document.addEventListener('click', handleClickOutside);
				} else {
					document.body.style.overflow = '';
					expandedSubmenu.value = null;
					// Retirer les gestionnaires d'événements quand le menu est fermé
					document.removeEventListener('click', handleClickOutside);
				}
			}
		}
	);

	// Lifecycle hooks
	onMounted(() => {
		isMounted.value = true;

		if (import.meta.client) {
			window.addEventListener('resize', handleResize);
			window.addEventListener('keydown', handleEscapeKey);
		}

		// Force la fermeture du menu au chargement
		if (props.isOpen) {
			setTimeout(() => {
				close();
			}, 0);
		}
	});

	onBeforeUnmount(() => {
		if (import.meta.client) {
			window.removeEventListener('resize', handleResize);
			window.removeEventListener('keydown', handleEscapeKey);
			document.removeEventListener('click', handleClickOutside);

			// Réinitialiser l'overflow du body
			document.body.style.overflow = '';
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.mobile-menu {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: func.z('navbar') + 10;
		visibility: hidden;
		pointer-events: none;
		transition: visibility 0.3s ease;

		&--open {
			visibility: visible;
			pointer-events: auto;

			.mobile-menu__backdrop {
				opacity: 1;
			}

			.mobile-menu__panel {
				transform: translateX(0);
			}
		}

		&__backdrop {
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background-color: rgba(0, 0, 0, 0.5);
			backdrop-filter: blur(4px);
			opacity: 0;
			transition: opacity 0.4s ease;
			cursor: pointer;
		}

		&__panel {
			position: absolute;
			top: 0;
			right: 0;
			width: 85%;
			max-width: 360px;
			height: 100%;
			background-color: vars.$white;
			display: flex;
			flex-direction: column;
			transform: translateX(100%);
			transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
			overflow-y: auto;
			-webkit-overflow-scrolling: touch;
			box-shadow: -5px 0 30px rgba(0, 0, 0, 0.15);
		}

		&__header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: vars.$spacing-md;
			border-bottom: 1px solid vars.$white-dark;
			height: 70px;
		}

		&__logo {
			height: 40px;
			display: flex;
			align-items: center;
		}

		&__close {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 40px;
			height: 40px;
			border-radius: 50%;
			transition: background-color vars.$transition-base;
			color: vars.$black-light;

			&:hover {
				background-color: vars.$white-dark;
			}
		}

		&__nav {
			flex: 1;
			padding: vars.$spacing-md;
			overflow-y: auto;
		}

		&__nav-list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
		}

		&__footer {
			padding: vars.$spacing-md;
			border-top: 1px solid vars.$white-dark;
		}

		&__buttons {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}
	}

	// Animation pour le backdrop
	.fade-enter-active,
	.fade-leave-active {
		transition: opacity 0.3s ease;
	}

	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}
</style>
