import { useEventListener } from '@vueuse/core';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';

import type { UseSwiperOptions } from '@/types/composables/ui';

export function useSwiper(options: UseSwiperOptions) {
    const { props, emit, swiperRef } = options;

    const activeIndex = ref(0);
    const slideWidth = ref(0);
    const translateX = ref(0);
    let autoplayTimer: number | null = null;

    const totalDots = computed(() => {
        return Math.ceil((props.slides - (props.slidesToShow ?? 1) + 1) / (props.slidesToScroll ?? 1));
    });

    const slideStyles = computed(() => {
        const slidesToShow = props.slidesToShow ?? 1;
        const gap = props.gap ?? 16;
        return {
            width:
                slidesToShow > 1
                    ? `calc((100% / ${slidesToShow}) - ${(gap * (slidesToShow - 1)) / slidesToShow}px)`
                    : '100%',
            marginRight: `${gap}px`,
            height: props.height ? `${props.height}px` : 'auto',
        };
    });

    const canGoBack = computed(() => {
        return props.infinite || activeIndex.value > 0;
    });

    const canGoForward = computed(() => {
        return props.infinite || activeIndex.value < props.slides - (props.slidesToShow ?? 1);
    });

    const isDotActive = (dotIndex: number) => {
        const slidesToScroll = props.slidesToScroll ?? 1;
        const startSlide = dotIndex * slidesToScroll;
        const endSlide = Math.min(startSlide + slidesToScroll - 1, props.slides - 1);
        return activeIndex.value >= startSlide && activeIndex.value <= endSlide;
    };

    const updateTranslateX = () => {
        if (swiperRef.value) {
            const gap = props.gap ?? 16;
            const slideWidthWithGap = slideWidth.value + gap;
            translateX.value = activeIndex.value * slideWidthWithGap;
        }
    };

    const goToSlide = (index: number) => {
        const slidesToShow = props.slidesToShow ?? 1;
        const maxIndex = props.slides - slidesToShow;
        const newIndex = Math.max(0, Math.min(index, maxIndex));

        activeIndex.value = newIndex;
        updateTranslateX();
        emit('change', activeIndex.value);

        if (props.autoplay && autoplayTimer) {
            clearInterval(autoplayTimer);
            startAutoplay();
        }
    };

    const prev = () => {
        const slidesToScroll = props.slidesToScroll ?? 1;
        const slidesToShow = props.slidesToShow ?? 1;
        if (activeIndex.value > 0) {
            goToSlide(activeIndex.value - slidesToScroll);
        } else if (props.infinite) {
            goToSlide(props.slides - slidesToShow);
        }
    };

    const next = () => {
        const slidesToScroll = props.slidesToScroll ?? 1;
        const slidesToShow = props.slidesToShow ?? 1;
        if (activeIndex.value < props.slides - slidesToShow) {
            goToSlide(activeIndex.value + slidesToScroll);
        } else if (props.infinite) {
            goToSlide(0);
        }
    };

    const startAutoplay = () => {
        // Évite d'empiler deux intervals (toggle autoplay rapide) : on repart toujours propre.
        if (autoplayTimer) {
            return;
        }
        const slidesToShow = props.slidesToShow ?? 1;
        if (props.autoplay && props.slides > slidesToShow) {
            autoplayTimer = window.setInterval(() => {
                if (activeIndex.value < props.slides - slidesToShow) {
                    next();
                } else {
                    goToSlide(0);
                }
            }, props.autoplayInterval ?? 5000);
        }
    };

    const stopAutoplay = () => {
        if (autoplayTimer) {
            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    };

    const calculateDimensions = () => {
        if (swiperRef.value) {
            const slidesToShow = props.slidesToShow ?? 1;
            const gap = props.gap ?? 16;
            const containerWidth = swiperRef.value.offsetWidth;
            slideWidth.value =
                slidesToShow > 1 ? (containerWidth - gap * (slidesToShow - 1)) / slidesToShow : containerWidth;
            updateTranslateX();
        }
    };

    useEventListener(window, 'resize', calculateDimensions, { passive: true });

    onMounted(() => {
        calculateDimensions();
        if (props.autoplay) {
            startAutoplay();
        }
    });

    onUnmounted(() => {
        stopAutoplay();
    });

    watch(() => props.slides, calculateDimensions);
    watch(() => props.slidesToShow, calculateDimensions);
    watch(
        () => props.autoplay,
        (newVal) => {
            if (newVal) {
                startAutoplay();
            } else {
                stopAutoplay();
            }
        },
    );

    return {
        activeIndex,
        translateX,
        totalDots,
        slideStyles,
        canGoBack,
        canGoForward,
        isDotActive,
        prev,
        next,
        goToSlide,
    };
}
