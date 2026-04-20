import { ref, computed, watch, onMounted, readonly } from 'vue';

import { STORAGE_KEYS } from '@/config/constants';

import { useResponsive } from './useResponsive';

import type { UseSidebarOptions, UseSidebarReturn } from '@/types/composables/ui';
import type { Router } from 'vue-router';

// SSR-safe: useRoute() auto-import unavailable at module scope, fall back to router current route.
const getRoute = () => (import.meta.client ? (useNuxtApp().$router as Router).currentRoute : ref({ path: '' }));

export function useSidebar(options: UseSidebarOptions = {}): UseSidebarReturn {
    const {
        storageKey = 'SIDEBAR_COLLAPSED',
        defaultCollapsed = false,
        closeOnRouteChange = true,
        classPrefix = 'layout',
    } = options;

    const route = getRoute();
    const { isBelow } = useResponsive();

    const isCollapsed = ref(defaultCollapsed);
    const isMobileOpen = ref(false);

    // DESKTOP breakpoint (1024px) aligns with SCSS responsive(tablet) max-width 1023px.
    const isMobileMode = computed(() => isBelow('DESKTOP'));
    const showOverlay = computed(() => isMobileMode.value && isMobileOpen.value);

    const layoutClasses = computed(() => ({
        [`${classPrefix}--collapsed`]: isCollapsed.value,
        [`${classPrefix}--mobile-open`]: isMobileOpen.value,
    }));

    const toggleMobile = () => {
        isMobileOpen.value = !isMobileOpen.value;
    };

    const toggleCollapsed = () => {
        isCollapsed.value = !isCollapsed.value;
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem(STORAGE_KEYS[storageKey], String(isCollapsed.value));
        }
    };

    const closeMobile = () => {
        isMobileOpen.value = false;
    };

    const openMobile = () => {
        isMobileOpen.value = true;
    };

    watch(isMobileMode, (mobile) => {
        if (!mobile) {
            isMobileOpen.value = false;
        }
    });

    watch(
        () => route.value.path,
        () => {
            if (closeOnRouteChange && isMobileMode.value) {
                isMobileOpen.value = false;
            }
        },
    );

    onMounted(() => {
        if (typeof localStorage !== 'undefined') {
            const savedState = localStorage.getItem(STORAGE_KEYS[storageKey]);
            if (savedState !== null) {
                isCollapsed.value = savedState === 'true';
            }
        }
    });

    return {
        isCollapsed,
        isMobileOpen,
        showOverlay: readonly(showOverlay),
        layoutClasses: readonly(layoutClasses),
        toggleMobile,
        toggleCollapsed,
        closeMobile,
        openMobile,
    };
}
