<template>
    <div class="content-carousel">
        <div v-if="isLoading" class="content-carousel__state">
            <Spinner type="circle" :label="loadingLabel" />
        </div>

        <div v-else-if="isError" class="content-carousel__state">
            <p>{{ errorMessage }}</p>
        </div>

        <div v-else-if="!items || items.length === 0" class="content-carousel__state">
            <EmptyState :title="emptyTitle" :description="emptyDescription" />
        </div>

        <div v-else class="content-carousel__content">
            <slot name="header"></slot>

            <Swiper
                :slides="items.length"
                :slides-to-show="responsiveSlides"
                :slides-to-scroll="1"
                :gap="gap"
                :autoplay="autoplay"
                :autoplay-interval="autoplayInterval"
                :show-controls="false"
                :show-dots="showDots"
                @change="$emit('change', $event)"
            >
                <template v-for="(item, index) in items" :key="item.id" #[`slide-${index}`]>
                    <slot name="slide" :item="item" :index="index"></slot>
                </template>
            </Swiper>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, onBeforeUnmount } from 'vue';

    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Spinner from '@/components/loaders/Spinner.vue';
    import Swiper from '@/components/ui/Swiper.vue';
    import { BREAKPOINTS } from '@/config/constants';

    import type { ContentCarouselProps } from '@/types/components/ui';

    type Props = ContentCarouselProps;

    const props = withDefaults(defineProps<Props>(), {
        isLoading: false,
        isError: false,
        loadingLabel: 'Chargement...',
        errorMessage: 'Une erreur est survenue.',
        emptyTitle: 'Aucun contenu',
        emptyDescription: 'Aucun contenu disponible pour le moment.',
        slidesDesktop: 3,
        slidesTablet: 2,
        slidesMobile: 1,
        autoplay: false,
        autoplayInterval: 5000,
        gap: 4,
        showDots: true,
    });

    defineEmits<{ change: [index: number] }>();

    const responsiveSlides = ref(props.slidesMobile);

    const updateSlides = () => {
        const width = window.innerWidth;
        if (width < BREAKPOINTS.MD) {
            responsiveSlides.value = props.slidesMobile;
        } else if (width < BREAKPOINTS.LG) {
            responsiveSlides.value = props.slidesTablet;
        } else {
            responsiveSlides.value = props.slidesDesktop;
        }
    };

    onMounted(() => {
        updateSlides();
        window.addEventListener('resize', updateSlides, { passive: true });
    });

    onBeforeUnmount(() => {
        window.removeEventListener('resize', updateSlides);
    });
</script>

<style lang="scss" scoped>
    .content-carousel {
        &__state {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 200px;
        }
    }
</style>
