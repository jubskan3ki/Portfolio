import { defineStore } from 'pinia';
import { ref } from 'vue';

import { TIMEOUTS } from '@/config/constants';
import { lockBodyOverflow, unlockBodyOverflow } from '@/services/utils/dom';
import { TimeoutManager } from '@/services/utils/timeoutManager';

import type { ModalOptions, ModalState } from '@/types/stores/modal';

const defaultOptions: ModalState['options'] = {
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

export const useModalStore = defineStore('modal', () => {
    // SSR-safe: TimeoutManager par instance (pas de fuite inter-requêtes)
    const closeTimeouts = new TimeoutManager();

    const visible = ref(false);
    const options = ref<ModalState['options']>({ ...defaultOptions });

    function open(opts: ModalOptions): void {
        const modalId = opts.id || `modal-${Date.now()}`;

        closeTimeouts.clear(modalId);

        options.value = {
            ...defaultOptions,
            ...opts,
            id: modalId,
        };

        visible.value = true;
        lockBodyOverflow();
    }

    function close(): void {
        const currentId = options.value.id;
        visible.value = false;
        unlockBodyOverflow();

        if (currentId) {
            closeTimeouts.set(
                currentId,
                () => {
                    options.value = { ...defaultOptions };
                    closeTimeouts.delete(currentId);
                },
                TIMEOUTS.MODAL_CLOSE_ANIMATION,
            );
        } else {
            options.value = { ...defaultOptions };
        }
    }

    function cleanup(): void {
        closeTimeouts.clearAll();
        // Décrément symétrique du lock posé dans open(), au lieu d'écraser le
        // compteur partagé (resetBodyOverflow déverrouillerait les autres modales).
        if (visible.value) {
            unlockBodyOverflow();
            visible.value = false;
        }
    }

    return {
        visible,
        options,
        open,
        close,
        cleanup,
    };
});
