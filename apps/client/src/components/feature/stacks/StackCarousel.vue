<template>
    <ContentCarousel
        :items="stacks"
        :is-loading="isLoading"
        :is-error="isError"
        loading-label="Chargement des technologies..."
        error-message="Une erreur est survenue lors du chargement des technologies."
        empty-title="Aucune technologie"
        empty-description="Aucune technologie n'est disponible pour le moment."
        :slides-desktop="4"
        :autoplay="autoplay"
        show-dots
    >
        <template #slide="{ item }">
            <StackCard :stack="item as Stack" />
        </template>
    </ContentCarousel>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import ContentCarousel from '@/components/ui/ContentCarousel.vue';
    import { useFeaturedStacks } from '@/services/api/modules/stacks';

    import StackCard from './StackCard.vue';

    import type { Stack, StackCarouselProps } from '@/types/feature/stacks';

    type Props = StackCarouselProps;

    const props = withDefaults(defineProps<Props>(), {
        limit: 10,
        autoplay: true,
    });

    const { data, isLoading, isError } = useFeaturedStacks(props.limit);

    const stacks = computed(() => data.value ?? []);
</script>
