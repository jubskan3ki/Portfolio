<template>
    <div :class="classes">
        <Skeleton
            v-if="showImage"
            type="image"
            width="100%"
            :height="imageHeight"
            class="skeleton-card__image"
        />

        <div class="skeleton-card__content">
            <div v-if="showAvatar" class="skeleton-card__header">
                <Skeleton type="avatar" :width="40" :height="40" />
                <div class="skeleton-card__meta">
                    <Skeleton type="text" width="120px" height="14px" />
                    <Skeleton type="text" width="80px" height="12px" />
                </div>
            </div>

            <Skeleton type="text" width="90%" :height="titleHeight" class="skeleton-card__title" />

            <div v-if="showDescription" class="skeleton-card__description">
                <Skeleton
                    v-for="i in descriptionLines"
                    :key="i"
                    type="text"
                    :width="i === descriptionLines ? '65%' : '100%'"
                    height="14px"
                />
            </div>

            <div v-if="showTags" class="skeleton-card__tags">
                <Skeleton
                    v-for="i in 3"
                    :key="i"
                    type="button"
                    :width="50 + i * 15"
                    height="24px"
                    radius="12px"
                />
            </div>

            <div v-if="showFooter" class="skeleton-card__footer">
                <Skeleton type="text" width="100px" height="14px" />
                <Skeleton type="button" width="80px" height="32px" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import Skeleton from './Skeleton.vue';

    import type { SkeletonCardProps } from '@/types/components/loaders';

    const props = withDefaults(defineProps<SkeletonCardProps>(), {
        variant: 'default',
        showImage: true,
        showAvatar: false,
        showDescription: true,
        showTags: true,
        showFooter: false,
        imageHeight: '180px',
        titleHeight: '22px',
        descriptionLines: 2,
    });

    const classes = computed(() => ['skeleton-card', `skeleton-card--${props.variant}`]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/functions' as fn;

    .skeleton-card {
        background: v.$white;
        border-radius: v.$border-radius-lg;
        overflow: hidden;
        border: 1px solid fn.color-alpha(v.$border-color, 0.5);

        &__image {
            width: 100%;
        }

        &__content {
            padding: v.$spacing-md;
            display: flex;
            flex-direction: column;
            gap: v.$spacing-xs;
        }

        &__header {
            display: flex;
            align-items: center;
            gap: v.$spacing-sm;
            margin-bottom: v.$spacing-xs;
        }

        &__meta {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: v.$spacing-xxs;
        }

        &__title {
            margin-bottom: v.$spacing-xs;
        }

        &__description {
            display: flex;
            flex-direction: column;
            gap: v.$spacing-xxs;
        }

        &__tags {
            display: flex;
            flex-wrap: wrap;
            gap: v.$spacing-xxs;
            margin-top: v.$spacing-xs;
        }

        &__footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: v.$spacing-sm;
            padding-top: v.$spacing-sm;
            border-top: 1px solid fn.color-alpha(v.$border-color, 0.3);
        }

        &--article .skeleton-card__image {
            aspect-ratio: 16 / 10;
        }

        &--project .skeleton-card__image {
            aspect-ratio: 16 / 9;
        }

        &--stack {
            .skeleton-card__content {
                text-align: center;
                align-items: center;
            }
            .skeleton-card__image {
                display: none;
            }
        }

        &--experience .skeleton-card__image {
            display: none;
        }
    }
</style>
