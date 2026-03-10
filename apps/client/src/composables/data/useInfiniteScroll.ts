import { ref, onMounted, onUnmounted, type Ref } from 'vue';

interface UseInfiniteScrollOptions {
    threshold?: number;
    rootMargin?: string;
    enabled?: Ref<boolean>;
}

export function useInfiniteScroll(callback: () => void, options: UseInfiniteScrollOptions = {}) {
    const { threshold = 0.1, rootMargin = '100px', enabled = ref(true) } = options;

    const targetRef = ref<HTMLElement | null>(null);
    const isIntersecting = ref(false);
    let observer: IntersectionObserver | null = null;

    const handleIntersect = (entries: IntersectionObserverEntry[]) => {
        const entry = entries[0];
        if (!entry) {
            return;
        }

        isIntersecting.value = entry.isIntersecting;

        if (entry.isIntersecting && enabled.value) {
            callback();
        }
    };

    const observe = () => {
        if (typeof window === 'undefined' || !targetRef.value) {
            return;
        }

        observer = new IntersectionObserver(handleIntersect, {
            threshold,
            rootMargin,
        });

        observer.observe(targetRef.value);
    };

    const disconnect = () => {
        if (observer) {
            observer.disconnect();
            observer = null;
        }
    };

    onMounted(() => {
        observe();
    });

    onUnmounted(() => {
        disconnect();
    });

    const setTarget = (el: HTMLElement | null) => {
        disconnect();
        targetRef.value = el;
        if (el) {
            observe();
        }
    };

    return {
        targetRef,
        isIntersecting,
        setTarget,
        disconnect,
    };
}
