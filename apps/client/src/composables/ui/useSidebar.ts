// src/composables/ui/useSidebar.ts
// Composable pour la gestion de la sidebar (partagé entre layouts)

import { ref, computed, watch, onMounted, readonly } from 'vue';

import { STORAGE_KEYS, type StorageKey } from '@/config/constants';

import { useResponsive } from './useResponsive';

import type { UseSidebarOptions as BaseSidebarOptions, UseSidebarReturn } from '@/types/composables/ui';
import type { Router } from 'vue-router';

// SSR-safe route access (useRoute() auto-imported by Nuxt is unavailable at module scope)
const getRoute = () => (import.meta.client ? (useNuxtApp().$router as Router).currentRoute : ref({ path: '' }));

// Extended options type using StorageKey from config
interface UseSidebarOptions extends Omit<BaseSidebarOptions, 'storageKey'> {
    storageKey?: StorageKey;
}

// Sidebar state and interactions
export function useSidebar(options: UseSidebarOptions = {}): UseSidebarReturn {
    const {
        storageKey = 'SIDEBAR_COLLAPSED',
        defaultCollapsed = false,
        closeOnRouteChange = true,
        classPrefix = 'layout',
    } = options;

    const route = getRoute();
    const { isBelow } = useResponsive();

    // État
    const isCollapsed = ref(defaultCollapsed);
    const isMobileOpen = ref(false);

    // Computed - Use DESKTOP breakpoint (1024px) to match CSS @include mix.responsive(tablet)
    // which triggers at max-width: 1023px
    const isMobileMode = computed(() => isBelow('DESKTOP'));
    const showOverlay = computed(() => isMobileMode.value && isMobileOpen.value);

    const layoutClasses = computed(() => ({
        [`${classPrefix}--collapsed`]: isCollapsed.value,
        [`${classPrefix}--mobile-open`]: isMobileOpen.value,
    }));

    // Méthodes
    const toggleMobile = () => {
        isMobileOpen.value = !isMobileOpen.value;
    };

    const toggleCollapsed = () => {
        isCollapsed.value = !isCollapsed.value;
        // Persister l'état
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

    // Fermer le menu mobile quand on passe en desktop
    watch(isMobileMode, (mobile) => {
        if (!mobile) {
            isMobileOpen.value = false;
        }
    });

    // Fermer le menu mobile lors du changement de route
    watch(
        () => route.value.path,
        () => {
            if (closeOnRouteChange && isMobileMode.value) {
                isMobileOpen.value = false;
            }
        },
    );

    // Charger l'état depuis localStorage au montage
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
