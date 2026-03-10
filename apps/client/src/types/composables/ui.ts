// Types pour les composables ui/

import type { ComputedRef, MaybeRefOrGetter, Ref } from 'vue';

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
    storageKey?: string;
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
