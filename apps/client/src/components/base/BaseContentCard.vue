<template>
    <component :is="to ? NuxtLink : 'div'" :to="to || undefined" v-bind="$attrs" class="content-card">
        <div class="content-card__visual" :style="imageTransitionStyle">
            <BaseImage
                v-if="image"
                :src="image"
                :alt="imageAlt"
                :width="imageWidth"
                :height="imageHeight"
                aspect-ratio="16:9"
                object-fit="cover"
                :quality="85"
                :lazy="!eager"
                sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 400px"
                class="content-card__image"
            >
                <template #placeholder>
                    <div class="content-card__skeleton"></div>
                </template>
            </BaseImage>
            <div v-else class="content-card__placeholder">
                <BaseIcon :name="placeholderIcon" :size="28" />
            </div>

            <span v-if="badge" class="content-card__badge">
                {{ badge }}
            </span>

            <slot name="visual-overlay"></slot>
        </div>

        <div class="content-card__content">
            <slot name="before-title"></slot>

            <h3 class="content-card__title" :style="titleTransitionStyle">{{ title }}</h3>

            <p v-if="description" class="content-card__description">
                {{ description }}
            </p>

            <div v-if="tags.length > 0" class="content-card__tags">
                <span v-for="tag in displayedTags" :key="tag" class="content-card__tag">
                    {{ tag }}
                </span>
                <span v-if="remainingTagsCount > 0" class="content-card__tag content-card__tag--more">
                    +{{ remainingTagsCount }}
                </span>
            </div>

            <div v-if="showFooter" class="content-card__footer">
                <slot name="footer-left"></slot>
                <slot name="footer-right">
                    <BaseIcon name="arrow-right" :size="16" class="content-card__arrow" />
                </slot>
            </div>
        </div>
    </component>
</template>

<script setup lang="ts">
    import { computed, resolveComponent } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseImage from '@/components/base/BaseImage.vue';

    import type { BaseContentCardProps } from '@/types/components/base';

    const props = withDefaults(defineProps<BaseContentCardProps>(), {
        to: '',
        image: '',
        imageAlt: '',
        imageWidth: 640,
        imageHeight: 400,
        placeholderIcon: 'file-text',
        badge: '',
        description: '',
        tags: () => [],
        maxTags: 3,
        transitionKey: '',
        eager: false,
        showFooter: true,
    });

    const NuxtLink = resolveComponent('NuxtLink');

    defineOptions({ inheritAttrs: false });

    const displayedTags = computed(() => props.tags.slice(0, props.maxTags));
    const remainingTagsCount = computed(() => Math.max(0, props.tags.length - props.maxTags));

    const imageTransitionStyle = computed(() =>
        props.transitionKey ? { viewTransitionName: `hero-media-${props.transitionKey}` } : undefined,
    );
    const titleTransitionStyle = computed(() =>
        props.transitionKey ? { viewTransitionName: `hero-title-${props.transitionKey}` } : undefined,
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .content-card {
        display: flex;
        flex-direction: column;
        height: 100%;
        text-decoration: none;
        color: inherit;
        background: vars.$white;
        border: 1px solid vars.$border-color;
        border-radius: vars.$border-radius-lg;
        overflow: hidden;
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;

        &:hover {
            transform: translateY(-2px);
            border-color: fn.color-alpha(vars.$primary-color, 0.22);
            box-shadow:
                0 6px 14px fn.color-alpha(vars.$black, 0.05),
                0 2px 4px fn.color-alpha(vars.$black, 0.03);

            .content-card__image :deep(.base-image__img) {
                transform: scale(1.02);
            }

            .content-card__title {
                color: vars.$primary-color;
            }

            .content-card__arrow {
                transform: translateX(3px);
                opacity: 1;
            }
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }
    }

    .content-card__visual {
        position: relative;
        aspect-ratio: 16 / 10;
        overflow: hidden;
        background: vars.$bg-secondary;
    }

    .content-card__image {
        width: 100%;
        height: 100%;

        :deep(.base-image__img) {
            transition: transform 0.4s ease;
        }
    }

    .content-card__skeleton {
        width: 100%;
        height: 100%;
        background: vars.$gray-light;
        animation: skeleton-pulse 1.5s ease-in-out infinite;
        will-change: opacity;
    }

    @keyframes skeleton-pulse {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }

    .content-card__placeholder {
        @include mix.flex-center;

        height: 100%;
        color: vars.$gray-light;
    }

    .content-card__badge {
        position: absolute;
        top: vars.$spacing-xs;
        left: vars.$spacing-xs;
        padding: vars.$spacing-xxxs vars.$spacing-xs;
        font-size: 11px;
        font-weight: vars.$font-weight-semibold;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: vars.$white;
        background: fn.color-alpha(vars.$primary-color, 0.9);
        border-radius: vars.$border-radius-sm;
    }

    .content-card__content {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: vars.$spacing-md;
    }

    .content-card__title {
        margin: 0 0 vars.$spacing-xs;
        font-size: vars.$font-size-lg;
        font-weight: vars.$font-weight-semibold;
        color: vars.$text-primary;
        line-height: 1.3;
        min-height: calc(1.3em * 2);
        transition: color 0.2s ease;

        @include mix.truncate(2);
    }

    .content-card__description {
        flex: 1;
        margin: 0 0 vars.$spacing-sm;
        font-size: vars.$font-size-sm;
        color: vars.$text-secondary;
        line-height: 1.6;
        min-height: calc(1.6em * 2);

        @include mix.truncate(2);
    }

    .content-card__tags {
        display: flex;
        flex-wrap: wrap;
        gap: vars.$spacing-xxs;
        margin-bottom: vars.$spacing-sm;
    }

    .content-card__tag {
        padding: vars.$spacing-xxxs vars.$spacing-xxs;
        font-size: 11px;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-muted;
        background: vars.$bg-secondary;
        border-radius: vars.$border-radius-sm;

        &--more {
            color: vars.$primary-color;
            background: fn.color-alpha(vars.$primary-color, 0.08);
        }
    }

    .content-card__footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: auto;
        padding-top: vars.$spacing-sm;
        border-top: 1px solid vars.$border-color;
    }

    .content-card__arrow {
        color: vars.$primary-color;
        opacity: 0;
        transform: translateX(0);
        transition:
            transform 0.2s ease,
            opacity 0.2s ease;
    }

    @media (prefers-reduced-motion: reduce) {
        .content-card {
            transition: none;

            &:hover {
                transform: none;
            }
        }

        .content-card__image :deep(.base-image__img) {
            transition: none;
        }
    }

    @include mix.responsive(mobile) {
        .content-card__content {
            padding: vars.$spacing-sm;
        }

        .content-card__title {
            font-size: vars.$font-size-base;
        }
    }
</style>
