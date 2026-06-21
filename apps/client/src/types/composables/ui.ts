// Types pour les composables ui/

import type { Chart, ChartData, ChartOptions, ChartType } from 'chart.js';
import type { ComputedRef, MaybeRefOrGetter, Ref } from 'vue';
import type { Breakpoint, StorageKey } from '@/config/constants';
import type { LinkTarget, RouteObject } from '../components/base';
import type { DateRange, SwiperProps } from '../components/ui';

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

export interface TiltCSSOptions {
    maxRotation?: number;
    perspective?: number;
    scale?: number;
    smoothing?: number;
    resetOnLeave?: boolean;
}

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

export interface UseDropdownOptions {
    onOpen?: () => void;
    onClose?: () => void;
    closeOnSelect?: boolean;
    disabled?: Ref<boolean> | boolean;
    /** Sélecteurs CSS à ignorer par le click-outside (ex. un panneau téléporté hors du conteneur). */
    ignore?: string[];
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

export interface UseShareReturn {
    shareUrl: ComputedRef<string>;
    linkCopied: Ref<boolean>;
    shareOn: (platform: 'twitter' | 'linkedin') => void;
    copyLink: () => Promise<void>;
}

export interface TocItem {
    id: string;
    text: string;
    level: number;
}

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

export interface UseSwiperOptions {
    props: SwiperProps;
    emit: (event: 'change', index: number) => void;
    swiperRef: Readonly<Ref<HTMLElement | null>>;
}

export interface UseDateRangePickerOptions {
    model: Ref<DateRange>;
    availableDates: Ref<string[]>;
    minDays: Ref<number>;
    maxDays: Ref<number>;
    disabled: Ref<boolean>;
    dropdownRef: Readonly<Ref<HTMLElement | null>>;
}

export interface UseDateRangeSelectionOptions {
    model: Ref<DateRange>;
    availableDates: Ref<string[]>;
    minDays: Ref<number>;
    maxDays: Ref<number>;
}

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

export interface UseProgressTimerOptions {
    // Accepte un getter pour que la durée puisse être relue dynamiquement
    // (reset/start après changement de prop) au lieu d'être figée à la création.
    duration: number | (() => number);
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

export interface UseDragScrollOptions {
    inertia?: boolean;
    dragThreshold?: number;
}

export interface UseCalendarGridOptions {
    tempStartDate: Ref<string>;
    tempEndDate: Ref<string>;
    hoverDate: Ref<string>;
    isDateAvailable: (date: string) => boolean;
    isDateDisabled: (date: string) => boolean;
}

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
