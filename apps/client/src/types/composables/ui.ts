// Types pour les composables ui/

import type { Chart, ChartData, ChartOptions, ChartType } from 'chart.js';
import type { ComputedRef, MaybeRefOrGetter, Ref } from 'vue';
import type { Breakpoint, StorageKey } from '@/config/constants';
import type { LinkTarget, RouteObject } from '../components/base';
import type { DateRange, SwiperProps } from '../components/ui';

// useClickOutside

export type ClickOutsideHandler = (event: MouseEvent | TouchEvent) => void;

export interface UseClickOutsideOptions {
    ignore?: string[];
    enabled?: Ref<boolean> | boolean;
    immediate?: boolean;
}

export interface UseClickOutsideReturn {
    start: () => void;
    stop: () => void;
    isActive: Ref<boolean>;
}

// useTiltCSS

export interface TiltCSSOptions {
    maxRotation?: number;
    perspective?: number;
    scale?: number;
    smoothing?: number;
    resetOnLeave?: boolean;
}

// useScrollToTop

export interface UseScrollToTopOptions {
    threshold?: number;
    onScroll?: (scrollY: number) => void;
}

export interface UseScrollToTopReturn {
    showButton: Readonly<Ref<boolean>>;
    scrollY: Readonly<Ref<number>>;
    scrollToTop: (behavior?: ScrollBehavior) => void;
    scrollToElement: (selector: string, options?: ScrollIntoViewOptions) => void;
}

// useSidebar

export interface UseSidebarOptions {
    storageKey?: StorageKey;
    defaultCollapsed?: boolean;
    closeOnRouteChange?: boolean;
    classPrefix?: string;
}

export interface UseSidebarReturn {
    isCollapsed: Ref<boolean>;
    isMobileOpen: Ref<boolean>;
    showOverlay: Readonly<Ref<boolean>>;
    layoutClasses: Readonly<Ref<Record<string, boolean>>>;
    toggleMobile: () => void;
    toggleCollapsed: () => void;
    closeMobile: () => void;
    openMobile: () => void;
}

// useTabIndicator

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

// useDropdown

export interface UseDropdownOptions {
    onOpen?: () => void;
    onClose?: () => void;
    closeOnSelect?: boolean;
    disabled?: Ref<boolean> | boolean;
}

export interface UseDropdownReturn {
    isOpen: Ref<boolean>;
    highlightedIndex: Ref<number>;
    open: () => void;
    close: () => void;
    toggle: () => void;
    navigate: (direction: 1 | -1, optionsLength: number) => void;
    setHighlighted: (index: number) => void;
    resetHighlighted: () => void;
    handleKeydown: (event: KeyboardEvent, optionsLength: number, onSelect?: () => void) => void;
    scrollToHighlighted: (optionsRef: Ref<HTMLElement | null>, optionClass: string) => void;
    getActiveDescendant: (baseId: string) => string | undefined;
}

// useShare

export interface UseShareReturn {
    shareUrl: ComputedRef<string>;
    linkCopied: Ref<boolean>;
    shareOn: (platform: 'twitter' | 'linkedin') => void;
    copyLink: () => Promise<void>;
}

// useTableOfContents

export interface TocItem {
    id: string;
    text: string;
    level: number;
}

// useLinkResolver

export interface UseLinkResolverOptions {
    to?: string | RouteObject;
    params?: Record<string, string | number>;
    target?: LinkTarget | '';
}

export interface UseLinkResolverReturn {
    isExternalLink: ComputedRef<boolean>;
    isInternalLink: ComputedRef<boolean>;
    linkProps: ComputedRef<Record<string, unknown>>;
    resolvedPath: ComputedRef<string>;
}

// useChartLifecycle

export interface UseChartLifecycleOptions<T extends ChartType = ChartType> {
    type: T;
    defaultOptions?: ChartOptions<T>;
}

export interface UseChartLifecycleReturn<T extends ChartType = ChartType> {
    chart: Ref<Chart<T> | null>;
    canvasRef: Ref<HTMLCanvasElement | null>;
    initChart: (data: ChartData<T>, options?: ChartOptions<T>) => Promise<boolean>;
    updateData: (data: ChartData<T>) => void;
    updateOptions: (options: ChartOptions<T>) => void;
    destroyChart: () => void;
    isInitialized: Ref<boolean>;
}

// useSwiper

export interface UseSwiperOptions {
    props: SwiperProps;
    emit: (event: 'change', index: number) => void;
    swiperRef: Readonly<Ref<HTMLElement | null>>;
}

// useDateRangePicker

export interface UseDateRangePickerOptions {
    model: Ref<DateRange>;
    availableDates: Ref<string[]>;
    minDays: Ref<number>;
    maxDays: Ref<number>;
    disabled: Ref<boolean>;
    dropdownRef: Readonly<Ref<HTMLElement | null>>;
}

// useDateRangeSelection

export interface UseDateRangeSelectionOptions {
    model: Ref<DateRange>;
    availableDates: Ref<string[]>;
    minDays: Ref<number>;
    maxDays: Ref<number>;
}

// useTypingEffect

export interface UseTypingEffectOptions {
    typeSpeed?: number;
    deleteSpeed?: number;
    pauseMs?: number;
    startDelay?: number;
    enabled?: Ref<boolean>;
}

export interface UseTypingEffectReturn {
    currentText: Ref<string>;
    isPaused: Ref<boolean>;
}

// useProgressTimer

export interface UseProgressTimerOptions {
    duration: number;
    onComplete?: () => void;
    autoStart?: boolean;
    stepTime?: number;
}

export interface UseProgressTimerReturn {
    progress: Ref<number>;
    isRunning: Ref<boolean>;
    remainingTime: Ref<number>;
    start: () => void;
    pause: () => void;
    resume: () => void;
    reset: () => void;
    stop: () => void;
}

// useDragScroll

export interface UseDragScrollOptions {
    inertia?: boolean;
    dragThreshold?: number;
}

// useCalendarGrid

export interface UseCalendarGridOptions {
    tempStartDate: Ref<string>;
    tempEndDate: Ref<string>;
    hoverDate: Ref<string>;
    isDateAvailable: (date: string) => boolean;
    isDateDisabled: (date: string) => boolean;
}

// useResponsive

export interface UseResponsiveOptions {
    initialBreakpoint?: Breakpoint;
}

export interface UseResponsiveReturn {
    windowWidth: Readonly<Ref<number>>;
    isMobile: Readonly<Ref<boolean>>;
    isTablet: Readonly<Ref<boolean>>;
    isDesktop: Readonly<Ref<boolean>>;
    currentBreakpoint: Readonly<Ref<Breakpoint>>;
    isBelow: (breakpoint: Breakpoint) => boolean;
    isAbove: (breakpoint: Breakpoint) => boolean;
}
