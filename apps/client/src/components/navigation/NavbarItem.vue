<template>
    <li :class="itemClasses" role="none">
        <NuxtLink :to="item.path" :class="linkClasses" :aria-current="isActive ? 'page' : undefined" role="menuitem">
            <span v-if="item.icon" class="navbar-item__icon" aria-hidden="true">
                <BaseIcon :name="item.icon" :size="16" />
            </span>
            <span class="navbar-item__label">{{ item.label }}</span>
            <span v-if="item.children" class="navbar-item__arrow" aria-hidden="true">
                <BaseIcon name="chevron-down" :size="12" />
            </span>
        </NuxtLink>
    </li>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { NavbarItemProps } from '@/types/components/navigation';

    type Props = NavbarItemProps;

    const props = defineProps<Props>();

    const itemClasses = computed(() => [
        'navbar-item',
        {
            'navbar-item--active': props.isActive,
            'navbar-item--has-children': props.item.children,
        },
    ]);

    const linkClasses = computed(() => [
        'navbar-item__link',
        {
            'navbar-item__link--active': props.isActive,
        },
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .navbar-item {
        position: relative;
        list-style: none;

        &__link {
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            font-weight: 500;
            color: vars.$text-secondary;
            text-decoration: none;
            border-radius: vars.$border-radius-lg;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            overflow: hidden;

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                background: transparent;
                border-radius: inherit;
                border: 1px solid transparent;
                transition: all 0.3s ease;
                z-index: -1;
            }

            &:hover {
                color: vars.$primary-color;
                transform: translateY(-2px);

                &::before {
                    background: func.color-alpha(vars.$primary-color, 0.06);
                    border-color: func.color-alpha(vars.$primary-color, 0.1);
                }

                .navbar-item__arrow {
                    transform: rotate(180deg);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &:active {
                transform: translateY(-1px) scale(0.98);
            }

            &--active {
                color: vars.$primary-color;
                font-weight: 600;

                &::before {
                    background: func.color-alpha(vars.$primary-color, 0.08);
                    border-color: func.color-alpha(vars.$primary-color, 0.12);
                }
            }
        }

        &__icon {
            @include mix.flex-center;

            color: inherit;
            transition: transform 0.3s ease;

            .navbar-item__link:hover & {
                transform: scale(1.1);
            }
        }

        &__label {
            white-space: nowrap;
        }

        &__arrow {
            @include mix.flex-center;

            margin-left: vars.$spacing-xxxxs;
            opacity: 0.5;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        &__indicator {
            position: absolute;
            bottom: 6px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 2px;
            background: func.color-alpha(vars.$primary-color, 0.6);
            border-radius: vars.$border-radius-full;
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        &--has-children {
            .navbar-item__link {
                padding-right: vars.$spacing-xs;
            }
        }
    }
</style>
