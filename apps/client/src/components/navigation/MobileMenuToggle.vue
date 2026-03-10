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
        <span class="mobile-menu-toggle__ripple" aria-hidden="true"></span>
    </button>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    interface Props {
        isActive?: boolean;
    }

    const props = withDefaults(defineProps<Props>(), {
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
        border-radius: vars.$border-radius-lg;
        cursor: pointer;
        z-index: vars.$z-index-modal;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

        // Glass effect
        background: func.color-alpha(vars.$white, 0.7);
        backdrop-filter: blur(12px) saturate(1.2);
        border: 1px solid func.color-alpha(vars.$gray-light, 0.3);
        box-shadow: 0 2px 8px func.color-alpha(vars.$black, 0.06);

        @include mix.responsive(tablet-up) {
            display: none;
        }

        &:hover {
            background: func.color-alpha(vars.$white, 0.85);
            border-color: func.color-alpha(vars.$primary-color, 0.15);
            box-shadow: 0 4px 16px func.color-alpha(vars.$primary-color, 0.1);

            .mobile-menu-toggle__line {
                background: vars.$primary-color;
            }
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }

        &:active {
            transform: scale(0.95);
            box-shadow: 0 1px 4px func.color-alpha(vars.$black, 0.08);

            .mobile-menu-toggle__ripple {
                transform: scale(2);
                opacity: 0;
            }
        }

        &--active {
            background: func.color-alpha(vars.$primary-color, 0.12);
            border-color: func.color-alpha(vars.$primary-color, 0.25);
            box-shadow: 0 4px 16px func.color-alpha(vars.$primary-color, 0.15);

            .mobile-menu-toggle__line {
                background: vars.$primary-color;

                &--top {
                    transform: translateY(6px) rotate(45deg);
                }

                &--middle {
                    opacity: 0;
                    transform: scaleX(0);
                }

                &--bottom {
                    transform: translateY(-6px) rotate(-45deg);
                }
            }
        }

        &__icon {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 14px;
            gap: 4px;
        }

        &__line {
            position: absolute;
            width: 100%;
            height: 2px;
            background: vars.$text-primary;
            border-radius: vars.$border-radius-full;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

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

        &__ripple {
            position: absolute;
            inset: 0;
            background: func.color-alpha(vars.$primary-color, 0.2);
            border-radius: inherit;
            transform: scale(0);
            opacity: 1;
            transition: all 0.4s ease;
            pointer-events: none;
        }
    }
</style>
