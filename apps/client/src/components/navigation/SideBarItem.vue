<template>
    <li class="sidebar-item" role="none">
        <NuxtLink
            :to="to"
            :class="linkClasses"
            :title="isCollapsed ? text : undefined"
            :aria-current="isActive ? 'page' : undefined"
            role="menuitem"
        >
            <span class="sidebar-item__indicator" aria-hidden="true"></span>

            <span v-if="icon" class="sidebar-item__icon" aria-hidden="true">
                <BaseIcon :name="icon" :size="20" />
            </span>

            <Transition name="fade">
                <span v-if="!isCollapsed" class="sidebar-item__text">{{ text }}</span>
            </Transition>

            <span
                v-if="badge && !isCollapsed"
                :class="badgeClasses"
                :aria-label="`${badge.value || ''} ${badge.type || 'notification'}`"
            >
                <template v-if="badge.value">{{ badge.value }}</template>
                <span v-else class="sidebar-item__badge-dot"></span>
            </span>

            <Tooltip v-if="isCollapsed" :content="text" position="right">
                <span class="sidebar-item__tooltip-trigger"></span>
            </Tooltip>
        </NuxtLink>
    </li>
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Tooltip from '@/components/ui/Tooltip.vue';

    import type { SideBarItemProps } from '@/types/components/navigation';

    const props = withDefaults(defineProps<SideBarItemProps>(), {
        icon: '',
        badge: undefined,
        isCollapsed: false,
    });

    const route = useRoute();

    const isActive = computed(() => {
        if (props.to === '/' && route.path === '/') {
            return true;
        }
        return props.to !== '/' && route.path.startsWith(props.to);
    });

    const linkClasses = computed(() => [
        'sidebar-item__link',
        {
            'sidebar-item__link--active': isActive.value,
            'sidebar-item__link--collapsed': props.isCollapsed,
        },
    ]);

    const badgeClasses = computed(() => ['sidebar-item__badge', `sidebar-item__badge--${props.badge?.type || 'info'}`]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .sidebar-item {
        margin: 0 vars.$spacing-xs;
        list-style: none;

        &__link {
            position: relative;
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            color: vars.$text-secondary;
            text-decoration: none;
            font-weight: 500;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover {
                background: func.color-alpha(vars.$gray-light, 0.5);
                color: vars.$text-primary;
                transform: translateX(2px);

                .sidebar-item__icon {
                    transform: scale(1.1);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--active {
                background: func.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;

                .sidebar-item__indicator {
                    transform: scaleY(1);
                }

                .sidebar-item__icon {
                    color: vars.$primary-color;
                }

                &:hover {
                    background: func.color-alpha(vars.$primary-color, 0.15);
                }
            }

            &--collapsed {
                justify-content: center;
                padding: vars.$spacing-xs;

                .sidebar-item__icon {
                    margin: 0;
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
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            transition: all 0.3s ease;
        }

        &__text {
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 20px;
            height: 20px;
            padding: 0 vars.$spacing-xxs;
            border-radius: vars.$border-radius-full;
            font-weight: 600;
            line-height: 1;

            &--info {
                background: func.color-alpha(vars.$info-color, 0.15);
                color: vars.$info-color;
            }

            &--success {
                background: func.color-alpha(vars.$success-color, 0.15);
                color: vars.$success-color;
            }

            &--warning {
                background: func.color-alpha(vars.$warning-color, 0.15);
                color: vars.$warning-dark;
            }

            &--danger {
                background: func.color-alpha(vars.$danger-color, 0.15);
                color: vars.$danger-color;
            }
        }

        &__badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentcolor;
            animation: pulse 2s ease-in-out infinite;
        }

        &__tooltip-trigger {
            position: absolute;
            inset: 0;
        }
    }

    // Fade transition
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: 0.6;
            transform: scale(0.9);
        }
    }
</style>
