// src/composables/ui/useScrollToTop.ts
// Composable pour le bouton "retour en haut"

import { ref, readonly, onMounted, onUnmounted } from 'vue';

import { SCROLL_THRESHOLDS } from '@/config/constants';

import type { UseScrollToTopOptions, UseScrollToTopReturn } from '@/types/composables/ui';

// Scroll-to-top button with RAF throttling
export function useScrollToTop(options: UseScrollToTopOptions = {}): UseScrollToTopReturn {
    const { threshold = SCROLL_THRESHOLDS.SHOW_SCROLL_TOP, onScroll } = options;

    // État
    const showButton = ref(false);
    const scrollY = ref(0);

    // RAF throttling
    let ticking = false;

    const handleScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                scrollY.value = window.scrollY;
                showButton.value = window.scrollY > threshold;

                // Callback optionnel
                if (onScroll) {
                    onScroll(window.scrollY);
                }

                ticking = false;
            });
            ticking = true;
        }
    };

    // Méthodes
    const scrollToTop = (behavior: ScrollBehavior = 'smooth') => {
        window.scrollTo({ top: 0, behavior });
    };

    const scrollToElement = (selector: string, options?: ScrollIntoViewOptions) => {
        const element = document.querySelector(selector);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
                ...options,
            });
        }
    };

    // Lifecycle
    onMounted(() => {
        // Vérifier l'état initial
        scrollY.value = window.scrollY;
        showButton.value = window.scrollY > threshold;

        window.addEventListener('scroll', handleScroll, { passive: true });
    });

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll, { passive: true } as EventListenerOptions);
    });

    return {
        showButton: readonly(showButton),
        scrollY: readonly(scrollY),
        scrollToTop,
        scrollToElement,
    };
}
