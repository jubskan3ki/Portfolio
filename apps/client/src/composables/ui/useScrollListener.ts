import { useEventListener } from '@vueuse/core';

export function useScrollListener(callback: (event: Event) => void): void {
    useEventListener(window, 'scroll', callback, { passive: true });
}
