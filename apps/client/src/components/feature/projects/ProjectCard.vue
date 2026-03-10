<template>
    <BaseContentCard
        :to="projectLink"
        :image="project.image"
        :image-alt="project.title"
        placeholder-icon="folder"
        :badge="project.category"
        :title="project.title"
        :description="truncatedDescription"
        :tags="project.technologies"
        :max-tags="maxTechnologies"
        v-bind="projectLink ? prefetchHandlers : {}"
        :class="customClass"
    >
        <template #footer-left>
            <time :datetime="project.date" class="project-card__date">
                {{ formattedDate }}
            </time>
        </template>
    </BaseContentCard>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseContentCard from '@/components/base/BaseContentCard.vue';
    import { useCardPrefetch } from '@/composables/performance/usePrefetch';
    import { queryKeys } from '@/services/api/modules';
    import { projectsApi } from '@/services/api/modules/projects';
    import { formatDateShort } from '@/services/utils/date';
    import { truncateText } from '@/services/utils/helpers';

    import type { ProjectCardProps } from '@/types/feature/project';

    type Props = ProjectCardProps;

    const props = withDefaults(defineProps<Props>(), {
        featured: false,
        hoverable: true,
        flat: false,
        descriptionLength: 100,
        maxTechnologies: 3,
        customClass: '',
    });

    const projectLink = computed(() => (props.project.slug ? `/projects/${props.project.slug}` : ''));

    // Prefetch on hover
    const prefetchHandlers = useCardPrefetch(
        () => props.project.slug,
        (s) => queryKeys.projects.detail(s),
        (s) => projectsApi.getBySlug(s),
    );

    const truncatedDescription = computed(() => truncateText(props.project.description || '', props.descriptionLength));
    const formattedDate = computed(() => formatDateShort(props.project.date));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .project-card__date {
        font-size: vars.$font-size-xs;
        color: vars.$text-muted;
    }
</style>
