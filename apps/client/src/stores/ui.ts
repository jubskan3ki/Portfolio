// Store unifié pour l'UI (navigation, scroll, menus)

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

import { SCROLL_THRESHOLDS } from '@/config/constants';
import { lockBodyOverflow, unlockBodyOverflow } from '@/services/utils/dom';

export const useUiStore = defineStore('ui', () => {
    // === État du menu mobile ===
    const isMobileMenuOpen = ref(false);
    const expandedSubmenuIndex = ref<number | null>(null);

    // === État du scroll ===
    const scrollY = ref(0);
    const lastScrollY = ref(0);
    const isScrolled = computed(() => scrollY.value > SCROLL_THRESHOLDS.IS_SCROLLED);
    const isScrollingUp = ref(false);

    // === Actions Menu Mobile ===
    const openMobileMenu = () => {
        isMobileMenuOpen.value = true;
        lockBodyOverflow();
    };

    const closeMobileMenu = () => {
        isMobileMenuOpen.value = false;
        expandedSubmenuIndex.value = null;
        unlockBodyOverflow();
    };

    const toggleMobileMenu = () => {
        isMobileMenuOpen.value ? closeMobileMenu() : openMobileMenu();
    };

    // === Actions Sous-menus ===
    const expandSubmenu = (index: number) => {
        expandedSubmenuIndex.value = index;
    };

    const collapseSubmenu = () => {
        expandedSubmenuIndex.value = null;
    };

    const toggleSubmenu = (index: number) => {
        expandedSubmenuIndex.value === index ? collapseSubmenu() : expandSubmenu(index);
    };

    // === Actions Scroll ===
    const updateScroll = (y: number) => {
        isScrollingUp.value = y < lastScrollY.value;
        lastScrollY.value = scrollY.value;
        scrollY.value = y;
    };

    const scrollToTop = () => {
        if (import.meta.client) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    };

    return {
        // État
        isMobileMenuOpen,
        expandedSubmenuIndex,
        scrollY,
        isScrolled,
        isScrollingUp,

        // Actions Menu Mobile
        openMobileMenu,
        closeMobileMenu,
        toggleMobileMenu,

        // Actions Sous-menus
        expandSubmenu,
        collapseSubmenu,
        toggleSubmenu,

        // Actions Scroll
        updateScroll,
        scrollToTop,
    };
});
