// types/store/navBar.ts

/**
 * Types pour le store de navigation
 */

import type { Ref } from 'vue';

// Interface pour l'état du store de navigation
export interface NavState {
	isMobileMenuOpen: boolean;
	expandedSubmenuIndex: number | null;
}

// Interface pour les actions du store de navigation
export interface NavActions {
	openMobileMenu(): void;
	closeMobileMenu(): void;
	toggleMobileMenu(): void;
	expandSubmenu(index: number): void;
	collapseSubmenu(): void;
	toggleSubmenu(index: number): void;
}

// Interface pour la fonction defineStore avec ref
export interface NavStoreDefinition {
	// État
	isMobileMenuOpen: Ref<boolean>;
	expandedSubmenuIndex: Ref<number | null>;

	// Actions
	openMobileMenu: () => void;
	closeMobileMenu: () => void;
	toggleMobileMenu: () => void;
	expandSubmenu: (index: number) => void;
	collapseSubmenu: () => void;
	toggleSubmenu: (index: number) => void;
}

// Interface pour le résultat du composable useNavStore
export interface UseNavStoreReturn extends NavStoreDefinition {}
