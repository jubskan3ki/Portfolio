// src/store/modal.ts
import { defineStore } from 'pinia';

import type { ModalOptions, ModalState } from '@/types/store/modal';

export const useModalStore = defineStore('modal', {
	state: (): ModalState => ({
		visible: false,
		options: {
			id: '',
			title: '',
			content: '',
			component: undefined,
			componentProps: {},
			size: 'md',
			closable: true,
			closeOnClickOutside: true,
			hideCloseButton: false,
			persistent: false,
		},
	}),

	actions: {
		/**
		 * Ouvre une modale avec les options spécifiées
		 */
		open(options: ModalOptions): void {
			// Générer un ID unique si non fourni
			if (!options.id) {
				options.id = `modal-${Date.now()}`;
			}

			this.options = {
				...this.options, // Options par défaut
				...options, // Options personnalisées
			};

			this.visible = true;

			// Empêche le défilement de la page lorsque la modale est ouverte
			if (typeof document !== 'undefined') {
				document.body.style.overflow = 'hidden';
			}
		},

		/**
		 * Ferme la modale actuellement ouverte
		 */
		close(): void {
			this.visible = false;

			// Réactive le défilement de la page
			if (typeof document !== 'undefined') {
				document.body.style.overflow = '';
			}

			// Réinitialiser les options après un délai (pour l'animation)
			setTimeout(() => {
				this.options = {
					id: '',
					title: '',
					content: '',
					component: undefined,
					componentProps: {},
					size: 'md',
					closable: true,
					closeOnClickOutside: true,
					hideCloseButton: false,
					persistent: false,
				};
			}, 300); // Correspondant à la durée de l'animation
		},
	},
});

export default useModalStore;
