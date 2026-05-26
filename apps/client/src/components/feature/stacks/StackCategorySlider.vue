<template>
    <section class="stack-slider">
        <header class="stack-slider__header">
            <div class="stack-slider__title-wrapper">
                <div class="stack-slider__icon">
                    <BaseIcon :name="icon" :size="20" />
                </div>
                <h2 class="stack-slider__title">{{ label }}</h2>
                <span class="stack-slider__count">{{ stacks.length }}</span>
            </div>

            <div v-if="canScroll" class="stack-slider__nav">
                <button
                    class="stack-slider__arrow stack-slider__arrow--prev"
                    :class="{ 'stack-slider__arrow--disabled': !canScrollLeft }"
                    :disabled="!canScrollLeft"
                    aria-label="Précédent"
                    @click="scrollToPrev"
                >
                    <BaseIcon name="chevron-left" :size="20" />
                </button>
                <button
                    class="stack-slider__arrow stack-slider__arrow--next"
                    :class="{ 'stack-slider__arrow--disabled': !canScrollRight }"
                    :disabled="!canScrollRight"
                    aria-label="Suivant"
                    @click="scrollToNext"
                >
                    <BaseIcon name="chevron-right" :size="20" />
                </button>
            </div>
        </header>

        <div ref="sliderRef" class="stack-slider__track" @scroll="updateScrollState">
            <div class="stack-slider__cards">
                <StackCard
                    v-for="(stack, index) in stacks"
                    :key="stack.id"
                    :stack="stack"
                    :style="{ '--card-index': prefersReducedMotion ? 0 : index }"
                    class="stack-slider__card"
                    @click="$emit('navigate', stack.slug)"
                />
            </div>
        </div>

        <div v-if="canScroll" class="stack-slider__progress">
            <div
                class="stack-slider__progress-fill"
                :style="{ transform: `scaleX(${scrollProgress / 100})` }"
            ></div>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
    import { useDragScroll } from '@/composables/ui/useDragScroll';

    import StackCard from './StackCard.vue';

    import type { StackCategorySliderProps } from '@/types/feature/stacks';

    defineProps<StackCategorySliderProps>();

    defineEmits<{
        navigate: [slug: string];
    }>();

    const { prefersReducedMotion } = useReducedMotion();

    // Scroll state
    const sliderRef = ref<HTMLElement | null>(null);
    const canScrollLeft = ref(false);
    const canScrollRight = ref(false);
    const scrollProgress = ref(0);

    // Card width + gap for scroll calculations
    const CARD_WIDTH = 320;
    const GAP = 24;
    const SCROLL_AMOUNT = (CARD_WIDTH + GAP) * 2; // Scroll 2 cards at a time

    const canScroll = computed(() => canScrollLeft.value || canScrollRight.value);

    useDragScroll(sliderRef);

    let rafId: number | null = null;
    const readScrollState = () => {
        rafId = null;
        const el = sliderRef.value;
        if (!el) {
            return;
        }

        const { scrollLeft, scrollWidth, clientWidth } = el;
        const maxScroll = scrollWidth - clientWidth;

        const nextLeft = scrollLeft > 5;
        const nextRight = scrollLeft < maxScroll - 5;
        const nextProgress = maxScroll > 0 ? (scrollLeft / maxScroll) * 100 : 0;

        if (nextLeft !== canScrollLeft.value) {
            canScrollLeft.value = nextLeft;
        }
        if (nextRight !== canScrollRight.value) {
            canScrollRight.value = nextRight;
        }
        if (nextProgress !== scrollProgress.value) {
            scrollProgress.value = nextProgress;
        }
    };

    const updateScrollState = () => {
        if (rafId !== null) {
            return;
        }
        rafId = requestAnimationFrame(readScrollState);
    };

    const scrollToPrev = () => {
        const el = sliderRef.value;
        if (!el) {
            return;
        }

        el.scrollTo({
            left: Math.max(0, el.scrollLeft - SCROLL_AMOUNT),
            behavior: prefersReducedMotion.value ? 'auto' : 'smooth',
        });
    };

    const scrollToNext = () => {
        const el = sliderRef.value;
        if (!el) {
            return;
        }

        const maxScroll = el.scrollWidth - el.clientWidth;
        el.scrollTo({
            left: Math.min(maxScroll, el.scrollLeft + SCROLL_AMOUNT),
            behavior: prefersReducedMotion.value ? 'auto' : 'smooth',
        });
    };

    // Initialize and update on resize
    let resizeObserver: ResizeObserver | null = null;

    onMounted(() => {
        const scheduleFirst = (cb: () => void) => {
            if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
                (window as unknown as { requestIdleCallback: (cb: () => void, opts?: { timeout: number }) => number })
                    .requestIdleCallback(cb, { timeout: 200 });
            } else {
                setTimeout(cb, 0);
            }
        };

        scheduleFirst(() => {
            nextTick(() => {
                updateScrollState();

                if (sliderRef.value) {
                    resizeObserver = new ResizeObserver(updateScrollState);
                    resizeObserver.observe(sliderRef.value);
                }
            });
        });
    });

    onUnmounted(() => {
        if (rafId !== null) {
            cancelAnimationFrame(rafId);
            rafId = null;
        }
        if (resizeObserver) {
            resizeObserver.disconnect();
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .stack-slider {
        position: relative;
        margin-bottom: vars.$spacing-xxl;

        content-visibility: auto;
        contain-intrinsic-size: auto 480px;

        &:last-child {
            margin-bottom: 0;
        }
    }

    // Header
    .stack-slider__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: vars.$spacing-lg;
        padding-right: vars.$spacing-sm;
    }

    .stack-slider__title-wrapper {
        display: flex;
        align-items: center;
        gap: vars.$spacing-sm;
    }

    .stack-slider__icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, vars.$primary-color, vars.$primary-dark);
        border-radius: vars.$border-radius-md;
        color: vars.$white;
        box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.3);
    }

    .stack-slider__title {
        margin: 0;
        font-size: vars.$font-size-xl;
        font-weight: vars.$font-weight-bold;
        color: vars.$text-primary;
    }

    .stack-slider__count {
        padding: vars.$spacing-xxs vars.$spacing-sm;
        background: vars.$bg-secondary;
        border-radius: vars.$border-radius-full;
        font-size: vars.$font-size-sm;
        font-weight: vars.$font-weight-semibold;
        color: vars.$text-muted;
    }

    // Navigation
    .stack-slider__nav {
        display: flex;
        gap: vars.$spacing-xs;
    }

    .stack-slider__arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: fn.color-alpha(vars.$white, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        border-radius: vars.$border-radius-md;
        color: vars.$text-secondary;
        cursor: pointer;
        transition: all 0.2s ease;
        padding: 0;

        &:hover:not(:disabled) {
            background: vars.$white;
            border-color: vars.$primary-color;
            color: vars.$primary-color;
            transform: scale(1.05);
            box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.15);
        }

        &--disabled,
        &:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
        }
    }

    // Track
    .stack-slider__track {
        overflow-x: auto;
        overflow-y: hidden;
        scroll-snap-type: x mandatory;
        scrollbar-width: none;
        -ms-overflow-style: none;
        margin: 0 calc(-1 * vars.$spacing-md);
        padding: vars.$spacing-sm vars.$spacing-md;
        cursor: grab;
        touch-action: pan-y;
        user-select: none;

        &.is-dragging {
            cursor: grabbing;
            scroll-snap-type: none;
        }

        &::-webkit-scrollbar {
            display: none;
        }
    }

    .stack-slider__cards {
        display: flex;
        gap: vars.$spacing-lg;
    }

    .stack-slider__card {
        flex: 0 0 320px;
        scroll-snap-align: start;
        animation: cardSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        animation-delay: calc(var(--card-index, 0) * 50ms);
        opacity: 0;

        @media (prefers-reduced-motion: reduce) {
            animation: none;
            opacity: 1;
        }
    }

    // Progress indicator
    .stack-slider__progress {
        position: relative;
        height: 3px;
        margin-top: vars.$spacing-md;
        background: fn.color-alpha(vars.$border-color, 0.3);
        border-radius: vars.$border-radius-full;
        overflow: hidden;
    }

    .stack-slider__progress-fill {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: linear-gradient(90deg, vars.$primary-color, vars.$primary-dark);
        border-radius: vars.$border-radius-full;
        transform-origin: left center;
        transform: scaleX(0);
        transition: transform 0.15s ease-out;
        will-change: transform;
    }

    // Animation
    @keyframes cardSlideIn {
        from {
            opacity: 0;
            transform: translateX(20px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    // Responsive - Tablet
    @include mix.responsive(tablet) {
        .stack-slider__title {
            font-size: vars.$font-size-lg;
        }

        .stack-slider__icon {
            width: 36px;
            height: 36px;
        }

        .stack-slider__card {
            flex: 0 0 300px;
        }
    }

    // Responsive - Mobile
    @include mix.responsive(mobile) {
        .stack-slider {
            margin-bottom: vars.$spacing-xl;
        }

        .stack-slider__header {
            flex-wrap: wrap;
            gap: vars.$spacing-sm;
        }

        .stack-slider__title {
            font-size: vars.$font-size-base;
        }

        .stack-slider__icon {
            width: 32px;
            height: 32px;
        }

        .stack-slider__nav {
            order: -1;
            width: 100%;
            justify-content: flex-end;
        }

        .stack-slider__arrow {
            width: 36px;
            height: 36px;
        }

        .stack-slider__card {
            flex: 0 0 280px;
        }

        .stack-slider__track {
            margin: 0 calc(-1 * vars.$spacing-sm);
            padding: vars.$spacing-xs vars.$spacing-sm;
        }

        .stack-slider__cards {
            gap: vars.$spacing-md;
        }
    }
</style>
