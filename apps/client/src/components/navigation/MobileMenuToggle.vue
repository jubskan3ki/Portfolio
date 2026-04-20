<template>
    <button
        :class="toggleClasses"
        :aria-label="isActive ? 'Fermer le menu de navigation' : 'Ouvrir le menu de navigation'"
        :aria-expanded="isActive"
        aria-controls="mobile-menu"
        @click="emit('toggle')"
    >
        <span class="mobile-menu-toggle__icon" aria-hidden="true">
            <span class="mobile-menu-toggle__line mobile-menu-toggle__line--top"></span>
            <span class="mobile-menu-toggle__line mobile-menu-toggle__line--middle"></span>
            <span class="mobile-menu-toggle__line mobile-menu-toggle__line--bottom"></span>
        </span>
    </button>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { MobileMenuToggleProps } from '@/types/components/navigation';

    const props = withDefaults(defineProps<MobileMenuToggleProps>(), {
        isActive: false,
    });

    const emit = defineEmits<{
        toggle: [];
    }>();

    const toggleClasses = computed(() => ['mobile-menu-toggle', { 'mobile-menu-toggle--active': props.isActive }]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .mobile-menu-toggle {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        padding: 0;
        border: 0;
        background: transparent;
        color: vars.$text-primary;
        cursor: pointer;
        z-index: vars.$z-index-modal;

        @include mix.responsive(tablet-up) {
            display: none;
        }

        &,
        &:hover,
        &:focus,
        &:active,
        &:hover:not(:disabled),
        &.mobile-menu-toggle--active,
        &.mobile-menu-toggle--active:hover {
            background: transparent;
            background-color: transparent;
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
            border-radius: vars.$border-radius-md;
        }

        &__icon {
            position: relative;
            display: block;
            width: vars.$spacing-md;
            height: 14px;
            transition: transform vars.$transition-base;
        }

        &:hover &__icon {
            transform: rotate(15deg);
        }

        &:active &__icon {
            transform: rotate(15deg) scale(0.9);
        }

        &--active &__icon,
        &--active:hover &__icon {
            transform: rotate(90deg);
        }

        &--active:active &__icon {
            transform: rotate(90deg) scale(0.9);
        }

        &__line {
            position: absolute;
            left: 0;
            width: 100%;
            height: vars.$spacing-xxxxs;
            background-color: currentcolor;
            border-radius: vars.$border-radius-full;

            &--top {
                top: 0;
            }

            &--middle {
                top: 50%;
                transform: translateY(-50%);
            }

            &--bottom {
                bottom: 0;
            }
        }
    }
</style>
