// src/store/navBar.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

import type { NavStoreDefinition } from '@/types/store/navBar';

export const useNavStore = defineStore('nav', (): NavStoreDefinition => {
	// État
	const isMobileMenuOpen = ref<boolean>(false);
	const expandedSubmenuIndex = ref<number | null>(null);

	// Actions
	/**
	 * Ouvre le menu mobile
	 */
	const openMobileMenu = (): void => {
		isMobileMenuOpen.value = true;

		// Empêcher le défilement du body quand le menu est ouvert
		if (typeof document !== 'undefined') {
			document.body.style.overflow = 'hidden';
		}
	};

	/**
	 * Ferme le menu mobile
	 */
	const closeMobileMenu = (): void => {
		isMobileMenuOpen.value = false;
		expandedSubmenuIndex.value = null;

		// Rétablir le défilement du body
		if (typeof document !== 'undefined') {
			document.body.style.overflow = '';
		}
	};

	/**
	 * Bascule l'état du menu mobile
	 */
	const toggleMobileMenu = (): void => {
		if (isMobileMenuOpen.value) {
			closeMobileMenu();
		} else {
			openMobileMenu();
		}
	};

	/**
	 * Développe un sous-menu par son index
	 * @param index Index du sous-menu à développer
	 */
	const expandSubmenu = (index: number): void => {
		expandedSubmenuIndex.value = index;
	};

	/**
	 * Replie le sous-menu actif
	 */
	const collapseSubmenu = (): void => {
		expandedSubmenuIndex.value = null;
	};

	/**
	 * Bascule l'état d'un sous-menu
	 * @param index Index du sous-menu à basculer
	 */
	const toggleSubmenu = (index: number): void => {
		if (expandedSubmenuIndex.value === index) {
			collapseSubmenu();
		} else {
			expandSubmenu(index);
		}
	};

	return {
		// État
		isMobileMenuOpen,
		expandedSubmenuIndex,

		// Actions
		openMobileMenu,
		closeMobileMenu,
		toggleMobileMenu,
		expandSubmenu,
		collapseSubmenu,
		toggleSubmenu,
	};
});

export default useNavStore;
