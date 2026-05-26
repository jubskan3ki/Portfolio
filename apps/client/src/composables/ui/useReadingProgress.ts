import { useEventListener } from '@vueuse/core';
import type { Ref } from 'vue';
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';

export function useReadingProgress(containerRef: Ref<HTMLElement | null>) {
    const progress = ref(0);
    const isVisible = ref(false);

    let topDoc = 0;
    let height = 1;
    let resizeObs: ResizeObserver | null = null;
    let visibilityObs: IntersectionObserver | null = null;
    let rafId: number | null = null;

    function measure() {
        const el = containerRef.value;
        if (!el) {
            return;
        }
        const rect = el.getBoundingClientRect();
        topDoc = rect.top + window.scrollY;
        height = Math.max(1, rect.height);
    }

    function update() {
        const winH = window.innerHeight;
        const scrolled = window.scrollY + winH - topDoc;
        let pct = (scrolled / height) * 100;
        if (pct < 0) {
            pct = 0;
        } else if (pct > 100) {
            pct = 100;
        }
        progress.value = pct;
    }

    function onScroll() {
        if (rafId !== null) {
            return;
        }
        rafId = requestAnimationFrame(() => {
            rafId = null;
            update();
        });
    }

    onMounted(() => {
        const el = containerRef.value;
        if (!el) {
            // Defer until ref is set.
            watch(
                containerRef,
                (val) => {
                    if (val) {
                        bind(val);
                    }
                },
                { once: true },
            );
            return;
        }
        bind(el);
    });

    function bind(el: HTMLElement) {
        measure();
        update();

        if (typeof ResizeObserver !== 'undefined') {
            resizeObs = new ResizeObserver(() => {
                measure();
                update();
            });
            resizeObs.observe(el);
        }

        if (typeof IntersectionObserver !== 'undefined') {
            visibilityObs = new IntersectionObserver(
                (entries) => {
                    for (const entry of entries) {
                        isVisible.value = entry.isIntersecting || entry.boundingClientRect.top < 0;
                    }
                },
                { threshold: 0, rootMargin: '0px 0px 0px 0px' },
            );
            visibilityObs.observe(el);
        } else {
            isVisible.value = true;
        }
    }

    useEventListener(typeof window !== 'undefined' ? window : null, 'scroll', onScroll, { passive: true });

    onBeforeUnmount(() => {
        if (rafId !== null) {
            cancelAnimationFrame(rafId);
        }
        resizeObs?.disconnect();
        visibilityObs?.disconnect();
    });

    return { progress, isVisible };
}
