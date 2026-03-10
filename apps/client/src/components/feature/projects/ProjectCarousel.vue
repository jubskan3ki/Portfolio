<template>
    <ContentCarousel
        :items="projects"
        :is-loading="isLoading"
        :is-error="isError"
        loading-label="Chargement des projets..."
        error-message="Une erreur est survenue lors du chargement des projets."
        empty-title="Aucun projet"
        empty-description="Aucun projet n'est disponible pour le moment."
        :slides-desktop="3"
        :autoplay="autoplay"
        show-dots
    >
        <template #slide="{ item }">
            <ProjectCard :project="item as Project" />
        </template>
    </ContentCarousel>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import ContentCarousel from '@/components/ui/ContentCarousel.vue';
    import { useFeaturedProjects } from '@/services/api/modules/projects';

    import ProjectCard from './ProjectCard.vue';

    import type { Project, ProjectCarouselProps } from '@/types/feature/project';

    type Props = ProjectCarouselProps;

    const props = withDefaults(defineProps<Props>(), {
        limit: 6,
        autoplay: true,
    });

    const { data, isLoading, isError } = useFeaturedProjects(props.limit);

    const projects = computed(() => data.value ?? []);
</script>
