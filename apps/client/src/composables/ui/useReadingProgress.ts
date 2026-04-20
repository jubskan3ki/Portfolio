import { useEventListener } from '@vueuse/core';
import { ref, onMounted, onBeforeUnmount } from 'vue';

import type { Ref } from 'vue';

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

        isVisible.value = rect.top < windowHeight;

        if (rect.top >= windowHeight) {
            progress.value = 0;
            return;
        }

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
