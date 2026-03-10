<template>
    <div class="swiper-container" :class="{ 'swiper--fullwidth': fullwidth }">
        <div v-if="showControls && slides > slidesToShow" class="swiper__controls">
            <button
                class="swiper__arrow swiper__arrow--prev"
                :disabled="!canGoBack"
                aria-label="Précédent"
                @click="prev"
            >
                <BaseIcon name="chevron-left" :size="24" />
            </button>
        </div>

        <div ref="swiperRef" class="swiper__wrapper">
            <div class="swiper__track" :style="{ transform: `translateX(-${translateX}px)` }">
                <div
                    v-for="idx in slides"
                    :key="idx - 1"
                    class="swiper__slide"
                    :class="{ 'swiper__slide--active': activeIndex === idx - 1 }"
                    :style="slideStyles"
                >
                    <slot :name="`slide-${idx - 1}`" :index="idx - 1" :active="activeIndex === idx - 1"></slot>
                </div>
            </div>
        </div>

        <div v-if="showControls && slides > slidesToShow" class="swiper__controls">
            <button
                class="swiper__arrow swiper__arrow--next"
                :disabled="!canGoForward"
                aria-label="Suivant"
                @click="next"
            >
                <BaseIcon name="chevron-right" :size="24" />
            </button>
        </div>

        <div v-if="showDots && slides > slidesToShow" class="swiper__dots">
            <button
                v-for="idx in totalDots"
                :key="idx - 1"
                class="swiper__dot"
                :class="{ 'swiper__dot--active': isDotActive(idx - 1) }"
                :aria-label="`Diapositive ${idx}`"
                @click="goToSlide((idx - 1) * slidesToScroll)"
            ></button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useSwiper } from '@/composables/ui/useSwiper';

    import type { SwiperProps } from '@/types/components/ui';

    type Props = SwiperProps;

    const props = withDefaults(defineProps<Props>(), {
        slidesToShow: 1,
        slidesToScroll: 1,
        showControls: true,
        showDots: true,
        autoplay: false,
        autoplayInterval: 5000,
        infinite: false,
        fullwidth: false,
        height: undefined,
        gap: 16,
    });

    const emit = defineEmits(['change']);

    const {
        activeIndex,
        swiperRef,
        translateX,
        totalDots,
        slideStyles,
        canGoBack,
        canGoForward,
        isDotActive,
        prev,
        next,
        goToSlide,
    } = useSwiper({ props, emit });

    defineExpose({
        prev,
        next,
        goToSlide,
        currentSlide: activeIndex,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .swiper-container {
        position: relative;
        width: 100%;
        margin: 0 auto;
        overflow: hidden;

        &.swiper--fullwidth {
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
        }
    }

    .swiper {
        &__wrapper {
            overflow: hidden;
            width: 100%;
        }

        &__track {
            display: flex;
            transition: transform 0.5s ease-in-out;
        }

        &__slide {
            flex-shrink: 0;
            padding: 10px;
            position: relative;

            &--active {
                z-index: 1;
            }
        }

        &__controls {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            z-index: 10;
            width: 100%;
            display: flex;
            justify-content: space-between;
            pointer-events: none;

            .swiper__arrow {
                pointer-events: auto;
            }
        }

        &__arrow {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: func.color-alpha(vars.$white, 0.8);
            color: vars.$primary-color;
            box-shadow: vars.$box-shadow;
            cursor: pointer;
            transition: all vars.$transition-base;
            border: none;

            &:hover:not(:disabled) {
                background: vars.$white;
                transform: scale(1.1);
            }

            &:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: scale(1);
            }

            &--prev {
                margin-left: 12px;
            }

            &--next {
                margin-right: 12px;
            }
        }

        &__dots {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin: 8px 0;
        }

        &__dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: func.color-alpha(vars.$primary-color, 0.3);
            border: none;
            padding: 0;
            cursor: pointer;
            transition: all vars.$transition-base;

            &:hover {
                background-color: func.color-alpha(vars.$primary-color, 0.6);
            }

            &--active {
                background-color: vars.$primary-color;
                transform: scale(1.2);
            }
        }
    }
</style>
