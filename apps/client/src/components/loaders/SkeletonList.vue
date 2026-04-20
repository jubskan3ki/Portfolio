<template>
    <div :class="classes" :style="style">
        <SkeletonCard
            v-for="i in count"
            :key="i"
            :variant="variant"
            :show-image="showImage"
            :show-avatar="showAvatar"
            :show-description="showDescription"
            :show-tags="showTags"
            :show-footer="showFooter"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import SkeletonCard from './SkeletonCard.vue';

    import type { SkeletonListProps } from '@/types/components/loaders';

    const props = withDefaults(defineProps<SkeletonListProps>(), {
        count: 6,
        layout: 'grid',
        columns: 3,
        variant: 'default',
        showImage: true,
        showAvatar: false,
        showDescription: true,
        showTags: true,
        showFooter: false,
    });

    const classes = computed(() => ['skeleton-list', `skeleton-list--${props.layout}`]);

    const style = computed(() =>
        props.layout === 'grid'
            ? {
                '--cols': props.columns,
            }
            : {},
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/mixins' as m;

    .skeleton-list {
        --cols: 3;

        &--grid {
            display: grid;
            grid-template-columns: repeat(var(--cols), 1fr);
            gap: v.$spacing-lg;

            @include m.responsive(tablet) {
                grid-template-columns: repeat(2, 1fr);
            }

            @include m.responsive(mobile) {
                grid-template-columns: 1fr;
            }
        }

        &--list {
            display: flex;
            flex-direction: column;
            gap: v.$spacing-md;
        }
    }
</style>
