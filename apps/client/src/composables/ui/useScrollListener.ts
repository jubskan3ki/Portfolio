import { useEventListener } from '@vueuse/core';

/**
 * Registers a passive scroll event listener on the window.
 * Automatically cleans up the listener when the component is unmounted.
 */
export function useScrollListener(callback: (event: Event) => void): void {
    useEventListener(window, 'scroll', callback, { passive: true });
}
