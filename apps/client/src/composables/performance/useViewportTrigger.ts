import { ref, computed, onMounted, onUnmounted } from 'vue';

import type { UseViewportTriggerOptions } from '@/types/composables/performance';

export function useViewportTrigger(options: UseViewportTriggerOptions = {}) {
    const { rootMargin = '200px', once = true, ssrEager = false } = options;
    const targetRef = ref<HTMLElement | null>(null);
    const isVisible = ref(false);

    if (import.meta.server) {
        isVisible.value = ssrEager;
        return { targetRef, isVisible, enabled: computed(() => isVisible.value) };
    }

    let observer: IntersectionObserver | null = null;

    onMounted(() => {
        if (!targetRef.value) {
            return;
        }
        observer = new IntersectionObserver(
            ([entry]) => {
                if (entry?.isIntersecting) {
                    isVisible.value = true;
                    if (once) {
                        observer?.disconnect();
                    }
                }
            },
            { rootMargin },
        );
        observer.observe(targetRef.value);
    });

    onUnmounted(() => observer?.disconnect());

    return { targetRef, isVisible, enabled: computed(() => isVisible.value) };
}
