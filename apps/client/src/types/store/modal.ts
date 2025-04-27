// types/store/modal.ts
import type { ComputedRef } from 'vue';

// Tailles disponibles pour les modales
export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

// Interface pour les options de configuration d'une modale
export interface ModalOptions {
	id?: string;
	title?: string;
	content?: string;
	component?: string;
	componentProps?: Record<string, any>;
	size?: ModalSize;
	closable?: boolean;
	closeOnClickOutside?: boolean;
	hideCloseButton?: boolean;
	persistent?: boolean;
}

// Interface pour l'état du store de modales
export interface ModalState {
	visible: boolean;
	options: ModalOptions;
}

// Interface pour les actions du store de modales
export interface ModalActions {
	open(options: ModalOptions): void;
	close(): void;
}

// Interface pour les options de la modale de confirmation
export interface ModalConfirmationOptions {
	title?: string;
	content?: string;
	confirmText?: string;
	cancelText?: string;
	onConfirm?: () => void;
	onCancel?: () => void;
	variant?: 'default' | 'danger' | 'warning';
}

// Interface de retour pour le composable useModal
export interface UseModalReturn {
	openModal: (options: ModalOptions) => void;
	openComponentModal: (componentName: string, props?: Record<string, any>, options?: Partial<ModalOptions>) => void;
	openModalConfirmation: (options: ModalConfirmationOptions) => void;
	closeModal: () => void;
	isVisible: ComputedRef<boolean>;
	currentModal: ComputedRef<ModalOptions>;
}
