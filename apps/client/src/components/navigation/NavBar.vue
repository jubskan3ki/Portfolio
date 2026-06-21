<template>
    <nav :class="navbarClasses" :aria-label="ariaLabel" role="navigation">
        <div class="navbar__inner">
            <div class="navbar__container">
                <div class="navbar__logo">
                    <slot name="logo">
                        <AppLogo />
                    </slot>
                </div>

                <ul class="navbar__nav" role="menubar">
                    <NavbarItem
                        v-for="item in navigationItems"
                        :key="item.path"
                        :item="item"
                        :is-active="isActiveRoute(item.path, route.path)"
                    />
                </ul>

                <div class="navbar__actions">
                    <slot name="actions"></slot>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';
    import { useRoute } from 'vue-router';

    import NavbarItem from '@/components/navigation/NavbarItem.vue';
    import AppLogo from '@/components/ui/AppLogo.vue';
    import { useScrollListener } from '@/composables';
    import { isActiveRoute, navigationItems } from '@/config/navBar';

    import type { NavBarProps } from '@/types/components/navigation';

    const props = withDefaults(defineProps<NavBarProps>(), {
        sticky: false,
        transparent: false,
        elevated: false,
        ariaLabel: 'Navigation principale',
        customClass: '',
    });

    const route = useRoute();
    const isScrolled = ref(false);
    let ticking = false;

    const navbarClasses = computed(() => [
        'navbar',
        {
            'navbar--sticky': props.sticky,
            'navbar--scrolled': isScrolled.value,
            'navbar--transparent': props.transparent && !isScrolled.value,
            'navbar--elevated': props.elevated,
        },
        props.customClass,
    ]);

    const handleScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                isScrolled.value = window.scrollY > 20;
                ticking = false;
            });
            ticking = true;
        }
    };

    // Auto-managed scroll listener with cleanup (passive: true by default)
    useScrollListener(handleScroll);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .navbar {
        position: relative;
        width: 100%;
        z-index: vars.$z-index-sticky;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);

        &__inner {
            width: 100%;
            padding: 0 vars.$spacing-xl;

            @include mix.responsive(mobile) {
                padding: 0 vars.$spacing-xxxxs;
            }
        }

        &__container {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: vars.$navbar-height;
            transition: height 0.4s cubic-bezier(0.16, 1, 0.3, 1);

            @include mix.responsive(mobile) {
                height: vars.$navbar-height-mobile;
            }
        }

        &__logo {
            position: relative;
            display: flex;
            align-items: center;
            flex-shrink: 0;
            z-index: 2;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                transform: translateY(-2px) scale(1.02);
            }
        }

        &__nav {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            list-style: none;
            margin: 0;
            padding: 0;

            @include mix.responsive(tablet) {
                display: none;
            }
        }

        &__actions {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin-left: vars.$spacing-md;

            @include mix.responsive(tablet) {
                margin-left: auto;
            }
        }

        // States
        &--sticky {
            position: fixed;
            top: 0;
            left: 0;
        }

        &--scrolled {
            background: func.color-alpha(vars.$white, 0.75);
            backdrop-filter: blur(20px) saturate(1.2);
            border-bottom: 1px solid func.color-alpha(vars.$primary-color, 0.06);
            box-shadow:
                0 4px 30px func.color-alpha(vars.$black, 0.04),
                0 1px 2px func.color-alpha(vars.$black, 0.02);

            .navbar__container {
                height: calc(vars.$navbar-height - 10px);

                @include mix.responsive(mobile) {
                    height: calc(vars.$navbar-height-mobile - 5px);
                }
            }
        }

        &--transparent:not(&--scrolled) {
            background: transparent;
        }

        &--elevated {
            box-shadow: vars.$box-shadow-medium;
        }
    }
</style>
