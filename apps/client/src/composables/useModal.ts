// src/composables/useModal.ts
import { computed } from 'vue';

import { useModalStore } from '@/store/modal';
import type { ModalConfirmationOptions, ModalOptions, UseModalReturn } from '@/types/store/modal';

/**
 * Composable pour la gestion des modales
 */
export function useModal(): UseModalReturn {
	const modalStore = useModalStore();

	// Utiliser des computed pour accéder aux propriétés de state au lieu des actions
	const isVisible = computed(() => modalStore.$state.visible);
	const currentModal = computed(() => modalStore.$state.options);

	/**
	 * Ouvre une modale avec le contenu spécifié
	 */
	function openModal(options: ModalOptions): void {
		modalStore.open(options);
	}

	/**
	 * Ouvre une modale avec un composant spécifié
	 */
	function openComponentModal(
		componentName: string,
		props: Record<string, any> = {},
		options: Partial<ModalOptions> = {}
	): void {
		modalStore.open({
			component: componentName,
			componentProps: props,
			...options,
		});
	}

	/**
	 * Ouvre une modale de confirmation simple
	 */
	function openModalConfirmation(options: ModalConfirmationOptions): void {
		modalStore.open({
			component: 'ModalConfirmation',
			componentProps: options,
			size: 'sm',
			closable: true,
			closeOnClickOutside: false,
		});
	}

	/**
	 * Ferme la modale actuellement ouverte
	 */
	function closeModal(): void {
		modalStore.close();
	}

	return {
		openModal,
		openComponentModal,
		openModalConfirmation,
		closeModal,
		isVisible, // Computed property
		currentModal, // Computed property
	};
}

export default useModal;
