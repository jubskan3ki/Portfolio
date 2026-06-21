<template>
    <div
        class="tooltip"
        :class="[customClass]"
        @mouseenter="show"
        @mouseleave="hide"
        @focus="show"
        @blur="hide"
    >
        <div ref="triggerRef" class="tooltip__trigger">
            <slot></slot>
        </div>

        <Teleport to="body">
            <Transition name="tooltip">
                <div
                    v-if="isVisible"
                    :id="tooltipId"
                    ref="tooltipRef"
                    class="tooltip__content"
                    :class="[`tooltip__content--${position}`, `tooltip__content--${variant}`]"
                    :style="tooltipStyle"
                    role="tooltip"
                >
                    <div class="tooltip__arrow"></div>
                    <div class="tooltip__body">
                        <slot name="content">{{ content }}</slot>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup lang="ts">
    import { useThrottleFn } from '@vueuse/core';
    import { nextTick, onBeforeUnmount, onMounted, ref, useId, watch } from 'vue';

    import type { TooltipProps } from '@/types/components/ui';

    type Props = TooltipProps;

    const props = withDefaults(defineProps<Props>(), {
        content: '',
        position: 'top',
        trigger: 'hover',
        delay: 200,
        variant: 'dark',
        offset: 10,
        customClass: '',
    });

    const tooltipId = `tooltip-${useId()}`;

    const isVisible = ref(false);
    const triggerRef = ref<HTMLElement | null>(null);
    const tooltipRef = ref<HTMLElement | null>(null);
    const tooltipStyle = ref({
        top: '0px',
        left: '0px',
    });

    let showTimer: ReturnType<typeof setTimeout> | null = null;
    let hideTimer: ReturnType<typeof setTimeout> | null = null;

    const show = () => {
        if (props.trigger !== 'hover') {
            return;
        }

        if (hideTimer) {
            clearTimeout(hideTimer);
        }

        showTimer = setTimeout(() => {
            isVisible.value = true;
            nextTick(() => updatePosition());
        }, props.delay);
    };

    const hide = () => {
        if (props.trigger !== 'hover') {
            return;
        }

        if (showTimer) {
            clearTimeout(showTimer);
        }

        hideTimer = setTimeout(() => {
            isVisible.value = false;
        }, props.delay);
    };

    const toggle = () => {
        isVisible.value = !isVisible.value;
        if (isVisible.value) {
            nextTick(() => updatePosition());
        }
    };

    const updatePosition = () => {
        if (!triggerRef.value || !tooltipRef.value) {
            return;
        }

        const triggerRect = triggerRef.value.getBoundingClientRect();
        const tooltipRect = tooltipRef.value.getBoundingClientRect();

        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

        let top = 0;
        let left = 0;

        switch (props.position) {
            case 'top':
                top = triggerRect.top + scrollTop - tooltipRect.height - props.offset;
                left = triggerRect.left + scrollLeft + triggerRect.width / 2 - tooltipRect.width / 2;
                break;
            case 'bottom':
                top = triggerRect.bottom + scrollTop + props.offset;
                left = triggerRect.left + scrollLeft + triggerRect.width / 2 - tooltipRect.width / 2;
                break;
            case 'left':
                top = triggerRect.top + scrollTop + triggerRect.height / 2 - tooltipRect.height / 2;
                left = triggerRect.left + scrollLeft - tooltipRect.width - props.offset;
                break;
            case 'right':
                top = triggerRect.top + scrollTop + triggerRect.height / 2 - tooltipRect.height / 2;
                left = triggerRect.right + scrollLeft + props.offset;
                break;
        }

        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        left = Math.max(props.offset, Math.min(left, viewportWidth - tooltipRect.width - props.offset));
        top = Math.max(props.offset, Math.min(top, viewportHeight + scrollTop - tooltipRect.height - props.offset));

        tooltipStyle.value = {
            top: `${top}px`,
            left: `${left}px`,
        };
    };

    const handleClickTrigger = (event: MouseEvent) => {
        if (props.trigger !== 'click') {
            return;
        }

        const target = event.target as Node;
        const targetIsTrigger = triggerRef.value?.contains(target);

        if (targetIsTrigger) {
            toggle();
            event.stopPropagation();
        }
    };

    const handleClickOutside = (event: MouseEvent) => {
        if (!isVisible.value) {
            return;
        }

        const target = event.target as Node;
        const clickedOutside = !tooltipRef.value?.contains(target) && !triggerRef.value?.contains(target);

        if (clickedOutside) {
            isVisible.value = false;
        }
    };

    const handleResize = useThrottleFn(() => {
        if (isVisible.value) {
            updatePosition();
        }
    }, 16);

    const handleScroll = useThrottleFn(() => {
        if (isVisible.value) {
            updatePosition();
        }
    }, 16);

    let repositionListenersAttached = false;

    const attachRepositionListeners = () => {
        if (repositionListenersAttached) {
            return;
        }
        repositionListenersAttached = true;
        window.addEventListener('resize', handleResize);
        window.addEventListener('scroll', handleScroll, true);
    };

    const detachRepositionListeners = () => {
        if (!repositionListenersAttached) {
            return;
        }
        repositionListenersAttached = false;
        window.removeEventListener('resize', handleResize);
        window.removeEventListener('scroll', handleScroll, true);
    };

    // N'attache les listeners globaux de repositionnement que pendant l'affichage,
    // pour ne pas garder un scroll(capture) actif par instance montée mais cachée.
    watch(isVisible, (visible) => {
        if (visible) {
            attachRepositionListeners();
        } else {
            detachRepositionListeners();
        }
    });

    onMounted(() => {
        if (props.trigger === 'click') {
            document.addEventListener('click', handleClickOutside);
            triggerRef.value?.addEventListener('click', handleClickTrigger);
        }
    });

    onBeforeUnmount(() => {
        if (props.trigger === 'click') {
            document.removeEventListener('click', handleClickOutside);
            triggerRef.value?.removeEventListener('click', handleClickTrigger);
        }

        detachRepositionListeners();

        if (showTimer) {
            clearTimeout(showTimer);
        }
        if (hideTimer) {
            clearTimeout(hideTimer);
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .tooltip {
        display: inline-block;
        position: relative;

        &__trigger {
            display: inline-block;
        }

        &__content {
            position: fixed;
            z-index: vars.$z-index-tooltip;
            max-width: 300px;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-md;
            box-shadow: vars.$box-shadow-medium;
            pointer-events: none;
            line-height: vars.$line-height-normal;

            &--dark {
                background-color: vars.$black;
                color: vars.$white;

                .tooltip__arrow {
                    background-color: vars.$black;
                }
            }

            &--light {
                background-color: vars.$white;
                color: vars.$text-primary;
                border: 1px solid func.color-alpha(vars.$gray-light, 0.5);

                .tooltip__arrow {
                    background-color: vars.$white;
                    border: 1px solid func.color-alpha(vars.$gray-light, 0.5);
                }
            }

            &--primary {
                background-color: vars.$primary-color;
                color: vars.$white;

                .tooltip__arrow {
                    background-color: vars.$primary-color;
                }
            }

            &--top .tooltip__arrow {
                bottom: -4px;
                left: 50%;
                transform: translateX(-50%) rotate(45deg);
            }

            &--bottom .tooltip__arrow {
                top: -4px;
                left: 50%;
                transform: translateX(-50%) rotate(45deg);
            }

            &--left .tooltip__arrow {
                right: -4px;
                top: 50%;
                transform: translateY(-50%) rotate(45deg);
            }

            &--right .tooltip__arrow {
                left: -4px;
                top: 50%;
                transform: translateY(-50%) rotate(45deg);
            }
        }

        &__arrow {
            position: absolute;
            width: 8px;
            height: 8px;
        }

        &__body {
            position: relative;
            z-index: 1;
        }
    }

    .tooltip-enter-active,
    .tooltip-leave-active {
        transition: all 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .tooltip-enter-from,
    .tooltip-leave-to {
        opacity: 0;
        transform: scale(0.95);
    }
</style>
