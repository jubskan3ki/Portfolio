<template>
    <li class="mobile-menu-item" role="none">
        <div class="mobile-menu-item__wrapper">
            <NuxtLink
                :to="item.path"
                :class="linkClasses"
                :aria-current="isActive ? 'page' : undefined"
                role="menuitem"
                @click="closeMenu"
            >
                <span class="mobile-menu-item__indicator" aria-hidden="true"></span>
                <span v-if="item.icon" class="mobile-menu-item__icon" aria-hidden="true">
                    <BaseIcon :name="item.icon" :size="20" />
                </span>
                <span class="mobile-menu-item__text">{{ item.label }}</span>
            </NuxtLink>

            <button
                v-if="hasChildren"
                :class="toggleClasses"
                :aria-expanded="isExpanded"
                :aria-controls="`submenu-${index}`"
                :aria-label="isExpanded ? 'Réduire le sous-menu' : 'Développer le sous-menu'"
                @click="toggleSubmenu"
            >
                <BaseIcon name="chevron-down" :size="16" />
            </button>
        </div>

        <Transition name="submenu">
            <ul v-if="hasChildren && isExpanded" :id="`submenu-${index}`" class="mobile-menu-item__submenu" role="menu">
                <li
                    v-for="subItem in item.children"
                    :key="subItem.path"
                    class="mobile-menu-item__submenu-item"
                    role="none"
                >
                    <NuxtLink
                        :to="subItem.path"
                        :class="getSubmenuLinkClasses(subItem.path)"
                        :aria-current="isSubItemActive(subItem.path) ? 'page' : undefined"
                        role="menuitem"
                        @click="closeMenu"
                    >
                        <span v-if="subItem.icon" class="mobile-menu-item__submenu-icon" aria-hidden="true">
                            <BaseIcon :name="subItem.icon" :size="16" />
                        </span>
                        <span>{{ subItem.label }}</span>
                    </NuxtLink>
                </li>
            </ul>
        </Transition>
    </li>
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { isActiveRoute } from '@/config/navBar';
    import { useUiStore } from '@/stores/ui';

    import type { MobileMenuItemProps } from '@/types/components/navigation';

    const props = defineProps<MobileMenuItemProps>();

    const route = useRoute();
    const navStore = useUiStore();

    const hasChildren = computed(() => props.item.children && props.item.children.length > 0);
    const isActive = computed(() => isActiveRoute(props.item.path, route.path));
    const isExpanded = computed(() => navStore.expandedSubmenuIndex === props.index);

    const linkClasses = computed(() => [
        'mobile-menu-item__link',
        {
            'mobile-menu-item__link--active': isActive.value,
            'mobile-menu-item__link--has-children': hasChildren.value,
        },
    ]);

    const toggleClasses = computed(() => [
        'mobile-menu-item__toggle',
        { 'mobile-menu-item__toggle--expanded': isExpanded.value },
    ]);

    const getSubmenuLinkClasses = (path: string) => [
        'mobile-menu-item__submenu-link',
        { 'mobile-menu-item__submenu-link--active': isSubItemActive(path) },
    ];

    const closeMenu = () => {
        navStore.closeMobileMenu();
    };

    const toggleSubmenu = () => {
        navStore.toggleSubmenu(props.index);
    };

    const isSubItemActive = (path: string) => {
        return isActiveRoute(path, route.path);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .mobile-menu-item {
        position: relative;
        display: flex;
        flex-direction: column;
        width: 100%;

        &__wrapper {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
        }

        &__link {
            position: relative;
            flex: 1;
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            color: vars.$text-primary;
            font-weight: 500;
            text-decoration: none;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                background: func.color-alpha(vars.$gray-light, 0.5);
                transform: translateX(4px);

                .mobile-menu-item__icon {
                    transform: scale(1.1);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--active {
                color: vars.$primary-color;
                background: func.color-alpha(vars.$primary-color, 0.1);

                .mobile-menu-item__indicator {
                    transform: scaleY(1);
                }

                &:hover {
                    background: func.color-alpha(vars.$primary-color, 0.15);
                }
            }
        }

        &__indicator {
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%) scaleY(0);
            width: 3px;
            height: 60%;
            background: vars.$primary-color;
            border-radius: 0 vars.$border-radius-full vars.$border-radius-full 0;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: inherit;
            transition: transform 0.3s ease;
        }

        &__text {
            flex: 1;
        }

        &__toggle {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: vars.$border-radius-full;
            color: vars.$text-secondary;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                background: func.color-alpha(vars.$gray-light, 0.5);
                color: vars.$primary-color;
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--expanded {
                background: func.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;
                transform: rotate(180deg);
            }
        }

        &__submenu {
            list-style: none;
            margin: vars.$spacing-xxs 0;
            padding: 0 0 0 vars.$spacing-xl;
            border-left: 2px solid func.color-alpha(vars.$gray-light, 0.5);
            margin-left: vars.$spacing-lg;
        }

        &__submenu-item {
            &:not(:last-child) {
                margin-bottom: vars.$spacing-xxxs;
            }
        }

        &__submenu-link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            border-radius: vars.$border-radius-md;
            color: vars.$text-secondary;
            text-decoration: none;
            transition: all 0.2s ease;

            &:hover {
                background: func.color-alpha(vars.$gray-light, 0.4);
                color: vars.$text-primary;
                transform: translateX(2px);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--active {
                color: vars.$primary-color;
                font-weight: 500;
                background: func.color-alpha(vars.$primary-color, 0.08);
            }
        }

        &__submenu-icon {
            display: flex;
            align-items: center;
            opacity: 0.7;
        }
    }

    // Submenu transition
    .submenu-enter-active,
    .submenu-leave-active {
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        overflow: hidden;
    }

    .submenu-enter-from,
    .submenu-leave-to {
        opacity: 0;
        max-height: 0;
        transform: translateY(-10px);
    }

    .submenu-enter-to,
    .submenu-leave-from {
        opacity: 1;
        max-height: 500px;
        transform: translateY(0);
    }
</style>
