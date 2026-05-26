import type { Ref } from 'vue';
import { onUnmounted, ref } from 'vue';

const FOCUSABLE_SELECTOR = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

export function useFocusTrap(containerRef: Ref<HTMLElement | null>) {
    const isActive = ref(false);
    let previousActiveElement: Element | null = null;

    const getFocusableElements = (): HTMLElement[] => {
        if (!containerRef.value) {
            return [];
        }

        return Array.from(containerRef.value.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
            (el) => !el.hasAttribute('disabled') && el.offsetParent !== null,
        );
    };

    const handleKeyDown = (e: KeyboardEvent) => {
        if (!isActive.value || e.key !== 'Tab') {
            return;
        }

        const focusableElements = getFocusableElements();
        if (focusableElements.length === 0) {
            return;
        }

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (!firstElement || !lastElement) {
            return;
        }

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    };

    const activate = () => {
        previousActiveElement = document.activeElement;
        isActive.value = true;
        document.addEventListener('keydown', handleKeyDown);

        const focusableElements = getFocusableElements();
        if (focusableElements[0]) {
            focusableElements[0].focus();
        }
    };

    const deactivate = () => {
        isActive.value = false;
        document.removeEventListener('keydown', handleKeyDown);

        if (previousActiveElement instanceof HTMLElement) {
            previousActiveElement.focus();
        }
    };

    onUnmounted(() => {
        deactivate();
    });

    return {
        isActive,
        activate,
        deactivate,
        getFocusableElements,
    };
}
