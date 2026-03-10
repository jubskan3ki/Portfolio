<template>
    <div class="admin-layout" :class="layoutClasses">
        <!-- Background effects -->
        <div class="admin-layout__bg" aria-hidden="true">
            <div class="admin-layout__dots"></div>
            <div class="admin-layout__glow admin-layout__glow--1"></div>
            <div class="admin-layout__glow admin-layout__glow--2"></div>
        </div>

        <!-- Mobile overlay (behind sidebar, above content) -->
        <Transition name="fade">
            <div
                v-if="showMobileOverlay"
                class="admin-layout__overlay"
                role="button"
                tabindex="0"
                aria-label="Fermer le menu"
                @click="closeMobileSidebar"
                @keydown.enter="closeMobileSidebar"
                @keydown.escape="closeMobileSidebar"
            ></div>
        </Transition>

        <!-- Sidebar -->
        <AdminSidebar id="admin-navigation" :collapsed="sidebarCollapsed" :mobile-open="mobileMenuOpen" />

        <!-- Main content area -->
        <div class="admin-layout__content">
            <!-- Header -->
            <AdminHeader
                :collapsed="sidebarCollapsed"
                @toggle-sidebar="toggleMobileSidebar"
                @toggle-collapse="toggleSidebarCollapse"
            />

            <!-- Main -->
            <main id="main-content" class="admin-layout__main">
                <div class="admin-layout__container">
                    <AdminBreadcrumb v-if="showBreadcrumb" />
                    <ErrorBoundary
                        title="Une erreur est survenue"
                        fallback-message="Une erreur inattendue s'est produite. Veuillez recharger la page."
                        :show-home-button="false"
                        show-details
                        @retry="handleErrorRetry"
                    >
                        <slot></slot>
                    </ErrorBoundary>
                </div>
            </main>
        </div>

        <!-- Alerts & Modals -->
        <AlertList position="top-right" />
        <Modal />
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import AlertList from '@/components/feedback/AlertList.vue';
    import ErrorBoundary from '@/components/feedback/ErrorBoundary.vue';
    import Modal from '@/components/feedback/Modal.vue';
    import AdminBreadcrumb from '@/components/layouts/AdminBreadcrumb.vue';
    import AdminHeader from '@/components/layouts/AdminHeader.vue';
    import AdminSidebar from '@/components/layouts/AdminSidebar.vue';
    import { useSidebar } from '@/composables';
    import { ADMIN_ROUTES } from '@/config/routes';

    const route = useRoute();

    // Sidebar management (handles mobile, collapse, localStorage, route change)
    const {
        isCollapsed: sidebarCollapsed,
        isMobileOpen: mobileMenuOpen,
        showOverlay: showMobileOverlay,
        layoutClasses,
        toggleMobile: toggleMobileSidebar,
        toggleCollapsed: toggleSidebarCollapse,
        closeMobile: closeMobileSidebar,
    } = useSidebar({
        storageKey: 'ADMIN_SIDEBAR_COLLAPSED',
        classPrefix: 'admin-layout',
    });

    // Computed
    const showBreadcrumb = computed(() => {
        return route.path !== ADMIN_ROUTES.BASE.path && route.path !== ADMIN_ROUTES.DASHBOARD.path;
    });

    // Methods
    const handleErrorRetry = async () => {
        // Use navigateTo instead of window.location.reload() for bfcache compatibility
        await navigateTo(route.fullPath, { replace: true, external: false });
    };
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/effects/layout-bg' as bg;

    .admin-layout {
        display: flex;
        min-height: 100vh;
        position: relative;
        background-color: vars.$admin-bg;
        width: 100%;
        max-width: 100vw;

        /* Background layer */
        &__bg {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }

        /* Dots pattern */
        &__dots {
            position: absolute;
            inset: -20%;

            @include mix.dots-pattern(func.color-alpha(vars.$primary-color, 0.03), 2px, 32px);

            animation: dots-drift 120s linear infinite;
        }

        /* Glow effects */
        &__glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.4;

            &--1 {
                top: -10%;
                right: -5%;
                width: 40%;
                height: 40%;
                background: radial-gradient(circle, func.color-alpha(vars.$primary-color, 0.15) 0%, transparent 70%);
                animation: glow-float 20s ease-in-out infinite;
            }

            &--2 {
                bottom: -10%;
                left: -5%;
                width: 35%;
                height: 35%;
                background: radial-gradient(circle, func.color-alpha(vars.$secondary-color, 0.1) 0%, transparent 70%);
                animation: glow-float 25s ease-in-out infinite reverse;
            }
        }

        /* Overlay - z-index between content and sidebar */
        &__overlay {
            position: fixed;
            inset: 0;
            background: func.color-alpha(vars.$black, 0.5);
            backdrop-filter: blur(4px);
            z-index: vars.$z-index-fixed;
            cursor: pointer;
        }

        /* Content area */
        &__content {
            flex: 1;
            margin-left: vars.$admin-sidebar-width;
            transition: margin-left vars.$admin-transition;
            display: flex;
            flex-direction: column;
            min-width: 0;
            position: relative;
            z-index: 1;
        }

        &--collapsed &__content {
            margin-left: vars.$admin-sidebar-collapsed;
        }

        /* Main content */
        &__main {
            flex: 1;
            margin-top: vars.$admin-header-height;
            overflow-x: hidden;
        }

        &__container {
            max-width: 1600px;
            margin: 0 auto;
            padding: vars.$spacing-xl;
            animation: page-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1);

            @include mix.responsive(tablet) {
                padding: vars.$spacing-lg;
            }

            @include mix.responsive(mobile) {
                padding: vars.$spacing-md;
            }
        }

        /* Mobile/Tablet adjustments */
        @include mix.responsive(tablet) {
            &__content {
                margin-left: 0;
                width: 100%;
            }

            &--collapsed &__content {
                margin-left: 0;
            }
        }
    }

    /* Animations */
    @include bg.glow-float-keyframes(20px, -20px, 1.1);

    @keyframes page-enter {
        from {
            opacity: 0;
            transform: translateY(10px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Transitions */
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.3s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
