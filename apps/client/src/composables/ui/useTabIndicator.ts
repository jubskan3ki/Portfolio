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

    // rAF coalescing: collapse bursts of Vue reactivity updates (active tab change + tabs deep
    // changes + resize observer ticks) into a single layout read per frame.
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

        // Element not yet laid out (e.g. inside a transition). Defer once more.
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

        // Prefer ResizeObserver on the track when available - fires only on real layout changes
        // and avoids the window-level forced reflow path that `resize` events trigger.
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
