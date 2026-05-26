import type { Ref } from 'vue';
import { getCurrentScope, onScopeDispose, ref, watch } from 'vue';

import type { ClickOutsideHandler, UseClickOutsideOptions, UseClickOutsideReturn } from '@/types/composables/ui';

export function useClickOutside(
    target: Ref<HTMLElement | null>,
    handler: ClickOutsideHandler,
    options: UseClickOutsideOptions = {},
): UseClickOutsideReturn {
    const { ignore = [], enabled = true, immediate = true } = options;

    const isActive = ref(false);

    const isEnabled = (): boolean => {
        if (typeof enabled === 'boolean') {
            return enabled;
        }
        return enabled.value;
    };

    const shouldIgnore = (event: MouseEvent | TouchEvent): boolean => {
        if (ignore.length === 0) {
            return false;
        }

        const path = event.composedPath();
        return ignore.some((selector) => {
            try {
                const elements = document.querySelectorAll(selector);
                return Array.from(elements).some((el) => path.includes(el));
            } catch {
                return false;
            }
        });
    };

    const listener = (event: MouseEvent | TouchEvent): void => {
        if (!isEnabled() || !isActive.value) {
            return;
        }

        const el = target.value;
        if (!el) {
            return;
        }

        if (el === event.target || event.composedPath().includes(el)) {
            return;
        }
        if (shouldIgnore(event)) {
            return;
        }

        handler(event);
    };

    const start = (): void => {
        if (typeof window === 'undefined' || isActive.value) {
            return;
        }

        window.addEventListener('mousedown', listener, { passive: true });
        window.addEventListener('touchstart', listener, { passive: true });
        isActive.value = true;
    };

    const stop = (): void => {
        if (typeof window === 'undefined' || !isActive.value) {
            return;
        }

        window.removeEventListener('mousedown', listener, { passive: true } as EventListenerOptions);
        window.removeEventListener('touchstart', listener, { passive: true } as EventListenerOptions);
        isActive.value = false;
    };

    if (typeof enabled !== 'boolean') {
        watch(enabled, (newEnabled) => {
            if (newEnabled && !isActive.value) {
                start();
            } else if (!newEnabled && isActive.value) {
                stop();
            }
        });
    }

    if (immediate && isEnabled()) {
        start();
    }

    if (getCurrentScope()) {
        onScopeDispose(stop);
    }

    return { start, stop, isActive };
}
