import { useEventListener } from '@vueuse/core';
import { ref, onMounted, onBeforeUnmount } from 'vue';

import type { Ref } from 'vue';

/**
 * Tracks reading progress based on scroll position within a container element.
 * Returns a progress percentage (0-100) and visibility flag.
 */
export function useReadingProgress(containerRef: Ref<HTMLElement | null>) {
    const progress = ref(0);
    const isVisible = ref(false);

    function updateProgress() {
        const el = containerRef.value;
        if (!el) {
            return;
        }

        const rect = el.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        // Show progress bar once the article is in view
        isVisible.value = rect.top < windowHeight;

        if (rect.top >= windowHeight) {
            progress.value = 0;
            return;
        }

        // Calculate how far through the article the user has scrolled
        const totalHeight = rect.height;
        const scrolled = windowHeight - rect.top;
        const pct = Math.min(100, Math.max(0, (scrolled / totalHeight) * 100));
        progress.value = pct;
    }

    let rafId: number | null = null;
    function onScroll() {
        if (rafId) {
            return;
        }
        rafId = requestAnimationFrame(() => {
            updateProgress();
            rafId = null;
        });
    }

    useEventListener(window, 'scroll', onScroll, { passive: true });

    onMounted(() => {
        updateProgress();
    });

    onBeforeUnmount(() => {
        if (rafId) {
            cancelAnimationFrame(rafId);
        }
    });

    return { progress, isVisible };
}
