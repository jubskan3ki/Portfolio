import { ref, computed, onMounted, onUnmounted, readonly, type Ref } from 'vue';

import { BREAKPOINTS, type Breakpoint } from '@/config/constants';

// Local types that use Breakpoint from config
interface UseResponsiveOptions {
    initialBreakpoint?: Breakpoint;
}

interface UseResponsiveReturn {
    windowWidth: Readonly<Ref<number>>;
    isMobile: Readonly<Ref<boolean>>;
    isTablet: Readonly<Ref<boolean>>;
    isDesktop: Readonly<Ref<boolean>>;
    currentBreakpoint: Readonly<Ref<Breakpoint>>;
    isBelow: (breakpoint: Breakpoint) => boolean;
    isAbove: (breakpoint: Breakpoint) => boolean;
}

// Re-export types for external use
export function useResponsive(options: UseResponsiveOptions = {}): UseResponsiveReturn {
    const { initialBreakpoint = 'DESKTOP' } = options;

    const windowWidth = ref<number>(BREAKPOINTS[initialBreakpoint]);

    const isMobile = computed(() => windowWidth.value < BREAKPOINTS.TABLET);
    const isTablet = computed(() => windowWidth.value >= BREAKPOINTS.TABLET && windowWidth.value < BREAKPOINTS.DESKTOP);
    const isDesktop = computed(() => windowWidth.value >= BREAKPOINTS.DESKTOP);

    const currentBreakpoint = computed((): Breakpoint => {
        if (windowWidth.value <= BREAKPOINTS.MOBILE) {
            return 'MOBILE';
        }
        if (windowWidth.value < BREAKPOINTS.DESKTOP) {
            return 'TABLET';
        }
        if (windowWidth.value < BREAKPOINTS.WIDE) {
            return 'DESKTOP';
        }
        return 'WIDE';
    });

    const isBelow = (breakpoint: Breakpoint): boolean => {
        return windowWidth.value < BREAKPOINTS[breakpoint];
    };

    const isAbove = (breakpoint: Breakpoint): boolean => {
        return windowWidth.value >= BREAKPOINTS[breakpoint];
    };

    let resizeTimeout: ReturnType<typeof setTimeout> | null = null;

    const handleResize = () => {
        if (resizeTimeout) {
            clearTimeout(resizeTimeout);
        }
        resizeTimeout = setTimeout(() => {
            windowWidth.value = window.innerWidth;
        }, 100);
    };

    onMounted(() => {
        windowWidth.value = window.innerWidth;
        window.addEventListener('resize', handleResize, { passive: true });
    });

    onUnmounted(() => {
        window.removeEventListener('resize', handleResize, { passive: true } as EventListenerOptions);
        if (resizeTimeout) {
            clearTimeout(resizeTimeout);
        }
    });

    return {
        windowWidth: readonly(windowWidth),
        isMobile: readonly(isMobile),
        isTablet: readonly(isTablet),
        isDesktop: readonly(isDesktop),
        currentBreakpoint: readonly(currentBreakpoint),
        isBelow,
        isAbove,
    };
}
