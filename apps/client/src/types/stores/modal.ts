// types/stores/modal.ts
import type { ModalOptions as BaseModalOptions } from '@/types/components/feedback';

// Re-export ModalSize from feedback for consistency
// Extend base ModalOptions with store-specific fields
export interface ModalOptions extends BaseModalOptions {
    /** Unique identifier for the modal instance */
    id?: string;
}

// Interface pour l'état du store de modales
export interface ModalState {
    visible: boolean;
    options: ModalOptions;
}
