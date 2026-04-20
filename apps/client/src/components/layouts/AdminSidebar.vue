<template>
    <aside class="admin-sidebar" :class="sidebarClasses">
        <div class="admin-sidebar__logo">
            <NuxtLink to="/admin/dashboard" class="admin-sidebar__logo-link">
                <AppLogo :size="collapsed ? 'sm' : 'md'" dark />
                <Transition name="fade-slide">
                    <span v-if="!collapsed" class="admin-sidebar__logo-text">Admin</span>
                </Transition>
            </NuxtLink>
        </div>

        <nav class="admin-sidebar__nav" aria-label="Navigation principale">
            <ul class="admin-sidebar__menu" role="list">
                <li v-for="item in menuItems" :key="item.path" class="admin-sidebar__item">
                    <NuxtLink
                        :to="item.path"
                        class="admin-sidebar__link"
                        :class="{ 'admin-sidebar__link--active': isActive(item.path) }"
                        :title="collapsed ? item.label : undefined"
                        :aria-current="isActive(item.path) ? 'page' : undefined"
                    >
                        <span class="admin-sidebar__link-icon">
                            <BaseIcon :name="item.icon" :size="20" aria-hidden="true" />
                        </span>
                        <Transition name="fade-slide">
                            <span v-if="!collapsed" class="admin-sidebar__link-text">
                                {{ item.label }}
                            </span>
                        </Transition>
                        <small v-if="item.badge && !collapsed" class="admin-sidebar__badge">
                            {{ item.badge }}
                        </small>
                    </NuxtLink>
                </li>
            </ul>
        </nav>

        <div class="admin-sidebar__footer">
            <button
                type="button"
                class="admin-sidebar__footer-btn admin-sidebar__footer-btn--logout"
                :title="collapsed ? 'Deconnexion' : undefined"
                :disabled="isLoggingOut"
                @click="handleLogout"
            >
                <span class="admin-sidebar__link-icon">
                    <BaseIcon :name="isLoggingOut ? 'loader' : 'log-out'" :size="18" aria-hidden="true" />
                </span>
                <Transition name="fade-slide">
                    <span v-if="!collapsed" class="admin-sidebar__footer-text">
                        {{ isLoggingOut ? 'Deconnexion...' : 'Deconnexion' }}
                    </span>
                </Transition>
            </button>

            <a
                href="/"
                target="_blank"
                rel="noopener"
                class="admin-sidebar__footer-btn"
                :title="collapsed ? 'Voir le site' : undefined"
            >
                <span class="admin-sidebar__link-icon">
                    <BaseIcon name="external-link" :size="18" aria-hidden="true" />
                </span>
                <Transition name="fade-slide">
                    <span v-if="!collapsed" class="admin-sidebar__footer-text">Voir le site</span>
                </Transition>
            </a>
        </div>
    </aside>
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import AppLogo from '@/components/ui/AppLogo.vue';
    import { adminMenuItems, isMenuItemActive } from '@/config/adminNav';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { useLogout } from '@/services/api/modules/auth';

    import type { AdminSidebarProps } from '@/types/components/layouts';

    const props = withDefaults(defineProps<AdminSidebarProps>(), {
        mobileOpen: false,
        menuItems: () => [],
    });

    const route = useRoute();
    const logoutMutation = useLogout();

    const isLoggingOut = computed(() => logoutMutation.isPending.value);

    // All menu items including settings
    const menuItems = computed(() => {
        return props.menuItems?.length ? props.menuItems : adminMenuItems;
    });

    const sidebarClasses = computed(() => ({
        'admin-sidebar--collapsed': props.collapsed,
        'admin-sidebar--mobile-open': props.mobileOpen,
    }));

    const isActive = (path: string): boolean => {
        return isMenuItemActive(path, route.path);
    };

    const handleLogout = () => {
        if (isLoggingOut.value) {
            return;
        }

        logoutMutation.mutate(undefined, {
            onSettled: () => {
                navigateTo(ADMIN_ROUTES.LOGIN.path, { replace: true });
            },
        });
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .admin-sidebar {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: vars.$admin-sidebar-width;
        background: linear-gradient(180deg, #1a1f2e 0%, #151925 100%);
        color: vars.$white;
        display: flex;
        flex-direction: column;
        transition: width 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        z-index: vars.$z-index-fixed + 1;
        overflow: hidden;
        border-right: 1px solid func.color-alpha(vars.$white, 0.06);

        &--collapsed {
            width: vars.$admin-sidebar-collapsed;
        }

        // Logo
        &__logo {
            height: 75px;
            display: flex;
            align-items: center;
            padding: 0 vars.$spacing-md;
            border-bottom: 1px solid func.color-alpha(vars.$white, 0.08);
            flex-shrink: 0;
        }

        &__logo-link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            text-decoration: none;
            color: inherit;
            transition: opacity vars.$transition-fast;

            &:hover {
                opacity: 0.9;
            }
        }

        &__logo-text {
            font-weight: vars.$font-weight-bold;
            white-space: nowrap;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, vars.$white, func.color-alpha(vars.$white, 0.7));
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        // Navigation
        &__nav {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: vars.$spacing-lg 0;

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

        &__menu {
            list-style: none;
            padding: 0 vars.$spacing-xs;
            margin: 0;
        }

        &__item {
            margin-bottom: vars.$spacing-xxs;
        }

        &__link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            padding: vars.$spacing-xs vars.$spacing-sm;
            color: vars.$admin-sidebar-text-secondary;
            text-decoration: none;
            border-radius: vars.$border-radius-md;
            transition: all 0.2s ease;
            font-weight: vars.$font-weight-medium;

            &:hover {
                background-color: func.color-alpha(vars.$white, 0.08);
                color: vars.$white;
            }

            &--active {
                background: func.color-alpha(vars.$primary-color, 0.15);
                color: vars.$white;

                .admin-sidebar__link-icon {
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
            white-space: nowrap;
            overflow: hidden;
        }

        &__badge {
            margin-left: auto;
            padding: 2px vars.$spacing-xs;
            font-weight: vars.$font-weight-bold;
            background: vars.$primary-color;
            border-radius: vars.$border-radius-full;
        }

        // Footer
        &__footer {
            flex-shrink: 0;
            padding: vars.$spacing-xs vars.$spacing-xs vars.$spacing-md;
            border-top: 1px solid func.color-alpha(vars.$white, 0.06);
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxs;
        }

        &__footer-btn {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 8px 16px;
            color: rgba(255, 255, 255, 0.58);
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.2s ease;
            background: none;
            border: none;
            width: 100%;
            cursor: pointer;
            text-align: left;
            justify-content: flex-start;

            &:hover {
                background-color: func.color-alpha(vars.$white, 0.06);
                color: vars.$admin-sidebar-text-secondary;
            }

            &--logout {
                &:hover {
                    background-color: func.color-alpha(vars.$danger-color, 0.15);
                    color: vars.$danger-color;
                }
            }

            &:disabled {
                opacity: 0.6;
                cursor: not-allowed;

                .lucide-loader {
                    animation: spin 1s linear infinite;
                }
            }
        }

        &__footer-text {
            white-space: nowrap;
        }

        // Mobile
        @include mix.responsive(tablet) {
            transform: translateX(-100%);
            box-shadow: 4px 0 24px func.color-alpha(vars.$black, 0.3);

            &--mobile-open {
                transform: translateX(0);
            }
        }
    }

    // Transitions
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.2s ease;
    }

    .fade-slide-enter-from,
    .fade-slide-leave-to {
        opacity: 0;
        transform: translateX(-8px);
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
