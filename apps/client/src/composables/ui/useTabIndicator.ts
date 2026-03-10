import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed, toValue } from 'vue';

import type { MaybeRefOrGetter, Ref, ComputedRef } from 'vue';

export interface UseTabIndicatorOptions {
    trackRef: Ref<HTMLElement | null>;
    tabRefs: Ref<Array<HTMLElement | null>>;
    activeIndex: MaybeRefOrGetter<number>;
    tabs: MaybeRefOrGetter<unknown[]>;
    mode?: 'css-vars' | 'inline-style';
    listenResize?: boolean;
}

export interface UseTabIndicatorReturn {
    updateIndicator: () => void;
    indicatorReady: Ref<boolean>;
    indicatorStyle: ComputedRef<{ width: string; transform: string }>;
    setTabRef: (index: number, el: HTMLElement | null) => void;
}

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

    const updateIndicator = () => {
        const index = toValue(options.activeIndex);
        const activeBtn = tabRefs.value[index];
        const track = trackRef.value;

        if (!activeBtn || !track || index === -1) {
            indicatorReady.value = false;
            return;
        }

        if (activeBtn.offsetWidth === 0) {
            requestAnimationFrame(updateIndicator);
            return;
        }

        const left = activeBtn.offsetLeft;
        const width = activeBtn.offsetWidth;

        if (mode === 'css-vars') {
            track.style.setProperty('--indicator-left', `${left}px`);
            track.style.setProperty('--indicator-width', `${width}px`);
        }

        indicatorLeft.value = left;
        indicatorWidth.value = width;
        indicatorReady.value = true;
    };

    watch(
        () => toValue(options.activeIndex),
        () => nextTick(updateIndicator),
    );

    watch(
        () => toValue(options.tabs),
        () => nextTick(updateIndicator),
        { deep: true },
    );

    onMounted(() => {
        nextTick(() => requestAnimationFrame(updateIndicator));
        if (listenResize) {
            window.addEventListener('resize', updateIndicator);
        }
    });

    onBeforeUnmount(() => {
        if (listenResize) {
            window.removeEventListener('resize', updateIndicator);
        }
    });

    return { updateIndicator, indicatorReady, indicatorStyle, setTabRef };
}
