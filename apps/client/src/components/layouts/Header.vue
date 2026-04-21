<template>
    <header class="header" role="banner">
        <nav class="header__nav" :class="{ 'header__nav--scrolled': isScrolled }" aria-label="Navigation principale">
            <div class="header__inner">
                <div class="header__left">
                    <NuxtLink to="/" class="header__logo" aria-label="Accueil">
                        <AppLogo size="md" />
                        <span class="header__logo-text">Juba Ait-adda</span>
                    </NuxtLink>
                </div>

                <div class="header__center">
                    <LazySearchGlobal placeholder="Rechercher..." mode="public" />
                </div>

                <div class="header__right">
                    <ul class="header__menu" role="menubar">
                        <NavbarItem
                            v-for="(item, index) in navigationItems"
                            :key="item.path"
                            :item="item"
                            :index="index"
                            :is-active="isActiveRoute(item.path, route.path)"
                        />
                    </ul>
                    <MobileMenuToggle :is-active="isMobileMenuOpen" class="header__toggle" @toggle="toggleMobileMenu" />
                </div>
            </div>
        </nav>

        <!-- Mobile Menu (slides from left, lazy-loaded on first open) -->
        <LazyMobileMenu v-if="mobileMenuMounted" :is-open="isMobileMenuOpen" @close="closeMobileMenu" />
    </header>
</template>

<script setup lang="ts">
    import { ref, watch } from 'vue';

    import MobileMenuToggle from '@/components/navigation/MobileMenuToggle.vue';
    import NavbarItem from '@/components/navigation/NavbarItem.vue';
    import AppLogo from '@/components/ui/AppLogo.vue';
    import { useEscapeKey } from '@/composables/accessibility/useEscapeKey';
    import { useHeaderScroll } from '@/composables/ui/useHeaderScroll';
    import { isActiveRoute, navigationItems } from '@/config/navBar';

    const isMobileMenuOpen = ref(false);
    const mobileMenuMounted = ref(false);
    const route = useRoute();

    const { isScrolled } = useHeaderScroll(20);

    useEscapeKey(() => {
        if (isMobileMenuOpen.value) {
            closeMobileMenu();
        }
    });

    const toggleMobileMenu = () => {
        if (!mobileMenuMounted.value) {
            mobileMenuMounted.value = true;
        }
        isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    const closeMobileMenu = () => {
        isMobileMenuOpen.value = false;
    };

    watch(() => route.path, closeMobileMenu);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: vars.$z-index-sticky;

        &__nav {
            width: 100%;
            background: func.color-alpha(vars.$white, 0.85);
            transition:
                background-color 0.3s ease,
                box-shadow 0.3s ease;

            &--scrolled {
                background: func.color-alpha(vars.$white, 0.9);
                backdrop-filter: blur(20px) saturate(1.2);
                box-shadow: 0 4px 24px func.color-alpha(vars.$black, 0.04);
            }
        }

        &__inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 75px;
            padding: 0 vars.$spacing-xl;
            max-width: 1400px;
            margin: 0 auto;
            gap: vars.$spacing-lg;

            @include mix.responsive(tablet) {
                padding: 0 vars.$spacing-xxxxs;
                gap: vars.$spacing-xxxxs;
            }

            @include mix.responsive(mobile) {
                padding: 0 vars.$spacing-xxxxs;
                gap: vars.$spacing-xxxxs;
            }
        }

        // Left section: Toggle + Logo
        &__left {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            flex-shrink: 0;
        }

        &__toggle {
            display: none;

            @include mix.responsive(tablet) {
                display: flex;
            }
        }

        &__logo {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            text-decoration: none;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                transform: scale(1.02);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 4px;
                border-radius: vars.$border-radius-md;
            }
        }

        &__logo-text {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            letter-spacing: -0.02em;

            @include mix.responsive(mobile) {
                display: none;
            }
        }

        // Center section: Search
        &__center {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            max-width: 400px;
            min-width: 0;
            min-height: 44px;

            @include mix.responsive(tablet) {
                max-width: 280px;
            }

            @include mix.responsive(mobile) {
                max-width: none;
                flex: 1;
            }

            :deep(.search-global) {
                width: 100%;
            }
        }

        // Right section: Desktop Nav
        &__right {
            display: flex;
            align-items: center;
            flex-shrink: 0;
        }

        &__menu {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
            list-style: none;
            margin: 0;
            padding: 0;

            @include mix.responsive(tablet) {
                display: none;
            }
        }
    }
</style>
