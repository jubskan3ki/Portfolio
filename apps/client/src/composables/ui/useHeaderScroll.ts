import { useEventListener } from '@vueuse/core';
import { ref, onMounted } from 'vue';

/**
 * Tracks whether the page has been scrolled past a threshold.
 * Uses RAF throttling for performance.
 */
export function useHeaderScroll(threshold = 20) {
    const isScrolled = ref(false);
    let ticking = false;

    const handleScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                isScrolled.value = window.scrollY > threshold;
                ticking = false;
            });
            ticking = true;
        }
    };

    if (import.meta.client) {
        useEventListener(window, 'scroll', handleScroll, { passive: true });
    }

    onMounted(() => {
        handleScroll();
    });

    return { isScrolled };
}
