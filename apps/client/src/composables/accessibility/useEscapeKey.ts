import { onMounted, onUnmounted, ref } from 'vue';

import type { UseEscapeKeyOptions } from '@/types/composables/accessibility';

export function useEscapeKey(callback: () => void, options: UseEscapeKeyOptions = {}) {
    const { enabled = true } = options;

    const isListening = ref(false);

    const isEnabled = () => {
        if (typeof enabled === 'boolean') {
            return enabled;
        }
        return enabled.value;
    };

    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && isEnabled()) {
            callback();
        }
    };

    const start = () => {
        if (isListening.value) {
            return;
        }
        document.addEventListener('keydown', handleKeyDown);
        isListening.value = true;
    };

    const stop = () => {
        document.removeEventListener('keydown', handleKeyDown);
        isListening.value = false;
    };

    onMounted(() => {
        start();
    });

    onUnmounted(() => {
        stop();
    });

    return {
        isListening,
        start,
        stop,
    };
}
