import { ref, computed, onMounted, onUnmounted } from 'vue';

interface UseViewportTriggerOptions {
    /** Distance before the element enters viewport to start loading */
    rootMargin?: string;
    /** Once triggered, stay triggered (default: true) */
    once?: boolean;
    /** Force immediate on server for SSR-critical content (default: false) */
    ssrEager?: boolean;
}

export function useViewportTrigger(options: UseViewportTriggerOptions = {}) {
    const { rootMargin = '200px', once = true, ssrEager = false } = options;
    const targetRef = ref<HTMLElement | null>(null);
    const isVisible = ref(false);

    // SSR: only enable if ssrEager
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
