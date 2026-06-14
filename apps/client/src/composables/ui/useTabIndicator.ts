import { computed, nextTick, onBeforeUnmount, onMounted, ref, toValue, watch } from 'vue';

import type { UseTabIndicatorOptions, UseTabIndicatorReturn } from '@/types/composables/ui';

export function useTabIndicator(options: UseTabIndicatorOptions): UseTabIndicatorReturn {
    const { trackRef, tabRefs, mode = 'css-vars', listenResize = false } = options;

    const indicatorReady = ref(false);
    const indicatorLeft = ref(0);
    const indicatorWidth = ref(0);

    const indicatorStyle = computed(() => ({
        width: `${indicatorWidth.value}px`,
        transform: `translateX(${indicatorLeft.value}px)`,
    }));

    const setTabRef = (index: number, el: HTMLElement | null) => {
        tabRefs.value[index] = el;
    };

    // rAF coalescing : regroupe les rafales d'updates (tab actif, tabs, resize) en une seule lecture layout par frame.
    let rafId: number | null = null;
    let resizeObs: ResizeObserver | null = null;

    const readAndApply = () => {
        rafId = null;
        const index = toValue(options.activeIndex);
        const activeBtn = tabRefs.value[index];
        const track = trackRef.value;

        if (!activeBtn || !track || index === -1) {
            indicatorReady.value = false;
            return;
        }

        // Élément pas encore layouté (ex. dans une transition) : on diffère d'une frame de plus.
        const width = activeBtn.offsetWidth;
        if (width === 0) {
            schedule();
            return;
        }

        const left = activeBtn.offsetLeft;

        if (mode === 'css-vars') {
            track.style.setProperty('--indicator-left', `${left}px`);
            track.style.setProperty('--indicator-width', `${width}px`);
        }

        indicatorLeft.value = left;
        indicatorWidth.value = width;
        indicatorReady.value = true;
    };

    const schedule = () => {
        if (rafId !== null) {
            return;
        }
        rafId = requestAnimationFrame(readAndApply);
    };

    const updateIndicator = schedule;

    watch(
        () => toValue(options.activeIndex),
        () => nextTick(schedule),
    );

    watch(
        () => toValue(options.tabs),
        () => nextTick(schedule),
        { deep: true },
    );

    onMounted(() => {
        nextTick(schedule);

        // ResizeObserver sur la track si dispo : ne déclenche que sur vrai changement de layout, sans reflow forcé global.
        const track = trackRef.value;
        if (listenResize) {
            if (typeof ResizeObserver !== 'undefined' && track) {
                resizeObs = new ResizeObserver(schedule);
                resizeObs.observe(track);
            } else {
                window.addEventListener('resize', schedule, { passive: true });
            }
        }
    });

    onBeforeUnmount(() => {
        if (rafId !== null) {
            cancelAnimationFrame(rafId);
            rafId = null;
        }
        if (resizeObs) {
            resizeObs.disconnect();
            resizeObs = null;
        } else if (listenResize) {
            window.removeEventListener('resize', schedule);
        }
    });

    return { updateIndicator, indicatorReady, indicatorStyle, setTabRef };
}
