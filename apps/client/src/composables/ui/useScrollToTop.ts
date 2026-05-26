import { onMounted, onUnmounted, readonly, ref } from 'vue';

import { SCROLL_THRESHOLDS } from '@/config/constants';

import type { UseScrollToTopOptions, UseScrollToTopReturn } from '@/types/composables/ui';

export function useScrollToTop(options: UseScrollToTopOptions = {}): UseScrollToTopReturn {
    const { threshold = SCROLL_THRESHOLDS.SHOW_SCROLL_TOP, onScroll } = options;

    const showButton = ref(false);
    const scrollY = ref(0);

    let ticking = false;

    const handleScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                scrollY.value = window.scrollY;
                showButton.value = window.scrollY > threshold;

                if (onScroll) {
                    onScroll(window.scrollY);
                }

                ticking = false;
            });
            ticking = true;
        }
    };

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

    onMounted(() => {
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
