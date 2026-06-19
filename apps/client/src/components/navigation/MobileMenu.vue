<template>
    <ClientOnly>
        <Teleport to="body">
            <div :class="menuClasses" :aria-hidden="!isOpen">
                <Transition name="fade">
                    <div
                        v-if="isOpen"
                        class="mobile-menu__backdrop"
                        role="button"
                        tabindex="0"
                        aria-label="Fermer le menu"
                        @click="close"
                        @keydown.enter="close"
                        @keydown.space.prevent="close"
                    ></div>
                </Transition>

                <Transition name="slide">
                    <aside
                        v-show="isOpen"
                        ref="panelRef"
                        class="mobile-menu__panel"
                        role="dialog"
                        aria-modal="true"
                        aria-label="Menu de navigation"
                    >
                        <header class="mobile-menu__header">
                            <NuxtLink to="/" class="mobile-menu__logo" @click="close">
                                <AppLogo dark />
                                <span class="mobile-menu__logo-text">Menu</span>
                            </NuxtLink>
                            <button class="mobile-menu__close" aria-label="Fermer le menu" @click="close">
                                <BaseIcon name="x" :size="24" />
                            </button>
                        </header>

                        <nav class="mobile-menu__nav" aria-label="Navigation mobile">
                            <ul class="mobile-menu__list">
                                <li v-for="item in navigationItems" :key="item.path" class="mobile-menu__item">
                                    <NuxtLink
                                        :to="item.path"
                                        class="mobile-menu__link"
                                        :class="{ 'mobile-menu__link--active': isActiveRoute(item.path, route.path) }"
                                        :aria-current="isActiveRoute(item.path, route.path) ? 'page' : undefined"
                                        @click="close"
                                    >
                                        <span class="mobile-menu__link-icon">
                                            <BaseIcon :name="item.icon || 'circle'" :size="20" />
                                        </span>
                                        <span class="mobile-menu__link-text">{{ item.label }}</span>
                                        <BaseIcon name="chevron-right" :size="16" class="mobile-menu__link-arrow" />
                                    </NuxtLink>
                                </li>
                            </ul>
                        </nav>

                        <footer class="mobile-menu__footer">
                            <NuxtLink to="/contact" class="mobile-menu__cta" @click="close">
                                <BaseIcon name="mail" :size="18" />
                                <span>Me contacter</span>
                            </NuxtLink>
                        </footer>
                    </aside>
                </Transition>
            </div>
        </Teleport>
    </ClientOnly>
</template>

<script setup lang="ts">
    import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import AppLogo from '@/components/ui/AppLogo.vue';
    import { useEscapeKey, useResponsive } from '@/composables';
    import { isActiveRoute, navigationItems } from '@/config/navBar';

    import type { MobileMenuProps } from '@/types/components/navigation';

    const props = withDefaults(defineProps<MobileMenuProps>(), {
        isOpen: false,
        customClass: '',
    });

    const emit = defineEmits<{
        close: [];
        'update:isOpen': [value: boolean];
    }>();

    const panelRef = ref<HTMLElement | null>(null);
    const isMounted = ref(false);
    const route = useRoute();

    const menuClasses = computed(() => ['mobile-menu', { 'mobile-menu--open': props.isOpen }, props.customClass]);

    const close = () => {
        emit('close');
        emit('update:isOpen', false);
    };

    const handleClickOutside = (event: MouseEvent) => {
        if (!props.isOpen) {
            return;
        }

        const panel = panelRef.value;
        const toggle = document.querySelector('.mobile-menu-toggle');

        if (panel && !panel.contains(event.target as Node) && toggle && !toggle.contains(event.target as Node)) {
            close();
        }
    };

    // Escape key via composable (auto cleanup)
    useEscapeKey(() => {
        if (props.isOpen) {
            close();
        }
    });

    // Auto-close on desktop resize via composable (auto cleanup)
    const { isDesktop } = useResponsive();
    watch(isDesktop, (val) => {
        if (val && props.isOpen) {
            close();
        }
    });

    watch(
        () => props.isOpen,
        (newValue) => {
            if (!isMounted.value || !import.meta.client) {
                return;
            }

            if (newValue) {
                document.body.style.overflow = 'hidden';
                document.addEventListener('click', handleClickOutside);
            } else {
                document.body.style.overflow = '';
                document.removeEventListener('click', handleClickOutside);
            }
        },
    );

    onMounted(() => {
        isMounted.value = true;

        if (props.isOpen) {
            document.body.style.overflow = 'hidden';
            document.addEventListener('click', handleClickOutside);
        }
    });

    onBeforeUnmount(() => {
        if (import.meta.client) {
            document.removeEventListener('click', handleClickOutside);
            document.body.style.overflow = '';
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .mobile-menu {
        position: fixed;
        inset: 0;
        z-index: vars.$z-index-fixed;
        visibility: hidden;
        pointer-events: none;

        &--open {
            visibility: visible;
            pointer-events: auto;
        }

        // Backdrop
        &__backdrop {
            position: absolute;
            inset: 0;
            background: func.color-alpha(vars.$black, 0.6);
            backdrop-filter: blur(8px);
            cursor: pointer;
        }

        // Panel - Dark theme inspired by admin (slides from LEFT)
        &__panel {
            position: absolute;
            top: 0;
            left: 0;
            width: 85%;
            max-width: 320px;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: linear-gradient(180deg, #1e2330 0%, #171b26 100%);
            box-shadow:
                10px 0 40px func.color-alpha(vars.$black, 0.3),
                2px 0 10px func.color-alpha(vars.$black, 0.2);
        }

        // Header
        &__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: vars.$spacing-xxxxs vars.$spacing-lg;
            border-bottom: 1px solid func.color-alpha(vars.$white, 0.08);
            min-height: 70px;
        }

        &__logo {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            text-decoration: none;
            color: vars.$white;
            transition: opacity 0.2s ease;

            &:hover {
                opacity: 0.9;
            }
        }

        &__logo-text {
            font-weight: vars.$font-weight-bold;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, vars.$white, func.color-alpha(vars.$white, 0.7));
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        &__close {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            padding: 0;
            border-radius: vars.$border-radius-md;
            color: func.color-alpha(vars.$white, 0.7);
            background: func.color-alpha(vars.$white, 0.06);
            border: 1px solid func.color-alpha(vars.$white, 0.08);
            cursor: pointer;
            transition:
                background-color vars.$transition-base,
                color vars.$transition-base,
                transform vars.$transition-base;

            &:hover {
                background: func.color-alpha(vars.$white, 0.1);
                color: vars.$white;
                transform: rotate(90deg);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }

        // Navigation
        &__nav {
            flex: 1;
            overflow-y: auto;
            padding: vars.$spacing-lg;

            // Custom scrollbar
            &::-webkit-scrollbar {
                width: 4px;
            }

            &::-webkit-scrollbar-track {
                background: transparent;
            }

            &::-webkit-scrollbar-thumb {
                background: func.color-alpha(vars.$white, 0.1);
                border-radius: 2px;
            }
        }

        &__list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        &__item {
            margin-bottom: vars.$spacing-xxxs;
        }

        &__link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            color: func.color-alpha(vars.$white, 0.65);
            text-decoration: none;
            border-radius: vars.$border-radius-md;
            transition: all 0.2s ease;
            font-weight: vars.$font-weight-medium;

            &:hover {
                background: func.color-alpha(vars.$white, 0.08);
                color: vars.$white;

                .mobile-menu__link-arrow {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            &--active {
                background: func.color-alpha(vars.$primary-color, 0.15);
                color: vars.$white;

                .mobile-menu__link-icon {
                    color: vars.$primary-light;
                }

                .mobile-menu__link-arrow {
                    opacity: 1;
                    color: vars.$primary-light;
                }
            }
        }

        &__link-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            transition: color 0.2s ease;
        }

        &__link-text {
            flex: 1;
        }

        &__link-arrow {
            opacity: 0;
            transform: translateX(-4px);
            transition: all 0.2s ease;
            color: func.color-alpha(vars.$white, 0.4);
        }

        // Footer
        &__footer {
            padding: vars.$spacing-lg;
            border-top: 1px solid func.color-alpha(vars.$white, 0.06);
        }

        &__cta {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xxs;
            width: 100%;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            background: vars.$primary-color;
            color: vars.$white;
            text-decoration: none;
            border-radius: vars.$border-radius-md;
            font-weight: vars.$font-weight-semibold;
            transition: all 0.3s ease;

            &:hover {
                background: vars.$primary-dark;
                transform: translateY(-2px);
                box-shadow: 0 4px 16px func.color-alpha(vars.$primary-color, 0.3);
            }

            &:focus-visible {
                outline: 2px solid vars.$white;
                outline-offset: 2px;
            }
        }
    }

    // Transitions
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.3s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }

    .slide-enter-active,
    .slide-leave-active {
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .slide-enter-from,
    .slide-leave-to {
        transform: translateX(-100%);
    }
</style>
