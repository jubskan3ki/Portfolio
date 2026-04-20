<template>
    <div class="base-image" :class="containerClasses">
        <div v-if="isLoading && showPlaceholder" class="base-image__placeholder">
            <slot name="placeholder">
                <div class="base-image__skeleton"></div>
            </slot>
        </div>

        <!-- External absolute URLs bypass IPX proxying -->
        <img
            v-if="src && isAbsoluteExternal"
            :src="resolvedSrc"
            :alt="alt"
            :width="width"
            :height="height"
            :loading="lazy ? 'lazy' : 'eager'"
            class="base-image__img"
            :class="{ 'base-image__img--loaded': !isLoading }"
            @load="handleLoad"
            @error="handleError"
        />

        <NuxtImg
            v-else-if="src"
            :src="resolvedSrc"
            :alt="alt"
            :width="width"
            :height="height"
            :loading="lazy ? 'lazy' : 'eager'"
            :placeholder="placeholder"
            :quality="quality"
            :format="format"
            :sizes="sizes"
            :densities="densities"
            :preload="preload"
            class="base-image__img"
            :class="{ 'base-image__img--loaded': !isLoading }"
            @load="handleLoad"
            @error="handleError"
        />

        <div v-if="hasError" class="base-image__error">
            <slot name="error">
                <BaseIcon name="image-off" :size="errorIconSize" />
                <span v-if="showErrorText" class="base-image__error-text">Image non disponible</span>
            </slot>
        </div>

        <div v-if="$slots.overlay" class="base-image__overlay">
            <slot name="overlay"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue';

    import { resolveMediaUrl } from '@/services/utils/helpers';

    import BaseIcon from './BaseIcon.vue';

    import type { ImageProps } from '@/types/components/base';

    type Props = ImageProps;

    const props = withDefaults(defineProps<Props>(), {
        lazy: true,
        quality: 80,
        format: 'webp',
        densities: 'x1 x2',
        showPlaceholder: true,
        aspectRatio: 'auto',
        objectFit: 'cover',
        rounded: false,
    });

    const emit = defineEmits<{
        load: [event: Event];
        error: [event: string | Event];
    }>();

    const isLoading = ref(true);
    const hasError = ref(false);
    const resolvedSrc = computed(() => resolveMediaUrl(props.src));

    // External http(s) URLs skip IPX; /media/ is proxied via the IPX alias in nuxt.config.ts.
    const isAbsoluteExternal = computed(() => /^https?:\/\//i.test(resolvedSrc.value));

    const toNum = (v: string | number | undefined) =>
        (typeof v === 'string' ? parseInt(v, 10) : v) || 0;
    const isSmall = computed(
        () => (toNum(props.width) > 0 && toNum(props.width) < 80)
            || (toNum(props.height) > 0 && toNum(props.height) < 80),
    );
    const errorIconSize = computed(() => (isSmall.value ? 18 : 32));
    const showErrorText = computed(() => !isSmall.value);

    const containerClasses = computed(() => [
        `base-image--ratio-${props.aspectRatio}`,
        `base-image--fit-${props.objectFit}`,
        {
            'base-image--rounded-sm': props.rounded === 'sm',
            'base-image--rounded-md': props.rounded === 'md' || props.rounded === true,
            'base-image--rounded-lg': props.rounded === 'lg',
            'base-image--rounded-full': props.rounded === 'full',
            'base-image--loading': isLoading.value,
            'base-image--error': hasError.value,
        },
    ]);

    const handleLoad = (event: Event) => {
        isLoading.value = false;
        hasError.value = false;
        emit('load', event);
    };

    const handleError = (event: string | Event) => {
        isLoading.value = false;
        hasError.value = true;
        emit('error', event);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .base-image {
        position: relative;
        overflow: hidden;

        &--ratio-1\:1 {
            aspect-ratio: 1 / 1;
        }

        &--ratio-4\:3 {
            aspect-ratio: 4 / 3;
        }

        &--ratio-16\:9 {
            aspect-ratio: 16 / 9;
        }

        &--ratio-21\:9 {
            aspect-ratio: 21 / 9;
        }

        &--fit-cover .base-image__img {
            object-fit: cover;
        }

        &--fit-contain .base-image__img {
            object-fit: contain;
        }

        &--fit-fill .base-image__img {
            object-fit: fill;
        }

        &--fit-none .base-image__img {
            object-fit: none;
        }

        &--fit-scale-down .base-image__img {
            object-fit: scale-down;
        }

        &--rounded-sm {
            border-radius: vars.$border-radius-sm;
        }

        &--rounded-md {
            border-radius: vars.$border-radius-md;
        }

        &--rounded-lg {
            border-radius: vars.$border-radius-lg;
        }

        &--rounded-full {
            border-radius: vars.$border-radius-full;
        }

        &__img {
            width: 100%;
            height: 100%;
            display: block;
            opacity: 0;
            transition: opacity vars.$transition-base;

            &--loaded {
                opacity: 1;
            }
        }

        &__placeholder,
        &__skeleton {
            position: absolute;
            inset: 0;
        }

        &__skeleton {
            background: linear-gradient(90deg, vars.$gray-light 25%, vars.$white-dark 50%, vars.$gray-light 75%);
            background-size: 200% 100%;
            animation: skeleton-pulse 1.5s ease-in-out infinite;
        }

        &__error {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xxs;
            color: vars.$gray;
            background-color: vars.$white-dark;
        }

        &__overlay {
            position: absolute;
            inset: 0;
            pointer-events: none;

            > * {
                pointer-events: auto;
            }
        }
    }

    @keyframes skeleton-pulse {
        0% {
            background-position: 200% 0;
        }

        100% {
            background-position: -200% 0;
        }
    }
</style>
